from django.contrib import admin


from client_app.hr.training_event.models import Employees_Training, Training_Event


# Register your models here.
admin.site.register(Training_Event)
admin.site.register(Employees_Training)

