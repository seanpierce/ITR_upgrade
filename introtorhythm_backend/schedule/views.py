from datetime import datetime
from rest_framework import viewsets

from .models import Show
from .serializers import ShowSerializer

class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.filter(end_date_time__gt=datetime.now(), active=True).order_by("start_date_time")
    serializer_class = ShowSerializer
