from django.contrib import admin
from .models import Task,Announcement,Training,Meeting
# Register your models here.

admin.site.register(Task)
admin.site.register(Announcement)
admin.site.register(Training)
admin.site.register(Meeting)
