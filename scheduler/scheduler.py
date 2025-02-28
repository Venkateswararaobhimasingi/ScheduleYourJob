from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime
from croniter import croniter
from django.utils.timezone import now
from django.db import transaction
from .models import ScheduledJob, JobExecutionHistory
import pytz

def run_scheduled_jobs():
    jobs = ScheduledJob.objects.all()
    current_time = now().astimezone(pytz.timezone("Asia/Kolkata"))  # Convert to IST

    for job in jobs:
        with transaction.atomic():  # Prevents duplicate execution
            job = ScheduledJob.objects.select_for_update().get(id=job.id)  # Lock job row

            if not job.next_run_at:
                cron = croniter(job.cron_expression, current_time)
                job.last_executed_at = current_time
                job.next_run_at = cron.get_next(datetime)
                job.save()
                continue

            if job.next_run_at <= current_time:
                try:
                    response = requests.get(job.url) if job.method == "GET" else requests.post(job.url, data={})

                    job.last_executed_at = current_time
                    cron = croniter(job.cron_expression, current_time)
                    job.next_run_at = cron.get_next(datetime)
                    job.save()

                    JobExecutionHistory.objects.create(
                        job=job,
                        executed_at=current_time,
                        response_status=response.status_code,
                        response_body=response.text[:500],  # Limit response storage
                    )

                except Exception as e:
                    print(f"Error executing job {job.url}: {e}")
                    JobExecutionHistory.objects.create(
                        job=job,
                        executed_at=current_time,
                        response_status=500,
                        response_body=str(e),
                    )

scheduler = BackgroundScheduler()

def start():
    global scheduler
    if not scheduler.running:
        scheduler.add_job(run_scheduled_jobs, "interval", minutes=1)
        scheduler.start()
