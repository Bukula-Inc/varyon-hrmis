from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dict_to_object import Dict_To_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Appraisal_Form:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.system_settings()
        if system_settings.status == utils.ok:
            self.settings = Dict_To_Object(system_settings.data)



    def appraisal_form(dbms,object):
        
        appraised_employees = []
        
    
        
        
        employee = dbms.get_list("Employee", user=object.user, limit=6)
        if employee.status == utils.ok:
            if len (employee.data.rows) > 0:
                for emp in employee.data.rows:
                    
                    appraisal_form = dbms.get_list("Appraisal_Form",filters={"appraisee_name": emp["full_name"],"status__in":["Submitted"]}, user=object.user)
                    if appraisal_form.status == utils.ok:
                        if len (appraisal_form.data.rows) > 0:
                            for app in appraisal_form.data.rows:
                                appraised_employees.append({
                                    "appraisal_name": emp["full_name"],
                                    "date": app["appraisal_date"] ,
                                })

          
        appraisal_stats = dbms.get_list("Appraisal_Form", user=object.user)

        if appraisal_stats.status == utils.ok:
            appraisal_forms = appraisal_stats.data.rows
            status = {
                "submitted": 0,
                "draft": 0,
            }
            for form in appraisal_forms:
                if form['status'] == 'Submitted':
                    status['submitted'] += 1
                elif form['status'] == 'Draft':
                    status["draft"] += 1

            total_logged = len(appraisal_forms)



        results = {
            "appraisal_form_stats": status,
            "appraised_employees": appraised_employees,

        }
        

        return utils.respond(utils.ok, results)
   

    
    






