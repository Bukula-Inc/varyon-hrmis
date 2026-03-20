from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Designation:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.get_system_settings()
        if system_settings.get("status") == utils.ok:
            self.settings = Generate_Object(system_settings.get("data"))



    def designation(dbms,object):
        designation_employees = []
        chart_data =utils.from_dict_to_object({
            "labels": [],
            "value": [],
        })
        


        
        designation = dbms.get_list("Designation", filters={"status__in":["Active"]}, user=object.user, limit=4)
        if designation.get("status") == utils.ok:
            if len (designation.get ("data").get ("rows")) > 0:
                for des in designation.get ("data").get ("rows"):
                    
                    employees = dbms.get_list("Employee", filters={"designation": des["name"],"status":"Active"}, user=object.user)
                    if employees.get("status") == utils.ok:
                        designation_employees.append({
                            "designation_name": des["name"],
                            "number_of_employees": len(employees.get ("data").get ("rows")),
                        })
                        chart_data.labels.append(
                            des["name"],
                        )
                        chart_data.value.append(
                            len(employees.get ("data").get ("rows")),
                        )
            
        

        results = {
            "designation_employees": designation_employees,
            "designations": chart_data,
        }
        

        return utils.respond(utils.ok, results)
    

        
        






