from django.contrib import admin


from client_app.hr.interview.models import Feedback, Interview


# Register your models here.
admin.site.register(Feedback)
admin.site.register(Interview)

