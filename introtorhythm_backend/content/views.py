from rest_framework import viewsets

from .models import MarqueeText, About
from .serializers import MarqueeTextSerializer, AboutSerializer

class MarqueeTextViewSet(viewsets.ModelViewSet):
    queryset = MarqueeText.objects.all()
    serializer_class = MarqueeTextSerializer

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
