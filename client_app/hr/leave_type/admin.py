from django.contrib import admin

from .models import Leave_Type
from client_app.hr.leave_type.models import Leave_Type

# Register your models here.
admin.site.register(Leave_Type)
