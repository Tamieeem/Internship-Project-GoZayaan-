from .logging import save_api_log


class LoggingMixin:
    """
    Mixin to automatically log exceptions for any ViewSet.
    """

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        save_api_log(
            self.request,
            response.data if hasattr(response, 'data') else {},
            response.status_code,
            error=str(exc)
        )
        return response
