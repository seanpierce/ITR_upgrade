from datetime import datetime

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from content.models import MarqueeText, About
from content.serializers import MarqueeTextSerializer, AboutSerializer
from schedule.models import Show
from schedule.serializers import ShowSerializer

class GetContentViewSet(viewsets.ViewSet):
    """
    Custom endpoint returning combined content from multiple models.
    """

    def list(self, request):
        # Query the DB
        shows = Show.objects.filter(end_date_time__gt=datetime.now(), active=True).order_by("start_date_time")

        # Find current show in Python
        current_show = next((s for s in shows if s.happening_now), None)
        coming_up = [s for s in shows if s != current_show]

        # Serialize the data
        marquee_text = MarqueeText.objects.filter(active=True)
        about = About.objects.all()
        marquee_serializer = MarqueeTextSerializer(marquee_text, many=True)
        about_serializer = AboutSerializer(about, many=True)
        show_serializer = ShowSerializer(shows, many=True)

        return Response({
            "marqueeText": marquee_serializer.data[0] if marquee_serializer.data else None,
            "about": about_serializer.data[0] if about_serializer.data else None,
            "currentShow": ShowSerializer(current_show).data if current_show else None,
            "comingUp": ShowSerializer(coming_up, many=True).data if coming_up else [],
        })