from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion

dates = Dates ()
utils = Utils ()
pp = utils.pretty_print
throw = utils.throw
def check_memo (dbms, object):
    if not DataConversion.safe_get (object.body, "memo"):
        throw ("Memo is missing")

def commute_leave_days_save (dbms, object):
    core = Core_Hr(dbms, obj=object)
    leave_commutation = object.body
    hr_ss = core.get_company_settings (core.company)
    emp = core.get_doc ("Employee", object.body.employee)
    lt = DataConversion.safe_get (leave_commutation, "leave_type")
    total_days =  DataConversion.convert_to_float (DataConversion.safe_get (leave_commutation, "commutated_days", 0))
    leave_days = core.emp_leave_annual_days (DataConversion.safe_get (leave_commutation, 'employee',), leave_type=lt)
    remaining_days = DataConversion.convert_to_float (DataConversion.safe_get (leave_days, "remaining_days", 0))
    if remaining_days < total_days:
        throw ("You have <strong class='text-rose-600'>insufficient Leave Balance</strong>")
    if not emp:
        throw ("Failed To Process Unknown Employee")
    DataConversion.safe_set (object.body, "amount", DataConversion.convert_to_float (DataConversion.safe_get (emp, "basic_pay", 0)) / DataConversion.convert_to_int (DataConversion.safe_get (emp, "working_days", DataConversion.safe_get (hr_ss, "working_days", 22))) * DataConversion.convert_to_float(DataConversion.safe_get (object.body, "commutated_days",0)))

def commutation_memo (dbms, object):
    core = Core_Hr(dbms, obj=object)
    DataConversion.safe_set (object.body, "paid", "Unsettled")
    DataConversion.safe_set (object.body, "approved",  "Approved")
    DataConversion.safe_set (object.body, "commuted_on", dates.today ())
    leave_commutation = object.body
    lt = DataConversion.safe_get (leave_commutation, "leave_type")
    total_days =  DataConversion.convert_to_float (DataConversion.safe_get (leave_commutation, "commutated_days", 0))
    leave_days = core.emp_leave_annual_days (DataConversion.safe_get (leave_commutation, 'employee',), leave_type=lt)
    remaining_days = DataConversion.convert_to_float (DataConversion.safe_get (leave_days, "remaining_days", 0))
    if remaining_days < total_days:
        throw ("You have <strong class='text-rose-600'>insufficient Leave Balance</strong>")
    
    # r = dbms.update ("Leave_Commutation_Memo", object.body, update_submitted=True)
    # pp (r)
    # throw ("pppppp")

def commute_leave_days (dbms, object):
    core = Core_Hr(dbms, user=object.user, obj=object)
    core_payroll = Core_Payroll (dbms)

    leave_commutation = object.body
    lt = DataConversion.safe_get (leave_commutation, "leave_type")
    if not lt:
        throw ("Leave Type is required")
    memo = core.get_doc ("Leave_Commutation_Memo", DataConversion.safe_get (leave_commutation, "memo"))
    if not memo:
        throw ("Memo is missing")
    
    leave_days = core.emp_leave_annual_days (DataConversion.safe_get (leave_commutation, 'employee',), leave_type=lt)
    remaining_days = DataConversion.convert_to_float (DataConversion.safe_get (leave_days, "remaining_days", 0))
    total_days =  DataConversion.convert_to_float (DataConversion.safe_get (leave_commutation, "commutated_days", 0))
    if remaining_days < total_days:
        throw ("You have <strong class='text-rose-600'>insufficient Leave Balance</strong>")

    ent = utils.from_dict_to_object ()
    DataConversion.safe_set (ent, "is_active", 0)
    DataConversion.safe_set (ent, "employee", DataConversion.safe_get (leave_commutation, "employee"))
    DataConversion.safe_set (ent, "employee_name", DataConversion.safe_get (leave_commutation, "fullname"))
    DataConversion.safe_set (ent, "leave_type", lt)
    DataConversion.safe_set (ent, "entry_type", "Application")
    DataConversion.safe_set (ent, "cancel_reference", None)
    DataConversion.safe_set (ent, "used_leave_days", total_days)
    DataConversion.safe_set (ent, "remaining_leave_days", 0)
    DataConversion.safe_set (ent, "leave_days_in_working_hours", 0)
    DataConversion.safe_set (ent, "total_days", 0)
    DataConversion.safe_set (ent, "status", "Submitted")
    DataConversion.safe_set (ent, "docstatus", 1)
    DataConversion.safe_set (ent, "allocated_leave_days", 0)
    DataConversion.safe_set (ent, "from_date",dates.today ())
    DataConversion.safe_set (ent, "to_date", dates.add_days (dates.today (), DataConversion.safe_get (leave_commutation, "commutated_days", 0)))

    r = dbms.create ("Leave_Entry", ent)

    if r.status != utils.ok:
        return throw ("Failed to process leave Application")
    DataConversion.safe_set (memo, "approved", "Settled")
    r = dbms.update ("Leave_Commutation_Memo", memo, update_submitted=True)
    result = core_payroll.notify_payroll (
        employee_number=DataConversion.safe_get (memo, "employee"),
        amount=DataConversion.safe_get (memo, "amount"),
        doc_type="Leave_Commutation",
        doc_name=DataConversion.safe_get (memo, "name"),
        length_or_period=1,
        effective_date=dates.get_last_date_of_current_month (),
        sc="Leave Commutation",
        entry_type="Earning"
    )
    # pp (result)
    DataConversion.safe_set (object.body, "paid", "Unsettled")
    DataConversion.safe_set (object.body, "approved",  "Approved")
    DataConversion.safe_set (object.body, "commuted_on", dates.today ())