from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

dates = Dates ()
utils = Utils()
pp = utils.pretty_print
throw =utils.throw

def validate_employee_promotion (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    obj = DataConversion.safe_get (object, "body", {})
    posting_date = DataConversion.safe_get (obj, "promotion_date", dates.today())
    employee = DataConversion.safe_get (obj, "employee")
    designation = DataConversion.safe_get (obj, "designation")
    department = DataConversion.safe_get (obj, "department")
    revised_department = DataConversion.safe_get (obj, "revised_department")
    promotion_options = DataConversion.safe_get (obj, "promotion_options")
    role = DataConversion.safe_get (obj, "role")
    employee_grade = DataConversion.safe_get (obj, "employee_grade")
    revised_basic = DataConversion.safe_get (obj, "revised_basic")
    earnings = DataConversion.safe_get (obj, "earnings", [])
    deductions = DataConversion.safe_get (obj, "deductions", [])

    if not employee:
        throw ("Employee is <strong class='text-rose-600'>required</strong>")
    emp = core_hr.get_doc ("Employee", employee)
    if not emp:
        throw ("Employee is not <strong class='text-rose-500'>required</strong>")
    if not designation:
        throw ("Job Title is <strong class='text-rose-600'>required</strong>")
    if not department:
        throw ("Department / Unit is <strong class='text-rose-600'>required</strong>")
    if not posting_date:
        throw ("Promotion Date is <strong class='text-rose-600'>required</strong>")
    if not promotion_options:
        throw ("Promotion Option is <strong class='text-rose-600'>required</strong>")
    if str (promotion_options).lower () == "designation based":
        if not role:
            throw ("Role is <strong class='text-rose-600'>required</strong>")
        if not revised_department:
            throw ("Revised Department is <strong class='text-rose-600'>required</strong>")
    if str (promotion_options).lower () == "salary based":
        if not employee_grade:
            throw ("Employee Grade is <strong class='text-rose-600'>required</strong>")
        if not revised_basic or float (revised_basic) <= 0:
            throw ("Revised Basic is <strong class='text-rose-600'>required</strong> and must be greater than zero")
        if not earnings or len (earnings) == 0:
            throw ("At least one Earning is <strong class='text-rose-600'>required</strong>")
        if not deductions or len (deductions) == 0:
            throw ("At least one Deduction is <strong class='text-rose-600'>required</strong>")

def employee_promotion_save (dbms, object):
    validate_employee_promotion (dbms, object)


def employee_promotion (dbms, object):
    validate_employee_promotion (dbms, object)
    core_hr = Core_Hr (dbms=dbms)
    obj = DataConversion.safe_get (object, "body")

    emp = core_hr.get_doc ("Employee", DataConversion.safe_get (obj, "employee"))
    DataConversion.safe_set (emp, "designation", DataConversion.safe_get (obj, "role"))
    DataConversion.safe_set (emp, "basic_pay", DataConversion.safe_get (obj, "revised_basic"))
    DataConversion.safe_set (emp, "employee_grade", DataConversion.safe_get (obj, "employee_grade"))
    DataConversion.safe_set (emp, "department", DataConversion.safe_get (obj, "revised_department"))

    dbms.update ("Employee", emp, update_submitted=True)