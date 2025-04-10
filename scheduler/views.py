from django.shortcuts import render, redirect
from .models import ScheduledJob
from django.contrib.auth.decorators import login_required
import requests
@login_required
def dashboard(request):
    jobs = ScheduledJob.objects.all().order_by('-created_at') 
    return render(request, "scheduler/dashboard.html", {"jobs": jobs})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ScheduledJob
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_job(request):
    if request.method == "POST":
        url = request.POST.get("url")
        method = request.POST.get("method")
        cron_expression = request.POST.get("cron_expression")

        if not url or not cron_expression:
            return JsonResponse({"error": "URL and Cron Expression are required."}, status=400)

        # Create and save job
        job = ScheduledJob.objects.create(
            url=url,
            method=method,
            cron_expression=cron_expression
        )

        # Redirect to dashboard after job creation
        return redirect("dashboard")  

    return render(request, "scheduler/create_job.html")




def delete_job(request):
    job_id=request.POST.get('id')
    job = ScheduledJob.objects.get(id=job_id)
    job.delete()
    return redirect("dashboard")



from django.http import JsonResponse
from django.utils.timezone import now
import pytz
from datetime import datetime
from .models import ScheduledJob, JobExecutionHistory

def sample_function(request):
    ist = pytz.timezone("Asia/Kolkata")
    print(datetime.now(ist))
    print("✅ Scheduled job executed successfully!")

    # Fetch all scheduled jobs
    scheduled_jobs = ScheduledJob.objects.all()

    for job in scheduled_jobs:
        # Get execution history for the job
        history_records = JobExecutionHistory.objects.filter(job=job).order_by('-id')

        if history_records.count() > 100:
            # Find the oldest records by getting the IDs beyond the latest 100
            oldest_ids = history_records.values_list('id', flat=True)[100:]
            
            # Delete records with those IDs
            JobExecutionHistory.objects.filter(id__in=oldest_ids).delete()

    return JsonResponse({"message": "Job executed", "status": "success"})




from django.shortcuts import render, get_object_or_404
from .models import ScheduledJob, JobExecutionHistory

def job_history(request):
    job_id=request.POST.get('id')
    job = get_object_or_404(ScheduledJob, id=job_id)
    history = JobExecutionHistory.objects.filter(job=job).order_by("-executed_at")
    return render(request, "scheduler/job_history.html", {"job": job, "history": history})

from django.contrib.auth import logout as auth_logout
def custom_logout(request):
    auth_logout(request)
    return redirect("login")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
              # Redirect to 'next' URL or dashboard
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "scheduler/login.html")

def calls(job):
    if job.method == "GET":
        response = requests.get(job.url) 
    else :
        response = requests.post(job.url, data={})
    return response



def m1(request):
    return render(request, "scheduler/m1.html")
def m2(request):
    return render(request, "scheduler/m2.html")
def m3(request):
    return render(request, "scheduler/m3.html")