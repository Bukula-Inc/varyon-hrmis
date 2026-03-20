from services.raw import Raw
from controllers.caching import Caching
from controllers.hooks.controller import Hooks_Controller
from django.db import transaction, connections
from django.db.utils import DatabaseError
from django.utils.html import escape
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from management.defaults.core.tenant_admin import tenant_admin
from controllers.core_functions.core.user_controller import User_Controller
from client_app.authentication.models import Lite_User
from controllers.dbms.workflow import Workflow
from django.db.models.fields.related import ForeignKey
from django.db.models import Q, F
from ..utils import Utils
from ..utils.dates import Dates
from time import time
import operator
from functools import reduce
import re, json
from controllers.dbms.config import shared_models, cacheable_content, cacheable_lists, excluded_models

utils = Utils()
pp = utils.pretty_print
throw = utils.throw
dates = Dates()


class DBMS:
    def __init__(self, validation=utils.from_dict_to_object(), init_admin=False, skip_user_validation=False) -> None:
        # initialize caching
        self.caching = Caching.init()
        self.operating_docs = utils.from_dict_to_object({ "creating":{}, "updating":{}, "submitting":{}, "cancelling":{}, "deleting":{}, "retrieving":{}})
        # switch database depending on the requested domain
        self.raw = Raw()
        self.use_super_admin=False
        self.query_builder = Q
        self.main_tenant_db = self.raw.admin_db_config.get("NAME")
        self.shared_models = shared_models
        self.cacheable_content = cacheable_content
        self.cacheable_lists = cacheable_lists
        self.excluded_models = excluded_models
        self.skip_user_validation = skip_user_validation
        
        try:
            if init_admin:
                self.raw.add_tenant_db_to_db_list()
                self.config = self.raw.admin_db_config                
                self.tenant_db = self.config.get("NAME")
                validation = utils.from_dict_to_object({"host": self.raw.admin_url, "tenant_db":self.tenant_db, "tenant_id": f"{self.tenant_db}&%0"})
                self.host = self.raw.admin_url
            self.validation = validation
            if validation:
                domain = validation.host
                self.tenant_db = validation.tenant_db
                self.tenant_id = validation.tenant_id
                self.minify = validation.minify
                if self.validation.api_key:
                    self.use_super_admin = True
                db_config = self.raw.get_tenant_configurations(self.tenant_db)
                db_config.status == utils.ok or throw(f"DB ERROR:: Couldn't fetch tenant db configurations: {db_config.error_message} ")
                config_data = db_config.get("data")
                name = config_data.get("NAME") or config_data.get("dbname") or ''
                if name and name != '':
                    self.config = config_data
                    self.host = domain
                else:
                    return
                    # raise Exception(f"DATABASE CONNECTION ERROR: {domain}")
        except Exception as e:
            raise Exception(F"DATABASE CONNECTION ERROR: {e}")
        
        # init user controller
        self.current_user_id = utils.from_dict_to_object()
        self.current_user = utils.from_dict_to_object()
        self.admin_user = utils.from_dict_to_object()
        self.workflow = Workflow(self)
        self.exempt_models = ["Doc_Status", "Tenant", "Country","Industry","Sector","Registration_Type"]
        
        # INITIALIZE CACHING
        self.caching.init_caching(self.tenant_db)


        # get adminstrator
        admin_data = self.get_users("Administrator", get_role=False, fetch_password=True, skip_workflow=True, is_admin=True)

        if admin_data.status == utils.ok:
            self.admin_user = admin_data.data
            if self.use_super_admin or init_admin:
                self.current_user_id = self.admin_user.id
                self.current_user = self.admin_user
                self.validation.user = self.current_user_id
        
        if getattr(self.validation, "user", None):
            try:
                usr = self.get_users(self.validation.user, get_role=False, fetch_password=True, fetch_both=False)
                if usr.status == utils.ok:
                    self.current_user_id = self.validation.user
                    self.current_user = usr.data
            except Exception as e:
                if not self.skip_user_validation:
                    throw(f"Failed to configure user: {str(e)}")
        else:
            try:
                if admin_data.status == utils.ok and admin_data.data:
                    self.current_user_id = admin_data.data.id
                    self.current_user = admin_data.data
                else:
                    if not self.skip_user_validation:
                        throw(f"{self.tenant_db} Admin user retrieval failed::>|: {admin_data.error_message}")
            except Exception as e:
                throw(f"Failed to configure admin user: {str(e)}")
       
        
        self.user_controller = User_Controller(self, getattr(validation, "user", None), validation)


        # get system settings
        self.system_settings = utils.from_dict_to_object({})
        system_settings = self.get_system_settings(get_user_allowed_content=False)
        if system_settings.status == utils.ok:
            self.system_settings = system_settings.data
        
        
        
        self.complex_operator_map = {
            '|': operator.or_,
            '&': operator.and_,
            '=': lambda x, y: Q(**{x: y}),
            '!=': lambda x, y: ~Q(**{x: y}),
            '>': lambda x, y: Q(**{x + '__gt': y}),
            '<': lambda x, y: Q(**{x + '__lt': y}),
            '>=': lambda x, y: Q(**{x + '__gte': y}),
            '<=': lambda x, y: Q(**{x + '__lte': y}),
            'in': lambda x, y: Q(**{x + '__in': y}),
            'isnull': lambda x, y: Q(**{x + '__isnull': y}),
            'contains': lambda x, y: Q(**{x + '__contains': y}),
            'icontains': lambda x, y: Q(**{x + '__icontains': y}),
            'startswith': lambda x, y: Q(**{x + '__startswith': y}),
            'istartswith': lambda x, y: Q(**{x + '__istartswith': y}),
            'endswith': lambda x, y: Q(**{x + '__endswith': y}),
            'iendswith': lambda x, y: Q(**{x + '__iendswith': y}),
            'range': lambda x, y: Q(**{x + '__range': y}),
            'year': lambda x, y: Q(**{x + '__year': y}),
            'month': lambda x, y: Q(**{x + '__month': y}),
            'day': lambda x, y: Q(**{x + '__day': y}),
            'week_day': lambda x, y: Q(**{x + '__week_day': y}),
            'hour': lambda x, y: Q(**{x + '__hour': y}),
            'minute': lambda x, y: Q(**{x + '__minute': y}),
            'second': lambda x, y: Q(**{x + '__second': y}),
        }

        self.workflow.dbms.current_user = self.current_user
        self.workflow.dbms.current_user_id = self.current_user_id
        # self.workflow.dbms.current_user_object = self.current_user_object
        self.workflow.dbms.system_settings = self.system_settings
        self.workflow.usr = self.current_user

    # to get_data if its in object generator
    def normalize_data(self, obj):
        if isinstance(obj, dict):
            return utils.from_dict_to_object(obj)
        return obj
    


    # get users information
    def get_users(self, id=None, jsonfy=True, get_all=False, get_role=False, fetch_by_email=False, fetch_both=False, fetch_password=False,user_id=None, fetch_linked_fields=True, fetch_linked_tables=True, skip_workflow=True, is_admin=False):
        try:
            if not get_all:
                usr = None
                user=None
                raw = utils.from_dict_to_object()
                if not is_admin:
                    user = self.get_doc("Lite_User", id, privilege=True, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, jsonfy=jsonfy, fetch_both=fetch_both, skip_workflows=skip_workflow, ignore_case_sensitivity=True)
                else:
                    user = self.get_doc("Lite_User", id, privilege=True, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, jsonfy=jsonfy,fetch_both=fetch_both, skip_workflows=skip_workflow, fetch_by_field="first_name", ignore_case_sensitivity=True)
                if user and user.status == utils.ok:
                    usr = user.data
                    if fetch_both:
                        usr = user.data.jsonfied
                        # usr.company_info = comp
                        raw = user.data.raw
                        # raw.company_info = comp
                else:
                    return user
                if not fetch_password  and jsonfy:
                    del usr["password"]
                if get_role:
                    role = self.get_doc("Role", usr.main_role, privilege=True, skip_workflows=True, fetch_linked_fields=True, fetch_linked_tables=True, ignore_case_sensitivity=True)
                    if role.status == utils.ok:
                        if jsonfy:
                            usr["user_role"] = role.data
                        else:
                            usr.user_role = role.data
                # if user has switched company
                if self.validation.user_current_company:
                    original_company = usr.default_company
                    usr.default_company = self.validation.user_current_company
                    raw.default_company = self.validation.user_current_company
                    if original_company != self.validation.user_current_company:
                        usr.permitted_companies.append({"company": original_company})
                if fetch_both:
                    return utils.respond(utils.ok,{"jsonfied": usr, "raw": raw})
                if not usr:
                    return utils.respond(utils.internal_server_error, f"Failed to fetch user:{usr}")
                return utils.respond(utils.ok, usr)
            else:
                users = Lite_User.objects.all()
                if users and len(users) > 0:
                    user_list = []
                    for usr in users:
                        us = {
                            "id": usr.id,
                            "last_login": usr.last_login,
                            "is_superuser": usr.is_superuser,
                            "name": usr.name,
                            "email": usr.email,
                            "first_name": usr.first_name,
                            "middle_name": usr.middle_name,
                            "last_name": usr.last_name,
                            "contact_no": usr.contact_no,
                            "gender": usr.gender,
                            "is_active": usr.is_active,
                            "is_staff": usr.is_staff,
                            "created_on": usr.created_on,
                            "creation_time": usr.creation_time,
                            "last_modified": usr.creation_time,
                            "docstatus": usr.docstatus,
                            "status": "Active",
                            "owner_id": usr.owner_id,
                            "disabled": usr.disabled,
                            "doctype": "Lite_User",
                            "main_role": usr.main_role,
                            "dp": usr.dp,
                        }
                        if usr.status:
                            us["status"] = usr.status.name
                        if get_role:
                            role = self.get_doc("Role", user.main_role, privilege=True, skip_workflows=True, jsonfy=jsonfy, ignore_case_sensitivity=True)
                            if role.status == utils.ok:
                                us["user_role"] = role.data                       
                        user_list.append(us)
                    return utils.respond(utils.ok,{"total_pages":0, "rows": user_list})
                return utils.respond(utils.no_content,[])
        except Exception as e:
            return utils.respond(utils.not_found, f"User with ID {id} not found: {e}")
        
    # get admin user
    def get_administrator(self, jsonfy=False):
       return self.get_users(tenant_admin.get("first_name"), jsonfy=jsonfy, fetch_by_email=True,is_admin=True)

    def create_user_pool(self, data):
        doc = self.get_doc("User_Pool",data.name, privilege=True, ignore_case_sensitivity=True)
        if doc.status == utils.ok:
            return doc
        return self.create("User_Pool", data, privilege=True)
        

    # validate data before processing
    def validate_data(self, model, data, validation_type, ignore_name_validation=False):
        mapped_values = {"docstatus":data.get("docstatus",0), "disabled":data.get("disabled", 0), "idx": data.get("idx", 0)}
        exclusive_fields = ["format", "created_on", "creation_time", "last_modified", "docstatus", "disabled", "status", "owner", "modified_by", "idx","id"]
        data or throw("Validation data not found!")
        fields = model.get("fields")
        normal_fields = fields.get("normal_fields")
        foreign_key_fields = fields.get("foreign_key_fields")
        many_to_many_fields = fields.get("many_to_many_fields")
        # mapping normal fields
        if normal_fields.get("name") and not data.get("name"):
            throw("Name field is mandatory for this record!")
        if data.get("name"):
            mapped_values["name"] = data.get("name").strip()
        if data.get("id"):
            mapped_values["id"] = int(data.get("id"))
        
        if normal_fields:
            for label, value in normal_fields.items():
                if label not in exclusive_fields:
                    val = data.get(label, None)
                    if not val:
                        if value.get("default") or value.get("default") == 0:
                            val = value.get("default")
                        elif value.get("null") == False and label not in exclusive_fields:
                            throw(f"{utils.capitalize(utils.replace_character(label,'_', ' '))} required!")
                    if val:
                        if utils.is_digit(val):
                            mapped_values[label] = val
                        else:
                            mapped_values[label] = val.strip() if utils.is_string(val) else val
                    else:
                        mapped_values[label] = val

        # mapping foreign fields
        if foreign_key_fields:
            for label, config in foreign_key_fields.items():
                if label not in exclusive_fields:
                    val = data.get(label)
                    if val:
                        doc = self.get_django_object(config.get("model_name"), val)
                        if doc.get("status") == utils.ok:
                            mapped_values[label] = doc.get("data")
                        else:
                            throw(f"{utils.capitalize(utils.replace_character(doc.get('error_message'), '_', ' '))}")
                    elif config.get("constraints").get("null") == False and  label not in exclusive_fields:
                        throw(f"{utils.capitalize(utils.replace_character(label,'_', ' '))} required!")
        # mapping table fields
        if many_to_many_fields:
            for label, config in many_to_many_fields.items():
                child_data = data.get(label)
                child_mapped = []
                if child_data and len(child_data) > 0:
                    model_config = utils.get_model_object(config.get("remote_model_name"))
                    if model_config.get("status") == utils.ok:
                        model_data = model_config.get("data")
                        for row in child_data:
                            normalized = self.normalize_data(row)
                            validated = self.validate_data(model_data, normalized, validation_type, True)
                            if validated.get("status") == utils.ok:
                                v_data = validated.get("data")
                                v_data["doctype"] = model_data.get("model_name")
                                v_data["parent_type"] = model.get("model_name")
                                if validation_type == utils.VALIDATION_TYPE_UPDATE:
                                    v_data["parent"] = data.get("name")
                                child_mapped.append(v_data)
                mapped_values[label] = child_mapped
        return utils.respond(utils.ok, mapped_values)


    def map_foreign_key_fields(self, model, data, exclusive_fields):
        mapped_values = {}
        foreign_key_fields = model.get("fields", {}).get("foreign_key_fields", {})
        for label, config in foreign_key_fields.items():
            if label not in exclusive_fields:
                val = data.get(label)
                if val:
                    doc = self.get_django_object(config.get("model_name"), val)
                    if doc.get("status") == utils.ok:
                        mapped_values[label] = doc.get("data")
                    else:
                        throw(f"{utils.capitalize(utils.replace_character(doc.get('error_message'), '_', ' '))}")
                elif not config.get("constraints", {}).get("null", False):
                    throw(f"{utils.capitalize(utils.replace_character(label, '_', ' '))} required!")
        return mapped_values
    



    def map_table_fields(self, model, data, exclusive_fields,validation_type):
        mapped_values = {}
        many_to_many_fields = model.get("fields", {}).get("many_to_many_fields", {})
        for label, config in many_to_many_fields.items():
            child_data = data.get(label)
            child_mapped = []
            if child_data and len(child_data) > 0:
                model_config = utils.get_model_object(config.get("remote_model_name"))
                if model_config.get("status") == utils.ok:
                    model_data = model_config.get("data")
                    for row in child_data:
                        normalized = self.normalize_data(row)
                        validated = self.validate_data(model_data, normalized, validation_type, True)
                        if validated.get("status") == utils.ok:
                            v_data = validated.get("data")
                            v_data["doctype"] = model_data.get("model_name")
                            v_data["parent_type"] = model.get("model_name")
                            if validation_type == utils.VALIDATION_TYPE_UPDATE:
                                v_data["parent"] = data.get("name")
                            child_mapped.append(v_data)
            mapped_values[label] = child_mapped
        return mapped_values


    
    # generate filters for fetching
    def generate_query_filters(self, model,filters):
        # if self.validation.user_current_company_id and "company_id" in normal_fields
        fields = model.fields
        normal_fields = fields.normal_fields
        foreign_key_fields = fields.foreign_key_fields
        new_filters = {}
        if filters:
            for label, value in filters.items():
                field_name = label.split('__')[0]
                if field_name in normal_fields.keys():
                    new_filters[label] = value
                elif field_name in foreign_key_fields.keys():
                    field_config = foreign_key_fields.get(field_name)
                    if isinstance(value, list):
                        new_vals = []
                        for v in value:
                            doc = self.get_django_object(field_config.model_name, v)
                            if doc.status == utils.ok:
                                new_vals.append(doc.data.id)
                        new_filters[label] = new_vals 
                    else:
                        doc = self.get_django_object(field_config.model_name, value)
                        if doc.status == utils.ok:
                           new_filters[label] = doc.data
            return utils.respond(utils.ok, new_filters)
        return utils.respond(utils.no_content,"")
    


    def generate_complex_filters(self, filters):
        parts = re.findall(r'(".*?"|\S+)(\s*([<>!=]+)\s*(".*?"|\S+))?', filters)
        q_filters = []
        current_q = None
        for part in parts:
            if len(part) == 1:
                field = part[0]
                q = Q(**{field: True})
            else:
                field, _, op, value = part
                q = self.complex_operator_map[op](field, value.strip('"'))
            if current_q is None:
                current_q = q
            elif part[1] == '&':
                current_q &= q
            elif part[1] == '|':
                current_q |= q
        q_filters.append(current_q)
        return reduce(operator.and_, q_filters)
    

    # extract
    def extract_lite_data(self, result, model_data, fetch_linked_fields=False):
        if not result:
            return utils.respond(utils.no_content, "")
        annotations = {fk + '__name': F(fk + '__name') for fk in utils.get_object_keys(model_data.fields.foreign_key_fields)}
        values_fields = utils.get_object_keys(model_data.fields.normal_fields) + [f"{fk}__name" for fk in utils.get_object_keys(model_data.fields.foreign_key_fields)]

        if model_data.fields.foreign_key_fields.get("owner"):
            annotations["owner_first_name"] = F("owner__first_name")
            annotations["owner_middle_name"] = F("owner__middle_name")
            annotations["owner_last_name"] = F("owner__last_name")
            values_fields.extend(["owner_first_name","owner_middle_name","owner_last_name"])
        
        if model_data.fields.foreign_key_fields.get("status"):
            annotations["status_color"] =  F("status__status_color")
            annotations["status_inner_color"] =  F("status__inner_color")
            values_fields.extend(["status_color","status_inner_color"])
        if model_data.name in ["Lite_User", "Tenant"] and result and len(result) > 1:
            try:
                if "password" in values_fields:
                    values_fields.remove("password")
                elif "db_password" in values_fields:
                    values_fields.remove("db_password")
                    values_fields.remove("api_key")
                    values_fields.remove("db_name")
                    values_fields.remove("db_user")
                    values_fields.remove("db_host")
                    values_fields.remove("db_port")
                    values_fields.remove("tenant_url")
                    values_fields.remove("total_users")
                    values_fields.remove("total_storage")
                    values_fields.remove("license_no")
                    values_fields.remove("subscription_frequency")
                    values_fields.remove("customer")
                    values_fields.remove("expiry_date")
            except Exception as e:
                pass


        data = result.annotate(**annotations).values(*values_fields)
        json_data = list(data)
        if json_data:
            df = utils.to_data_frame(json_data)
            df.columns = df.columns.str.replace('__name', '')
            data = df.to_dict('records')
            return utils.respond(utils.ok, data)
        return utils.respond(utils.no_content,"")


    
    # extract data from django objects to json
    def extract_data(self, result, model_data, fetch_linked_fields=False, fetch_linked_tables=False, use_main_tenant=False):
        data = []
        model = model_data.model_object
        fk_fields = []
        many_to_many_fields = []
        fk_fields = [field.name for field in model._meta.get_fields() if isinstance(field, ForeignKey)]
        many_to_many_fields = [field.name for field in model._meta.get_fields() if field.many_to_many]
        for instance in result:
            row = dict(filter(lambda item: item[0] not in many_to_many_fields, model_to_dict(instance).items()))
            row["created_on"] = getattr(instance, "created_on", None)
            row["creation_time"] = getattr(instance, "creation_time", None)
            row["last_modified"] = getattr(instance, "last_modified", None)
            row["linked_fields"] = {}
            fk_instance = None
            
            for fk_field in fk_fields:
                try:
                    fk_instance = getattr(instance, fk_field)
                    if fk_instance:
                        if fk_instance and row.get(fk_field):
                            row[fk_field] = getattr(fk_instance, "name", None)
                            if fetch_linked_fields:
                                # row["linked_fields"][fk_field] = dict(filter(lambda item: not isinstance(item[1], list), model_to_dict(fk_instance).items()))
                                fk_dict = model_to_dict(fk_instance)
                                values = dict(filter(lambda item: not isinstance(item[1], list), model_to_dict(fk_instance).items()))
                                # Replace FK numeric IDs with their "name" field values
                                for field in fk_instance._meta.get_fields():
                                    if isinstance(field, ForeignKey):
                                        field_name = field.name
                                        related_instance = getattr(fk_instance, field_name, None)
                                        if related_instance:  # If the related instance exists
                                            values[field_name] = getattr(related_instance, "name", fk_dict[field_name])
                                # Assign the updated dictionary
                                row["linked_fields"][fk_field] = values

                                if fk_field in ["owner", "modified_by"]:
                                    try:
                                        del row["linked_fields"][fk_field]["password"]
                                    except:
                                        pass
                    else:
                        pass
                except Exception as e:
                    if not isinstance(row[fk_field], str) and not isinstance(row[fk_field], int) and not isinstance(row[fk_field], float):
                        row[fk_field] = None
                    # if the field being fetch
                    if fk_field == "tenant" and model_data.name == "User_Pool" and instance.tenant_id:
                        tenant = self.get_doc("Tenant", instance.tenant_id, fetch_by_field="id")
                        if tenant.status == utils.ok:
                            row[fk_field] = tenant.data.name
                        pass
                    else:
                        pass
                        # print("Failed to extract FK value while extracting data", str(e))
            if  getattr(instance, "status", None) and model.__name__ != "Tenant":
                row["status_info"] = model_to_dict(instance.status)
                # pp(row["status_info"])
            if fetch_linked_tables:
                for m2m_field in many_to_many_fields:
                    m2m_object = getattr(instance, m2m_field, None)
                    child_model_data = []
                    if m2m_object:
                        for obj in m2m_object.all().using(self.tenant_db if not use_main_tenant else self.main_tenant_db):
                            child_obj = model_to_dict(obj)
                            try:
                                child_obj["created_on"] = getattr(obj,"created_on", "")
                                child_obj["creation_time"] = getattr(obj,"creation_time", "")
                            except Exception as e:
                                pass
                            for label, value in child_obj.items():
                                if isinstance(value, list):
                                    try:
                                        child_obj[label] = [model_to_dict(ob) for ob in value]
                                    except Exception as e:
                                        pass
                            child_obj["linked_fields"] = {}
                            related_model_name = ""
                            
                            try:
                                related_model_name = obj._meta.model.__name__
                            except Exception as e:
                                throw(f"FAILED TO EXTRACT FOREIGN KEY VALUE: {str(e)}")
                            model_config = utils.get_model_object(related_model_name)
                            if model_config.status == utils.ok:
                                fks = model_config.data.fields.foreign_key_fields
                                if fks:
                                    for fk in fks.keys():
                                        fk_object = None
                                        try:
                                            fk_object = getattr(obj, fk, None)
                                        except Exception as e:
                                            manual_fetch = self.get_django_object(fks.get(fk).get("model_name"),child_obj.get(fk),use_main_tenant=use_main_tenant)
                                            if manual_fetch.status != utils.ok:
                                                pp(f"Mini child processing failure: {str(e)}", obj._state.db)
                                            else:
                                                fk_object = manual_fetch.data
                                        if fk_object:
                                            try:
                                                child_obj[fk] = getattr(fk_object, "name", None)
                                                if fetch_linked_fields:
                                                    linked = dict(filter(lambda item: not isinstance(item[1], list), model_to_dict(fk_object).items()))
                                                    child_obj["linked_fields"][fk] = linked
                                                    if fk in ["owner", "modified_by"]:
                                                        try:
                                                            del child_obj["linked_fields"][fk]["password"]
                                                        except:
                                                            pass
                                            except Exception as e:
                                                pp(f"Failed to to assign foreign key value to table field: {str(e)}")
                            child_model_data.append(child_obj)
                            if child_model_data:
                                if "id" in child_model_data[0]:
                                    child_model_data = utils.sort(child_model_data,sort_by="id")
                        row[m2m_field] = child_model_data
            data.append(row)
        return utils.respond(utils.ok, data)


    # increment naming series
    def increase_series(self, model):
        series = self.get_django_object("Series", model)
        if series.status != utils.ok:
            return utils.respond(utils.not_found,f"Series not found for doc {model}")
        series_data = series.data
        naming_series = series_data.name_format
        if naming_series:
            placeholders = utils.extract_placeholders(naming_series)
            if "series_count" in placeholders:
                series_data.series_count = series_data.series_count + 1
                series_data.save(using=self.tenant_db)
        series = self.get_doc("Series", model, skip_user_evaluation=True, privilege=True, skip_cache=True)
        if series.status != utils.ok:
            return series
        series_data = series.data
        count = series_data.series_count
        series_digits = series_data.series_digits or 4
        count_string = f"{count}"
        new_count = ""
        if count_string and len(count_string) < series_digits:
            renaming = series_digits - len(f"{count_string}")
            for i in range(renaming):
                new_count += "0"
            new_count += count_string
        else:
            new_count = count_string
        series_data["series_count"] = new_count
        return utils.respond(utils.ok,series_data)

    def check_if_doc_exists(self,model,name):
        doc =  self.get_doc(model, name, privilege=True, skip_workflows=True)
        if doc.status == utils.ok:
            return True
        return False
    def validate_exempt_models(self, model):
        if model in self.exempt_models:
            return utils.respond(utils.ok, ["name"])
        return utils.respond(utils.unauthorized,False)
        

    def create_audit_trail(self, doc_name ,model, action,items=[]):
        if model != "Audit_Trail":
            if action == "Created":
                return self.create("Audit_Trail",utils.from_dict_to_object({
                    "name":doc_name, 
                    "doc_name":doc_name, 
                    "document_type": utils.replace_character(model, "_", " "),
                    "audit_items":[{
                        "date_created": dates.today(), 
                        "time_created":dates.time(),
                        "action": action, 
                        "field": "",
                        "before_content": "",
                        "after_content": "",
                    }]
                }), create_trail=False)
            else:
                trail = self.get_doc("Audit_Trail", doc_name, privilege=True, fetch_linked_tables=True,get_trail=False)
                if trail.status == utils.ok:
                    updated = trail.data
                    updated.doc_name = doc_name
                    updated.audit_items.extend(items)
                    updated =  self.update("Audit_Trail", updated, update_submitted=True, skip_hooks=True)
                else:
                    return self.create("Audit_Trail",utils.from_dict_to_object({
                    "name":doc_name, 
                    "doc_name":doc_name, 
                    "document_type": utils.replace_character(model, "_", " "),
                    "audit_items":items
                }), create_trail=False)

    # create new record
    def create(
            self, 
            model, 
            body, 
            user_id=None, 
            privilege=False, 
            skip_user_evaluation=False, 
            skip_workflows=False, 
            create_trail=True, 
            fetch_linked_fields=True, 
            fetch_linked_tables=True, 
            submit_after_create=False, 
            fetch_if_exists=False,
            owner_id=None
        ):
        with transaction.atomic():
            try:
                model_config = utils.get_model_object(model)
                model_config.status == utils.ok or throw(f'Failed to fetch model configurations: {model_config.error_message}')
                model_data = model_config.data
                model_fields = model_data.fields
                table_data = {}
                # get the model object
                model_object = model_data.model_object()
                model_object._state.db = self.tenant_db
                ex_data = self.normalize_data(body)
                docstatus = ex_data.docstatus or 0
                user_data = None
                if owner_id:
                    user_data = owner_id
                else:
                    if not skip_user_evaluation and not self.use_super_admin and not self.skip_user_validation:
                        if not privilege:
                            if self.current_user_id:
                                user_data = self.current_user_id
                            else:
                                return utils.respond(utils.user_not_in_headers, "User ID Missing in headers")
                        else:
                            user_data = self.admin_user.id or None
                object = ex_data
                if hasattr(object, "name") and object.name is not None:
                    object.name = str(object.name).strip()
                else:
                    object.name = None

                if not object.name:
                # if not ex_data.name:
                    utils.create_naming_series(model, self, object)
                # handle hooks

                # CHECK IF DOCUMENT WITH THE SAME NAME EXISTS
                if ex_data.name:
                    if self.check_if_doc_exists(model, ex_data.name):
                        if fetch_if_exists:
                            exisitng =  self.get_doc(model, ex_data.name, privilege=privilege, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
                            if exisitng.status == utils.ok:
                                return exisitng
                        else:
                            return utils.respond(utils.found, f"{utils.replace_character(model, '_',' ')} with name <strong class='text-secondary_color'>{ex_data.name}</strong> already exists!")
                
                # operation_id = f"{model}_{object.name}"
                operation_id = utils.generate_unique_id(utils.get_object_keys(self.operating_docs.creating))
                self.operating_docs.creating[operation_id] = utils.from_dict_to_object({
                    "body": object,
                    "user_id": user_id,
                    "model": model,
                    "method": utils.REQUEST_TYPE_POST,
                    "doc_status": ex_data.get("status", "Active"),
                    # before content
                    "before_model": model,
                    "before_method": self.validation.get("method", utils.REQUEST_TYPE_POST)
                })

                hc = Hooks_Controller(self, self.operating_docs.creating[operation_id])
                hc.hook_type = "before_save"
                hc.init_hooks(utils.REQUEST_TYPE_POST)
                validation = self.operating_docs.creating[operation_id]
                object = validation.body

                if not skip_workflows:
                    workflows = self.workflow.init_workflow(model, validation, model_data)
                    if workflows and workflows.status == utils.ok:
                        object.doc_status = validation.doc_status
                object.status = validation.doc_status
                ex_data = self.normalize_data(object)


                ex_data.status = ex_data.get("status", "Active")
                ex_data.doctype = model
                validated = self.validate_data(model_data, ex_data, utils.VALIDATION_TYPE_CREATE)
                
                validated.status == utils.ok or throw(f"Data Validation Failed:{validated.error_message}")
                data = validated.data
                data_keys = utils.get_object_keys(data)
                normal_fields = utils.get_object_keys(model_data.fields.normal_fields)
                fk_fields = utils.get_object_keys(model_data.fields.foreign_key_fields)
                many_to_may_data_keys = utils.get_object_keys(model_data.fields.many_to_many_fields)
                all_fields = utils.get_object_keys(model_data.fields.normal_fields) + utils.get_object_keys(model_data.fields.foreign_key_fields)
                if data.name:
                    data.name = data.name.strip()

                # if the user is on a prefered company, lets link it
                if self.validation.user_current_company_id and "company_id" in normal_fields:
                    data.company_id = self.validation.user_current_company_id
                    
                
                _status = ex_data.get("status", "Active")
                status_object = None
                if model not in ["Tenant"]:
                    status_data = self.get_django_object("Doc_Status", _status)
                    if status_data.status == utils.ok:
                        status = status_data.data
                        status_object = status_data.data
                        if "status" in normal_fields:
                            data.status = status.name
                        if "status" in fk_fields:
                            data.status = status
                        docstatus = status.initial_docstatus
                    elif model != "Doc_Status":
                        throw(f"Failed to fetch Document Status: {status_data.get('error_message','')}")
                elif model == "Tenant":
                    data.status = "Initialized"

                # time to save the info
                try:
                    many_to_many = [] 
                    if model_fields.get("many_to_many_fields"):
                        many_to_many = list(model_fields.get("many_to_many_fields").keys()) 
                    # save the many object
                    to_save = {}
                    for field_name, value in data.items():
                        if field_name not in many_to_many and field_name in all_fields:
                            to_save[field_name] = value
                    
                    try:
                        if "owner" in data_keys or "owner" in fk_fields:
                            to_save["owner_id"] = user_data
                            data["modified_by_id"] = user_data
                        model_object = model_data.model_object.objects.using(self.tenant_db).create(**to_save)
                        
                    except Exception as e:
                        return utils.respond(utils.unprocessable_entity, f"Failed to save {utils.capitalize(utils.replace_character(model,'_',' '))}: {str(e)}")
                    # process child tables
                    
                    try:
                        many_to_many_fields = model_data.fields.many_to_many_fields
                        if many_to_many_fields:
                            for label, conf in many_to_many_fields.items():
                                table_data[label] = []
                                ct_data = data.get(label)
                                child = None
                                if ct_data:
                                    for row in ct_data:
                                        try:
                                            row.id = None
                                        except:
                                            pass
                                        m2m_fields = [field.name for field in conf.remote_model._meta.get_fields() if field.many_to_many]
                                        for field in m2m_fields:
                                            if field in row:
                                                del row[field]
                                        # if "status" in m2m_fields:
                                        row["status"] = data.status
                                        if model == "Tenant":
                                            row["status"] = status_object
                                    # if "parent" in m2m_fields:
                                        row["parent"] = data.get("name", None)
                                        try:
                                            # Create child instance without many-to-many relationship
                                            child = conf.remote_model(**row)
                                            child.save(using=self.tenant_db)
                                            getattr(model_object, label).set([child])
                                            

                                        except Exception as e:
                                            # print(f"Child table saving failed on create for table:{str(e)}")
                                            model_object.delete()
                                        table_data[label].append(child)
                    except Exception as e:
                        model_object.delete()
                        return utils.respond(utils.internal_server_error, f"Child Table Processing Failed: {str(e)}")
                    # attach child tables

                        
                    if many_to_many:
                        for field in many_to_many:
                            try:
                                mtm = getattr(model_object, field)
                                mtm.set(table_data.get(field))
                            except Exception as e:
                                model_object.delete()
                                print(f"Failed to link child table to document:{str(e)}")
                        model_object.save(using=self.tenant_db)
                        if not model_object.id:
                            for label, values in table_data:
                                for td in values:
                                    td.delete(using=self.tenant_db)
                    doc =  self.get_doc(model, model_object.name, privilege=True, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
                    if doc.status == utils.ok:
                        if create_trail:
                            self.create_audit_trail(doc.data.name,model, "Created",[{
                                "action": "Created", "action_by": user_data, "date_created": dates.today(), "time_created":dates.time()
                            }])

                        # init after save hooks
                        hc.hook_type = "after_save"
                        hc.result = doc.data
                        hc.init_hooks(utils.REQUEST_TYPE_POST)

                        if data.docstatus == 1 or submit_after_create:
                            submitted = self.submit_doc(model,[doc.data.id], ignore_docstatus=True, privilege=privilege)
                            if submitted.status == utils.ok:
                                doc =  self.get_doc(model, model_object.name, privilege=True, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
                    elif fetch_if_exists:
                        exisitng =  self.get_doc(model, model_object.name, privilege=True, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
                        if exisitng.status == utils.ok:
                            doc = exisitng
                    del self.operating_docs.creating[operation_id]
                    return doc
                except Exception as e:
                    transaction.set_rollback(True)
                    return utils.respond(utils.internal_server_error, f'Failed to save {utils.capitalize(utils.replace_character(model,"_"," "))}: {str(e)}')
            except Exception as e:
                transaction.set_rollback(True)
                return utils.respond(utils.internal_server_error, f"{str(e)}")

    # update document
    def update(self, model, body, user_id=None, update_submitted=False, privilege=False, skip_user_evaluation=False, skip_hooks=False, skip_audit_trail=False):
        with transaction.atomic():
            ex_data = self.normalize_data(body)
            try:
                initial_docstatus = body.docstatus
                initial_status = body.status
                model_config = utils.get_model_object(model)
                model_config.status == utils.ok or throw(f'Failed to fetch model configurations: {model_config.error_message}')
                model_data = model_config.data
                model_fields = model_data.fields
                table_data = {}

                # get the model object
                modeled_data = self.get_django_object(model, ex_data.get("id"))
                modeled_data.status == utils.ok or throw(f"Failed to fetch document: {modeled_data.error_message}")
                model_object = modeled_data.data
                
                user_data = None
                if not privilege and not self.use_super_admin:
                    if self.current_user_id:
                        user_data = self.current_user_id
                    else:
                        return utils.respond(utils.user_not_in_headers, "User ID missing in the headers!")
                else:
                    user_data = self.admin_user.id or None

                # get old doc to prepare audit trail
                old_doc = self.get_doc(model, body.get("id"), user=user_id, skip_workflows=True)
                utils.evaluate_response(old_doc, f"An error occurred while fetching upadte document: {old_doc.error_message}")
                old_data = old_doc.data

                object = ex_data
                object.doc_status = getattr(object,"status", "Active")


                operation_id = f"{model}_{object.name}"
                operation_id = utils.generate_unique_id(utils.get_object_keys(self.operating_docs.updating))
                self.operating_docs.updating[operation_id] = utils.from_dict_to_object({
                    "body": object,
                    "model": model,
                    "method": utils.REQUEST_TYPE_PATCH,
                    "doc_status": ex_data.get("status", "Active"),
                    # before content
                    "before_model": model,
                    "before_method": self.validation.get("method", utils.REQUEST_TYPE_PATCH)
                })
                
                # handle hooks
                if skip_hooks == False:
                    hc = Hooks_Controller(self, self.operating_docs.updating[operation_id])
                    hc.hook_type = "before_update"
                    hc.init_hooks(utils.REQUEST_TYPE_PATCH)

                validation = utils.from_dict_to_object(self.operating_docs.updating[operation_id])
                object = validation.body
                object.status = validation.doc_status
                ex_data = self.normalize_data(object)
                ex_data["status"] = ex_data.get("status", "Active")
                ex_data["doctype"] = model
                validated = self.validate_data(model_data, ex_data, utils.VALIDATION_TYPE_UPDATE)
                validated.status == utils.ok or throw(f"Data Validation Failed: {validated.error_message}")
                data = validated.data

                # handle status from workflow if any
                if self.validation.workflow_doc_status:
                    if ex_data.status.lower() in ["draft", "active"]:
                        ex_data.status = self.validation.workflow_doc_status

                # if the doc was cancelling
                if initial_docstatus == 2:
                    ex_data.status = initial_status
                    ex_data.docstatus = initial_docstatus
                _status = ex_data.get("status", "Active")
                status_data = self.get_django_object("Doc_Status", _status)
                status_data.status == utils.ok or throw(f"Failed to fetch Document Status: {status_data.error_message}")
                status_obj = status_data.data
                if model not in ["Doc_Status", "Series", "Tenant"]:
                    status = status_obj
                    data["status"] = status
                elif model == "Tenant":
                    data["status"] = _status
                # time to save the info
                try:
                    many_to_many = [] 
                    model_object._state.db = self.tenant_db
                    if model_fields.get("many_to_many_fields"):
                        many_to_many = list(model_fields.get("many_to_many_fields").keys()) 
                    for field_name, value in data.items():
                        if field_name not in many_to_many:
                            setattr(model_object, field_name, value)
                    setattr(model_object, 'modified_by_id', user_data)
                    model_object.save(using=self.tenant_db)

                    # process child tables
                    try:
                        many_to_many_fields = model_data.fields.many_to_many_fields
                        if many_to_many_fields:
                            for label, conf in many_to_many_fields.items():
                                table_data[label] = []
                                ct_data = data.get(label)
                                ct_old_data = self.get_child_table_data(conf, old_data.name, jsonfy=False)
                                existing = {}
                                new_ids = []
                                if ct_old_data and ct_old_data.status == utils.ok:
                                    remote_model = conf.remote_model
                                    for ct_row in ct_old_data.data:
                                        ct_doc = remote_model.objects.using(self.tenant_db).get(pk=int(ct_row.id))
                                        existing[ct_doc.id] = ct_doc
                                for row in ct_data:
                                    id = row.get("id")
                                    ct_model = existing.get(id) if id else conf.remote_model()
                                    if ct_model:
                                        if ct_model.id:
                                            new_ids.append(ct_model.id)
                                        for rw_label, rw_val in row.items():
                                            if rw_label != "id" and rw_val != None:
                                                try:
                                                    setattr(ct_model, rw_label, rw_val)
                                                except:
                                                    pass
                                        try:
                                            setattr(ct_model, "status", data.get("status",None))
                                        except:
                                            pass
                                        setattr(ct_model, "docstatus", data.get("docstatus", 0))
                                        setattr(ct_model, "parent", data.get("name", None))
                                        if not row.get("id"):
                                            setattr(ct_model, 'modified_by_id', user_data)
                                        try:
                                            if ct_model and table_data:
                                                if ct_model.id:
                                                    ct_model.save(using=self.tenant_db)
                                                    new_ids.append(ct_model.id)
                                                else:
                                                    # if the child table doesnt have an id
                                                    recostruct = {rl: getattr(ct_model, rl, None) for rl in vars(ct_model) if rl != "_state"}
                                                    ct_model = conf.remote_model.objects.using(self.tenant_db).create(**recostruct)
                                                    new_ids.append(ct_model.id)
                                                table_data[label].append(ct_model)
                                        except Exception as e:
                                            pass
                                # clean the table by removing what doesnt exist
                                if new_ids:
                                    exkeys = utils.get_object_keys(existing) or []
                                    if new_ids:
                                        to_be_deleted = list(set(exkeys) - set(new_ids))
                                        if to_be_deleted:
                                            try:
                                                conf.remote_model.objects.using(self.tenant_db).filter(id__in=to_be_deleted).delete()
                                            except Exception as e:
                                                pp(f"An error occurred while deleting child table component:{str(e)}")
                    except Exception as e:
                        return utils.respond(utils.internal_server_error, f"Child Table Processing Failed: {e}")
                    # attach child tables
                    try:
                        if many_to_many:
                            for field in many_to_many:
                                mtm = getattr(model_object, field)
                                mtm.set(table_data.get(field))
                        model_object.save(using=self.tenant_db)
                        
                    except Exception as e:
                        pp(str(e))
                        
                    doc =  self.get_doc(model, model_object.name, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
                    
                    # update audit trail
                    if old_doc.status == utils.ok and  model != "Audit_Trail" and skip_audit_trail == False:
                        old_data = old_doc.data
                        # update index for the data
                        
                        trail_items = []
                        for label, value in old_data.items():
                            if not isinstance(old_data.get(label),list):
                                if old_data.get(label) != doc.data.get(label):
                                    trail_items.append(utils.from_object_to_dict({
                                        "action": "Updated",
                                        "field": utils.capitalize(utils.replace_character(label, "_"," ")),
                                        "before_content": old_data.get(label),
                                        "after_content": doc.data.get(label),
                                        "date_created": dates.today(), 
                                        "time_created":dates.time()
                                    }))
                        if len(trail_items) > 0:
                            update_trail = self.create_audit_trail(doc.data.name,model,"Updated",trail_items)

                    # after update event
                    if skip_hooks == False:
                        hc.hook_type = "after_update"
                        hc.result = doc.data
                        hc.init_hooks(utils.REQUEST_TYPE_PATCH)
                    del self.operating_docs.updating[operation_id]

                    # update the cache for the updated record
                    if model in self.cacheable_content:
                        self.caching.update_tenant_cache(self.tenant_db,model,old_data.name,doc.name,doc)
                    return doc
                except Exception as e:
                    return utils.respond(utils.internal_server_error, f'Failed to update {utils.capitalize(utils.replace_character(model,"_"," "))}: {str(e)}')
            except Exception as e:
                transaction.set_rollback(True)
                return utils.respond(utils.internal_server_error, f"{str(e)}")

        











    def get_list(  
        self,
        model,
        page_size=None,
        current_page=None,
        fields=[],
        filters={},
        order_by=None,
        limit=None,
        fetch_linked_fields=False,
        fetch_linked_tables=False,
        user=None,
        skip_user_evaluation=False,
        privilege=False,
        only_count=False,
        complex_filters=Q(),
        fetch_lite=False,
        as_dict=False,
        lower_dict_keys=False,
        as_dict_key = "name",
        return_summary_in_dict=False,
        skip_company_validation = False,
        use_main_tenant=False,
        skip_hooks=False
    ):
        final_filters = utils.from_dict_to_object()
        flt = utils.string_to_json(filters) if filters else utils.from_dict_to_object()
        if flt.status == utils.ok:
            final_filters = flt.data
        if model == "Model":
            objects = utils.get_model_object(get_all=True, get_objects=False)
            if objects.get("status") == utils.ok:
                return utils.respond(utils.ok, {"rows":objects.get("data")})
            return objects
        
        # evaluate user permission
        if not skip_user_evaluation and not privilege:
            evaluate = self.user_controller.evaluate_user_permission_on_doctype(model)
            if evaluate.status != utils.ok:
                pass
                # return evaluate
        
        model_config = utils.get_model_object(model)
        model_config.status == utils.ok or throw(f'Failed to fetch model configurations: {model_config.error_message}')
        model_data = model_config.data
        model_object = model_data.model_object
        if not privilege and  not self.use_super_admin:
            if self.current_user_id:
                user_data = self.current_user_id
            else:
                exempt = self.validate_exempt_models(model)
                if exempt.status == utils.ok:
                    user_data = self.admin_user
                    fields = exempt.data
                else:
                    return utils.respond(utils.user_not_in_headers, "User ID Missing in headers")
        else:
            user_data = self.admin_user
        try:
            # before fetching lets execute the before hooks
            operation_id = utils.generate_unique_id(utils.get_object_keys(self.operating_docs.retrieving))
            self.operating_docs.retrieving[operation_id] = utils.from_dict_to_object({
                "body": {},
                "user_id": self.current_user_id,
                "model": model,
                "method": utils.REQUEST_TYPE_GET,
                "before_model": model,
                "is_list_fetch":True,
                "filters": final_filters
            })
            if not skip_hooks:
                hc = Hooks_Controller(self, self.operating_docs.retrieving[operation_id])
                hc.hook_type = "before_fetch"
                hc.is_single_doc = False
                hc.has_fetched = False
                hc.init_hooks(utils.REQUEST_TYPE_GET)
            validation = self.operating_docs.retrieving[operation_id]
            if validation.filters:
                final_filters = validation.filters


            query_filters = Q()
            qf = self.generate_query_filters(model_data, final_filters)
            if qf.status == utils.ok:
                query_filters =  Q(**qf.data)
            if not complex_filters:
                complex_filters = Q()
            # add company id field if it exists

            try:
                company_ids = [self.validation.user_current_company_id]
                if self.system_settings.linked_fields.default_company and self.system_settings.linked_fields.default_company.child_companies:
                    company_ids.extend(utils.get_list_of_dicts_column_field(self.system_settings.linked_fields.default_company.child_companies, "id"))

                # if ("company_id" in utils.get_object_keys(model_data.fields.get("normal_fields")) or "company" in utils.get_object_keys(model_data.fields.get("foreign_key_fields"))) and self.validation.user_current_company_id and not skip_company_validation:
                if  "company" in utils.get_object_keys(model_data.fields.get("foreign_key_fields")) and self.validation.user_current_company_id and not skip_company_validation  and model not in self.shared_models:
                    query_filters &= Q(company_id__in=company_ids) | Q(company_id__isnull=True)
            except Exception as e:
                pass

            result = model_object.objects.using(self.tenant_db if not use_main_tenant else self.main_tenant_db).filter(complex_filters, query_filters).select_related()
            total_records = model_object.objects.using(self.tenant_db if not use_main_tenant else self.main_tenant_db).count()
            if only_count:
                return utils.respond(utils.ok, total_records)

            # order data
            order = ['-id']
            if order_by and isinstance(order_by,list) and len(order_by) > 0:
                # jsonfy = utils.string_to_json(order_by)
                # pp(jsonfy)
                # if jsonfy.get("status") == utils.ok:
                    order = tuple(order_by)
            ordered = result.order_by(*order)

            # paginate the results
            paginator = Paginator(ordered, page_size or 100**10)
            page = paginator.get_page(current_page)
            recs = page.object_list
            records = recs
            total_pages = paginator.num_pages
            x_data = None
            if fetch_lite or  (not fetch_linked_fields and not fetch_linked_tables):
                x_data = self.extract_lite_data(records, model_data, fetch_linked_fields=fetch_linked_fields)
            else:
                x_data = self.extract_data(records, model_data, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, use_main_tenant=use_main_tenant)
            
            if x_data.get("status") != utils.ok:
                return x_data
            
            data = x_data.get("data")
            if recs and len(recs) > 0 and limit and limit > 0:
                data = data[:limit]
            if len(data) == 0:
                return utils.respond(utils.no_content, data)
            

            # after fetching the document
            operation_id = utils.generate_unique_id(utils.get_object_keys(self.operating_docs.retrieving))
            self.operating_docs.retrieving[operation_id] = utils.from_dict_to_object({
                "body": data,
                "user_id": self.current_user_id,
                "model": model,
                "method": utils.REQUEST_TYPE_GET,
                "before": data,
                "before_model": model,
                "is_list_fetch":True,
                "filters": final_filters
            })
            if not skip_hooks:
                hc = Hooks_Controller(self, self.operating_docs.retrieving[operation_id])
                hc.hook_type = "after_fetch"
                hc.is_single_doc = True
                hc.has_fetched = True
                hc.init_hooks(utils.REQUEST_TYPE_GET)
            validation = self.operating_docs.retrieving[operation_id]
            data = validation.body or data

            if fields and len(fields) > 0:
                try:
                    data =  utils.get_fields(data,fields)
                except Exception as e:
                    pass

            if as_dict:
                if return_summary_in_dict:
                    return utils.respond(utils.ok, {
                        "total_pages": total_pages,
                        "total_records": total_records,
                        "queried_total": len(data),
                        "rows": utils.array_to_dict(data,as_dict_key,lower_dict_keys)
                    })
                return utils.respond(utils.ok, utils.array_to_dict(data,as_dict_key,lower_dict_keys))
           
            return utils.respond(utils.ok, {
                "total_pages": total_pages,
                "total_records": total_records,
                "queried_total": len(data),
                "rows": data,
            })
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{str(e)}")
        
    
    def sql(self, query, params=None, fetch='all'):
        try:
            with connections[self.tenant_db].cursor() as cursor:
                cursor.execute(query, params or [])

                if query.strip().lower().startswith("select"):
                    columns = [col[0].lower() for col in cursor.description]

                    if fetch == 'one':
                        row = cursor.fetchone()
                        if row:
                            return utils.respond(utils.ok, dict(zip(columns, row)))
                        return utils.respond(utils.no_content, "")
                    elif fetch == 'all':
                        rows = cursor.fetchall()
                        return utils.respond(utils.ok, [dict(zip(columns, row)) for row in rows])
                    else:
                        return utils.respond(utils.no_content, "")

                # For INSERT/UPDATE/DELETE
                if query.strip().lower().startswith(("insert", "update", "delete")):
                    return {'success': True, 'rows_affected': cursor.rowcount}
        except DatabaseError as e:
            pp(str(e))
            return utils.respond(utils.internal_server_error, str(e))
        
    def get_django_object(self, model, name, use_main_tenant=False, using_db=None):
        model_config = utils.get_model_object(model)
        model_config.get("status") == utils.ok or throw(f'Failed to fetch model configurations: {model_config.get("error_message")}')
        model_data = model_config.get("data")
        model_object = model_data.get("model_object")
        db_to_use = self.tenant_db if not use_main_tenant else self.main_tenant_db
        if using_db and not use_main_tenant:
            db_to_use = using_db
        try:
            result = None
            result = model_object.objects.using(db_to_use).get(name=name)
            return utils.respond(utils.ok, result)
        except model_object.DoesNotExist as e:
            try:
                if f"{name}".isdigit():
                    result = model_object.objects.using(db_to_use).get(pk=name)
                    return utils.respond(utils.ok, result)
            except model_object.DoesNotExist as e:
                pass
            return utils.respond(utils.not_found, f"{utils.replace_character(model,'_', ' ')} record with name/id '{name}' not found in the system. Please ensure the record is created before its linked to other records!")
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{str(e)}")


    # get document
    def get_doc(
            self, 
            model, 
            name, 
            jsonfy=True, 
            fetch_linked_fields=True, 
            fetch_linked_tables=True, 
            user=None, 
            privilege=False, 
            skip_user_evaluation=False, 
            get_print_format=False, 
            skip_workflows=False, 
            fetch_both=False, 
            get_trail=False,
            fetch_by_field=None, 
            use_main_tenant=False,
            extra_filters={},
            skip_cache=False,
            ignore_case_sensitivity=True
    ):
        try:
            if model == "Model":
                return utils.get_model_object(model=name, get_all=True, get_objects=False)
            model_config = utils.get_model_object(model)
            model_config.status == utils.ok or throw(f'Failed to fetch model configurations: {model_config.error_message}')
            model_data = model_config.data
            model_object = model_data.model_object
            fk_fields = utils.get_object_keys(model_data.fields.foreign_key_fields)

            # user_data = None

            if not privilege and not self.use_super_admin:
                if self.current_user_id:
                    user_data = self.current_user_id
                else:
                    return utils.respond(utils.user_not_in_headers, "User ID Missing in headers")
            else:
                user_data = self.admin_user

            # check if the document exists in cache
            if not skip_cache and not fetch_both:
                cached_value = self.caching.get_tenant_cached_value(self.tenant_db,model,name)
                if cached_value:
                    return utils.respond(utils.ok, cached_value)

            try:
                result = None
                if not fetch_by_field:
                    filter= {"id":name} if f"{name}".isdigit() else {"name__iexact":name}
                else:
                    filter= {f"{fetch_by_field}{'__iexact' if fetch_by_field != 'id' else ''}": name}
                if isinstance(extra_filters, dict):
                    filter.update(**extra_filters)
                result = model_object.objects.using(self.tenant_db if not use_main_tenant else self.main_tenant_db).filter(**filter).select_related(*fk_fields)
                if not result:
                    result = model_object.objects.using(self.tenant_db if not use_main_tenant else self.main_tenant_db).filter(**{"name":name}).select_related(*fk_fields)
                    if not result:
                        return utils.respond(utils.not_found, f"{utils.replace_character(model,'_',' ')} record with name/id '{name}' not found in the system. Please ensure the name/id of the targeted record exists.")
                if not jsonfy and result:
                    return utils.respond(utils.ok, result[0])
                x_data = self.extract_data(result, model_data, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, use_main_tenant=use_main_tenant)
                x_data.status == utils.ok or throw(f"Failed to extract document details: {x_data.error_message}")
                if not x_data.data:
                    return utils.respond(utils.no_content, x_data.data)
                
                if result:
                    data = x_data.data[0]
                    if get_print_format:
                        data.default_print_format = None
                        default_pf = self.get_list("Print_Format", filters={"app_model": model, "is_default": 1}, skip_user_evaluation=True, use_main_tenant=use_main_tenant)
                        if default_pf.status == utils.ok:
                            data.default_print_format = default_pf.data.rows[0].name
                    # fetch workflow configurations
                    if not skip_workflows:
                        workflows = self.workflow.fetch_doc_workflow(model, data.name, data.owner)
                        if workflows and workflows.status == utils.ok:
                            workflow = workflows.data
                            data.workflow = workflow
                    if get_trail:
                        data.audit_trail = {}
                        trail = self.get_doc("Audit_Trail", data.name, fetch_by_field="doc_name", privilege=True,get_trail=False, extra_filters={"document_type":utils.replace_character(model,"_"," ")}, use_main_tenant=use_main_tenant)
                        if trail.status == utils.ok:
                            data.audit_trail = trail.data
                            
                    # after fetching the document
                    operation_id = utils.generate_unique_id(utils.get_object_keys(self.operating_docs.retrieving))
                    self.operating_docs.retrieving[operation_id] = utils.from_dict_to_object({
                        "body": data,
                        "user_id": self.current_user_id,
                        "model": model,
                        "method": utils.REQUEST_TYPE_GET,
                        "before": data,
                        "before_model": model,
                    })

                    hc = Hooks_Controller(self, self.operating_docs.retrieving[operation_id])
                    hc.hook_type = "after_fetch"
                    hc.is_single_doc = True
                    hc.has_fetched = True
                    hc.init_hooks(utils.REQUEST_TYPE_GET)
                    validation = self.operating_docs.retrieving[operation_id]
                    object = validation.body

                    # lets cache the value if the value hasn't already been cached
                    if not skip_cache and model in self.cacheable_content:
                        self.caching.set_tenant_cache( self.tenant_db, model, name, object)


                    if fetch_both:
                        return utils.respond(utils.ok, {"jsonfied":object, "raw":result[0]})
                    return utils.respond(utils.ok, object)
                return utils.respond(utils.ok, result)
            except Exception as e:
                return utils.respond(utils.internal_server_error, f"{str(e)}")
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{str(e)}")



   

    

    # TO SUBMIT A SUBMITTABLE DOCUMENT
    def submit_doc(self, model, docs, user_id=None, skip_user_evaluation=False, privilege=False, ignore_docstatus=False):
        
        with transaction.atomic():   
            
            try:
                user_data = None
                if not privilege and not self.use_super_admin:
                    if self.current_user_id:
                        user_data = self.current_user_id
                    else:
                        return utils.respond(utils.user_not_in_headers, "User ID missing in the headers!")
                else:
                    user_data = self.admin_user
                
                model_config = utils.get_model_object(model)
                model_config.status == utils.ok or throw(f'Failed to fetch model configurations: {model_config.error_message}')
                doc_ids = self.form_request_docs_to_array(docs)
                names = []
                
                if doc_ids:
                    for doc_id in doc_ids:
                        doc = self.get_doc(model, doc_id, fetch_linked_fields=True, fetch_linked_tables=True, privilege=True)
                        doc.status == utils.ok or throw(f"Failed to fetch document: {doc.error_message}")
                        doc_data = doc.data
                        if doc_data.disabled == 1:
                            throw(f"You can not submit a disabled document: {doc_data.name}  is disabled!")
                        if doc_data.docstatus == 1 and not ignore_docstatus:
                            throw(f"You can not submit an already submitted document: {doc_data.name}!")
                        if doc_data.docstatus == 2:
                            throw(f"You can not submit a cancelled document: {doc_data.name}!")
                        if doc_data.docstatus == 3:
                            throw(f"You can not submit a rejected document: {doc_data.name}!")

                        self.validation.doc_status = "Submitted"
                        
                        # UPDATE THE MODEL AND REQUEST TYPE IN THE OBJECT
                        # operation_id = f"{model}_{doc_data.name}"
                        operation_id = utils.generate_unique_id(utils.get_object_keys(self.operating_docs.submitting))
                        self.operating_docs.submitting[operation_id] = utils.from_dict_to_object({
                            "body": doc_data,
                            "model": model,
                            "method": utils.REQUEST_TYPE_PUT,
                            "doc_status": "Submitted",
                            # before content
                            "before_model": model,
                            "before_method": self.validation.get("method", utils.REQUEST_TYPE_PUT)
                        })
                        
                        hc = Hooks_Controller(self, self.operating_docs.submitting[operation_id])
                        hc.hook_type = "before_submit"
                        
                        hc.init_hooks(utils.REQUEST_TYPE_PUT)
                        
                        # RESTORE PREVIOUS MODEL AND REQUEST TYPE
                        validation = self.operating_docs.submitting[operation_id]
                        object = validation.body
                        object.docstatus = 1
                        object.status = validation.doc_status or "Submitted"
                        if object.status == "Active":
                            object.status = "Submitted"

                        if object.status == "Submitted" and  self.validation.workflow_doc_status:
                            object.status =  self.validation.workflow_doc_status
                        
                        # update before final submission
                        
                        updated = self.update(validation.before_model, object, skip_hooks=True, privilege=privilege)
                        if updated.status == utils.ok:
                            names.append(updated.data.name)
                            # handle after submit hook
                            hc.hook_type = "after_submit"
                            hc.result = updated.data
                            hc.init_hooks(utils.REQUEST_TYPE_PUT)
                        else:
                            throw(updated.error_message)
                    del self.operating_docs.submitting[operation_id]
                    return utils.respond(utils.ok, f"{', '.join(names)} Docs Submitted Successfully")
                return utils.respond(utils.ok, {})
            except Exception as e:
                return utils.respond(utils.internal_server_error,f"{str(e)}")

    # TO CANCEL A DOCUMENT
    def cancel_doc(self, model, docs, user_id=None, skip_user_evaluation=False, privilege=False):
        with transaction.atomic():
            user_data = None
            if not privilege and not self.use_super_admin:
                if self.current_user_id:
                    user_data = self.current_user_id
                else:
                    return utils.respond(utils.user_not_in_headers, "User ID missing in the headers!")
            else:
                user_data = self.admin_user

                
            try:
                model_config = utils.get_model_object(model)
                model_config.status == utils.ok or throw(f'Failed to fetch model configurations: {model_config.error_message}')
                model_data = model_config.data
                many_to_many_fields = model_data.fields.many_to_many_fields
                doc_ids = self.form_request_docs_to_array(docs)
                names = []
                if doc_ids:
                    for doc_id in doc_ids:
                        doc = self.get_doc(model,doc_id,fetch_linked_fields=True, fetch_linked_tables=True, privilege=True)
                        if doc.status != utils.ok:
                            return utils.respond(utils.bad_request, f"Failed to fetch document: {doc.error_message}")
                        doc_data = doc.data
                        object = doc_data
                        object.doc_status = "Cancelled"
                        object.status = object.doc_status
                        if object.docstatus != 1:
                            return utils.respond(utils.unprocessable_entity, f"You can not cancel a document thats not submitted({object.name})")
                        object.docstatus = 2

                        # UPDATE THE MODEL AND REQUEST TYPE IN THE OBJECT
                        # operation_id = f"{model}_{doc_data.name}"
                        operation_id = utils.generate_unique_id(utils.get_object_keys(self.operating_docs.cancelling))
                        self.operating_docs.cancelling[operation_id] = utils.from_dict_to_object({
                            "body": doc_data,
                            "model": model,
                            "method": utils.REQUEST_TYPE_CANCEL,
                            "doc_status": "Cancelled",
                            # before content
                            "before_model": model,
                            "before_method": self.validation.get("method", utils.REQUEST_TYPE_CANCEL)
                        })

                        hc = Hooks_Controller(self, self.operating_docs.cancelling[operation_id])
                        hc.hook_type = "before_cancel"
                        
                        hc.init_hooks(utils.REQUEST_TYPE_CANCEL)
                        
                        
                        # RESTORE PREVIOUS MODEL AND REQUEST TYPE
                        validation = self.operating_docs.cancelling[operation_id]
                        object = validation.body
                        object.docstatus = 2
                        object.status = "Cancelled"
                        object.doc_status = object.status
                        # after running hooks
                        if many_to_many_fields:
                            for label, config in many_to_many_fields.items():
                                ct_data = getattr(object, label, None)
                                if ct_data and len(ct_data):
                                    for ct_row in ct_data:
                                        ct_row.docstatus = object.docstatus
                                        ct_row.status = object.status

                        
                        update = self.update(model, object, update_submitted=True, skip_hooks=False)
                        hc.hook_type = "after_cancel"
                        hc.result = update.data
                        hc.init_hooks(utils.REQUEST_TYPE_CANCEL)
                        names.append(object.name)
                    del self.operating_docs.cancelling[operation_id]
                    return utils.respond(utils.ok, f"{', '.join(names)} cancelled successfully")
                return utils.respond(utils.ok,{})
            except Exception as e:
                transaction.set_rollback(True)
                return utils.respond(utils.internal_server_error, f"{str(e)}")
        


    # TO DELETE DOCUMENTS
    def delete(self, model, docs, user=None, skip_user_evaluation=False, privilege=False, delete_submitted=False):
        with transaction.atomic():
            try:
                model_config = utils.get_model_object(model)
                model_config.get("status") == utils.ok or throw(f'Failed to fetch model configurations: {model_config.error_message}')
                model_data = model_config.get("data")
                many_to_many_fields = model_data.get("fields").get("many_to_many_fields")
                doc_ids = self.form_request_docs_to_array(docs)
                names = []
                if doc_ids:
                    deletion_message = ""
                    for doc_id in doc_ids:
                        doc = self.get_doc(model, doc_id, fetch_linked_fields=True, fetch_linked_tables=True, privilege=True)
                        doc.status == utils.ok or throw(f"Failed to fetch document: {doc.error_message}")
                        doc_data = doc.data
                        object = utils.from_dict_to_object(doc_data)
                        object.doc_status = object.status
                        (object.docstatus != 1 or delete_submitted == True) or throw(f"You can not delete a submitted document({object.name})")

                        # UPDATE THE MODEL AND REQUEST TYPE IN THE OBJECT
                        self.before_model = self.validation.model
                        self.before_method = getattr(self.validation, "method", utils.REQUEST_TYPE_DELETE)
                        self.validation.model = model
                        self.validation.method = utils.REQUEST_TYPE_DELETE

                        # handle hooks
                        self.validation.body = object
                        self.validation.user = user
                        hc = Hooks_Controller(self, self.validation)
                        hc.init_hooks(utils.REQUEST_TYPE_DELETE)

                        # RESTORE PREVIOUS MODEL AND REQUEST TYPE
                        self.validation.model = self.before_model
                        self.validation.method = self.before_method

                        obj = self.get_django_object(model, object.id)
                        obj.status == utils.ok or throw("Failed to get Document")
                        _obj = obj.data
                        # after running hooks
                        if many_to_many_fields:
                            for label, config in many_to_many_fields.items():
                                ct_data = doc_data.get(label)
                                if ct_data and len(ct_data):
                                    for ct_row in ct_data:
                                        ct_object = self.get_django_object(config.get("remote_model_name"), ct_row.get("id"))
                                        if ct_object and ct_object.get("status") == utils.ok:
                                            ct_object.get("data").delete(using=self.tenant_db)
                        try:
                            deleted = _obj.delete(using=self.tenant_db)
                            deletion_message += f"""<strong class='text-orange-700'> {_obj.name}</strong> Deleted Successfully <br>"""
                        except Exception as e:
                            deletion_message += f"""<strong class='text-orange-700'> {_obj.name}</strong> Deletion Failed: {str(e)} <br>"""
                            # names.append(f"Failed to delete record {_obj.name}. This record is already linked to other records in the system!")
                        # names.append(object.name)
                    return utils.respond(utils.ok, deletion_message)
                return utils.respond(utils.ok,{})
            except Exception as e:
                transaction.set_rollback(True)
                return utils.respond(utils.internal_server_error, f"{str(e)}")

    # get child table data
    def get_child_table_data(self,model, parent, jsonfy=True, fetch_linked_fields=False):
        model_object = model.get("remote_model")
        model_config = utils.get_model_object(model.get("remote_model_name"))
        model_config.get("status") == utils.ok or throw(f"Failed to fetch child table configurations: {model_config.get('error_message')}")
        model_data = model_config.get("data")

        try:
            data = model_object.objects.using(self.tenant_db).filter(parent=parent).values()
            if data:
                if not jsonfy:
                    return utils.respond(utils.ok, list(data))
                return self.extract_data(list(data))
        except Exception as e:
            return utils.respond(utils.internal_server_error,f"{str(e)}")

    def get_roles(self):
        roles = self.get_list("Role", fetch_linked_fields=True, fetch_linked_tables=True, skip_user_evaluation=True)
        if roles.status == utils.ok:
            return roles.data.rows
        return []
    

    def get_modules(self, filters={}, get_unavailable=False, fetch_linked_fields=True, fetch_linked_tables=True):
        filters.update({"available": 1})
        if get_unavailable:
            filters.update({"available__in":[0,1]})
        return self.get_list("Module", fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, filters=filters, skip_user_evaluation=True, privilege=True)
    
    def get_default_dashboards(self, filters={}, fetch_linked_fields=False,fetch_linked_tables=False):
        dashboards =  self.get_list("Default_Dashboard", filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, skip_user_evaluation=True, privilege=True)
        if dashboards.status == utils.ok:
            return dashboards.data.rows
        return []

    def get_menu_cards(self,filters={},fetch_linked_fields=True, fetch_linked_tables=True):
        roles = self.get_list("Menu_Card", filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, skip_user_evaluation=True)
        if roles.status == utils.ok:
            return roles.data.rows
        return []
    
    def get_card_items(self,filters={},fetch_linked_fields=True, fetch_linked_tables=True):
        card_items = self.get_list("Menu_Card_Item", filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, skip_user_evaluation=True)
        if card_items.status == utils.ok:
            return card_items.data.rows
        return []


    def get_system_settings(self, jsonfy=True, user=None, skip_user_evaluation=False, get_user_allowed_content=True):
        try:
            settings = self.get_doc("System_Settings","System Settings", privilege=True, fetch_linked_fields=True, fetch_linked_tables=True, jsonfy=jsonfy)
            if settings.status != utils.ok:
                return settings
            ss = settings.data
            
            company_name = ss.default_company
            if self.current_user and self.current_user.default_company:
                company_name = self.current_user.default_company
                ss.default_company = company_name
            
            comp = self.get_doc("Company", company_name, fetch_linked_fields=True, fetch_linked_tables=True,privilege=True,get_print_format=False)
            if comp.status == utils.ok:
                company = comp.data
                company.child_companies = []
                ss.linked_fields.default_company = company
                ss.linked_fields.reporting_currency = company.linked_fields.reporting_currency
                ss.default_currency = company.reporting_currency

                # if it is a group company
                if company.is_group_company:
                    child_companies = self.get_list("Company",filters={"parent_company":company.name},privilege=True, skip_company_validation=True)
                    if child_companies.status == utils.ok:
                        company.child_companies = child_companies.data.rows
            # get user allowed modules
            
            if self.current_user:
                ss.user = utils.from_object_to_dict(self.current_user)
                del ss.user["password"]
                if get_user_allowed_content:
                    try:
                        content = self.user_controller.get_user_allowed_content()
                        if content and content.status == utils.ok:
                            ss.allowed_content = content.data
                            ss.user_dashboard = ss.allowed_content.default
                    except Exception as e:
                        pp(f"Failed to fetch user allowed content:{str(e)}")
                employee_info = self.get_list("Employee", privilege=True,filters={"user": self.current_user.email})
                if employee_info and employee_info.status == utils.ok:
                    ss.employee_info = employee_info.data.rows[0]
            return utils.respond(utils.ok, ss)
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{str(e)}")
    

    # TO DELETE DOCUMENTS
    def truncate(self, models):
        parsed_models = utils.string_to_json(models)
        if parsed_models.status == utils.ok and len(parsed_models.get("data")) > 0:
            model_list = {}
            for model in parsed_models.data:
                model_list[model] = "Truncated Successfully"
                model_config = utils.get_model_object(model,get_objects=True)
                model_config.status == utils.ok or throw(f"Failed to get model meta for {model}")
                model_data = model_config.data
                model_object = model_data.model_object
                try:
                    trunc = model_object.objects.using(self.tenant_db).all().delete()
                except Exception as e:
                    print("failed to truncate")
                    return utils.respond(utils.internal_server_error,f"{str(e)}")
            return utils.respond(utils.ok,model_list)

    #tenant controller functions
    def get_tenants(self, filters={}):
        tenants =  self.get_list("Tenant", filters=filters, privilege=True, fetch_linked_tables=True, fetch_linked_fields=True)
        if tenants.status == utils.ok:
            return utils.respond(utils.ok, tenants.data.rows)
        return tenants
        
    def connect_tenant(self, tenant):
        try:
            connect = self.raw.add_tenant_db_to_db_list(tenant)
            if connect.status == utils.ok:
                dbms = DBMS(utils.from_dict_to_object({"host": tenant}))
                return utils.respond(utils.ok, dbms)
            else:
                return utils.respond(utils.internal_server_error, connect.error_message)
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{str(e)}")
        
    # get tenants allowed content
    def get_tenant_allowed_content(self, tenant="", get_dashboards=True, get_roles=True, get_allowed_menu_cards=False, get_detailed_content_for_role=False, get_detailed_content_for_dashboards=False):
        fetch_by_field = None
        allowed_content = utils.from_dict_to_object({"tenant":{}, "menu_cards":[], "modules":["core","controller"], "dashboards":[], "roles":[]})
        if not tenant:
            fetch_by_field = "db_name"
            tenant = self.tenant_db
        tenant = self.get_doc("Tenant",tenant, fetch_by_field=fetch_by_field, privilege=True, use_main_tenant=True, get_trail=False, skip_workflows=True, fetch_linked_fields=False)
        if tenant.status != utils.ok:
            return tenant
        allowed_content.tenant = tenant.data
        if tenant.data.modules:
            allowed_content.modules.extend(utils.get_object_keys(utils.array_to_dict(tenant.data.modules,"module")))
        if  allowed_content.modules:
            if get_roles:
                allowed_content.modules.append("core")
                if self.tenant_db == self.main_tenant_db:
                    allowed_content.modules.append("controller")
                roles = self.get_list("Role", filters={"module__in":allowed_content.modules,}, complex_filters=self.query_builder(module__isnull=False), privilege=True, fetch_linked_fields=get_detailed_content_for_role, fetch_linked_tables=get_detailed_content_for_role, skip_hooks=True)
                if roles.status == utils.ok:
                    if not get_detailed_content_for_role:
                        allowed_content.roles = utils.get_object_keys(utils.array_to_dict(roles.data.rows,"name")) or []
                    else:
                        allowed_content.roles = roles.data.rows
            if get_dashboards:
                dashboards = self.get_list("Default_Dashboard", filters={"module__in":allowed_content.modules,}, complex_filters=self.query_builder(module__isnull=False), privilege=True, fetch_linked_fields=get_detailed_content_for_dashboards, fetch_linked_tables=get_detailed_content_for_dashboards)
                if dashboards.status == utils.ok:
                    if not get_detailed_content_for_dashboards:
                        allowed_content.dashboards = utils.get_object_keys(utils.array_to_dict(dashboards.data.rows,"name")) or []
                    else:
                        allowed_content.dashboards = dashboards.data.rows
            if get_allowed_menu_cards:
                allowed_menu_cards = self.get_list("Module_Menu_Card", filters={"parent__in":utils.get_list_of_dicts_column_field(tenant.data.modules, "module_price")}, privilege=True,skip_hooks=True, skip_company_validation=True,fields=["menu_card"], use_main_tenant=True)
                if allowed_menu_cards.status == utils.ok:
                    allowed_content.menu_cards = utils.get_list_of_dicts_column_field(allowed_menu_cards.data.rows,"menu_card") or []
                    admin_filters = utils.from_dict_to_object({"module__in":["core"]})
                    if self.tenant_db == self.main_tenant_db:
                        admin_filters.module__in.append("controller")
                    controller_cards = self.get_list("Menu_Card", filters=admin_filters, fields=["name"], skip_hooks=True, privilege=True)
                    if controller_cards.status == utils.ok:
                        allowed_content.menu_cards.extend(utils.get_list_of_dicts_column_field(controller_cards.data.rows,"name"))

        return utils.respond(utils.ok, allowed_content)
        
    def form_request_docs_to_array(self, keys):
        docs = []
        if isinstance(keys,str) or isinstance(keys,int):
            if '[' in keys:
                new_keys = utils.string_to_json(keys)
                if new_keys.status != utils.ok:
                    return utils.respond(utils.bad_request,"doc field expected to either have a single ID value or and array of ID values!")
                docs = new_keys.data
            else:
                docs.append(keys)
        else:
            docs = keys
        return docs
