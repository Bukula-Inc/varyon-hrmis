from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils()
dates = Dates()
throw = utils.throw

class Appraisal:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.system_settings()
        if system_settings.status == utils.ok:
            self.settings = Dict_To_Object(system_settings.data)

    @staticmethod
    def appraisal(dbms, object):
        submitted_appraisals = []
        appraisal_data = dbms.get_list("Appraisal", user=object.user)
        if appraisal_data.status == utils.ok:
            appraisal_list = appraisal_data.data.rows
            status = {
                "submitted": sum(1 for appraisal in appraisal_list if appraisal['status'] == 'Submitted'),
                "draft": sum(1 for appraisal in appraisal_list if appraisal['status'] == 'Draft'),
                "total": len(appraisal_list),
            }
    
            employee_appraisals = dbms.get_list("Appraisal", filters={"status__in": ["Submitted"]}, user=object.user)
            if employee_appraisals.status == utils.ok:
                for app in employee_appraisals.data.rows:
                    employee_data = dbms.get_list("Employee", filters={"full_name": app["appraisee_name"]}, user=object.user)
                    if employee_data.status == utils.ok:
                            employees = employee_data.data.rows
                            for emp in employees:
                                submitted_appraisals.append({
                                    "appraisal_name": emp["full_name"],
                                    "date": app["appraisal_date"],
                                })
            results = {
                "appraisal_setup_stats": status,
                "submitted_appraisals": submitted_appraisals,
            }
            return utils.respond(utils.ok, results)