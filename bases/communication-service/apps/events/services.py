from django.template import Context, Template
from django.template.loader import render_to_string
from utils.choices import TemplateType
from .providers.provider_factory import get_provider
from django.conf import settings
from pathlib import Path
from weasyprint import HTML
# from PIL import Image
# from io import BytesIO


def process_and_send_message(event, resolved_template):
    """
    Main orchestrator. Uses already-resolved template from serializer
    to avoid duplicate DB queries.

    Flow:
        1. Collect & merge all contacts (template + request)
        2. Render body, subject, attachments
        3. Send via correct provider
        4. Return result dict
    """
    try:
        if event.template_type == TemplateType.MESSAGE:
            contacts, rendered = _prepare_message_data(
                event, resolved_template)
            is_success, api_response = send_via_sms_provider(
                provider=event.provider,
                contacts=contacts,
                title=rendered["title"],
                message_body=rendered["body"],
            )

        elif event.template_type == TemplateType.EMAIL:
            contacts, rendered = _prepare_email_data(event, resolved_template)
            is_success, api_response = send_via_email_provider(
                provider=event.provider,
                to_contacts=contacts["to"],
                subject=rendered["subject"],
                message_body=rendered["body"],
                cc_contacts=contacts["cc"],
                bcc_contacts=contacts["bcc"],
                attachments=rendered["attachments"],
                from_email=rendered.get("sender_email"),
            )

        else:
            return {"status": "error", "message": "Invalid template type"}

        if is_success:
            return {
                "status": "success",
                "message": api_response.get("msg", "Sent successfully"),
            }
        else:
            return {
                "status": "error",
                "message": api_response.get("msg", "Failed to send"),
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}


def _prepare_message_data(event, template):
    """
    Merge SMS contacts and render body text.
    Returns: (contacts_list, rendered_dict)
    """
    # Collect contacts from template
    template_contacts = [c.phone for c in template.contacts.all()]
    for group in template.groups.all():
        template_contacts += [c.phone for c in group.contacts.all()]

    # Merge with request contacts (deduplicated)
    all_contacts = list(dict.fromkeys(
        filter(None, template_contacts + (event.to_contact or []))
    ))

    body_rendered = ""
    if template.content and template.content.template_path:
        body_rendered = render_to_string(
            template.content.template_path, event.variables or {})

    rendered = {
        "title": _render_text(getattr(template, "title", ""), event.variables),
        "body": body_rendered,
    }

    return all_contacts, rendered


def _prepare_email_data(event, template):
    """
    Merge all TO/CC/BCC contacts, render subject + body + attachments.
    Returns: (contacts_dict, rendered_dict)
    """
    # --- TO contacts ---
    to_list = [c.email for c in template.to_contacts.all()]
    for group in template.to_group.all():
        to_list += [c.email for c in group.contacts.all()]
    to_list = list(dict.fromkeys(
        filter(None, to_list + (event.to_contact or []))))

    # --- CC contacts ---
    cc_list = [c.email for c in template.cc_contacts.all()]
    for group in template.cc_group.all():
        cc_list += [c.email for c in group.contacts.all()]
    cc_list = list(dict.fromkeys(filter(None, cc_list)))

    # --- BCC contacts ---
    bcc_list = [c.email for c in template.bcc_contacts.all()]
    for group in template.bcc_group.all():
        bcc_list += [c.email for c in group.contacts.all()]
    bcc_list = list(dict.fromkeys(filter(None, bcc_list)))

    contacts = {"to": to_list, "cc": cc_list, "bcc": bcc_list}

    # --- Render subject & body ---
    content = template.content
    subject_text = getattr(template, "subject", "")

    body_rendered = ""
    if content and content.template_path:
        body_rendered = render_to_string(
            content.template_path, event.variables or {})

    rendered = {
        "subject": subject_text,
        "body": body_rendered,
        "attachments": _prepare_attachments(template, event.variables),
        "from_email": getattr(template, "sender_email", None),
        }
    return contacts, rendered


def _prepare_attachments(template, variables):

    attachments = []

    for attachment in template.attachments.all():
        template_path = attachment.template_path
        if not template_path:
            continue


        rendered_content = render_to_string(
                    template_path, variables or {}
                )

        # Convert HTML → PDF
        try:
            pdf_bytes = HTML(string=rendered_content).write_pdf()
        except Exception as e:
            raise ValueError(
                f"Failed to generate PDF for template: {template_path}"
            ) from e

        # Generate filename
        filename = Path(template_path).stem + ".pdf"

        attachments.append({
            "filename": filename,
            "content": pdf_bytes,
            "is_binary": True,
        })

    return attachments

def _render_text(raw_text, variables):
    """
    Render a Django template string with the given variables dict.
    Returns empty string if raw_text is falsy.
    """
    if not raw_text:
        return ""
    return Template(raw_text).render(Context(variables or {}))


def send_via_sms_provider(provider, contacts, title, message_body):
    print(f"[SMS] Provider : {provider.name if provider else 'Default'}")
    print(f"[SMS] To       : {contacts}")
    print(f"[SMS] Title    : {title}")
    print(f"[SMS] Body     : {message_body}")
    return True, {"status": "success", "msg": "SMS Sent (Demo)"}


def send_via_email_provider(
    provider,
    to_contacts,
    subject,
    message_body,
    cc_contacts=None,
    bcc_contacts=None,
    attachments=None,
    from_email=None

):
    cc_contacts = cc_contacts or []
    bcc_contacts = bcc_contacts or []
    attachments = attachments or []

    try:

        email_provider = get_provider(provider)
        email_provider.send_email(
            to_contacts=to_contacts,
            subject=subject,
            message_body=message_body,
            cc_contacts=cc_contacts,
            bcc_contacts=bcc_contacts,
            attachments=attachments,
            from_email=from_email,

        )

        return True, {"msg": "Email sent successfully"}

    except Exception as e:
        return False, {"msg": str(e)}
