from django.contrib import admin

from client_app.hr.leave_allocation.models import Leave_Allocation, Leaves

# Register your models here.
admin.site.register(Leave_Allocation)
admin.site.register(Leaves)
