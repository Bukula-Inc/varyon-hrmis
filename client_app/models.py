from django.db import models
from django.utils import timezone
from datetime import date
from client_app.authentication.models import Lite_User
from client_app.core.doc_status.models import Doc_Status      
from controllers.utils import Utils

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

class BaseModel(models.Model):
    id= models.BigAutoField(primary_key=True)
    created_on = models.DateField(default=date.today, editable=False, null=True)
    creation_time = models.DateTimeField(default=timezone.now, editable=False, null=True)
    last_modified = models.DateField(default=date.today, editable=False, null=True)
    docstatus = models.IntegerField(default=0, null=True)
    owner = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, null=True, related_name='%(class)s_owner', default=None)
    modified_by = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, null=True, related_name='%(class)s_modified_by', default=None)
    idx = models.IntegerField(default=0, null=True)
    disabled = models.IntegerField(default=0, null=True)
    status = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, related_name='%(class)s_docstatus', default=None)
    doctype = models.CharField(max_length=255, null=True,default="")
    company_id = models.IntegerField(null=True, default=0)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.doctype:
            self.doctype = self.__class__.__name__
        super().save(*args, **kwargs)

class TableModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_on = models.DateField(default=date.today, editable=False, null=True)
    creation_time = models.DateTimeField(default=timezone.now, editable=False, null=True)
    last_modified = models.DateField(default=date.today, editable=False, null=True)
    docstatus = models.IntegerField(default=0, null=True)
    owner = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING,null=True, related_name='%(class)s_owner', default=None)
    modified_by = models.ForeignKey(Lite_User, on_delete=models.DO_NOTHING, null=True, related_name='%(class)s_modified_by', default=None)
    idx = models.IntegerField(default=0, null=True)
    disabled = models.IntegerField(default=0, null=True)
    status = models.ForeignKey(Doc_Status, on_delete=models.DO_NOTHING, null=True, related_name='%(class)s_tbldocstatus', default=None)
    parent_type = models.CharField(max_length=255, null=True,default="")
    parent = models.CharField(max_length=255, null=True,default="")
    doctype = models.CharField(max_length=255, null=True,default="")
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        last_object = self.__class__.objects.using(self._state.db).last()
        new_id = self.id
        if not new_id and last_object:
            self.id = last_object.id + 1
        if not self.doctype:
            self.doctype = self.__class__.__name__
        super().save(*args, **kwargs)



