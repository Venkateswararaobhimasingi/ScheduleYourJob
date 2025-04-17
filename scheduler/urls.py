from django.urls import path
from .views import dashboard, create_job, delete_job,sample_function,job_history,custom_logout,custom_login,m1,m2,m3,recreate_all_jobs,get_location_by_ip
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", custom_login, name="login"),
    path("logout/", custom_logout, name="logout"),
    path("create_job/", create_job, name="create_job"),
    path("delete/", delete_job, name="delete_job"),
    path("sf/",sample_function, name="sample_function"),
    path("history/", job_history, name="job_history"),  # /history/<int:job_id>
    path("m1/", m1, name="m1"),
    path("m2/", m2, name="m2"), 
    path("m3/", m3, name="m3"),
    path('rjob/',recreate_all_jobs,name="rjob"),
    path('cloc',get_location_by_ip,name="cloc"),

]
