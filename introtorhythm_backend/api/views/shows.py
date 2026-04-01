from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from schedule.services import initiate_ezstream
from schedule.models import Show
from schedule.serializers import ShowSerializer

class GetShowsAPIView(APIView):
    """
    API endpoint to handle requests to retrieve active shows. 
    It filters shows that have an end time greater than the current time and are marked as active, 
    then orders them by their start time.
    """
    def get(self, request):
        now = datetime.now()
        shows = Show.objects.filter(end_date_time__gt=now, active=True).order_by("start_date_time")
        return Response(ShowSerializer(shows, many=True).data)



class InitiateSchedulerAPIView(APIView):
    """
    API endpoint to trigger the scheduler to check for a show to be played at a specific date and time. 
    Then, the process initiates a new instance of ezstreame if a show is active. 
    This can be set up as a cron job to run every hour.
    For example, you can add the following line to your crontab (using `crontab -e`):
    0 * * * * curl -X GET "http://127.0.0.1:8000/my-endpoint/" -H "Authorization: Bearer MY_SECRET_KEY_123"
    """
    def get(self, request):
        today = timezone.localdate().strftime('%Y-%m-%d')
        current_hour = timezone.localtime().hour
        show = Show.objects.filter(date=today, start_time=current_hour, active=True).first()

        if show is None:
            return Response({"message": "No active show at this time."})

        # Here you would add the logic to initiate ezstream with the show's details.
        # This could involve making a system call, sending a message to a task queue, etc.
        # For example:
        result = initiate_ezstream(show)
        return Response({"message": result})