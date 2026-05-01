from .views import ContentViewSet, ProviderViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstantMessageAPIView , EventListAPIView, EventRetryAPIView, LogAdminViewSet



router = DefaultRouter()
router.register(r'content', ContentViewSet, basename='content')
router.register(r'providers', ProviderViewSet, basename='provider')
router.register(r'logs', LogAdminViewSet, basename='admin-logs')

urlpatterns = [
    path('', include(router.urls)),
    path('events/sent/', InstantMessageAPIView.as_view(),
         name='send-instant-message'),
    path('events/', EventListAPIView.as_view(),
         name='event-list'),
    path('events/<int:event_id>/retry/', EventRetryAPIView.as_view(),
         name='event-retry'),
]
