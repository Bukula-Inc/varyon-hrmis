from django.urls import path, include

urlpatterns = [
   
    path("staff_work_plan_report/",include ("client_app.staff.staff_reports.staff_work_plan_report.urls"), name='staff_work_plan_report'),
 
]