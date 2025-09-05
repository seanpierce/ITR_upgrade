from rest_framework import viewsets
from .models import Show
from .serializers import ShowSerializer

class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
