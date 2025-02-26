from django.contrib import admin
from .models import ScheduledJob,JobExecutionHistory

admin.site.register(ScheduledJob)
# Register your models here.
admin.site.register(JobExecutionHistory)