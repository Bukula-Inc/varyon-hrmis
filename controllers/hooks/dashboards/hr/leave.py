from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Leave:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.get_system_settings()
        if system_settings.get("status") == utils.ok:
            self.settings = system_settings.get("data")
        self.core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)

    def leave_allocation_side_view(dbms, object):
        core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
        allocated_employees= []
        leave_info = core_hr.get_leave_info ()
        employee = core_hr.get_list("Employee", filters={"status__in":["Active"]}, limit=6)
        allocated_employees = []
        leave_allocation_by_type = {}
        if employee:
            if len (employee) > 0:
                for emp in employee:
                    allocation = core_hr.get_list("leave_Allocation_Employees",filters={"employee_name": emp["full_name"],"status__in":["Submitted"]})
                    if allocation:
                        if len (allocation) > 0:
                            for allocation_ in allocation:
                                if allocation_['leave_type']:
                                    leave_allocation_by_type[allocation_["leave_type"]]=+1
                                else:
                                    leave_allocation_by_type[allocation_["leave_type"]] = 1
                                allocated_employees.append({
                                    "employee_name": allocation_["employee_name"],
                                    "total_leaves_allocated": allocation_["total_leaves_allocated"],
                                    
                                })

        results = {"allocated_employees": allocated_employees, "leave_usage": leave_info, "leave_allocation": leave_allocation_by_type}
        return utils.respond(utils.ok, results)
    

    def leave_application_side_view(dbms, object):
        core_hr = Core_Hr (dbms=dbms, obj=object)
        applied_employees= []
        department_employees = []
        application = core_hr.get_list("Leave_Application",)
        if application:
            if len (application) > 0:
                for app in application:
                    applied_employees.append({
                        "employee_name": app.employee_name,
                        "time_duration_formatted": app.time_duration_formatted,
                        "total_days": app.total_days,
                        "leave_type": app.leave_type,
                    })
        department = core_hr.get_list("Department", filters={"status__in":["Active"]}, limit=4)
        if department:
            if len (department) > 0:
                for dep in department:
                    employees = core_hr.get_list("Leave_Application",filters={"department": dep["name"]},)
                    if employees:
                        department_employees.append({
                            "department_name": dep["name"],
                            "number_of_employees": len(employees),
                        })
        results = {# "checkins": checkin,
            "applied_employees":applied_employees,
            "department_employees": department_employees,

        }
        return utils.respond(utils.ok, results)
    
    def leave_plan_sv(dbms, object):
        core_hr = Core_Hr (dbms=dbms)
        leave_types = {}
        return_data = []

        fetch_leave_applications =dbms.get_list("Leave_Application",)
        if fetch_leave_applications.status ==utils.ok:
            leave_types =utils.group(fetch_leave_applications.data.rows, "leave_type")
            for key, leave_type in leave_types.items():
                leave =utils.to_data_frame(leave_type)
                return_data.append(utils.from_dict_to_object({
                    "leave_type": key,
                    "used_leave": len(leave_type),
                    "avg_len": leave["total_days"].mean(),
                }))
        
        ls = core_hr.get_leave_info ()
        # fetch_

        # elif fetch_leave_applications.status ==utils.no_content:
        #     return_data =[]
        # else:
        #     return  

        return utils.respond(fetch_leave_applications.status, {"leave_type_data":return_data, "leave_summary": ls})
            
    # filter ={"date__range": [date_1, date_2]}
    # filters ={"from_date__range": [dates.string_to_date("2024-01-01"), dates.today()]}