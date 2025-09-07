from datetime import datetime
import pytz

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from content.models import MarqueeText, About
from content.serializers import MarqueeTextSerializer, AboutSerializer
from schedule.models import Show
from schedule.serializers import ShowSerializer

# current timezone (PST or PDT depending on time of year)
tz_name = datetime.now(pytz.timezone("America/Los_Angeles")).strftime('%Z')

class GetContentViewSet(viewsets.ViewSet):
    """
    Gets core content for the website including:
    - Marquee text
    - About text
    - Current show
    - Upcoming shows
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

        marquee_content = build_marquee_content(marquee_serializer.data, current_show, coming_up)

        return Response({
            "marqueeText": marquee_content,
            "about": about_serializer.data[0] if about_serializer.data else None,
            "currentShow": ShowSerializer(current_show).data if current_show else None,
            "comingUp": ShowSerializer(coming_up, many=True).data if coming_up else [],
        })
    

def build_marquee_content(marquee_serializer_data, current_show, other_shows):
    """
    Builds a single string combining marquee text, current show, and upcoming shows.
    
    Example output:
    "{marquee text content} | Listening Now: {current show title} | Coming Up: {title 1} at {start_time 1}, {title 2} at {start_time 2}"
    """

    # Base marquee text
    marquee_text = marquee_serializer_data[0]['content'] if marquee_serializer_data else ""

    parts = [marquee_text]

    # Add current show if present
    if current_show:
        parts.append(f"Listening Now: {current_show.title}")

    # Add upcoming shows
    if other_shows:
        upcoming_parts = []
        for show in other_shows:
            # Format start_time
            local_start = show.start_date_time.strftime('%I:%M %p')
            upcoming_parts.append(f"{show.title} at {local_start} {tz_name}")
        upcoming_str = ", ".join(upcoming_parts)
        parts.append(f"Coming Up: {upcoming_str}")

    # Join everything with ' | '
    return " | ".join(parts)