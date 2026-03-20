from django.contrib import admin



from client_app.hr.training_result.models import Result, Training_Result


# Register your models here.
admin.site.register(Training_Result)
admin.site.register(Result)

