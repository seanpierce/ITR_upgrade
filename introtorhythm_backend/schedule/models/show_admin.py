from django.contrib import admin
from django.utils.html import format_html
from schedule.helpers import TIMES
from .show_filter import ShowFilter


class ShowAdmin(admin.ModelAdmin):
    search_fields = ['title', 'info']
    list_filter = [ShowFilter, 'active']
    list_display = ['title', 'date', 'start_time', 'get_formatted_end_time', 'image_tag']
    actions = ['mark_shows_active', 'mark_shows_inactive']
    exclude = ['start_date_time', 'end_date_time', 'image_tag']

    def mark_shows_active(self, request, queryset):
        queryset.update(active=True)

    def mark_shows_inactive(self, request, queryset):
        queryset.update(active=False)

    def get_formatted_end_time(self, obj):
        """
        Returns the hour of the end_date_time field.
        Value is formatted using the TIMES helper.
        ex: if the hour is 18, field would show 6 pm.
        """
        if obj is None or obj.end_date_time is None:
            return None
        
        return TIMES[obj.end_date_time.hour]

    get_formatted_end_time.short_description = 'End Time'

    def image_tag(self, obj):
        img_html = """
            <img src="{}" 
                onclick="window.open('{}', '_blank')"
                style="cursor:pointer;max-height:150px;max-width:150px;" />
        """
        try:
            if obj is not None and obj.show_image:
                return format_html(img_html.format(obj.show_image.url, obj.show_image.url))
            else:
                return 'No image available'
        except:
            return 'No image available'

    image_tag.short_description = 'Image'