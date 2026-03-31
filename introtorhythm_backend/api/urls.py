from django.urls import path
from .views import *

urlpatterns = [
    path('shows/', GetShowsAPIView.as_view(), name='getshows'),
    path('scheduler/', InitiateSchedulerAPIView.as_view(), name='initiate_scheduler'),
    path('content/', GetContentAPIView.as_view(), name='get_content'),
]