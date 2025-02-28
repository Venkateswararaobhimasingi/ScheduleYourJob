from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime
from croniter import croniter
from django.utils.timezone import now
from .models import ScheduledJob,JobExecutionHistory
from .views import calls


import pytz
from django.utils.timezone import now
from croniter import croniter
from datetime import datetime

def run_scheduled_jobs():
    jobs = ScheduledJob.objects.all()
    current_time = now()

    # Convert to IST
    ist = pytz.timezone("Asia/Kolkata")
    current_time_ist = current_time.astimezone(ist)

    for job in jobs:
        if not job.next_run_at:
            cron = croniter(job.cron_expression, current_time_ist)
            job.last_executed_at = current_time_ist
            job.next_run_at = cron.get_next(datetime)
            job.save()
            continue

        if job.next_run_at <= current_time_ist:
            try:
               
                response = calls(job)
                

                job.last_executed_at = current_time_ist
                cron = croniter(job.cron_expression, current_time_ist)
                job.next_run_at = cron.get_next(datetime)
                job.save()
                JobExecutionHistory.objects.create(
                    job=job,
                    executed_at=current_time_ist,
                    response_status=response.status_code,
                    response_body=response.text[:500],  # Limit response storage
                )


            except Exception as e:
                print(f"Error executing job {job.url}: {e}")
                JobExecutionHistory.objects.create(
                    job=job,
                    executed_at=current_time_ist,
                    response_status=500,
                    response_body=str(e),
                )

scheduler = BackgroundScheduler()

def start():
    global scheduler
    if not scheduler.running:
        scheduler.add_job(run_scheduled_jobs, "interval", minutes=1)
        scheduler.start()
