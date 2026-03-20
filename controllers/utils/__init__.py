from cryptography.fernet import Fernet
from decimal import Decimal, ROUND_HALF_UP
import math
import html
import json
import base64
import os
import re
import string
import random
import qrcode
import uuid
import hashlib
from django.apps import apps
from django.db.models.fields.related import ManyToOneRel
from django.contrib.auth.hashers import make_password
from django.core import serializers
import time
from controllers.utils.jwt import JWT
from multitenancy.settings import INSTALLED_APPS, CLIENT_API_KEY_SECRET_KEY
from .dates import Dates
from datetime import date
import pandas as pd
from datetime import datetime, date
from controllers.utils.dict_to_object import Dict_To_Object, Object_To_Dict
from itertools import groupby
from operator import attrgetter, itemgetter
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse



dates = Dates()

jwt = JWT()

class Utils:
    # define status codes
    ok = 200
    created = 201
    no_content = 204
    moved_permanently = 301
    found = 302
    not_modified = 304
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_found = 404
    method_not_allowed = 405
    unprocessable_entity = 422
    internal_server_error = 422 #500
    not_implemented = 501
    bad_request = 502
    service_unavailable = 503
    user_not_in_headers = 401

    VALIDATION_TYPE_CREATE = "CREATE"
    VALIDATION_TYPE_GET = "GET"
    VALIDATION_TYPE_UPDATE = "UPDATE"
    VALIDATION_TYPE_DELETE = "DELETE"

    REQUEST_TYPE_GET = "GET"
    REQUEST_TYPE_GET_DOC_VALUE = "GET_DOC_VALUE"
    REQUEST_TYPE_X_FETCH = "X_FETCH"
    REQUEST_TYPE_DASHBOARD = "DASHBOARD"
    REQUEST_TYPE_POST = "POST"
    REQUEST_TYPE_UPLOAD = "UPLOAD"
    REQUEST_TYPE_EXTRACT_DOC_DATA = "EXTRACT_DOC_DATA"
    REQUEST_TYPE_X_POST = "X_POST"
    REQUEST_TYPE_CORE = "CORE"
    REQUEST_TYPE_EXPORT_DATA = "EXPORT_DATA"
    REQUEST_TYPE_WORKFLOW_ACTION = "WORKFLOW_ACTION"
    REQUEST_TYPE_PUT = "PUT"
    REQUEST_TYPE_CANCEL = "CANCEL"
    REQUEST_TYPE_PATCH = "PATCH"
    REQUEST_TYPE_DELETE = "DELETE"
    REQUEST_TYPE_TRUNCATE = "TRUNCATE"
    REQUEST_TYPE_FETCH_FORM_FIELDS = "FETCH_FORM_FIELDS"
    REQUEST_TYPE_AUTHENTICATE = "AUTHENTICATE"
    REQUEST_TYPE_RESET_PASSWORD = "RESET_PASSWORD"
    REQUEST_TYPE_PASSWORD_RESET_VALIDATION = "REQUEST_TYPE_PASSWORD_RESET_VALIDATION"


    def __init__(self) -> None:
        pass

    def respond(self, status, response, as_dict=False):
        resp = {"status": status}
        if status != self.ok and status != self.created:
            resp['error_message'] = response
        else:
            resp["data"] = response
        if as_dict:
            return resp
        return self.from_dict_to_object(resp)

    def evaluate_response(self,result:dict, error_message:str=None, statuses:list=[200]):
        if result.get("status") in statuses or result.get("status") == self.ok:
            return True
        else:
            if error_message:
                self.throw(error_message)
        return False
    
    def json_respond(self, status, message):
        return JsonResponse(message, status=status,safe=False)

    def get_request_domain(self, req):
        try:
            name = ""
            domain = req.get_host()
           
            if domain:
                name = domain.split(':')[0]
                if "www." in name:
                    name = name[4:]
                return self.respond(self.ok, name)
            return self.respond(self.not_found, "Domain not found!")
        except Exception as e:
            return self.respond(self.internal_server_error, e)

    def extract_api_key(self, request):
        if request.headers.get("Cookie") and "api_key" in request.headers.get("Cookie"):
            splited = request.headers.get("Cookie").split("key=")
            if splited and len(splited) > 1:
                try:
                    return splited[1]
                except Exception as e:
                    return False
            return False


    def validate_request(self, request, ignore_model=False, is_upload_request=False):
        jwt_token = request.COOKIES if hasattr(request, "COOKIES") else None
        method = request.method  
        headers = request.headers 
        data_obj = self.from_dict_to_object({})
        data_obj.body = None
        data_obj.is_report = False

        data_obj.tenant_db = getattr(request, "tenant_db", None)
        data_obj.tenant_id = getattr(request, "tenant_id", None)
        data_obj.path = getattr(request, "path", None)

        try:
            if not headers.get("model") and not ignore_model:
                return self.respond(self.bad_request, "Headers missing `Model` Parameter!")

            if headers.get("get-single") == '':
                return self.respond(self.bad_request, "Headers parameter `get-single` missing value id!")

            if method in ['POST', 'PATCH'] and not is_upload_request:
                body = request.body
                if not body:
                    return self.respond(self.not_found, "Request missing body!")
                body = self.string_to_json(body.decode('utf-8'))
                if not body.get("data"):
                    return self.respond(self.not_found, f'Request body missing data key: {body.get("error_message")}')
                data_obj.body = body.get("data")

            if method in ["PUT", "DELETE"] and not headers.get("doc"):
                return self.respond(self.bad_request, "Headers parameter `doc` missing value!")

            data_obj.model = headers.get("model")
            if headers.get("Module"):
                data_obj.module = headers.get("Module").lower()

            data_obj.extra_params = self.from_dict_to_object()
            if headers.get("Params"):
                xtra_params = self.string_to_json(headers.get("Params"))
                if xtra_params.status == self.ok:
                    data_obj.extra_params = xtra_params.data

            data_obj.method = method
            data_obj.get_single = headers.get("get_single")
            data_obj.api_key = headers.get("api_key") or getattr(request, "api_key", None)
            data_obj.xfunction = headers.get("xfunction")
            data_obj.host = self.get_request_domain(request).get("data")
            data_obj.tenant = data_obj.host.split(".")[0] if data_obj.host else None
            data_obj.filters = headers.get("filters", {})
            data_obj.page_size = headers.get("page-size")
            data_obj.current_page = headers.get("current-page")
            data_obj.order_by = headers.get("sort")
            data_obj.group_by = headers.get("group-by")
            data_obj.fields = headers.get("fields")
            data_obj.url_params = request.GET
            data_obj.fetch_linked_fields = headers.get("fetch-linked-fields", False)
            data_obj.fetch_linked_tables = headers.get("fetch-linked-tables", False)
            data_obj.fetch_lite = headers.get("fetch-lite", False)
            data_obj.minify = True if headers.get("minify", False) else False
            data_obj.headers = dict(headers)
            if not data_obj.api_key:
                api_key = self.extract_api_key(request)
                if api_key:
                    data_obj.api_key = api_key
            data_obj.headers["user"] = ""
            data_obj.status = self.ok
            if jwt_token:
                cookie = jwt_token.get("lite_user")
                decoded = jwt.decode_token(cookie)
                if decoded.get("status") == self.ok:
                    deco = decoded.get("data")
                    data_obj.user_current_company = deco.get("company")
                    data_obj.user_current_company_id = deco.get("cid")
                    data_obj.user = deco.get("user_id")
                    data_obj.headers["user"] = deco.get("user_id")
            return self.respond(self.ok, data_obj)

        except ValueError as e:
            raise ValueError(f"error, {e}")


    def get_path_to_base_folder(self):
        return os.getcwd()

    def concatnate_file_path(self, path, file_name):
        full_path = os.path.join(path, file_name)
        return full_path

    def string_to_json(self, param):
        if isinstance(param, str):
            try:
                return self.respond(self.ok, json.loads(param))
            except Exception as e:
                return self.respond(self.internal_server_error, f"String to json parsing error: {str(e)}")
        elif isinstance(param, list):
            return self.respond(self.ok, param)
        return self.respond(self.ok, param if isinstance(param, dict) else {})

    def json_to_string(self, objects):
        try:
            return self.respond(self.ok, json.loads(objects))
        except Exception as e:
            return self.respond(self.internal_server_error, f"String to json parsing error: {e}")

    def serialize(self, objects):
        try:
            return self.respond(self.ok, serializers.serialize('json', objects))
        except Exception as e:
            return self.respond(self.internal_server_error, f"String to json parsing error: {e}")

    def capitalize(self, str):
        try:
            return str.title()
        except:
            return ''

    def remove_special_characters(self, input_string):
        pattern = r'[^a-zA-Z0-9 ._]'
        return re.sub(pattern, '', f"{input_string}")

    def replace_character(self, str, target_key, replacement_key):
        return str.replace(target_key, replacement_key)

    def generate_password(self, lengttrns_typeh=8):
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        numbers = string.digits
        punctuation_characters = string.punctuation
        uppercase_chars = "".join(random.choices(uppercase_letters, k=10))
        lowercase_chars = "".join(random.choices(lowercase_letters, k=15))
        number_chars = "".join(random.choices(numbers, k=8))
        punctuation_chars = "".join(random.choices(punctuation_characters, k=13))
        all_chars = list(uppercase_chars + lowercase_chars + number_chars)
        random.shuffle(all_chars)
        password = "".join(all_chars)
        return password
    
    def generate_random_string(self, length=8):
        return self.generate_password(length)
    
    def generate_otp(self, length=8):
        numbers = string.digits
        number_chars = random.choices(numbers, k=length)
        random.shuffle(number_chars)
        return ''.join(number_chars)
    
    def generate_dashed_otp(self, length=16, group_size=4,separator=" "):
        numbers = string.digits
        number_chars = random.choices(numbers, k=length)
        otp = ''.join(number_chars)
        otp_with_hyphens = f'{separator}'.join([otp[i:i+group_size] for i in range(0, len(otp), group_size)])
        return otp_with_hyphens

    def validate_keys(self, keys, data):
        if len(keys) > 0:
            for key in keys:
                if (not data.get(key) or data.get(key) == None) and data.get(key) != 0:
                    return self.respond(self.not_found, f"Key '{key}' missing in data!")
        return self.respond(self.ok, "")

    def is_array(self,obj):
        return isinstance(obj,list)
    
    def is_dict(self,obj):
        return isinstance(obj,dict)
    
    def is_string(self,val):
        return isinstance(val,str)
    
        # check if value is digit
    def is_digit(self,val):
        if f"{val}".isdigit() or bool(re.match(r'^-?\d+\.\d+$', f"{val}")):
            return True
        return False
        
    def fixed_decimals(self,figure,decimals=4, round_down=False):
        if round_down:
            factor = 10 ** decimals
            return math.floor(float(figure or 0.0) * factor) / factor
        return round(float(figure or 0.00000), decimals)
    

    def decimal(self,figure=0, decimals=10):
        if figure is None:
            figure = 0.0
        else:
            figure = Decimal(str(figure))
        rounded_value = figure.quantize(Decimal('1.' + '0' * decimals), rounding=ROUND_HALF_UP)
        return rounded_value
    
    def is_decimal(self, figure=0):
        return isinstance(figure, Decimal)

    
    def percentage_to_decimal(self, percentage):
        if percentage:
            return float(percentage) / 100
        return 0
    
    def percentage_of(self, rate, value):
        return float(value or 0) * self.percentage_to_decimal(rate) 

    def throw(self, message="", bound=False):
        if bound:
            raise Exception(
                f"""\n\n>>>>>>>>>>>>>>>>>>>>>>>> EXCEPTION RAISED <<<<<<<<<<<<<<<<<<<<<<\n\n
                    {message}
                    \n\n>>>>>>>>>>>>>>>>>>>>>>>> EXCEPTION RAISED <<<<<<<<<<<<<<<<<<<<<<\n\n
                """
            )
        raise Exception(message)
    
    def format_amount(self, amount=0,decimals=2):
        return round(float(amount),decimals)
    
    
    # CREATE NAMING_SERIES
    def extract_placeholders(self,series_format):
        matches = re.findall(r'\{(\w+)\}', series_format)
        return matches

    def __replace_placeholders(self, series_format, replacements):
        def replace(match):
            key = match.group(1)
            return replacements.get(key, match.group(0))
        replaced = re.sub(r'\{(\w+)\}', replace, series_format)
        return replaced

    def create_naming_series(self,model, dbms, doc):
        series_config = dbms.increase_series(model)
        if series_config.status != self.ok:
            return series_config
        series = series_config.data
        
        naming = series.name_format
        if not naming:
            return self.respond(self.no_content,"Naming series field is empty!")
        placeholders = self.extract_placeholders(naming)
        if placeholders:
            split_date = dates.get_split_date()
            lowered = [ph.lower() for ph in placeholders]
            replacers = {}
            
            if "date" in lowered:
                replacers["DATE"] = f'{dates.today()}'
            if "year" in lowered:
                replacers["YEAR"] = f'{split_date.get("year")}'
            if "month" in lowered:
                replacers["MONTH"] = f'{split_date.get("month")}'
            if "day" in lowered:
                replacers["DAY"] = f'{split_date.get("day")}'
            if "time" in lowered:
                replacers["TIME"] = f'{split_date.get("time")}'
            if "timestamp" in lowered:
                replacers["TIMESTAMP"] = f'{split_date.get("timestamp")}'
            if "series_count" in lowered:
                replacers["series_count"] = series.get("series_count")
            body = doc
            for label in lowered:
                if body.get(label) and label not in ["year","month","day","time","timestamp","series_count","date"]:
                    replacers[label] = f'{body.get(label)}' or ""
            final_name = self.__replace_placeholders(naming,replacers)
            if final_name:
                doc.name = final_name
            return self.respond(self.ok,{"name":doc.name})
        

    def pretty_print(self, *args):
        def serialize_dates_and_decimals(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            elif isinstance(obj, Decimal):
                return str(obj)
            elif hasattr(obj, '__dict__'):
                return obj.__dict__
            return obj

        formatted_args = [json.dumps(arg, default=serialize_dates_and_decimals, indent=4) for arg in args]
        print("\n\n\n<|=======================================PRETTY PRINT=======================================|>\n\n\n")
        for arg in formatted_args:
            print(arg)
        print("\n\n\n<|=======================================PRETTY PRINT=======================================|>\n\n\n")

    def today(self,):
        return dates.today ()
        
    def thousand_separator(self,figure,decimals=2):
        import locale
        locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
        formatted_figure = locale.format_string('%0.2f', float(figure or 0), grouping=True)
        return(formatted_figure)
    
    def number_to_words(self,figure):
        import inflect
        p = inflect.engine()
        words = p.number_to_words(figure)
        return words
    
    def tax_name_from_tax_account(self,account):
        return account.split("-")[1]
    
    def is_date_value(self, val):
        date_pattern = r'(\b\d{4}[-/]\d{2}[-/]\d{2}(?:\s\d{2}:\d{2}:\d{2})?\b)|(\b\d{2}[-/]\d{2}[-/]\d{4}(?:\s\d{2}:\d{2}:\d{2})?\b)'
        match = re.search(date_pattern, f"{val}")
        return True if match else False

    
    def normalize_row_columns(self,row):
        new_row = {}
        for label, value in row.items():
            key = self.replace_character(self.remove_special_characters(label)," ","_").lower()
            new_row[key] = value.strip() if isinstance(value, str) else value
            if self.is_date_value(value):
                new_row[key] = dates.format_date_to_default(value)
        return self.from_dict_to_object(new_row)
    
    def encrypt_password(self, password=None, generate=False):
        pwd = password
        if generate:
            pwd = self.generate_password(6)
        elif not pwd:
            return self.respond(self.bad_request,"No Password provided")
        return self.respond(self.ok,{ "password": pwd, "encrypted": make_password(pwd)})

    
    def get_app_models(self, app_name,fetch_model_objects=False, model=None):
        models = []
        app_models = apps.get_app_config(app_name).get_models()
        for mdl in app_models:
            if fetch_model_objects:
                models.append(mdl)
            else:
                models.append(mdl.__name__)
            # if only looking for a certain model
            if model and mdl.__name__ == model:
                return mdl
        # if looking for a certain model and its not found
        if model:
            return False
        return models
    


    # Get Model Object
    def get_model_object(self, model=None, get_all=False, get_objects=True, get_fields=True, get_child_models=True):
        lst = []
        child_tables = []
        
        apps = [
            app.split(".")[-1] 
            for app in INSTALLED_APPS 
            if "client_app" in app 
            and app != "client_app" 
            and app.split('.')[-1] not in ["auth","admin","contenttypes","sessions","messages","staticfiles"]
        ]
        for app in apps:
            app_model = self.get_app_models(app, fetch_model_objects=True, model = model)
            if app_model:
                if isinstance(app_model, list):
                    for mdl in app_model:
                        model_fields = self.from_dict_to_object()
                        if get_fields:
                            model_fields = self.get_model_fields(mdl, get_objects=get_objects)
                        if get_child_models:
                            child_models = model_fields.get("data").get("child_models")
                        if child_models:
                            child_tables.extend(child_models)
                        lst.append({
                            "model_app": app,
                            "model_object": mdl if get_objects else None,
                            "name":mdl.__name__, 
                            "model_name":model, 
                            "fields": model_fields.get("data")
                        })
                else:
                    model_fields = self.get_model_fields(app_model, get_objects=get_objects)
                    res = {"model_app": app,"model_object": app_model if get_objects else None,"name":app_model.__name__, "model_name":model, "fields": model_fields.get("data") }

                    return self.respond(self.ok, res)
        final = []
        return self.respond(self.ok, lst)

    # get fields for the model
    def get_model_fields(self, model_object, get_objects=True):
        child_models = []
        try:
            model_fields = {}
            many_to_many_fields = {}
            foreign_key_fields = {}
            all_fields = model_object._meta.get_fields()
            for field in all_fields:
                field_type = field.get_internal_type()
                is_many_to_one = isinstance(field, ManyToOneRel)
                related_model = None
                if not is_many_to_one:
                    # if its a many to many field
                    if hasattr(field, 'remote_field') and hasattr(field.remote_field, 'through'):
                        intermediate_model = field.remote_field.through
                        remote_model = field.remote_field.model
                        child_models.append(remote_model.__name__)
                        many_to_many_fields[field.name]={
                            "field_name":field.name,
                            "remote_model":remote_model if get_objects else None,
                            "remote_model_name": remote_model.__name__,
                            "intermediate_model": intermediate_model if get_objects else None,
                            "intermediate_model_name": intermediate_model.__name__,
                            "constraints": self.__get_field_constraints(field, get_objects=get_objects)
                        }
                    
                    # if it is a foreign key field
                    elif field_type == "ForeignKey":
                        related_model = field.related_model
                        foreign_key_fields[field.name] = {
                            "field_name":field.name,
                            "model_object": related_model if get_objects else None,
                            "model_name": related_model.__name__,
                            "constraints": self.__get_field_constraints(field, get_objects=get_objects)
                        }

                    elif not is_many_to_one:
                        # pass
                        model_fields[field.name] = {
                            "field_name": field.name,
                            "field_type": field_type,
                            "related_model": related_model if get_objects else None,
                            "constraints": self.__get_field_constraints(field, get_objects=get_objects)
                        }
            return self.respond(
                self.ok, {
                    "normal_fields": model_fields, 
                    "many_to_many_fields": many_to_many_fields,
                    "foreign_key_fields": foreign_key_fields,
                    "child_models":child_models
                }
            )
        except Exception as e:
            self.throw(f"Model config generation failed: {e}")
    
    
    # to get field constraints
    def __get_field_constraints(self, field, get_objects=True):
        constraints = {
            "unique"      : getattr(field, "unique", False),
            "primary_key" : getattr(field, "primary_key", False),
            "null"        : getattr(field, "null", False),
            "blank"       : getattr(field, "blank", False),
            "default"     : getattr(field, "default", False) if get_objects else None,
        }
        return constraints

    

    def get_model_module(self, model):
        try:
            if isinstance(model, str):
                model_data = self.get_model_object(model,get_fields=False, get_child_models=False)
                if model_data.status == self.ok:
                    model = model_data.data.model_object
            if model:
                try:
                    content = model.__module__.split('.')[:-1]
                    if content and len(content) >=2:
                        if content[0] == "client_app":
                            return self.respond(self.ok, {
                                "wrapper_module": content[0],
                                "module": content[1],
                                "app": content[2],
                                "content_type": self.replace_character(model.__name__,"_"," ")
                            })
                except Exception as e:
                    return self.respond(self.internal_server_error,f"Failed to extract model content: {e}")
        except Exception as e:
            return self.respond(self.internal_server_error, str(e))


    def normalize_import_data(self, lst, doc=None):
        if len(lst) > 0:
            data = []
            for d in lst:
                for l, v in d.items():
                    if isinstance(v, (pd.Timestamp, datetime, date)):
                        d[l] = str(v)
                    if pd.isna(v):
                        d[l] = None
                if not d.get("status"):
                    d["status"] = "Pending Import"
                data.append(d)
            return data

    def sort(self, lst=[], is_object=False, descend=False, sort_by="id"):
        if is_object:
            return sorted(lst, key=lambda x: x.id, reverse=descend)
        return sorted(lst, key=lambda x: x[sort_by], reverse=descend)
    
    def remove_duplicates(self, lst:list):
        return list(set(lst))
    
    def array_to_dict(self, lst, key, lower=False):
        if lower:
            return self.from_dict_to_object(dict(map(lambda item: (f"{item[key] or ''}".strip().lower(), item), lst)))
        return self.from_dict_to_object(dict(map(lambda item: (f"{item[key] or ''}", item ), lst)))
    def reverse_array_to_dict(self, obj):
        return list(obj.values())

    def group(self,lst, group_by):
        return self.from_dict_to_object(dict(map(lambda x: (x[0], list(x[1])), groupby(sorted(lst, key=itemgetter(group_by)), itemgetter(group_by)))))
        # return dict(map(lambda x: (x[0], list(x[1])), groupby(sorted(lst, key=attrgetter(group_by)), attrgetter(group_by))))
    
    def get_fields(self, data, fields):
        df = self.to_data_frame(data)
        return df[list(fields)].to_dict('records')
    
    def get_list_of_dicts_column_field(self,lst:list, field:str, lower=False):
        lowered_field= field.lower()
        df = self.to_data_frame(lst)
        df.columns = df.columns.str.lower()
        if lower:
            return df[lowered_field].astype(str).str.lower().str.strip().tolist()
        return df[lowered_field].tolist()
    
    def extract_dict_fields_from_list(self,lst:list, fields:list):
        return list(map(lambda item: {field: item[field] for field in fields if field in item}, lst))



    def sum(self, data, field):
        df = self.to_data_frame(data)
        return df[field].apply(float).sum()
    
    def to_data_frame(self, data=[], is_dict=False):
        obj_vals = {}
        if not is_dict:
            obj = Object_To_Dict(data)
            obj_vals = obj.to_dict()
        else:
            obj_vals = data 
        return pd.DataFrame(obj_vals)

    def get_pandas_object(self):
        return pd
    
    def df_to_dict(self, pd, orient=True):
        if not orient:
            return pd.to_dict()
        return pd.to_dict(orient='records')

    def df_column_to_float(self,df, column_name):
        df[column_name] = df[column_name].astype(float)

    
    def from_dict_to_object(self, data={}):
        return Dict_To_Object(data)
    
    def from_object_to_dict(self, data):
        obj = Object_To_Dict(data)
        return obj.to_dict()
    
    def get_object_keys(self, obj = {}, lower=False):
        try:
            if lower:
                return [key.lower() for key in obj.keys()]
            return list(obj.keys())
        except Exception as e:
            return []
    
    def remove_keys_from_dict(self, data, keys_to_remove, remove_from_children=True, remove_null_values=False):
        """Recursively removes specified keys and optionally removes null values from a nested dictionary or list."""
        try:
            if isinstance(data, dict):
                # Remove specified keys
                for key in keys_to_remove:
                    try:
                        data.pop(key, None)
                    except Exception as e:
                        self.pretty_print(f"Error removing key '{key}': {str(e)}")

                # Recursively process child dictionaries if enabled
                if remove_from_children:
                    for k, v in list(data.items()):  # Use list(data.items()) to avoid runtime dict modification issues
                        try:
                            data[k] = self.remove_keys_from_dict(v, keys_to_remove, remove_from_children, remove_null_values)
                            # Remove null values if enabled
                            if remove_null_values and data[k] is None:
                                del data[k]
                        except Exception as e:
                            self.pretty_print(f"Error processing key '{k}': {str(e)}")

            elif isinstance(data, list):
                # Process each item in the list
                try:
                    data = [self.remove_keys_from_dict(item, keys_to_remove, remove_from_children, remove_null_values) for item in data]
                    # Remove null values if enabled
                    if remove_null_values:
                        data = [item for item in data if item is not None]
                except Exception as e:
                    self.pretty_print(f"Error processing list: {str(e)}")

        except Exception as e:
            self.pretty_print(f"Unexpected error: {str(e)}")

        return data



        
    def object_has_key(self, obj:dict, key:str):
        return key in obj
        
    def get_object_values(self, obj = {}):
        try:
            return list(obj.values())
        except Exception as e:
            return []
        
    def checker (self, data, is_list: bool = False):
        if data.status == self.ok:
            if is_list:
                return data.data.rows
            return data.data
        return None
    
    def check_datatype (self, variable, type):
        return isinstance (variable, type)

    def get_date_filter_range(self, date_str):
        if date_str and "-->" in date_str:
            splt = date_str.split("-->")
            return self.from_dict_to_object({ "from_date":splt[0].strip(), "to_date":splt[1].strip()})
        return False
    

    def calculate_exec_time(self,start_time, model=None):
        self.pretty_print(time.time() - start_time, model)

    def extract_object_fields(self, obj, fields):
        return self.from_dict_to_object({**{field: obj.get(field) for field in fields}})
    

    def generate_qr_code(self,name, data, host):
        clean_name = self.remove_special_characters(name)
        file_path = f"/media/{host}/private/qr_codes/qrcd{clean_name}.png"
        private_path = f"{self.get_path_to_base_folder()}/media/{host}/private/qr_codes/"
        qr_path = f"{private_path}qrcd{clean_name}.png"
        if not os.path.exists(private_path):
            try:
                os.makedirs(private_path, exist_ok=True)
            except Exception as e:
                self.pretty_print(f"An error occurred while creating qr code folder:{str(e)}")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=1,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="#151030", back_color="white")
        # Save the image
        img.save(qr_path)
        return file_path
    
    
    def get_text_from_html_string(self, str=""):
        return re.sub(r'<.*?>', '', html.unescape(str or ""))
    

    def get_datetime_string (self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        year = now.year
        month = now.month
        day = now.day
        datetime_string = f"{hour:02d}{minute:02d}{second:02d}"
        
        return datetime_string
    
    def remove_hyphens(self, date_string):
        return date_string.replace('-', '')
    
    def load_encryption_lib (self):
        return Fernet (CLIENT_API_KEY_SECRET_KEY)

    def generate_client_api_key (self, object):
        encrypt = self.load_encryption_lib ()
        client_credentials_obj = json.dumps (object).encode ()
        encrypted = encrypt.encrypt( client_credentials_obj)
        return base64.urlsafe_b64encode (encrypted).decode ()
    

    def decode_client_api_key (self, client_api_key: str):
        try:
            encrypt = self.load_encryption_lib ()
            encrypted = base64.urlsafe_b64decode (client_api_key.encode ())
            decrypted = encrypt.decrypt (encrypted)
            return self.from_dict_to_object (json.loads (decrypted.decode ()))
        except Exception as e:
            self.throw(f"Invalid API-KEY:{str(e)}")


    def find_single_missing_item_from_one_list(self, list_1:list, list_2: list, key: str):
        item_names_list_1 = set (item.get (key) for item in list_1)
        item_names_list_2 = set (item.get (key) for item in list_2)
        missing_in_list_1 = item_names_list_2 - item_names_list_1
        missing_in_list_2 = item_names_list_1 - item_names_list_2
        if missing_in_list_1:
            return missing_in_list_1.pop()
        if missing_in_list_2:
            return missing_in_list_2.pop()
        return None
    


    def generate_unique_id(self, existing_keys=[]):
        if not existing_keys:
            random_uuid = uuid.uuid4()
            return hashlib.sha256(str(random_uuid).encode()).hexdigest()
        else:
            attempts = 0
            while True:
                attempts += 1
                random_uuid = uuid.uuid4()
                key = hashlib.sha256(str(random_uuid).encode()).hexdigest()
                if key not in existing_keys:
                    return key
                if attempts == 50:
                    return False
                

                    
    def encode(self, obj):
        import datetime
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return str(obj)  
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        return obj