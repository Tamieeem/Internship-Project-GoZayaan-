from abc import ABC, abstractmethod


class BaseEmailProvider(ABC):
    """
    Base class for all email providers.
    Enforces a consistent interface.
    """
    @abstractmethod
    def send_email(
        self,
        to_contacts,
        subject,
        message_body,
        cc_contacts=None,
        bcc_contacts=None,
        attachments=None,
        from_email=None,
    ):
        raise NotImplementedError("Providers must implement send_email()")
