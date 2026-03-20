from controllers.utils import Utils
from controllers.utils.dates import Dates

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

class BJ_Calender:
    def __init__(self, dbms, object):
        self.dbms =dbms
        self.object =object
        self.today =dates.today()

    def new_calender(self):
        if dates.is_first_day_of_year ():
            this_years_holiday_list = dates._init_holidays ("ZM")
            obj = utils.from_dict_to_object ({
                "calendar_holidays": this_years_holiday_list
            })
            holidays = self.dbms.create ("Calender", body=obj, skip_user_evaluation=True, privilege=True)
            if holidays.status == utils.ok:
                return holidays.status

    @classmethod
    def bj_calender(cls, dbms, object):

        instance =cls(dbms,object)
        results =utils.from_dict_to_object({
            "new_calender": instance.new_calender() or 422,
        })

        return utils.respond(utils.ok, {"Conditions": results})