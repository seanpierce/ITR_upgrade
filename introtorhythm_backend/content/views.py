from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MarqueeText, About
from .serializers import MarqueeTextSerializer, AboutSerializer

class MarqueeTextViewSet(viewsets.ModelViewSet):
    queryset = MarqueeText.objects.all()
    serializer_class = MarqueeTextSerializer

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class GetContentViewSet(viewsets.ViewSet):
    """
    Custom endpoint returning combined content from multiple models.
    """

    def list(self, request):
        # Query the DB
        marquee_texts = MarqueeText.objects.filter(active=True)
        abouts = About.objects.all()

        # Serialize the data
        marquee_serializer = MarqueeTextSerializer(marquee_texts, many=True)
        about_serializer = AboutSerializer(abouts, many=True)

        # Return both in a dict
        return Response({
            "marqueeText": marquee_serializer.data[0] if marquee_serializer.data else None,
            "about": about_serializer.data[0] if about_serializer.data else None,
        })