import pandas as pd
import re
import json
from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr

utils = Utils()
pp = utils.pretty_print
throw = utils.throw
dates = Dates ()

def import_script_for_leave_application (dbms, doc, doctype):
    success = []
    failed = []
    core_hr = Core_Hr (dbms=dbms)
    extract_leave_application = doc.file_content
    extract_leave_application = [utils.normalize_row_columns(row) for row in extract_leave_application]
    employees = utils.array_to_dict (core_hr.get_list ("Employee", filters={"status__in": ["Suspended", "Active", "On Leave"]}), "name")

    for leave_application in extract_leave_application:
        id = DataConversion.safe_get (leave_application, "employee_id")
        lt = DataConversion.safe_get (leave_application, "leave_type", "Annual Leave")
        total_days = DataConversion.safe_get (leave_application, "days", 0)
        from_date = DataConversion.safe_get (leave_application, "from_date", dates.today ())

        if not id:
            DataConversion.safe_set (leave_application, "error", f"Employee ID {id} is Missing")
            DataConversion.safe_set (leave_application, "status", "Importation Failed")
            failed.append(leave_application)
        else:
            emp = DataConversion.safe_get (employees, id)
            if not emp:
                DataConversion.safe_set (leave_application, "error", f"Employee With Employee ID {id} Not Found")
                DataConversion.safe_set (leave_application, "status", "Importation Failed")
                failed.append(leave_application)
            else:
                ent = utils.from_dict_to_object ()
                DataConversion.safe_set (ent, "is_active", 0)
                DataConversion.safe_set (ent, "employee", DataConversion.safe_get (emp, "name"))
                DataConversion.safe_set (ent, "employee_name", DataConversion.safe_get (emp, "full_name",
                    f"""{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}"""
                ))
                DataConversion.safe_set (ent, "leave_type", lt)
                DataConversion.safe_set (ent, "entry_type", "Application")
                # DataConversion.safe_set (ent, "cancel_reference", DataConversion.safe_get (doc, "name"))
                DataConversion.safe_set (ent, "used_leave_days", total_days)
                DataConversion.safe_set (ent, "remaining_leave_days", 0)
                DataConversion.safe_set (ent, "leave_days_in_working_hours", 0)
                DataConversion.safe_set (ent, "total_days", 0)
                DataConversion.safe_set (ent, "status", "Submitted")
                DataConversion.safe_set (ent, "docstatus", 1)
                DataConversion.safe_set (ent, "allocated_leave_days", 0)
                DataConversion.safe_set (ent, "to_date", dates.add_days (from_date, total_days))
                pp (ent)
                create_application = dbms.create ("Leave_Entry", ent, dbms.validation.user,  submit_after_create=True)
                pp (create_application)

                if create_application.status == utils.ok:
                    DataConversion.safe_set (leave_application, "error", " - ")
                    DataConversion.safe_set (leave_application, "status", "Importation Successful")
                    success.append(leave_application)
                else:
                    DataConversion.safe_set (leave_application, "error", create_application.error_message)
                    DataConversion.safe_set (leave_application, "status", "Importation Failed")
                    failed.append(leave_application)

    doc.file_content = [*success, *failed]
    if failed and len(failed) > 0 and success and len(success) > 0:
        doc.status = "Partially Imported"
        doc.doc_status = "Partially Imported"
    elif len(failed) > 0 and len(success) == 0:
        doc.status = "Importation Failed"
        doc.doc_status = "Importation Failed"
    elif len(failed) == 0 and len(success) > 0:
        doc.status = "Importation Successful"
        doc.doc_status = "Importation Successful"
    update = dbms.update("Data_Importation", doc, dbms.current_user_id, update_submitted=True)
    return utils.respond(utils.ok, {"successful": success, "failed": failed})