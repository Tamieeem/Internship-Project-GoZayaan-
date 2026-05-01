from celery import shared_task
from django.utils import timezone
from apps.templates.models import EmailTemplate, MessageTemplate
from utils.choices import Status, TemplateType, Priority
from .models import Events
from .services import process_and_send_message
from .serializers import EventSerializer


@shared_task(bind=True, ignore_result=True)
def receive_instant_task(self, data):
    """
    from others apps → direct trigger this task → task will do the following:
    Validate → Save → Priority based queue → send_message_task
    """
    # Step 1: Validate data
    serializer = EventSerializer(data=data)
    if not serializer.is_valid():
        # validation failed — log and exit
        print(f"Validation failed: {serializer.errors}")
        return

    # Step 2: Priority pop
    priority = serializer.validated_data.pop("priority")

    # Step 3: Save to DB
    event = serializer.save(
        created_at=timezone.now(),
        status=Status.PENDING,
    )

    # Step 4: Priority
    queue = _get_queue(priority)
    send_message_task.apply_async(args=[event.id], queue=queue)


@shared_task(bind=True, ignore_result=True)
def send_message_task(self, event_id):
    # Step 1: Event fetch
    event = Events.objects.select_related("provider").get(id=event_id)

    # Step 2: Template fetch based on type
    if event.template_type == TemplateType.EMAIL:
        resolved_template = (
            EmailTemplate.objects.select_related("content")
            .prefetch_related(
                "to_contacts", "to_group__contacts",
                "cc_contacts", "cc_group__contacts",
                "bcc_contacts", "bcc_group__contacts",
                "attachments",
            )
            .filter(template_code=event.template_code, is_active=True)
            .first()
        )

    else:
        resolved_template = (
            MessageTemplate.objects.select_related("content")
            .prefetch_related("contacts", "groups__contacts")
            .filter(template_code=event.template_code, is_active=True)
            .first()
        )

    # if template not found
    if not resolved_template:
        event.status = Status.FAILED
        event.save(update_fields=["status"])
        return

    # Step 3: Service function call
    result = process_and_send_message(event, resolved_template)

    # Step 4: Status update
    if result.get("status") == "success":
        event.status = Status.SENT
        event.delivered_at = timezone.now()
        event.save(update_fields=["status", "delivered_at"])
    else:
        event.retry_count += 1
        max_retry = getattr(resolved_template, "max_retry", None)
        if max_retry is not None and event.retry_count >= max_retry:
            event.status = Status.FAILED
            event.save(update_fields=["status", "retry_count"])
        else:
            event.status = Status.IN_QUEUE
            event.save(update_fields=["status", "retry_count"])
            # send_message_task.delay(event_id)  # Retry the task
            queue = _get_queue(resolved_template.priority)
            send_message_task.apply_async(args=[event_id], queue=queue)


def _get_queue(priority):
    if priority == Priority.INSTANT:
        return "instant"
    elif priority == Priority.HIGH:
        return "high"
    return "low"
