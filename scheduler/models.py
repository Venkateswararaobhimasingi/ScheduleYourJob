from django.db import models
from django.contrib.auth.models import User
import json

from django.db import models

class ScheduledJob(models.Model):
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
    ]

    url = models.URLField()
    method = models.CharField(max_length=4, choices=METHOD_CHOICES, default='GET')
    cron_expression = models.CharField(max_length=100, help_text="Cron format expression" ,default="* * * * *")
    created_at = models.DateTimeField(auto_now_add=True)
    last_executed_at = models.DateTimeField(null=True, blank=True)
    interval_minutes = models.IntegerField(default=5) 
    next_run_at = models.DateTimeField(null=True, blank=True)
   
    def __str__(self):
        return f"{self.method} {self.url} (Cron: {self.cron_expression})"


class JobExecutionHistory(models.Model):
    job = models.ForeignKey(ScheduledJob, on_delete=models.CASCADE, related_name="executions")
    executed_at = models.DateTimeField(auto_now_add=True)
    response_status = models.IntegerField()
    response_body = models.TextField()

    def __str__(self):
        return f"Executed {self.job.method} {self.job.url} at {self.executed_at}"