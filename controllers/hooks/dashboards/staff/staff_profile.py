from datetime import datetime, date
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.object_generator import Generate_Object, Extract_Object
from controllers.core_functions.hr import Core_Hr
# from controllers.core_functions.project_management import Core_project_management

utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Staff_Profile:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_30_days = dates.add_days(dates.today(), -30)
        self.hr = Core_Hr(dbms,object.user,object)
        # self.project_management = Core_project_management(dbms ,object)
        self.employee = None
        system_settings =  self.dbms.system_settings
        if system_settings:
            self.settings = utils.from_dict_to_object(system_settings)
            self.defaults =  self.settings.accounting_defaults
            comp = getattr(self.defaults, self.settings.default_company)
            cd = self.dbms.get_doc("Company",comp.name,fetch_linked_fields=True,privilege=True)
            cd.status == utils.ok or throw("Failed to fetch company info!")
            self.company = utils.from_dict_to_object(cd.data)
        

    @classmethod
    def staff_profile(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        emp = {}
        employee = cls.hr.get_list("Employee", filters={"user":dbms.current_user.name}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if employee:
                employee = employee[0]
        return utils.respond(utils.ok,
         {  "leave_summary":  cls.hr.get_employee_leave_days(employee.id),
            # "employee_appraisals": cls.hr.get_employee_appraisals(employee.id),
            "staff_pending_tasks": cls.staff_tasks(cls,id=employee.id),
            "working_days": employee.working_days,
            "days_in_service": cls.days_in_service(cls,employee.date_of_joining),
        })
    
    # filters={"user":dbms.current_user.name},

    def staff_tasks(self, id):
        tasks_status_count = {}
        count_dict = {}
        
        work_plan_tasks = self.hr.get_employee_work_plan_tasks(id)  
        progress_status = work_plan_tasks.get("progress_tracker")
        if progress_status in count_dict:
            count_dict[progress_status] += 1
        else:
            count_dict[progress_status] = 1  
                
        for status, count in count_dict.items():
            tasks_status_count = {"status":status,"count" :count}
            return tasks_status_count
        
    
    def days_in_service(self, date_of_joining):
        current_date = date.today() 
        difference_in_days = (current_date - date_of_joining).days
        return difference_in_days
