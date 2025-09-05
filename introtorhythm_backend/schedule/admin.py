from django.contrib import admin

from schedule.models.show import Show
from schedule.models.show_admin import ShowAdmin

admin.site.register(Show, ShowAdmin)
