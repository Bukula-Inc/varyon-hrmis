from controllers.utils import Utils
from controllers.hooks import *
from controllers.file_controller import File_Controller
from controllers.authentication import Authentication

utils = Utils()
auth = Authentication()

class Exec:
    def __init__(self,dbms,params):
        self.params = params
        self.dbms = dbms
        self.method = params.method
        self.url_params = params.url_params
        self.body = params.body
        self.model = params.model
        self.get_single = params.get_single
        self.xfunction = params.xfunction
        self.filters = params.filters
        self.page_size = params.page_size
        self.current_page = params.current_page
        self.order_by = params.order_by
        self.group_by = params.group_by
        self.fields = params.fields
        self.headers = params.headers
        self.is_report = params.is_report
        self.has_fetched = False
        self.fetch_result= None
        self.fetch_linked_tables = params.fetch_linked_tables
        self.fetch_linked_fields = params.fetch_linked_fields
        self.fetch_lite = params.fetch_lite
        self.extra_params = params.extra_params
        self.content_type = params.content_type
        self.params.user = getattr(self.headers, "user", None)
        self.files = getattr(self.params,"files",None)
        self.min_exclusive_fields = ["linked_fields", "docstatus", "idx","status_info", "disabled", "doctype", "modified_by"]

    def execute (self):
        if self.method == utils.REQUEST_TYPE_AUTHENTICATE:
            return auth.login (self.dbms, self.body)
        
        if self.method == utils.REQUEST_TYPE_RESET_PASSWORD:
            return auth.request_password_reset (self.dbms, self.body)
        
        if self.method == utils.REQUEST_TYPE_PASSWORD_RESET_VALIDATION:
            return auth.validate_password_reset(self.dbms, self.body)
        
        else:
            try:
                self.user = self.params.user
            except Exception as e:
                return utils.respond(utils.bad_request,"User not set in the headers!")
                
        if self.method == utils.REQUEST_TYPE_GET:
            # IF THE REQUEST IS NOT FETCHING REPORTS
            if not self.is_report:
                if self.get_single:
                    if external_models.get(self.model):
                        return external_models.get(self.model)(self.dbms, self.params)
                    result = self.dbms.get_doc(
                        self.model,
                        self.get_single,
                        fetch_linked_fields=True,
                        user=self.user,
                        get_print_format=True,
                        get_trail=True,
                        fetch_by_field = self.extra_params.fetch_by_field if (self.extra_params and self.extra_params.fetch_by_field) else None
                    )
                    self.has_fetched = True
                    if result.status != utils.ok:
                        return result
                    self.fetch_result = result
                    self.fetch_result["data"] = {"total_pages":1, "rows":[result.get("data")]}
                    self.fetch_result["data"] = self.fetch_result.get("data").get("rows")[0]
                    return self.fetch_result
                
                else:
                    if external_models.get(self.model):
                        return external_models.get(self.model)(self.dbms, self.params)
                    result = self.dbms.get_list(
                        self.model,
                        filters=self.filters,
                        page_size=self.page_size,
                        current_page=self.current_page,
                        order_by=self.order_by,
                        fields=self.fields,
                        fetch_linked_tables=self.fetch_linked_tables,
                        fetch_linked_fields=self.fetch_linked_fields,
                        user=self.params.user,
                        fetch_lite=True,
                    )
                    return result
                    
            
            # IF THE REQUEST IS FETCHING REPORTS
            else:
                # IF THE REPORT IS SCRIPTED, ENGANGE CUSTOM SCRIPT
                try:
                    script = script_reports.get(self.model)
                    self.params.filters = utils.from_dict_to_object({})
                    if self.headers.Filters:
                        filters = utils.string_to_json(self.headers.Filters)
                        self.params.filters = filters.data if filters.status == utils.ok else utils.from_dict_to_object({})
                    if script and script != None:
                        try:
                            script_result = script(self.dbms, self.params)
                            if not script_result:
                                return utils.respond(utils.internal_server_error, f"Failed to generate {self.model} report: Script didn't return anything!")
                            if script_result.status != utils.ok and script_result.status != utils.no_content:
                                return utils.respond(utils.internal_server_error,script_result.get("error_message") or "Failed to generate report!")
                            return script_result
                        except Exception as e:
                            return utils.respond(utils.internal_server_error, f"<strong class='text-15'>{str(e)}</strong>")
                    #IF NOT SCRIPTED, JUST GO ON AND DO THE NORMAL FETCH
                    else:
                        result =  self.dbms.get_list(self.model, filters=self.filters, page_size=self.page_size, current_page=self.current_page, order_by=self.order_by,user=self.user)
                        if  result.status != utils.ok:
                            return result
                        return result
                except Exception as e:
                    return utils.respond(utils.internal_server_error, f"{e}")


        # IF POSTING NEW DATA
        elif self.method == utils.REQUEST_TYPE_POST:
            # handle naming series
            submit_after_create = False
            if external_models.get(self.model):
                return external_models.get(self.model)(self.dbms, self.params)
            if self.body.get("submit_after_create") and self.body.get("submit_after_create") == True:
                submit_after_create = True
                
            create = self.dbms.create(self.model,self.body,self.user, submit_after_create=submit_after_create)
            if self.params.minify and create.status == utils.ok:
                create.data = utils.remove_keys_from_dict(create.data, self.min_exclusive_fields,remove_null_values=True)
            return create
        
        # IF UPLOADING NEW FILE
        elif self.method == utils.REQUEST_TYPE_UPLOAD:
            if external_models.get(self.model):
                return external_models.get(self.model)(self.dbms, self.params)
            # handle naming series
            upload_manager = File_Controller(self.dbms, self.files)
            return upload_manager.write_files()
        
        # IF UPLOADING NEW FILE
        elif self.method == utils.REQUEST_TYPE_EXTRACT_DOC_DATA:
            if external_models.get(self.model):
                return external_models.get(self.model)(self.dbms, self.params)
            # handle naming series
            fc = File_Controller(self.dbms, self.files)
            val = fc.validate_files()
            if val.status != utils.ok:
                return val
            return fc.extract_data_importation_rows(file=self.files.get("doc"))

        # WHEN UPDATING EXISTING DATA
        elif self.method == utils.REQUEST_TYPE_PATCH:
            if external_models.get(self.model):
                return external_models.get(self.model)(self.dbms, self.params)
            
            patched = self.dbms.update(self.model,self.body,self.user)
            if self.params.minify and patched.status == utils.ok:
                patched.data = utils.remove_keys_from_dict(patched.data, self.min_exclusive_fields,remove_null_values=True)
            return patched
        
        # WHEN SUBMITTING EXISTING DATA
        elif self.method == utils.REQUEST_TYPE_PUT:
            if external_models.get(self.model):
                return external_models.get(self.model)(self.dbms, self.params)
            return self.dbms.submit_doc(self.model,self.headers.Doc,self.user)
        
        # WHEN CANCELLING DATA
        elif self.method == utils.REQUEST_TYPE_CANCEL:
            if external_models.get(self.model):
                return external_models.get(self.model)(self.dbms, self.params)
            return self.dbms.cancel_doc(self.model,self.headers.Doc,self.user)
        
        elif self.method == utils.REQUEST_TYPE_DELETE:
            if external_models.get(self.model):
                return external_models.get(self.model)(self.dbms, self.params)
            return self.dbms.delete(self.model,self.headers.Doc,self.user)
        
        elif self.method == utils.REQUEST_TYPE_TRUNCATE:
            return self.dbms.truncate(self.headers.Doc, self.user)
        
        
        elif self.method == utils.REQUEST_TYPE_X_FETCH:
            try:
                xfun = x_fetch.get(self.headers.Xfun) 
                if xfun:
                    result = xfun(self.dbms, self.params)
                    if not isinstance(result, dict):
                        return utils.respond(utils.unprocessable_entity,"X-Function expected to return a dictionary of {status, data or error_message}!")
                    elif not result.status:
                        return utils.respond(utils.unprocessable_entity,"X-Function result is only expected to return a dictionary of {status, data or error_message}!")
                    return result
                return utils.respond(utils.not_found,f"X-Function with key '{self.headers.Xfun}' not found in hooks!")
            except Exception as e:
                return utils.respond(utils.internal_server_error,f"Failed to fetch data: {e}")
            
        elif self.method == utils.REQUEST_TYPE_FETCH_FORM_FIELDS:
            try:
                ff = form_fields.get(self.headers.Model) 
                if ff:
                    result = ff(self.dbms, self.params)
                    if not isinstance(result, dict):
                        return utils.respond(utils.unprocessable_entity,"Form Fields expected to return a dictionary of {status, data or error_message}!")
                    elif not result.status:
                        return utils.respond(utils.unprocessable_entity,"Form Fields result is only expected to return a dictionary of {status, data or error_message}!")
                    return result
                return utils.respond(utils.not_found,f"Form Fields with key '{self.headers.Model}' not found in hooks!")
            except Exception as e:
                return utils.respond(utils.internal_server_error,f"Failed to fetch data: {e}")
            
        elif self.method == utils.REQUEST_TYPE_WORKFLOW_ACTION:
            try:
                return self.dbms.workflow.update_workflow(self.params)
            except Exception as e:
                return utils.respond(utils.internal_server_error,f"{e}")
        
        elif self.method == utils.REQUEST_TYPE_DASHBOARD:
            try:
                xfun = dashboards.get(self.headers.Xfun) 
                if xfun:
                    result = xfun(self.dbms,self.params)
                    if not isinstance(result,dict):
                        return utils.respond(utils.unprocessable_entity,"X-Function expected to return a dictionary of {status, data or error_message}!")
                    elif not result.status:
                        return utils.respond(utils.unprocessable_entity,"X-Function result is only expected to return a dictionary of {status, data or error_message}!")
                    elif not result.get("data") and not  result.get("error_message"):
                        return utils.respond(utils.unprocessable_entity,"X-Function result is only expected to return a dictionary of {status, data or error_message}!")
                    return result
                return utils.respond(utils.not_found,f"X-Function with key '{self.headers.Xfun}' not found in hooks!")
            except Exception as e:
                return utils.respond(utils.internal_server_error,f"{e}")
        
        elif self.method == utils.REQUEST_TYPE_X_POST:
            try:
                xfun = x_post.get(self.headers.Xfun) 
                if xfun:
                    result = xfun(self.dbms,self.params)
                    if not isinstance(result,dict):
                        return utils.respond(utils.unprocessable_entity,"X-Function expected to return a dictionary of {status, data or error_message}!")
                    elif not result.status:
                        return utils.respond(utils.unprocessable_entity,"X-Function result is only expected to return a dictionary of {status, data or error_message}!")
                    elif "data" not in result and "error_message" not in result:
                        return utils.respond(utils.unprocessable_entity,"X-Function result is only expected to return a dictionary of {status, data or error_message}!")
                    return result
                return utils.respond(utils.not_found,f"X-Function with key '{self.headers.Xfun}' not found in hooks!")
            except Exception as e:
                return utils.respond(utils.internal_server_error,f"{e}")
            
        elif self.method == utils.REQUEST_TYPE_CORE:
            from controllers.framework import Core
            try:
                if self.headers.Xfun:
                    return Core.init(self.dbms, self.params)
                return utils.respond(utils.not_found,f"xfun not found in headers!")
            except Exception as e:
                return utils.respond(utils.internal_server_error,f"{e}")
            
        elif self.method == utils.REQUEST_TYPE_EXPORT_DATA:
            from controllers.data_export import Data_Export
            try:
                dx = Data_Export(self.dbms,  self.params)
                return dx.export_data()
            except Exception as e:
                return utils.respond(utils.internal_server_error,f"{e}")
