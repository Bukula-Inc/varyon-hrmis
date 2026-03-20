from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
from datetime import datetime
from controllers.utils  import Dates

dates = Dates ()
utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def hr_budget_validate (dbms, object):
    budget = DataConversion.safe_get (object, "body", {})
    budget_lines = DataConversion.safe_get (budget, "budget_lines", [])
    from_date = DataConversion.safe_get (budget, "from_date")
    to_date = DataConversion.safe_get (budget, "to_date")
    total_funds = DataConversion.convert_to_float (DataConversion.safe_get (budget, "total_funds", 0))
    impact_on_budget = DataConversion.convert_to_float (DataConversion.safe_get (budget, "impact_on_budget", 0))
    difference = DataConversion.convert_to_float (DataConversion.safe_get (budget, "difference", 0))
    
    if not from_date:
        throw ("From Date is <strong class='text-rose-500'> required</strong>")
    if not to_date:
        throw ("To Date is <strong class='text-rose-500'> required</strong>")
    if not total_funds or total_funds <= 0:
        throw ("Total Funds must be greater than <strong class='text-rose-500'> 0.00</strong>")
    if not impact_on_budget or impact_on_budget < 0:
        throw ("Impact on Budget must be greater than or equal to <strong class='text-rose-500'> 0.00</strong>")
    if len (budget_lines) == 0:
        throw ("At least one Budget Line is <strong class='text-rose-500'> required</strong>")
    if difference != (total_funds - impact_on_budget):
        throw ("Difference must be equal to <strong class='text-rose-500'> Total Funds - Impact on Budget</strong>")
    if DataConversion.date_diff (to_date, from_date) < 0:
        throw ("To Date must be greater than or equal to <strong class='text-rose-500'> From Date</strong>")
    track_be = 0.00
    for i, be in enumerate (budget_lines):
        budget_line_expense = DataConversion.safe_get (be, "budget_line_expense")
        budget_line = DataConversion.safe_get (be, "budget_line")
        if not budget_line or len (budget_line.strip()) == 0:
            throw (f"Budget Line is <strong class='text-rose-500'> required</strong> for row {i + 1}")
        if not budget_line_expense or budget_line_expense <= 0:
            throw (f"Budget Line Expense must be greater than <strong class='text-rose-500'> 0.00</strong> for row {i + 1}")
        track_be += budget_line_expense

    if track_be != impact_on_budget:
        throw ("Sum of all Budget Line Expenses must be equal to <strong class='text-rose-500'> Impact on Budget</strong>")
    if difference != (total_funds - track_be):
        throw ("Difference must be equal to <strong class='text-rose-500'> Total Funds - Impact on Budget</strong>")
    
def before_hr_budget_save (dbms, object):
    hr_budget_validate (dbms, object)    
    

def before_hr_budget_update (dbms, object):
    hr_budget_validate (dbms, object)    
    

def hr_budget_submit (dbms, object):
    hr_budget_validate (dbms, object)
    budget = DataConversion.safe_get (object, "body", {})
    budget_lines = DataConversion.safe_get (budget, "budget_lines", [])
    for i, be in enumerate (budget_lines):
        new_ent = utils.from_dict_to_object ()
        DataConversion.safe_set (new_ent, "reference_doc","HR_Budget")
        DataConversion.safe_set (new_ent, "budget_reference", DataConversion.safe_get (budget, "name"))
        DataConversion.safe_set (new_ent, "budget_line", DataConversion.safe_get (be, "budget_line"))
        DataConversion.safe_set (new_ent, "total_balance", DataConversion.safe_get (be, "budget_line_expense"))
        DataConversion.safe_set (new_ent, "total_allocated", DataConversion.safe_get (be, "budget_line_expense"))
        DataConversion.safe_set (new_ent, "total_used_amount", 0.00)
        DataConversion.safe_set (new_ent, "entry_type", "Allocation")
        DataConversion.safe_set (new_ent, "status", "Submitted")
        r = dbms.create ("HR_Budget_Entries", new_ent)
        # pp (DataConversion.safe_get (be, "budget_line"), r)