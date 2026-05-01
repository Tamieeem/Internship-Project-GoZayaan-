from rest_framework import status
from apps.events.models import Logs


def save_api_log(request, response_data, status_code, error=''):
    """
    Global helper function to save API logs.
    """
    Logs.objects.create(
        status=status_code,
        error=error,
        region=request.data.get('region', '') if hasattr(
            request, 'data') else '',
        service=request.data.get('service', '') if hasattr(
            request, 'data') else '',
        request_by=str(request.user),
        api_path=request.path,
        request_body=request.data if hasattr(request, 'data') else {},
        response=response_data
    )
