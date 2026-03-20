from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

def before_allocation_save (dbms, object):
    object.doc_status = "Draft"
    if len(object.body.leave_allocation_employees) <= 0:
        throw(f"No allocation was done. Please have the Employee table filled.")

def create_leave_entry(dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    employees = utils.array_to_dict(core_hr.fetch_data_from_sql ("SELECT name, full_name, first_name, last_name, middle_name FROM employee"), "name")
    hr_ss = core_hr.get_company_settings (core_hr.company)
    working_hours = hr_ss.get("working_hrs", None) if hr_ss else 8
    leave_allocation =object.body
    employees_to_allocate_leave = leave_allocation.leave_allocation_employees or []
    for allocated_leave in employees_to_allocate_leave:
        emp = DataConversion.safe_get (employees, DataConversion.safe_get (allocated_leave, 'employee'))
        if emp:
            emp_name = DataConversion.safe_get (emp, 'full_name', f"""{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}""")
            days_allocated = DataConversion.convert_to_float(DataConversion.safe_get (allocated_leave, "total_leaves_allocated", 0.00))
            try:
                new_entry = utils.from_dict_to_object ()
                DataConversion.safe_set (new_entry, "allocated_leave_days", days_allocated)
                DataConversion.safe_set (new_entry, "used_leave_days", 0)
                DataConversion.safe_set (new_entry, "total_days", days_allocated)
                DataConversion.safe_set (new_entry, "remaining_leave_days", days_allocated)
                DataConversion.safe_set (new_entry, "leave_type", "Annual Leave")
                DataConversion.safe_set (new_entry, "status", "Submitted")
                DataConversion.safe_set (new_entry, "is_active", 1)
                DataConversion.safe_set (new_entry, "employee", DataConversion.safe_get (emp, "name"))
                DataConversion.safe_set (new_entry, "employee_name", emp_name)
                DataConversion.safe_set (new_entry, "from_date", dates.get_first_date_of_current_month ())
                DataConversion.safe_set (new_entry, "to_date", dates.get_first_date_of_current_month ())
                DataConversion.safe_set (new_entry, "entry_type", "Allocation")
                DataConversion.safe_set (new_entry, "reference", DataConversion.safe_get(allocated_leave, "name"))
                DataConversion.safe_set (new_entry, "leave_days_in_working_hours",
                    core_hr.to_and_from_hours_to_days (DataConversion.safe_get(new_entry, "remaining_leave_days", 0),
                        working_hours=DataConversion.convert_to_float(working_hours))
                )
                r = dbms.create ("Leave_Entry", new_entry)
                pp (r)
            except Exception as e:
                pp (f"ERROR: {e}")
                pass

def leave_allocation_cancel(dbms, object):
    core_hr = Core_Hr (dbms)
    leave_allocation = object.body
    get_entry = core_hr.get_list ("Leave_Entry", filters={"reference": leave_allocation.name, "is_active": 1}, limit=1)
    if not get_entry:
        throw ("No Leave Entry Associated With Allocation")
    entry = get_entry[0]
    entry.status = "Cancelled"
    dbms.update ("Leave_Entry", entry, update_submitted=True)