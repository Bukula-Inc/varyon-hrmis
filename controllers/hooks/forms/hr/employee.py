from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()

throw = utils.throw
pp = utils.pretty_print

def before_employee_update (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    middle_name = object.body.middle_name if object.body.middle_name else ""
    object.body.full_name = f"{object.body.first_name} {middle_name} {object.body.last_name}"
    # get basic pay
    emp = core_hr.get_doc ("Employee", object.body.name)
    object.body.basic_pay = emp.basic_pay
    


def before_employee_save(dbms, object):
    if DataConversion.safe_e (DataConversion.safe_get (object.body, "create_user"), "Create User", str, True):
        DataConversion.safe_set (object.body, "create_user", "Link User")
    if DataConversion.safe_e (DataConversion.safe_get (object.body, "inable_probation", 0), 1, int) and DataConversion.safe_get (object.body, "probation"):
        DataConversion.safe_set (object.body, "status", "Probation")
        DataConversion.safe_set (object, "doc_status", "Probation")
    if not DataConversion.safe_get (object.body, "full_name"):
        DataConversion.safe_set (object.body, "full_name", f"{DataConversion.safe_get(object.body, 'first_name')} {DataConversion.safe_get(object.body, 'middle_name', '')} {DataConversion.safe_get(object.body, 'last_name')}")

    if not DataConversion.safe_get (object.body, "basic_pay", 0):
        throw ("Basic Pay is <b class='text-rose-600'>Required!</b>")

def after_employee_save(dbms, object, result):
    core_hr = Core_Hr (dbms)

    due_date =None
    
    if DataConversion.safe_e (DataConversion.safe_get (result, "inable_probation", 0), 1, int) and DataConversion.safe_get (result, "probation"):
        fetch_probation_list = core_hr.get_doc("Probation", DataConversion.safe_get (result, "probation"))
        if fetch_probation_list:
            jd = DataConversion.convert_datetime_to_string (DataConversion.safe_get (result, "date_of_joining"), "%Y-%m-%d")
            due_date =dates.add_days (jd, (30 * DataConversion.convert_to_float (DataConversion.safe_get (fetch_probation_list, "probation_length", 0))))
            add_to_probation_list = utils.from_dict_to_object()
            DataConversion.safe_set (add_to_probation_list, "employee", DataConversion.safe_get (result, "name"))
            DataConversion.safe_set (add_to_probation_list, "start_date", DataConversion.safe_get (result, "date_of_joining"))
            DataConversion.safe_set (add_to_probation_list, "due_date", due_date)
            DataConversion.safe_set (add_to_probation_list, "probation_status", 1)
            add_to_list =dbms.create("Probation_List", add_to_probation_list)

            if add_to_list.status == utils.ok:
                pp("Added To Probation List")
            else:
                pp(f"Failed To Added To Probation List. \n {add_to_list.error_message}")
    
    cp = Core_Payroll (dbms)

    DataConversion.safe_set (object.body, "employee_saved", 2)
    DataConversion.safe_set (object, "doc_status", "Active")
    DataConversion.safe_set (object.body, "status", "Active")
    DataConversion.safe_set (object.body, "docstatus", 0)

    r = cp.notify_payroll (
        DataConversion.safe_get(object.body, "name"),
        DataConversion.convert_to_float (DataConversion.safe_get (object.body, "basic_pay")),
        entry_type="Earning",
        sc="Settling In Allowance",
        doc_type="Employee",
        doc_name=DataConversion.safe_get (object.body, "name"),
    )

    pp (r)

def before_employee_submit(dbms, object):
    cp = Core_Payroll (dbms)

    DataConversion.safe_set (object.body, "employee_saved", 2)
    DataConversion.safe_set (object, "doc_status", "Active")
    DataConversion.safe_set (object.body, "status", "Active")
    DataConversion.safe_set (object.body, "docstatus", 0)

    r = cp.notify_payroll (
        DataConversion.safe_get(object.body, "name"),
        DataConversion.convert_to_float (DataConversion.safe_get (object.body, "basic_pay")),
        entry_type="Earning",
        sc="Settling In Allowance",
        doc_type="Employee",
        doc_name=DataConversion.safe_get (object.body, "name"),
    )