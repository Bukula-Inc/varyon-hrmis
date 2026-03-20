from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def fetch_budget_line(dbms, object):
    return_object =utils.from_dict_to_object({
        "available_amount": 0.00
    })

    data =DataConversion.safe_get(DataConversion.safe_get(object, "body", {}),"data", {}), 
    record_type =DataConversion.safe_get(data[0], "model", None)

    fetch_budget_line =dbms.get_list("Budget_Line", filters={"record_type": record_type})
    if fetch_budget_line.status ==utils.no_content:
        throw(f"""<strong class="text-red-400 font-semibold"> No</strong> budget line was created for <strong class="text-red-400 font-semibold">{record_type.replace("_", " ")}</strong>""")
    elif fetch_budget_line.status !=utils.ok:
        throw(fetch_budget_line.error_message)


    
    budget_line =DataConversion.safe_get(DataConversion.safe_get(fetch_budget_line, "data", {}), "rows", [])
    budget_line_name =DataConversion.safe_get(budget_line[0], "name", "")

    get_budget =dbms.get_list("HR_Budget")
    # filters={"from_date__lt": dates.today(), "to_date__gt": dates.today()}
    if get_budget.status !=utils.ok:
        throw(f""" No budget was found.""")
    
    budget =DataConversion.safe_get(DataConversion.safe_get(get_budget, "data", {}), "rows")[0]
    pp(budget)
    budget_entries =dbms.get_list("HR_Budget_Entries", filters={"budget_reference": budget.name, "budget_line": budget_line_name})
    if budget_entries.status !=utils.ok:
        throw(f"""No budget entry was found.""")
    
    entry =DataConversion.safe_get(DataConversion.safe_get(budget_entries, "data", {}), "rows", [])[0]
    return_object.available_amount =DataConversion.convert_to_float(entry.total_balance) or 0.00
    return utils.respond(utils.ok, return_object)