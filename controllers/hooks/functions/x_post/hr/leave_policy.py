from  controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

utils = Utils ()
dates = Dates ()
pp =utils.pretty_print

throw = utils.throw
def get_policy_type(dbms, object):
    core_hr = Core_Hr(dbms=dbms)
    get_policy_type = object.body.data.get("id")
    policy_details =[]

    policy_type = None
    allocations =None
    
    if object.body.data.doc_name:
        fetch_doc =dbms.get_doc("Leave_Policy", object.body.data.doc_name)
        if fetch_doc.status ==utils.ok:
            policy_type =fetch_doc.data.policy_for
            allocations =fetch_doc.data.policy_details

    if policy_type !=None and policy_type ==get_policy_type:
        policy_details =allocations
    else:
        if get_policy_type == "Employment Type":
            employment_types = core_hr.get_employment_type_list()
            if employment_types: 
                for emp in employment_types:
                    if 'name' in emp:  
                        policy_details.append({
                            "policy_type": emp['name']
                        })
                    else:
                        utils.throw(f"Employment type {emp} does not have a 'name' key")
            else:
                utils.throw("No employment types found")
        elif get_policy_type == "Employee Grade":
            get_employment_grade = dbms.get_list("Employee_Grade")
            if get_employment_grade.status == utils.ok:
                data = get_employment_grade.data.rows
                for grade in data:
                    if 'name' in grade:  
                        policy_details.append({
                            "policy_type": grade['name']
                        })
                    else:
                        utils.throw(f"Employee grade {grade} does not have a 'name' key")
        elif get_policy_type == "Designation":
            get_designations = core_hr.get_designation_list()
            for desig in get_designations:
                if 'name' in desig: 
                    policy_details.append({
                        "policy_type": desig['name']
                    })
                else:
                    utils.throw(f"Designation {desig} does not have a 'name' key")

    return utils.respond(utils.ok, {"policy_details":policy_details})