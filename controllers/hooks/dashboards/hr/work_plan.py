from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Work_Plan:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.system_settings()
        if system_settings.status == utils.ok:
            self.settings = Dict_To_Object(system_settings.data)



    def work_plan(dbms,object):
        
        work_plan_activities = []
        
    
        
        
        employee = dbms.get_list("Employee", filters={"status__in":["Active"]}, user=object.user, limit=6)
        if employee.status == utils.ok:
            if len (employee.data.rows) > 0:
                for emp in employee.data.rows:
                    
                    plan = dbms.get_list("Work_Plan",filters={"employee_name": emp["full_name"],"status__in":["Submitted"]}, user=object.user)
                    if plan.status == utils.ok:
                        if len (plan.data.rows) > 0:
                            for pn in plan.data.rows:
                                work_plan_activities.append({
                                    "employee_name": emp["full_name"],
                                    "month": pn["month"] ,
                                    
                                })


        results = {
            # "checkins": checkin,
            "work_plan_activities": work_plan_activities,

        }
        

        return utils.respond(utils.ok, results)
   

    
    






