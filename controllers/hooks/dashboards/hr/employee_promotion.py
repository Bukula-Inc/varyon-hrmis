from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Promotion:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.get_system_settings()
        if system_settings.get("status") == utils.ok:
            self.settings = Generate_Object(system_settings.get("data"))



    def  employee_promotion(dbms,object):
        promoted_employees = []
        
        employee = dbms.get_list("Employee", filters={"status__in":["Active"]}, user=object.user, limit=6)
        if employee.get("status") == utils.ok:
            if len (employee.get ("data").get ("rows")) > 0:
                for emp in employee.get ("data").get ("rows"):
                    
                    employee_promotion = dbms.get_list("Employee_Promotion",filters={"employee_name": emp["full_name"],"status__in":["Submitted"]}, user=object.user)
                    if employee_promotion.get("status") == utils.ok:
                        if len (employee_promotion.get ("data").get ("rows")) > 0:
                            for pro in employee_promotion.get ("data").get ("rows"):
                                promoted_employees.append({
                                    "employee_name": emp["full_name"],
                                    "date": pro["promotion_date"] ,
                                })

        

                
            


        results = {
                "promoted_employees": promoted_employees,
        
            }
            

        return utils.respond(utils.ok, results)