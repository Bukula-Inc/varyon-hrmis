from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from collections import defaultdict


utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def filter_emps_by_policys_category (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    return_list = []
    policy_name =None
    policy = DataConversion.safe_get (object.body.data, "policy", None)
    if not policy:
        return utils.respond (utils.no_content, response="No Policy Found!, Select A Policy")
    get_policy = core_hr.get_doc ("Leave_Policy", name=policy)
    if not get_policy:
        return utils.respond (utils.no_content, response="No Policy Found")

    policy_for = DataConversion.safe_get (get_policy, "policy_for", None)
    leave_type = DataConversion.safe_get (get_policy, "name", None)
    if not leave_type:
        leave_type = "Annual Leave"
    policy_details = DataConversion.safe_get (get_policy, "policy_details", [])
    if not policy_for:
        return utils.respond (utils.no_content, response="Your Policy Has No Target")

    if len (policy_details) <= 0 or not policy_details:
        return utils.respond (utils.no_content, response="Your Policy Has No Configurations")
    
    if object.body.data.doc_name:
        fetch_doc =dbms.get_doc("Leave_Allocation", object.body.data.doc_name)
        if fetch_doc.status ==utils.ok:
            policy_name =fetch_doc.data.main_policy
            leave_allocation_employees =fetch_doc.data.leave_allocation_employees
    if policy_name !=None and policy_name ==policy:
        return_list =leave_allocation_employees
    else:
        dict_key = ""
        if str (policy_for).lower () == "employee grade":
            dict_key = "employee_grade"
        elif str (policy_for).lower () == "designation":
            dict_key = "designation"
        elif str (policy_for).lower () == "employment type":
            dict_key = "employment_type"

        emp_list =core_hr.get_list("Employee", fields=["name", "full_name", "first_name", "last_name", dict_key], filters= {"status__in": ["Active", "Suspended", "On Leave"]})
        if emp_list:
            policy_details = utils.array_to_dict (policy_details, "policy_type")

            emps_grouped =defaultdict(list)
            for emp in emp_list:
                key = emp[dict_key] or 'name_missing'
                emps_grouped[key].append(emp)
            grouped_emps =utils.from_dict_to_object(dict(emps_grouped))

            # grouped_emps =utils.group(emp_list, dict_key or "name")
            
            emp_lst = []
            for val in grouped_emps.values(): emp_lst += val
            
            for employee in emp_lst:
                
                full_name = DataConversion.safe_get (employee, "full_name")
                full_name = full_name if full_name else f"{DataConversion.safe_get (employee, 'first_name')} {DataConversion.safe_get (employee, 'middle_name', '')} {DataConversion.safe_get (employee, 'last_name')}"
                lt = DataConversion.safe_get (employee, dict_key)
                lt_days = DataConversion.safe_get (policy_details, lt)
                days = DataConversion.safe_get (lt_days, "total_days_allocated_per_month", 0.00)
                return_list.append ({
                    "employee": employee.name,
                    "employee_name": full_name,
                    # "policy_category": employee[dict_key] or f'No {dict_key.replace("_", " ")} is attached.',
                    "policy_category": lt,
                    # "total_leaves_allocated": policy_details[employee[dict_key]].total_days_allocated_per_month if employee[dict_key] else 0.00
                    "total_leaves_allocated": days
                })
        else:
            emp_list =core_hr.get_list("Employee", fields=["name", "full_name", "first_name", "last_name",], filters= {"status__in": ["Active", "Suspended", "On Leave"]})
            for employee  in emp_list:
                full_name = DataConversion.safe_get (employee, "full_name", None)
                full_name = full_name if full_name else f"{DataConversion.safe_get (employee, 'first_name')} {DataConversion.safe_get (employee, 'middle_name', '')} {DataConversion.safe_get (employee, 'last_name')}"
                lt = DataConversion.safe_get (employee, dict_key)
                lt_days = DataConversion.safe_get (policy_details, lt)
                days = DataConversion.safe_get (lt_days, "total_days_allocated_per_month", 0.00)
                return_list.append ({
                    "employee": employee.name,
                    "employee_name": full_name,
                    "policy_category": lt,
                    "total_leaves_allocated": days
                    # "policy_category": employee[dict_key] or f'No {dict_key.replace("_", " ")} is attached.',
                    # "total_leaves_allocated": policy_details[employee[dict_key]].total_days_allocated_per_month if employee[dict_key] else 0.00
                })
    return utils.respond (utils.ok, response={"status": utils.ok, "data": return_list})


def remove_duplicates (employee_list):
    unique_ids = set()
    unique_employees = []

    for employee in employee_list:
        if employee.id not in unique_ids:
            unique_ids.add(employee.id)
            unique_employees.append(employee)

    return unique_employees

def filter_emps_by_designation (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    return_list = []
    get_policy = core_hr.get_doc ("Leave_Policy", object.body.data.policy)

    if get_policy:
        dict_key = None
        leave_types = get_policy.policy_details
        if str (get_policy.leave_policy_main_control).lower () != "default":
            if str (get_policy.leave_policy_main_control).lower () == "salary grade":
                leave_types = get_policy.leave_policy_grade
                dict_key = "employee_grade"
            elif str (get_policy.leave_policy_main_control).lower () == "designation":
                leave_types = get_policy.policy_designation
                dict_key = "designation"

        for lev_ty in leave_types:
            get_emps = None
            if dict_key:
                if lev_ty.get (dict_key, None):
                    get_emps = core_hr.get_employee_list (filters={dict_key: lev_ty.get (dict_key, None), "status_in": ["Active", "Suspended", "On Leave"]})
            else:
                get_emps = core_hr.get_employee_list (filters={"status_in": ["Active", "Suspended", "On Leave"]})
            if get_emps:
                for emp in get_emps:
                    if not lev_ty.apply_on:
                        lty = core_hr.get_doc ("Leave_Type", lev_ty.leave_type)
                        if lty:
                            lev_ty.apply_on = lty.apply_on
                    if str (lev_ty.apply_on).lower () == "both" or str (lev_ty.apply_on) == emp.gender:
                        return_list.append ({
                            "employee": emp.name,
                            "leave_policy": get_policy.name,
                            "leave_type": lev_ty.leave_type
                        })
    return utils.respond (utils.ok, response={"status": utils.ok, "data": return_list})

def get_employee_analytics(dbms, object):
    core = Core_Hr(dbms, object.user)
    leave_types = []
    leave_type = core.get_doc ("Leave_Type", name=object.body.data.leave_type)
    get_leave_policy = core.get_doc ("Leave_Policy", name=object.body.data.leave_policy)
    emp = core.get_employee_leave_days(object.body.data.eid)
    if get_leave_policy:
        leave_types = get_leave_policy.policy_details
    return utils.respond(utils.ok,{"emp": emp, "policy": leave_types, "leave_type": leave_type})

def create_user_form_employee (dbms, object):
    new_user = dbms.create ("Lite_User", object.body.data, user_id=object.user)
    status = new_user.status
    msg = f"Failed To Create User"
    if status == utils.ok:
        msg = f"{new_user.data.first_name} {new_user.data.last_name} Was Created As User Successfully"
    return utils.respond (new_user.status, response=msg)

def create_user (employee, dbms):
    if employee.status == "Active":
        user = utils.from_dict_to_object ({
            "first_name": employee.first_name,
            "middle_name": employee.middle_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "contact_no": employee.contact,
            "department": employee.department,
            "main_role": "Staff",
            "company": employee.company,
        })
        new_user = dbms.create ("Lite_User", user)
        if new_user.status == utils.ok:
            employee.user = employee.email
            employee.create_user = "Link User"
            new_user_u = dbms.update ("Employee", employee, update_submitted=True)

def create_users_from_selected (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    if object.body.data.employees:
        for emp in object.body.data.employees:
            emp_name = emp.get ('values', None)
            if emp_name:
                employee = core_hr.get_doc ("Employee", emp_name.name)
                if not employee.user:
                    create_user (employee=employee, dbms=dbms)
    return utils.respond (status=utils.ok, response={"msg": "creation"})

def create_users_on_a_mass (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    employees = core_hr.get_list ("Employee")
    for employee in employees:
        if not employee.user:
            create_user (employee=employee, dbms=dbms)
    return utils.respond (status=utils.ok, response={"msg": "creation"})

def reinstate_employee (dbms, object):
    core_hr = Core_Hr (dbms)
    emp = core_hr.get_doc ("Employee", object.body.data.emp)
    if emp:
        emp.status = "Active"
        emp.last_day_of_work = None
        emp.docstatus = 0
        emp.is_separated_emp_paid = "Unsettled"
        emp.is_separated = 0
        dbms.update ("Employee", emp, update_submitted=True)
        return utils.respond (utils.ok, "Success")
    return utils.respond (utils.unprocessable_entity, response="Failed to Reinstate Employee")
