from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import date
from client_app.authentication.custom_auth import User_Manager
from client_app.core.doc_status.models import Doc_Status

class Last_Logged_In(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_on = models.DateField(default=date.today, editable=False)
    creation_time = models.DateTimeField(default=timezone.now, editable=False)
    last_modified = models.DateField(default=date.today, editable=False)
    docstatus = models.IntegerField(default=0, null=True)
    idx = models.IntegerField(default=0, null=True)
    disabled = models.IntegerField(default=0, null=True)
    status = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, related_name='%(class)s_tbldocstatus', default="", null=True)
    doctype = models.CharField(max_length=255, null=True,default="Lite_User_Permission")
    parent = models.CharField(max_length=255, null=True, default="")
    class Meta:
        db_table = 'last_logged_in'


class Lite_User_Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_on = models.DateField(default=date.today, editable=False)
    creation_time = models.DateTimeField(default=timezone.now, editable=False)
    last_modified = models.DateField(default=date.today, editable=False)
    docstatus = models.IntegerField(default=0, null=True)
    idx = models.IntegerField(default=0, null=True)
    disabled = models.IntegerField(default=0, null=True)
    status = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, related_name='%(class)s_tbldocstatus', default="", null=True)
    doctype = models.CharField(max_length=255, null=True,default="Lite_User_Permission")
    name = models.EmailField(null=True, default="")
    class Meta:
        db_table = 'lite_user_group'
        
class Lite_User_Permitted_Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_on = models.DateField(default=date.today, editable=False)
    creation_time = models.DateTimeField(default=timezone.now, editable=False)
    last_modified = models.DateField(default=date.today, editable=False)
    docstatus = models.IntegerField(default=0, null=True)
    idx = models.IntegerField(default=0, null=True)
    disabled = models.IntegerField(default=0, null=True)
    status = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, related_name='%(class)s_tbldocstatus', default="", null=True)
    parent_type = models.CharField(max_length=255, null=True,default="User")
    parent = models.CharField(max_length=255, null=True,default="")
    doctype = models.CharField(max_length=255, null=True,default="Lite_User_Permission")
    permitted_company_id = models.IntegerField( null=True,  default=0)
    class Meta:
        db_table = 'lite_user_permitted_company'


class Lite_User(AbstractBaseUser, PermissionsMixin):
    created_on = models.DateField(default=date.today, editable=False)
    creation_time = models.DateTimeField(default=timezone.now, editable=False)
    last_modified = models.DateField(default=date.today, editable=False)
    docstatus = models.IntegerField(default=0, null=True)
    owner = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True,blank=True, related_name='%(class)s_ownerlum', default=None)
    modified_by = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True, related_name='%(class)s_modified_bylum', default=None)
    disabled = models.IntegerField(default=0, null=True)
    status = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, related_name='%(class)s_lite_status', default=None,null=True)
    user_group = models.ForeignKey(Lite_User_Group, on_delete=models.DO_NOTHING, related_name='%(class)s_lite_user_group', default=None,null=True)
    doctype = models.CharField(max_length=255, null=True,default="")
    name = models.EmailField(unique=False, default="")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True, default="")
    last_name = models.CharField(max_length=255, null=True, default="")
    contact_no = models.CharField(max_length=255, null=True, default="")
    department = models.CharField(max_length=255, null=True, default="")
    gender = models.CharField(max_length=255, null=True, default="")
    main_role = models.CharField(max_length=255, null=True, default="")
    default_company = models.CharField( null=True, default="")
    permitted_companies = models.ManyToManyField(Lite_User_Permitted_Company, blank=True)
    dp = models.CharField(max_length=255, null=True, default="")
    is_onboarded = models.IntegerField(null=True, default=0)
    has_changed_default_password = models.IntegerField(default=0, null=True)
    is_active = models.BooleanField(default=True,null=True)
    is_staff = models.BooleanField(default=False,null=True)
    objects = User_Manager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name"]
    user_permissions = models.CharField(max_length=255, null=True, default="")
    groups = models.CharField(max_length=255, null=True, default="")
    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        self.name = self.email  
        super().save(*args, **kwargs)
    class Meta:
        db_table = "lite_user"
