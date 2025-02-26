import requests
from celery import shared_task
from django.utils.timezone import now
from .models import ScheduledJob

from celery import shared_task

from celery import shared_task

@shared_task
def execute_scheduled_job(job_id):
    print(f"Executing scheduled job with ID: {job_id}")
    return f"Executed job {job_id}"


'''@shared_task
def execute_scheduled_job(job_id):
    """
    Celery executes this task as per the Cron schedule.
    """
    print(f"Executing scheduled job with ID: {job_id}")
    job = ScheduledJob.objects.get(id=job_id)
    try:
        if job.method == "GET":
            response = requests.get(job.url)
        else:
            response = requests.post(job.url)

        # Update last execution time
        job.last_executed_at = now()
        job.save()
        return f"Executed {job.method} {job.url} - Status Code: {response.status_code}"
    except Exception as e:
        return f"Error executing {job.method} {job.url}: {str(e)}"'''
