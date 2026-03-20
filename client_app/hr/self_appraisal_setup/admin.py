from django.contrib import admin

from client_app.hr.self_appraisal_setup.models import Self_Appraisal_Appraisee, Self_Appraisal_Setup

# Register your models here.
admin.site.register(Self_Appraisal_Appraisee)
admin.site.register(Self_Appraisal_Setup)

