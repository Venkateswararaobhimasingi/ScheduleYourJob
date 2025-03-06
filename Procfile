web: gunicorn ScheduleYourJob.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn ScheduleYourJob.wsgi.wsgi