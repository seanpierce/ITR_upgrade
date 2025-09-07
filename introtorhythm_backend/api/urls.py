from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GetContentViewSet

router = DefaultRouter()
router.register(r'content', GetContentViewSet, basename='getcontent')

urlpatterns = [
    path('', include(router.urls))
]