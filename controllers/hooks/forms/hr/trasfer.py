from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion

utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

def validate_transfer (dbms, object):
    core_hr = Core_Hr (dbms)
    obj = DataConversion.safe_get (object, "body")
    if not DataConversion.safe_get (obj, "transfer_date"):
        DataConversion.safe_set (object.body, "transfer_date", dates.today ())
    emp_id = DataConversion.safe_get (obj, "employee")
    initiator = core_hr.get_doc ("Employee", emp_id)
    if not emp_id or not initiator:
        initiator = core_hr.get_user_as_employee ()
        if not initiator:
            throw (f"<b class='text-rose-600'>To Initiate Employee Transfer You Must Be Linked to an Employee in The system</b>")
    DataConversion.safe_set (object.body, "employee_name", DataConversion.safe_get (initiator, "full_name", f"""{DataConversion.safe_get (initiator, 'first_name')} {DataConversion.safe_get (initiator, 'middle_name', '')} {DataConversion.safe_get (initiator, 'last_name')}"""))
    DataConversion.safe_set (object.body, "department", DataConversion.safe_get (initiator, "department"))
    DataConversion.safe_set (object.body, "designation", DataConversion.safe_get (initiator, "designation"))
    DataConversion.safe_set (object.body, "employee", DataConversion.safe_get (initiator, "name"))

    transfer_employee = DataConversion.safe_get (obj, "transfer_employee")
    if not transfer_employee:
        throw (f"<b class='text-rose-600'>Transfer Employee is Required! </b>")
    transfer_employee_obj = core_hr.get_doc ("Employee", transfer_employee)
    
    DataConversion.safe_set (object.body, "transfer_employee", DataConversion.safe_get (transfer_employee_obj, "name"))
    DataConversion.safe_set (object.body, "transfer_employee_name", DataConversion.safe_get (transfer_employee_obj, "full_name", f"""{DataConversion.safe_get (transfer_employee_obj, 'first_name')} {DataConversion.safe_get (transfer_employee_obj, 'middle_name', '')} {DataConversion.safe_get (transfer_employee_obj, 'last_name')}"""))
    DataConversion.safe_set (object.body, "transfer_employee_department", DataConversion.safe_get (transfer_employee_obj, "department"))
    DataConversion.safe_set (object.body, "transfer_employee_designation", DataConversion.safe_get (transfer_employee_obj, "designation"))
    DataConversion.safe_set (object.body, "basic_pay", DataConversion.safe_get (transfer_employee_obj, "basic_pay"))
    DataConversion.safe_set (object.body, "from_location", DataConversion.safe_get (transfer_employee_obj, "branch"))

    if not DataConversion.safe_get (obj, "new_location"):
        throw (f"<b class='text-rose-600'>New Location is Required! </b>")
    if not DataConversion.safe_get (obj, "pay_settling_in_allowance"):
        DataConversion.safe_set (object.body, "pay_settling_in_allowance", 0)

def on_save_of_employee_memo (dbms, object):
    validate_transfer (dbms, object)

def on_submit_of_employee_memo (dbms, object):
    validate_transfer (dbms, object)
    cp = Core_Payroll (dbms)
    emp = DataConversion.safe_get(object.body, "transfer_employee")
    emp_info = cp.get_doc ("Employee", emp)
    DataConversion.safe_set (emp_info, "branch", DataConversion.safe_get (object.body, "new_location"))
    if DataConversion.safe_get (object.body, "pay_settling_in_allowance", 0):
        r = cp.notify_payroll (
            emp,
            DataConversion.convert_to_float (DataConversion.safe_get (object.body, "basic_pay")),
            entry_type="Earning",
            sc="Settling In Allowance",
            doc_type="Employee_Transfer_Memo",
            doc_name=DataConversion.safe_get (object.body, "name"),
        )

        pp (r)
    dbms.update ("Employee", emp_info, update_submitted=True)
