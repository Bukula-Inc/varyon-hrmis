from django.contrib import admin

from client_app.hr.interview_round.models import Interview_Round, Round


# Register your models here.
admin.site.register(Interview_Round)
admin.site.register(Round)

