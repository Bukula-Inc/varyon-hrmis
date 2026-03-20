from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates

utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates =Dates()

def get_leave_type (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    leave_type = core_hr.get_doc ("Leave_Type",  object.body.data.type)
    get_employees = []
    if leave_type:
        if str (leave_type.apply_on).lower () == "male":
            filters = {'gender': "Male", "status": "Active"}
        elif str (leave_type.apply_on).lower () == "female":
            filters = {'gender': "Female", "status": "Active"}
        else:
            filters = {"status": "Active"}
        get_emp_list = core_hr.get_employee_list (filters=filters)
        if get_emp_list:
            get_employees = get_emp_list
    return utils.respond (utils.ok, response={"status": utils.ok, "data": get_employees})

def on_leave_approval(leave_application, dbms, object):
    core_hr = Core_Hr (dbms=dbms, user=object.user, obj=object)
    if leave_application:
        employee = core_hr.get_doc ("Employee", leave_application.employee)
        if employee:
            approver = employee.leave_approver
            current_user = core_hr.get_doc ("Lite_User", object.user)
            if current_user: 
                employee = core_hr.get_list ("Employee", filters= {"user": current_user.name})
                if employee and employee[0].name == approver:
                    return True
                return None
            
def leave_plan_to_applications(dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    fetch_plans =dbms.get_list("Leave_Plan", filters={"days_before_from_date": dates.today()}, fetch_linked_fields=True)
    success_rate =utils.from_dict_to_object({
        "successful":[],
        "failed" :[]
    })
    if fetch_plans.status ==utils.ok:
        for plan in fetch_plans.data.rows:
            department =dbms.get_doc("Department", plan.linked_fields.planner.department, fetch_by_field ="id").data 
        
            application =utils.from_dict_to_object({
            "employee": plan.planner,
            "employee_name": plan.linked_fields.planner.first_name + " " + plan.linked_fields.planner.last_name,
            "leave_type": plan.leave_type,
            "leave_mode": "Days Leave",
            "company": core_hr.company,
            "department": department.name if department.status ==utils.ok else "",
            "attachment": "",
            "from_time": "",
            "to_time": "",
            "from_date": plan.from_date,
            "to_date": plan.to_date,
            "time_duration_formatted": "",
            "total_days": plan.days,
            "reason": "",
            },)

            create_plan =dbms.create("Leave_Application", application, submit_after_create=True)
            if create_plan.status != utils.ok:
                plan.reason_of_failure =create_plan.error_message
                success_rate.failed.append(plan)
            else:
                success_rate.successful.append(create_plan.data)

    pp(success_rate)


def leave_schedule_employees (dbms, object):
    core_hr = Core_Hr (dbms)
    dept = DataConversion.safe_get (object.body.data, "dept")
    lt = DataConversion.safe_get (object.body.data, "lt", "Annual Leave")
    if not dept:
        throw ("Department is <strong class='text-rose-500'>Require</strong>")
    employees = core_hr.get_list ("Employee", filters={"department": dept})
    if len (employees) < 0:
        throw ("Department has <strong class='text-rose-500'>No Employees</strong>")
    return_dict = {
        "department_days": 0.00,
        "leave_information": []
    }
    for emp in employees:
        row = {}
        emp_id = DataConversion.safe_get (emp, "name")
        dept_days = DataConversion.convert_to_float (DataConversion.safe_get (return_dict, "department_days", 0))
        leave_days = core_hr.emp_leave_annual_days (emp_id, leave_type=lt)
        rd = DataConversion.convert_to_float (DataConversion.safe_get (leave_days, "remaining_days", 0))
        DataConversion.safe_set (return_dict, "department_days", sum ([dept_days, rd]))
        DataConversion.safe_set (row, "employee", emp_id)
        DataConversion.safe_set (row, "employee_total_days", rd)
        DataConversion.safe_set (row, "full_name", DataConversion.safe_get (emp, "full_name", f"""{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name')} {DataConversion.safe_get (emp, 'last_name')}"""))
        DataConversion.safe_list_append (DataConversion.safe_get (return_dict, "leave_information", []), row)
    return utils.respond (utils.ok, return_dict)