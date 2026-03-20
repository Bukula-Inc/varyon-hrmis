from controllers.utils import Utils
from controllers.utils.dates import Dates
import copy, csv
from management.defaults.core.tenant_admin import tenant_admin
from controllers.mailing.templates.default_template import Default_Template
from controllers.mailing import Mailing
import pandas as pd
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class Core:
    def __init__(self, dbms, user=None, obj=None) -> None:
        self.dbms = dbms
        self.user = user
        self.defaults = None

    # DATA IMPORTATION
        
    def extract_data_importation_rows(self, doc):
        try:
            df = None
            file_path = utils.get_path_to_base_folder() + doc.file_url
            ext = file_path.split(".")[-1].lower()
            if ext == "csv":
                df = pd.read_csv(file_path)
            elif ext in ['xls', 'xlsx']:
                df = pd.read_excel(file_path, header=0, index_col=None)
            else:
                throw("You can only import data from Excel or CSV File!")
            rows = utils.normalize_import_data(df.to_dict(orient="records"), doc)
            return utils.respond(utils.ok, rows)
        except Exception as e:
            throw(f"Data Importation Failed: {e}")



    def start_data_importation(self, doc):
        from controllers.hooks import custom_imports
        mailing = Mailing(self.dbms)
        template = utils.from_dict_to_object()
        file_content = doc.file_content
        successful = []
        failed = []
        combined = []
        update = utils.from_dict_to_object(doc)
        update.status = "Importing"
        self.dbms.update("Data_Importation", update, privilege=True, update_submitted=True)
        user_id = None
        user = self.dbms.get_users(doc.owner, fetch_password=False)
        if user.status == utils.ok:
            user_id = user.data.id
        if custom_imports.get(doc.model):
            try:
                doc.owner_id = user_id
                result = custom_imports.get(doc.model)(self.dbms, utils.from_dict_to_object(doc), doc.get("model"))
            except Exception as e:
                print(custom_imports.get(doc.model).__name__, f"{e}")
                pass
        else:
            try:
                if file_content and len(file_content) > 0:
                    docstatus_info = self.dbms.get_doc("Doc_Status", doc.get("initial_status"),user=self.user, fetch_linked_tables=False)
                    for row in file_content:
                        status = "Active"
                        if docstatus_info.status == utils.ok:
                            ds = docstatus_info.data
                            row.status = ds.name
                            row.docstatus = ds.initial_docstatus
                            create = utils.from_dict_to_object()
                            try:
                                create = self.dbms.create(doc.model, utils.normalize_row_columns(row),self.user, fetch_linked_fields=False, fetch_linked_tables=False, owner_id=user_id)
                            except Exception as e:
                                error = utils.get_text_from_html_string(f"Failed to create data importation item: {str(e)}")
                                create.status = utils.unprocessable_entity
                                create.error_message = error
                                pp(error)
                            if create.status == utils.ok:
                                row.status = "Importation Successful"
                                row.error = "-"
                                successful.append(row)
                            else:
                                pp(create.error_message)
                                row.status = "Importation Failed"
                                row.error = utils.get_text_from_html_string(str(create.error_message))
                                failed.append(row)
                            combined.append(row)
                        if len(successful) == len(file_content):
                            status = "Importation Successful"
                        elif len(successful) > 0:
                            status = "Partially Imported"
                        else:
                            status = "Importation Failed"
                    update = doc
                    update.file_content = combined
                    update.total_successful = len(successful)
                    update.total_failed = len(failed)
                    update.successful_rows = successful
                    update.failed_rows = failed
                    update.status = status
                    updated = self.dbms.update("Data_Importation", update, privilege=True, update_submitted=True)
                    try:
                        doc.company = self.dbms.system_settings.linked_fields.default_company
                        template = Default_Template.data_importation(doc)
                    except Exception as e:
                        pass
                    if template:
                        mailing.send_mail(doc.owner,"Data Importation Concluded",template)
            except Exception as e:
                pp(f"An error occurred while importing data: {str(e)}")
            return utils.respond(utils.ok, "Importation Completed!")



    # USER MANAGEMENT
    def evaluate_user_permission_on_doctype(self, user, model, action):
        pass
         

    def get_user_default_dashboard(self, user_id):
        user = self.dbms.get_users(user_id)
        if user.get("status") == utils.ok:
            usr = user.get("data")
            main_role = usr.get("main_role")
            if not main_role:
                if usr.get("name") != tenant_admin.get("name"):
                    throw("Use does not have role assigned!")
                return utils.respond(utils.ok, {"dashboard":"Staff", "url":"/app/staff/staff_dashboard?app=staff_dashboard&module=staff&page=dashboard&content_type=Dashboard"})
            role_data = self.dbms.get_doc("Role", main_role, privilege=True, fetch_linked_fields=True)
            role_data.get("status") == utils.ok or throw(f"Failed to get user role: {role_data.get('error_message')}")
            role = utils.from_dict_to_object(role_data.get("data"))
            return utils.respond(
                utils.ok, 
                {
                    "dashboard": getattr(role.linked_fields.default_dashboard, "name", None), 
                    "url": getattr(role.linked_fields.default_dashboard,"url", None),
                    "module": getattr(role.linked_fields.default_dashboard, "module",None)
                }
            )
