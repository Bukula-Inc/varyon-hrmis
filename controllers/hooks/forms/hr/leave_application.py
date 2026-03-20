from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion
from datetime import datetime
from controllers.utils  import Dates

dates = Dates ()
utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def milliseconds_to_hours (ms):
    total_hours = int (ms) / 3600000
    return round (total_hours, 2)
def doc_status_for_leave (dbms, object):
    object.doc_status = "Draft"

def leave_application_save (dbms, object):
    core_hr = Core_Hr (dbms)
    hr_ss = core_hr.get_company_settings (core_hr.company)
    main_leave = DataConversion.safe_get (hr_ss, "main_leave", "Annual Leave")

    app = DataConversion.safe_get (object, "body", utils.from_dict_to_object ())
    # from_date = DataConversion.safe_get (app, "from_date")
    app_lt = DataConversion.safe_get (app, 'leave_type', '')
    leave_settings = utils.array_to_dict (DataConversion.safe_get (hr_ss, 'leave_settings', []), "leave_type")
    lt =  DataConversion.safe_get (leave_settings, app_lt)

    leave_applied = DataConversion.convert_to_float (DataConversion.safe_get (app, "total_days", 0))
    ltc = core_hr.get_doc ("Leave_Type", app_lt)
    emp = core_hr.get_doc ("Employee", object.body.employee)

    apply_on = DataConversion.safe_get (ltc, "apply_on", '')
    emp_gender = DataConversion.safe_get (emp, "gender", '')

    if leave_applied == 0:
        throw ("You can't <strong class='text-rose-600'>Apply for 0 days</strong>")
    if not apply_on:
        apply_on = "Both"
    if apply_on != "Both" and apply_on != emp_gender:
        throw (f"<strong class='text-rose-600'>{app_lt}</strong> is for <strong class='text-rose-600'>{apply_on}'s</strong> and not <strong class='text-rose-600'>{emp_gender}'s</strong>")
    if not emp:
        throw ("Cannot Process With <strong class='text-rose-600'>Applicant Of Leave</strong>")
    object.body.employee_name = emp.full_name or f"{emp.first_name} {emp.middle_name or ''} {emp.last_name}"
    if not object.body.department:
        if not emp.department:
            throw ("Employee Has No Department Which Will Affect The Approval Process")
        object.body.department = emp.department

    if DataConversion.safe_get (emp, "inable_probation", None) and not DataConversion.safe_get (app, "is_on_probation", None):
        throw (f"You are On Probation You Cannot Apply for <strong class='text-rose-600'>{DataConversion.safe_get (app, 'leave_type')}</strong>")
    if not ltc:
        throw ("<strong class='text-rose-600'>Unknown Leave type</strong>")

    ls = core_hr.get_list ("Leave_Schedule", {"department": DataConversion.safe_get (object.body, "department"), "is_active": 1, "leave_type": lt}, limit=1)
    if not ls:
        throw (f"Leave Schedule '{DataConversion.safe_get (object.body, 'department')}' Not found, Setup Leave Schedule for the department")
    lst_scheduled_emp = ls[0] if len (ls) > 0 else {}
    scheduled_emp_dict = utils.array_to_dict (DataConversion.safe_get (lst_scheduled_emp, "leave_information", []), "employee")
    scheduled_emp = DataConversion.safe_get (scheduled_emp_dict, DataConversion.safe_get (emp, "name"))
    from_dt = DataConversion.safe_get (scheduled_emp, "from_date")
    to_dt = DataConversion.safe_get (scheduled_emp, "to_date")
    if DataConversion.safe_le (DataConversion.safe_get (app, "from_date"), from_dt, datetime):
        throw ("Your Leave Application Schedule is not yet ready")
 
    mcd = DataConversion.convert_to_float (DataConversion.safe_get (ltc, "maximum_leave_allocated", 0))
    if mcd < leave_applied:
        throw ("Days Applied For Are Higher than <strong class='text-rose-600'>Maximum Consecutive Days</strong>")
    if lt or app_lt == main_leave:
        days = core_hr.emp_leave_annual_days (emp.name, leave_type=main_leave)
        rd = DataConversion.convert_to_float (DataConversion.safe_get (days, "remaining_days", 0))
        if (rd - leave_applied) < 0:
            throw ("You do not have <strong class='text-rose-600'>enough days</strong>")

        clb = DataConversion.convert_to_float (DataConversion.safe_get (days, "remaining_days", 0))
        if clb == 0:
            throw ("<strong class='text-rose-600'>You Have No Leave Balance<strong>")
        if clb < leave_applied:
            throw ("You Don't Have <strong class='text-rose-600'>Enough Leave Days </strong>")
        if object.body.leave_mode == "Days Leave":
            from_data = datetime.strptime(object.body.from_date, "%Y-%m-%d") if isinstance(object.body.from_date, str) else object.body.from_date
            to_data = datetime.strptime(object.body.to_date, "%Y-%m-%d") if isinstance(object.body.to_date, str) else object.body.to_date

            if from_data > to_data:
                throw ("Cannot Process <strong class='text-rose-600'>From Date Is Greater Than To Date</strong>")
        else:
            from_time = datetime.strptime(from_time, "%H:%M").time()
            to_time = datetime.strptime(to_time, "%H:%M").time()
            if to_time > from_time:
                throw ("Cannot Process <strong class='text-rose-600'>From Time Is Greater Than To Time</strong>")
        if not object.body.leave_handover_file and (object.body.leave_plan_tasks and len (object.body.leave_plan_tasks) <= 0):
            throw ("Cannot Process No handover Notes where Attached Please Attach Handover Notes")

    object.body.approved = 0

def leave_entry_updating(dbms, object):
    is_ok = False
    core = Core_Hr(dbms)
    core_payroll = Core_Payroll (dbms)
    application = object.body
    hr_ss = core.get_company_settings (core.company)
    working_hours = DataConversion.safe_get (hr_ss, 'working_hrs', 8)
    main_leave = DataConversion.safe_get (hr_ss, "main_leave", None)
    app_lt = DataConversion.safe_get (application, 'leave_type', '')
    leave_settings = utils.array_to_dict (DataConversion.safe_get (hr_ss, 'leave_settings', []), "leave_type")
    total_days = DataConversion.convert_to_float (DataConversion.safe_get(application, 'total_days', 0))
    lt =  DataConversion.safe_get (leave_settings, DataConversion.safe_get (application, 'leave_type', ''), None)
    emp = core.get_doc ("Employee", DataConversion.safe_get (application, "employee", None))
    leave_mode = str (DataConversion.safe_get (application, "leave_mode", "Days Leave")).lower ()
    if not emp:
        throw ("<strong class='text-rose-600'>Employee Not Found!</strong>")
    if lt or app_lt == main_leave:
        leave_days = core.emp_leave_annual_days (DataConversion.safe_get (application, 'employee', None), leave_type=main_leave)
        if not lt:
            main_leave = DataConversion.safe_get (application, "leave_type", None)
        if leave_mode == "hourly leave":
            total_days = core.to_and_from_hours_to_days (total_days, working_hours=working_hours, return_type="days")
        if main_leave:
            remaining_days = DataConversion.safe_get (leave_days, "remaining_days", 0)
            if remaining_days < total_days:
                throw ("You have <strong class='text-rose-600'>insufficient Leave Balance</strong>")
            ent = utils.from_dict_to_object ()
            DataConversion.safe_set (ent, "is_active", 0)
            DataConversion.safe_set (ent, "employee", DataConversion.safe_get (emp, "name"))
            DataConversion.safe_set (ent, "employee_name", DataConversion.safe_get (emp, "full_name",
                f"{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}"
            ))
            DataConversion.safe_set (ent, "leave_type", app_lt)
            DataConversion.safe_set (ent, "entry_type", "Application")
            DataConversion.safe_set (ent, "cancel_reference", DataConversion.safe_get (application, "name"))
            DataConversion.safe_set (ent, "used_leave_days", total_days)
            DataConversion.safe_set (ent, "remaining_leave_days", 0)
            DataConversion.safe_set (ent, "leave_days_in_working_hours", 0)
            DataConversion.safe_set (ent, "total_days", 0)
            DataConversion.safe_set (ent, "status", "Submitted")
            DataConversion.safe_set (ent, "docstatus", 1)
            DataConversion.safe_set (ent, "allocated_leave_days", 0)
            DataConversion.safe_set (ent, "from_date", DataConversion.safe_get (application, 'from_date', ''))
            DataConversion.safe_set (ent, "to_date", DataConversion.safe_get (application, 'to_date', ''))

            r = dbms.create ("Leave_Entry", ent)
            is_ok = True
        else:
            throw ("<strong class='text-rose-600'>Unknown Leave Type</strong>")
    else:
        lt = core.get_doc ("Leave_Type", app_lt)
        if not lt:
            throw ("<strong class='text-rose-600'>Unknown Leave Type</strong>")
        leave_days = core.emp_leave_annual_days (DataConversion.safe_get (application, 'employee', None), leave_type=app_lt)

        total_days_allocated_per_month = DataConversion.convert_to_float (DataConversion.safe_get (lt, "total_days_allocated_per_month", 0))
        maximum_leave_allocated = DataConversion.convert_to_float (DataConversion.safe_get (lt, "maximum_leave_allocated", 0))
        leave_type_year = DataConversion.safe_get (lt, "leave_type_year", "Calendar Year")
        first_day_of_the_year = dates.get_first_date_of_current_year ()
        last_day_of_the_year = dates.get_last_date_of_current_year ()
       
        if maximum_leave_allocated < total_days:
            throw ("Days Applied For Are Higher than <strong class='text-rose-600'>Maximum Consecutive Days</strong>")
        if leave_type_year == "Calendar Year":
            first_day_of_the_year = DataConversion.map_to_current_year (DataConversion.safe_get(emp, "date_of_joining", dates.today ()))
            last_day_of_the_year = dates.add_days (first_day_of_the_year, 364)

        get_entries = core.get_list ("Leave_Entry", filters={
            "employee": DataConversion.safe_get (application, "employee", None),
            "leave_type": app_lt,
            "from_date": first_day_of_the_year,
            "to_date": last_day_of_the_year,
        })
        active_entry = None
        entries_dict = utils.array_to_dict (get_entries, "entry_type")
        if "Allocation" in entries_dict:
            active_entry = DataConversion.safe_get (entries_dict, "Allocation", None)
        
        ent = utils.from_dict_to_object ()
        
        DataConversion.safe_set (ent, "is_active", 0)
        DataConversion.safe_set (ent, "employee", DataConversion.safe_get (emp, "name"))
        DataConversion.safe_set (ent, "employee_name", DataConversion.safe_get (emp, "full_name",
            f"{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}"
        ))
        DataConversion.safe_set (ent, "leave_type", app_lt)

        if not active_entry:
            DataConversion.safe_set (ent, "entry_type", "Allocation")
            DataConversion.safe_set (ent, "used_leave_days", 0)
            DataConversion.safe_set (ent, "remaining_leave_days", total_days_allocated_per_month)
            DataConversion.safe_set (ent, "leave_days_in_working_hours", core.to_and_from_hours_to_days (DataConversion.safe_get (ent, "remaining_leave_days"), working_hours=working_hours,))
            DataConversion.safe_set (ent, "total_days", total_days_allocated_per_month)    
            DataConversion.safe_set (ent, "from_date", first_day_of_the_year)    
            DataConversion.safe_set (ent, "to_date", last_day_of_the_year)
            DataConversion.safe_set (ent, "status", "Submitted")
            DataConversion.safe_set (ent, "docstatus", 1)
            DataConversion.safe_set (ent, "allocated_leave_days", total_days_allocated_per_month) 
            dbms.create ("Leave_Entry", ent)

        else:
            if DataConversion.safe_get (leave_days, "remaining_days", 0) < total_days:
                throw ("You have <strong class='text-rose-600'>insufficient Leave Balance</strong>")
        
        DataConversion.safe_set (ent, "entry_type", "Application")
        DataConversion.safe_set (ent, "cancel_reference", DataConversion.safe_get (application, "name"))
        DataConversion.safe_set (ent, "used_leave_days", total_days)
        DataConversion.safe_set (ent, "remaining_leave_days", 0)
        DataConversion.safe_set (ent, "leave_days_in_working_hours", 0)
        DataConversion.safe_set (ent, "total_days", 0)
        DataConversion.safe_set (ent, "status", "Submitted")
        DataConversion.safe_set (ent, "docstatus", 1)
        DataConversion.safe_set (ent, "allocated_leave_days", 0)
        DataConversion.safe_set (ent, "from_date", DataConversion.safe_get (application, 'from_date', ''))
        DataConversion.safe_set (ent, "to_date", DataConversion.safe_get (application, 'to_date', ''))
        
        r = dbms.create ("Leave_Entry", ent)
        if r.status == utils.ok:

            is_ok = True

    if DataConversion.is_today (DataConversion.safe_get (application, "from_date", None)):
        emp.status = "On Leave"
        dbms.update ("Employee", emp, update_submitted=True)

    object.body.approved = 1

    if not is_ok:
        throw ("<strong class='text-rose-600'>Leave Application Failed</strong>")
    if DataConversion.safe_e (app_lt, "annual leave", str, True):
        lb = core_payroll.get_doc ("Allowance_and_Benefit", "Leave Benefits")
        if lb:
            lb_grade = DataConversion.safe_get (lb, "categories", [])
            cats_dict = utils.array_to_dict (lb_grade, "salary_grade")
            if cats_dict:
                grade = DataConversion.safe_get (emp, "employee_grade")
                lb_info = DataConversion.safe_get (cats_dict, grade, {})
                amount = DataConversion.convert_to_float (DataConversion.safe_get (lb_info, "amount", 0))

                if amount:
                    r = core_payroll.notify_payroll (
                        DataConversion.safe_get (emp, "name"),
                        amount,
                        "Leave Benefits",
                        "Leave_Application",
                        DataConversion.safe_get (application, "name"),
                        entry_type="Earning"                   
                    )
            
def leave_application_cancel (dbms, object):
    throw ("<strong class='text-orange-600'>Leave Cancellation is Not Yet Enable</strong>")

def leave_schedule_validate (dbms, object):
    core_hr = Core_Hr (dbms)
    ls = DataConversion.safe_get (object, "body")
    planner = DataConversion.safe_get (ls, "planner",)
    department = DataConversion.safe_get (ls, "department",)
    leave_type = DataConversion.safe_get (ls, "leave_type",)
    start_date = DataConversion.safe_get (ls, "start_date",)
    end_date = DataConversion.safe_get (ls, "end_date",)
    leave_information = DataConversion.safe_get (ls, "leave_information", [])
    department_days = DataConversion.convert_to_float (DataConversion.safe_get (ls, "department_days",0))
    days = DataConversion.convert_to_float (DataConversion.safe_get (ls, "days",0))

    if not planner:
        throw ("Please Select <strong class='text-rose-600'>Planner</strong>")
    if not department:
        throw ("Please Select <strong class='text-rose-600'>Department</strong>")
    if not leave_type:
        throw ("Please Select <strong class='text-rose-600'>Leave Type</strong>")
    if not start_date:
        throw ("Please Select <strong class='text-rose-600'>Start Date</strong>")
    if not end_date:
        throw ("Please Select <strong class='text-rose-600'>End Date</strong>")
    if DataConversion.safe_lt (end_date, start_date, datetime):
        throw ("<strong class='text-rose-600'>End Date Cannot Be Less Than Start Date</strong>")
    if days <= 0:
        throw ("<strong class='text-rose-600'>Days Must Be Greater Than 0</strong>")
    if department_days <= 0:
        throw ("<strong class='text-rose-600'>Department Days Must Be Greater Than 0</strong>")
    if days > department_days:
        throw ("<strong class='text-rose-600'>Days Planed For Usage Cannot Be Greater Than Total Department Days</strong>")
    emp = core_hr.get_doc ("Employee", planner)
    if not emp:
        throw ("<strong class='text-rose-600'>Unknown Planner</strong>")
    
    department_emp = core_hr.get_list ("Employee", filters={"department": department})
    if len (department_emp) <= 0:
        throw (f"<strong class='text-rose-600'>No Employees Found In {department} Department</strong>")
    if len (leave_information) <= 0:
        throw ("<strong class='text-rose-600'>No Employees Found In Leave Schedule Information Table</strong>")
    total_days = 0
    for li in leave_information:
        emp_id = DataConversion.safe_get (li, "employee")
        days_planned_for = DataConversion.convert_to_float (DataConversion.safe_get (li, "total_days_to_used", 0))
        emp_id = DataConversion.safe_get (li, "employee")
        lds = core_hr.emp_leave_annual_days (emp_id, leave_type=leave_type)
        rd = DataConversion.convert_to_float (DataConversion.safe_get (lds, "remaining_days", 0))
        if days_planned_for > rd:
            throw (f"<strong class='text-rose-600'>{DataConversion.safe_get (li, 'employee_name', emp_id)} Has Insufficient Leave Balance</strong>")
        total_days += days_planned_for
    if total_days > department_days:
        throw (f"<strong class='text-rose-600'>Total Days Planned For Usage {total_days} Exceeds Total Department Days {department_days}</strong>")


def on_save_leave_schedule (dbms, object):
    leave_schedule_validate (dbms, object)
    core_hr = Core_Hr (dbms)
    ls = DataConversion.safe_get (object, "body")
    planner = DataConversion.safe_get (ls, "planner",)
    emp = core_hr.get_doc ("Employee", planner)
    DataConversion.safe_set (object.body, "planner_full_names", DataConversion.safe_get (emp, "full_name", f"{DataConversion.safe_get (emp, 'first_name',)} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name',)}"))

def on_update_leave_schedule (dbms, object):
    leave_schedule_validate (dbms, object)

def on_submit_leave_schedule (dbms, object):
    leave_schedule_validate (dbms, object)
    core_hr = Core_Hr (dbms)
    DataConversion.safe_set (object.body, "is_active", 1)
    ls = DataConversion.safe_get (object, "body")
    curr_ls = core_hr.get_list ("Leave_Schedule", filters={
        "department": DataConversion.safe_get (ls, "department",),
        "leave_type": DataConversion.safe_get (ls, "leave_type",),
        "is_active": 1,
    }, limit=1)

    if len (curr_ls) > 0:
        curr_ls = curr_ls[0]
        DataConversion.safe_set (curr_ls, "is_active", 0)
        dbms.update ("Leave_Schedule", curr_ls, update_submitted=True)
    DataConversion.safe_set (object.body, "is_active", 1)