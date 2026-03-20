from django.contrib import admin

from client_app.hr.staffing_plan.models import Staffing , Staffing_Plan


# Register your models here.
admin.site.register(Staffing_Plan)
admin.site.register(Staffing)

