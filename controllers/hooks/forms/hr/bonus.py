from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()

throw = utils.throw
pp = utils.pretty_print


def before_bonus_submit (dbms, object):
    core_payroll = Core_Payroll (dbms)
    bonus_employees = DataConversion.safe_get (object.body, "bonus_employees", [])
    if not  bonus_employees:
        throw ("there are no qualified employees to process bonus")
    for i, bonus in enumerate (bonus_employees):
        add_to_payroll =core_payroll.notify_payroll(
            employee_number=DataConversion.safe_get(bonus, "employee"),
            amount= DataConversion.convert_to_float (DataConversion.safe_get (bonus, "bonus_amount",0)),
            length_or_period=1,
            doc_type=DataConversion.safe_get(object.body, "doctype", "Bonus"),
            doc_name=DataConversion.safe_get(object.body, "name"),
            sc="Performance Reward",
            entry_type ="Earning"
        )

        pp (add_to_payroll)

def before_bonus_save (dbms, object):
    bonus_employees = DataConversion.safe_get (object.body, "bonus_employees", [])
    if bonus_employees:
        throw ("there are no qualified employees to process bonus")
    for i, bonus in enumerate (bonus_employees):
        if not DataConversion.safe_get (bonus, "employee"):
            throw (f"Employee No is missing on row # {i+1}")
        if not DataConversion.safe_get (bonus, "employee_name"):
            throw (f"Employee Name is missing on row # {i+1}")
        if not DataConversion.safe_get (bonus, "employee_designation"):
            throw (f"Employee Designation is missing on row # {i+1}")
        if not DataConversion.safe_get (bonus, "department"):
            throw (f"Employee Department is missing on row # {i+1}")
        if not DataConversion.safe_get (bonus, "score"):
            throw (f"Employee Score is missing on row # {i+1}")
        if not DataConversion.safe_get (bonus, "bonus_amount"):
            throw (f"Employee Score is missing on row # {i+1}")