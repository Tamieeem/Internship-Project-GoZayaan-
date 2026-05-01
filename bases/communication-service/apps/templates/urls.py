from amqp import Message
from django.urls import path, include
from .views import EmailTemplateViewSet, MessageTemplateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'email-templates', EmailTemplateViewSet,
                basename='email-template')
router.register(r'message-templates', MessageTemplateViewSet,
                basename='message-template')

urlpatterns = [
    path('', include(router.urls)),
]
