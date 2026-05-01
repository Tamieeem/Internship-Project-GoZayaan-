from .models import Events, Logs
from utils.viewsets import BaseModelViewSet
from .models import Provider, Content, Events
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.decorators import custom_permissions
from .serializers import EventSerializer, EventListSerializer, EventRetrySerializer, ProviderReadSerializer, ProviderWriteSerializer, ContentBodySerializer, LogListSerializer
from utils.choices import Priority, Status
from apps.templates.models import EmailTemplate, MessageTemplate
from utils.choices import TemplateType
from .tasks import send_message_task, _get_queue
from utils.pagination import StandardLimitOffsetPagination


@method_decorator(custom_permissions(is_admin=True, groups=['marketing']), name='initial')
class ProviderViewSet(BaseModelViewSet):
    queryset = Provider.objects.all().order_by('-id')
    filterset_fields = ['region', 'service', 'is_active', 'delivery_type']
    search_fields = ['name']
    read_serializer_class = ProviderReadSerializer
    write_serializer_class = ProviderWriteSerializer


@method_decorator(custom_permissions(is_admin=True, groups=['marketing']), name='initial')
class ContentViewSet(BaseModelViewSet):
    queryset = Content.objects.all().order_by('-id')
    filterset_fields = ['name']
    search_fields = ['name', 'template_path', 'body_text', 'body_html']
    lookup_field = 'id'
    read_serializer_class = ContentBodySerializer
    write_serializer_class = ContentBodySerializer


@method_decorator(custom_permissions(is_admin=True, groups=["marketing"]), name="initial")
class InstantMessageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Step 1: Validate request data
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Pull resolved_template out before saving
        # (it's a Python object, not a model field — must not be passed to .save())
        # resolved_template = serializer.validated_data.pop("resolved_template")
        # Step 2: Get priority before saving
        priority = serializer.validated_data.pop("priority")
        # Step 2: Save the event to DB with PENDING status
        event = serializer.save(
            created_at=timezone.now(),
            status=Status.PENDING,
        )

        # Step 4: Decide queue based on priority
        if priority == Priority.INSTANT:
            send_message_task.apply_async(
                args=[event.id], queue="instant"
            )
        elif priority == Priority.HIGH:
            send_message_task.apply_async(
                args=[event.id], queue="high"
            )
        else:
            # LOW  → low queue
            send_message_task.apply_async(
                args=[event.id], queue="low"
            )

        return Response(
            {
                "message": "Event queued  successfully",
                "event_id": event.id,
                "current_status": event.status,
                "received_at": event.created_at,
            },
            status=status.HTTP_201_CREATED,
        )


class EventListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # Status filter — optional query param
        status_filter = request.query_params.get("status", None)

        events = Events.objects.all().order_by("-created_at")

        if status_filter:
            events = events.filter(status=status_filter)

        # Pagination
        paginator = StandardLimitOffsetPagination()
        paginated_events = paginator.paginate_queryset(events, request)

        # Serializer
        serializer = EventListSerializer(paginated_events, many=True)
        return paginator.get_paginated_response(serializer.data)


class EventRetryAPIView(APIView):

    def patch(self, request, event_id, *args, **kwargs):
        try:
            event = Events.objects.get(id=event_id, status=Status.FAILED)
        except Events.DoesNotExist:
            return Response(
                {"error": "Failed event not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if event.template_type == TemplateType.EMAIL:
            template = EmailTemplate.objects.filter(
                template_code=event.template_code, is_active=True
            ).first()
        else:
            template = MessageTemplate.objects.filter(
                template_code=event.template_code, is_active=True
            ).first()

        if not template:
            return Response(
                {"error": "Template not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        queue = _get_queue(template.priority)

        # Reset
        event.retry_count = 0
        event.status = Status.PENDING
        event.save(update_fields=["status", "retry_count"])

        # Queue the task for retry
        send_message_task.apply_async(args=[event.id], queue=queue)

        # Serializer For Response
        serializer = EventRetrySerializer(event)
        return Response(
            {
                "message": "Event queued for retry.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@method_decorator(custom_permissions(is_admin=True, groups=['marketing']), name='initial')
class LogAdminViewSet(BaseModelViewSet):
    """
    Admin ViewSet for system Logs.
    Follows the project's standard pagination and security patterns.
    """
    queryset = Logs.objects.all().order_by('-created_at')

    pagination_class = StandardLimitOffsetPagination

    filterset_fields = ['status', 'region', 'service']

    search_fields = ['request_by', 'api_path', 'error']
    read_serializer_class = LogListSerializer
