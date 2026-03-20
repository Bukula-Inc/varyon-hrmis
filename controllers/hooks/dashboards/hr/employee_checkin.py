from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Checkin:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.get_system_settings()
        if system_settings.get("status") == utils.ok:
            self.settings = Generate_Object(system_settings.get("data"))



    def employee_checkin(dbms,object):
        total_logged=0
        department_employees = []
        


        
        employee_checkin = dbms.get_list("Employee_Checkin",filters={"status__in":["Active"]}, user=object.user)
        if employee_checkin.get("status") == utils.ok:
            employee_checkin_ = employee_checkin.get ("data").get ("rows")
            checkin = {
                "in": 0,
                "out": 0
            }
            for ckn in employee_checkin_:
                if str (ckn['log_type']).lower () == "in":
                    checkin['in'] += 1
                else:
                    checkin["out"] +=1
                
            total_logged = len(employee_checkin_)
    
        
        
        department = dbms.get_list("Department", filters={"status__in":["Active"]}, user=object.user, limit=4)
        if department.get("status") == utils.ok:
            if len (department.get ("data").get ("rows")) > 0:
                for dep in department.get ("data").get ("rows"):
                    
                    employees = dbms.get_list("Employee",filters={"department": dep["name"],"status__in":["Active"]}, user=object.user)
                    if employees.get("status") == utils.ok:
                        department_employees.append({
                            "department_name": dep["name"],
                            "number_of_employees": len(employees.get ("data").get ("rows")),
                        })


        results = {
            "checkins": checkin,
            "department_employees": department_employees,

        }
        

        return utils.respond(utils.ok, results)
    

        
        






