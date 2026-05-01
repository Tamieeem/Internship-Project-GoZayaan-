from django.urls import path, include
from .views import ContactViewSet, GroupViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'contacts', ContactViewSet,
                basename='contact')
router.register(r'groups', GroupViewSet,
                basename='group')

urlpatterns = [
    path('', include(router.urls)),
]
