from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.dispatch import receiver
import pytz

from schedule.helpers import TIMES, DURATION


uploads = FileSystemStorage(location=settings.BASE_DIR) 

class Show(models.Model):
    """
    Django model for the shows.show ORM/ data table.
    """
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    info = models.TextField(default=None, blank=True, null=True)
    date = models.DateField()
    start_time = models.IntegerField(choices=TIMES)
    duration = models.IntegerField(choices=DURATION, default=1)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    show_image = models.ImageField(upload_to='shows/images/', max_length=500, blank=True, help_text='The show\'s image that will be displayed on the site while the show is live.')
    show_flyer = models.ImageField(upload_to='shows/images/', max_length=500, blank=True, help_text='The show\'s flyer that will be used on the schedule page and for social media.')
    pre_recorded_show = models.FileField(upload_to='uploads/scheduler/', storage=uploads, max_length=500, blank=True, help_text='Optional upload field for pre-recorded shows. Files MUST be in MP3 format.')

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['date', 'start_time']

    @property
    def happening_now(self):
        """
        Returns True if the current time is between start_date_time and end_date_time.
        """
        now_local = timezone.localtime(timezone.now())  # now in local timezone
        if self.start_date_time and self.end_date_time:
            return self.start_date_time <= now_local <= self.end_date_time
        return False


@receiver(models.signals.pre_save, sender=Show)
def pre_save(sender, instance, **kwargs):
    """
    Method that is executed before the instance is saved to the database.
    """
    set_end_date_time(instance)
    auto_delete_files_on_change(instance)


@receiver(models.signals.post_delete, sender=Show)
def post_delete(sender, instance, using, **kwargs):
    """
    Method that is executed after the instance is deleted from the database.
    """
    delete_files_when_instance_is_deleted(instance)


def set_end_date_time(instance):
    """
    Sets start_date_time and end_date_time as aware datetimes in the server's local timezone.
    """
    local_tz = timezone.get_current_timezone()

    start_naive = datetime(
        year=instance.date.year,
        month=instance.date.month,
        day=instance.date.day,
        hour=instance.start_time
    )

    # make aware in local TZ
    start_local = timezone.make_aware(start_naive, local_tz)

    instance.start_date_time = start_local
    instance.end_date_time = start_local + timedelta(hours=instance.duration)


def auto_delete_files_on_change(instance):
    """
    Deletes old image(s) and audio files from filesystem (AWS S3 and local)
    when a corresponding `Image` or `File` object is updated
    with new file.
    """
    if not instance.pk:
        return None

    try:
        show = Show.objects.get(pk=instance.pk)
        old_image = show.show_image
        old_flyer = show.show_flyer
        old_pre_recorded_show = show.pre_recorded_show
    except:
        return None

    new_image = instance.show_image
    new_flyer = instance.show_flyer
    new_pre_recorded_show = instance.pre_recorded_show

    if not old_image == new_image:
        old_image.delete(save=False)

    if not old_flyer == new_flyer:
        old_flyer.delete(save=False)

    if not old_pre_recorded_show == new_pre_recorded_show:
        old_pre_recorded_show.delete(save=False)


def delete_files_when_instance_is_deleted(instance):
    """
    Deletes image(s) and audio files from filesystem (AWS S3 and local)
    when a corresponding `Image` or `File` record is deleted.
    """
    instance.show_image.delete(save=False)
    instance.show_flyer.delete(save=False)
    instance.pre_recorded_show.delete(save=False)
