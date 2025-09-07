from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from schedule.views import ShowViewSet
from content.views import MarqueeTextViewSet, AboutViewSet, GetContentViewSet

router = DefaultRouter()
router.register(r'schedule/shows', ShowViewSet, basename='Show')
router.register(r'content', GetContentViewSet, basename='GetContent')
router.register(r'content/marqueetext', MarqueeTextViewSet, basename='Marquee')
router.register(r'content/about', AboutViewSet, basename='About')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]