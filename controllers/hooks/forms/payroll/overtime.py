from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.payroll import Core_Payroll

utils = Utils ()
dates = Dates ()
throw = utils.throw
pp = utils.pretty_print

def overtime_pending(dbms, object):
    object.body.status = "Pending"

def overtime_draft(dbms, object):
    object.body.status = "Draft"
 
def validate_ot (dbms, object):
    ot = DataConversion.safe_get (object, "body", {})
    staff_to_work_on_overtime = DataConversion.safe_get (ot, "staff_to_work_on_overtime", [])
    if len (staff_to_work_on_overtime) < 0:
        throw ("Appointed Staff Members are <strong class='text-rose-500'>Require</strong>")
    
    list_to_save = []
    for i, staff_row in enumerate (staff_to_work_on_overtime):
        if not DataConversion.safe_get (staff_row, "employee"):
            throw (f"Staff No is <strong class='text-rose-500'>Missing</strong> on Row ({i+1})")
        DataConversion.safe_set (staff_row, "name", f"""{DataConversion.safe_get (staff_row, 'employee')} {DataConversion.safe_get (object.body, 'name')}""")
        DataConversion.safe_set (staff_row, "date_of_work", DataConversion.safe_get (object.body, "to_date"))
        DataConversion.safe_set (staff_row, "cleared", 0)
        DataConversion.safe_set (staff_row, "from_date", DataConversion.safe_get (ot, "from_date"))
        DataConversion.safe_set (staff_row, "to_date", DataConversion.safe_get (ot, "to_date"))
        DataConversion.safe_list_append (list_to_save, staff_row)
    
    if not utils.get_text_from_html_string (DataConversion.safe_get (ot, "why_working_hours")):
        throw ("Reason for not working during working days is <strong class='text-rose-500'>Require</strong>")
    if not utils.get_text_from_html_string (DataConversion.safe_get (ot, "purpose")):
        throw ("details of Work is <strong class='text-rose-500'>Require</strong>")
    if not DataConversion.safe_get (ot, "applicant"):
        throw ("Applicant is <strong class='text-rose-500'>Require</strong>")
    if not DataConversion.safe_get (ot, "supervisor"):
        throw ("Supervisor is <strong class='text-rose-500'>Require</strong>")
    if not DataConversion.safe_get (ot, "from_date"):
        throw ("from date is <strong class='text-rose-500'>Require</strong>")
    if not DataConversion.safe_get (ot, "to_date"):
        throw ("To date is <strong class='text-rose-500'>Require</strong>")
    
    DataConversion.safe_set (object.body, "staff_to_work_on_overtime", list_to_save)

def before_overtime_submit (dbms, object):
    validate_ot (dbms, object)
    DataConversion.safe_set (object.body, "is_approved", 0)
    
def before_overtime_save (dbms, object):
    validate_ot (dbms, object)
    DataConversion.safe_set (object.body, "is_approved", 1)


def validate_otc (dbms, object, submit=False):
    core_payroll = Core_Payroll (dbms)
    otc = DataConversion.safe_get (object, "body")
    emp = core_payroll.get_doc ("Employee", DataConversion.safe_get (otc, "employee"))
    if not emp:
        throw ("Overtime Claimer is <strong class='text-rose-500'>Require</strong>")
    overtime_worked = DataConversion.safe_get (otc, "overtime_worked", [])
    if not overtime_worked or len (overtime_worked) < 0:
        throw ("Overtime worked list is <strong class='text-rose-500'>Require</strong>")
    list_to_save = []
    success = 0
    for i, otc_row in enumerate (overtime_worked):
        amount = DataConversion.safe_get (otc_row, "total_amount")
        if not DataConversion.safe_get (otc_row, "day"):
            throw (f"Worked Overtime on Row ({i+1}) Day is <strong class='text-rose-600'>Missing</strong>")
        if not DataConversion.safe_get (otc_row, "date_of_work"):
            throw (f"Worked Overtime on Row ({i+1}) Date Of Work is <strong class='text-rose-600'>Missing</strong>")
        if not DataConversion.safe_get (otc_row, "from_time"):
            throw (f"Worked Overtime on Row ({i+1}) From Time is <strong class='text-rose-600'>Missing</strong>")
        if not DataConversion.safe_get (otc_row, "to_time"):
            throw (f"Worked Overtime on Row ({i+1}) To Time is <strong class='text-rose-600'>Missing</strong>")
        if not DataConversion.safe_get (otc_row, "total_hours"):
            throw (f"Worked Overtime on Row ({i+1}) Total Hours is <strong class='text-rose-600'>Missing</strong>")
        if not DataConversion.safe_get (otc_row, "rate"):
            throw (f"Worked Overtime on Row ({i+1}) Rate is <strong class='text-rose-600'>Missing</strong>")
        if not amount:
            throw (f"Worked Overtime on Row ({i+1}) Total Amount is <strong class='text-rose-600'>Missing</strong>")
        if submit:
            success +=1
            DataConversion.safe_set (otc_row, "cleared", 1)
            r = core_payroll.notify_payroll (
                employee_number=DataConversion.safe_get (emp, "name"),
                amount=amount,
                sc="Overtime",
                doc_type=DataConversion.safe_get (otc, "doctype"),
                doc_name=DataConversion.safe_get (otc, "name"),
                length_or_period=1,
                entry_type="Earning",
                posting_date=dates.today (),
            )
        else:
            DataConversion.safe_set (otc_row, "cleared", 0)

        DataConversion.safe_list_append (list_to_save, otc_row)
    if submit:
        query = """
            SELECT * FROM staffs_to_work_this_overtime
            WHERE (cleared = 0 OR cleared IS NULL)
            AND employee_id = %s
        """
        ots = core_payroll.fetch_data_from_sql (query, (DataConversion.safe_get (emp, 'id', 0),))
        if len (ots) >= success:
            for i in range (success):
                row = DataConversion.safe_list_get (ots, i)
                DataConversion.safe_set (row, "cleared", 1)
                r = dbms.update ("Staffs_To_Work_This_Overtime", utils.from_dict_to_object (row))
    DataConversion.safe_set (object.body, "overtime_worked", list_to_save)
    DataConversion.safe_set (object.body, "show", DataConversion.safe_get (otc, "show", "No"))

def before_overtime_claim_save (dbms, object):
    validate_otc (dbms, object)

def before_overtime_claim_submit (dbms, object):
    validate_otc (dbms, object, submit=True)