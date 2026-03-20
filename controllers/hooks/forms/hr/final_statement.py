from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr

utils = Utils ()
pp = utils.pretty_print
throw =utils.throw

def on_final_statement_save(dbms, object):
    object.body.calculated_totals = [{k: v for k, v in d.items() if k != "id"} for d in object.body.calculated_totals]
    object.body.asset = [{k: v for k, v in d.items() if k != "id"} for d in object.body.asset]



def on_final_statement_submission (dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object,)
    statement_f = object.body
    get_separation_doc = core_hr.get_list ("employee_separation", filters= { "employee": statement_f.employee_id})
    # "status": "Resignation Accepted",
    if get_separation_doc:
        employee = core_hr.get_doc ("Employee", name=statement_f.employee_id)
        separation = get_separation_doc[0]
        if separation.separation_type == "Termination":
            employee.status = "Terminated"
        elif separation.separation_type == "Resignation":
            employee.status = "Resigned"
        elif separation.separation_type == "Retirement":
            employee.status = "Retired"
        elif separation.separation_type == "Redundancy":
            employee.status = "Redundant"
    up = dbms.update ("Employee", employee)
    # pp (up)
