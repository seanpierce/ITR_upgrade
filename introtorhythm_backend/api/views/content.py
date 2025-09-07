from datetime import datetime
import pytz

from rest_framework import viewsets
from rest_framework.response import Response

from content.models import MarqueeText, About
from content.serializers import MarqueeTextSerializer, AboutSerializer
from schedule.models import Show
from schedule.serializers import ShowSerializer

PACIFIC = pytz.timezone("America/Los_Angeles")


class GetContentViewSet(viewsets.ViewSet):
    """
    API endpoint to retrieve core website content.

    Returns:
    - `marqueeText`: string combining active MarqueeText, current show, and upcoming shows (times in Pacific Time, PST/PDT).
    - `about`: Content for the about/info section of the website.

    Example marquee string:
    "{marquee text} | Listening Now: {current show} | Coming Up: {show1} at 02:00 PM PDT, {show2} at 05:00 PM PDT"
    """

    def list(self, request):
        now = datetime.now()

        # Fetch shows
        shows = Show.objects.filter(end_date_time__gt=now, active=True).order_by("start_date_time")

        # Determine current and upcoming shows
        current_show = shows.filter(start_date_time__lte=now, end_date_time__gte=now).first()
        coming_up = shows.exclude(id=current_show.id) if current_show else shows

        # Fetch other content
        marquee_text_obj = MarqueeText.objects.filter(active=True).first()
        about_text = About.objects.first()

        # Serialize content
        marquee_serializer_data = MarqueeTextSerializer(marquee_text_obj).data if marquee_text_obj else None
        about_serializer_data = AboutSerializer(about_text).data if about_text else None

        # Build marquee text string
        marquee_content = self.build_marquee_content(marquee_serializer_data, current_show, coming_up)

        return Response({
            "marqueeText": marquee_content,
            "about": about_serializer_data
        })

    @staticmethod
    def build_marquee_content(marquee_data, current_show, other_shows):
        """
        Builds a single string combining marquee text, current show, and upcoming shows,
        with Pacific Time (PST/PDT) shown for each show.
        """
        tz_name = datetime.now(pytz.timezone("America/Los_Angeles")).strftime('%Z')
        parts = []

        # Base marquee text
        if marquee_data and "content" in marquee_data:
            parts.append(marquee_data["content"])

        # Add current show
        if current_show:
            parts.append(f"Listening Now: {current_show.title}")

        # Add upcoming shows
        if other_shows:
            upcoming_parts = []
            for show in other_shows:
                if show.start_date_time:
                    # Convert to Pacific Time and format
                    formatted_time = show.start_date_time.strftime("%I:%M %p")
                else:
                    formatted_time = "Unknown Time"
                upcoming_parts.append(f"{show.title} at {formatted_time} {tz_name}")
            parts.append(f"Coming Up: {', '.join(upcoming_parts)}")

        return f"{' | '.join(parts)} | "