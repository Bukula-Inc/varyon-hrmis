import pandas as pd
import re
import json
from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr

utils = Utils()
pp = utils.pretty_print
throw = utils.throw
dates = Dates ()

def import_script_for_leave_allocation (dbms, doc, doctype):
    success = []
    failed = []
    core_hr = Core_Hr (dbms=dbms)
    hr_ss = core_hr.get_company_settings (core_hr.company)
    if hr_ss:
        working_hours = hr_ss.get ("working_hrs", None) if hr_ss.get ("working_hrs", None) else 8
    else:
        working_hours = 8
    extract_leave_allocation = doc.file_content
    extract_leave_allocation = [utils.normalize_row_columns(row) for row in extract_leave_allocation]

    for leave_allocation in extract_leave_allocation:
        employee = None
        days = 0
        if leave_allocation.get('id', None):
            employee_ = core_hr.get_doc ("Employee", leave_allocation.get('id', None))
            if employee_:
                employee = employee_
        elif leave_allocation.get ('name', None):
            employee_ = core_hr.get_doc ("Employee", leave_allocation.get ('name', None))
            if employee_:
                employee = employee_
        if leave_allocation.get ('total_days', None):
            days = int (leave_allocation.get ('total_days', 0))
        if leave_allocation.get ('days', None):
            days = int (leave_allocation.get ('days', 0))
        if employee:
            leave_allocation_employees = utils.from_dict_to_object ({
                "employee_name": employee.full_name if employee.full_name else f"{employee.first_name} {employee.middle or ''} {employee.last_name}",
                "employee": employee.name,
                "leave_type": utils.capitalize (leave_allocation.get('leave_type', "Annual Leave")),
                "total_days": days,
                "allocated_leave_days": days,
                "remaining_leave_days": days,
                "used_leave_days": 0,
                "from_date": dates.get_first_date_of_current_month (),
                "to_date": dates.get_last_date_of_current_month (),
                "leave_days_in_working_hours": core_hr.to_and_from_hours_to_days (float (days), float (working_hours)),
                "is_active": 1,
                "entry_type": "Allocation",
            })
            leave_allocation_employees.status = "Active"
            create_allocation = dbms.create ("Leave_Entry", utils.from_dict_to_object (leave_allocation_employees), dbms.validation.user,  submit_after_create=True)
            if create_allocation.status == utils.ok:
                leave_allocation["error"] = " - "
                leave_allocation["status"] = "Importation Successful"
                success.append(leave_allocation)
            else:
                leave_allocation["error"] = create_allocation.error_message
                leave_allocation["status"] = "Importation Failed"
                failed.append(leave_allocation)
        else:
            leave_allocation["error"] = f"Employee With {leave_allocation.get('id', None) or leave_allocation.get('name', None)} Was Not Found"
            leave_allocation["status"] = "Importation Failed"
            failed.append(leave_allocation)

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