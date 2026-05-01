import logging
import traceback

from django.db import transaction
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from utils.pagination import StandardLimitOffsetPagination
from utils.logging import save_api_log
from utils.mixins import LoggingMixin
from utils.decorators import custom_permissions

# Logger initialize
logger = logging.getLogger(__name__)


class BaseModelViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    Base ViewSet for all APIs.
    """
    pagination_class = StandardLimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    http_method_names = ['get', 'post', 'patch']

    read_serializer_class = None
    write_serializer_class = None
    custom_permission_groups: list = []

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return self.write_serializer_class or self.read_serializer_class
        return self.read_serializer_class

    def _read_data(self, instance):
        if self.read_serializer_class:
            return self.read_serializer_class(instance, context=self.get_serializer_context()).data
        return {}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                serializer.save()

            # Success flow
            response_data = self._read_data(serializer.instance)

            # API Hit log (save to the database)
            save_api_log(request, response_data, status.HTTP_201_CREATED)

            headers = self.get_success_headers(response_data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

        except IntegrityError as exc:
            # Error log for developers (File/Console e jabe)
            logger.exception("IntegrityError occurred during creation.")

            response_data = {
                "detail": "Database constraint error.",
                "error": str(exc)
            }
            # Error API Hit log (save to the database so that developers can see)
            save_api_log(request, response_data, status.HTTP_400_BAD_REQUEST)
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            # Unexpected error log with full traceback
            logger.exception("Unhandled exception during creation: %s", exc)
            tb = traceback.format_exc()

            response_data = {
                "detail": "Internal server error.",
                "error": str(exc),
                "traceback": tb,  # Detail error history JSON
            }
            save_api_log(request, response_data,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                serializer.save()

            response_data = self._read_data(instance)
            save_api_log(request, response_data, status.HTTP_200_OK)
            return Response(response_data, status=status.HTTP_200_OK)

        except IntegrityError as exc:
            logger.exception(
                "IntegrityError occurred during partial update for ID: %s", instance.id)

            response_data = {
                "detail": "Database constraint error.",
                "error": str(exc)
            }
            save_api_log(request, response_data, status.HTTP_400_BAD_REQUEST)
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.exception(
                "Unhandled exception during partial update for ID: %s. Error: %s", instance.id, exc)
            tb = traceback.format_exc()

            response_data = {
                "detail": "Internal server error.",
                "error": str(exc),
                "traceback": tb,
            }
            save_api_log(request, response_data,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
