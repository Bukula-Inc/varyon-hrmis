from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class Appraisal_Setup:
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
    def appraisal_setup(dbms, object):
        status  = []
        appraisal = dbms.get_list("Appraisal_Setup", user=object.user)
        if appraisal.status == utils.ok:
            appraisal_data = appraisal.data.rows
            status.append({
                "submitted": sum(1 for appraisal in appraisal_data if appraisal['status'] == 'Submitted'),
                "draft": sum(1 for appraisal in appraisal_data if appraisal['status'] == 'Draft'),
                "cancelled": sum(1 for appraisal in appraisal_data if appraisal['status'] == 'Cancelled'),
                "total": len(appraisal_data)
            })
            status_type = {
                "self_appraisal": sum(1 for app in appraisal_data if app['appraisal_type'] == 'Self-Rating'),
                "three_degree_apprisal": sum(1 for app in appraisal_data if app['appraisal_type'] == '360 degree Appraisal'),
            }
            results = {
                "appraisal_setup_stats": status,
                "appraisal_type": status_type,
            }
            return utils.respond(utils.ok, results)

    
    






