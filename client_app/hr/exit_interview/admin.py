from django.contrib import admin


from client_app.hr.exit_interview.models import Interviewers, Exit_Interview


# Register your models here.
admin.site.register(Interviewers)
admin.site.register(Exit_Interview)

