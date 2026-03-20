# from controllers.form_fields.payroll.payroll_processor import Core_Hr
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

class Separation_BJ:
    def __init__(self, dbms, object):
        self.dbms =dbms
        self.object =object
        self.today =dates.today()


    def update_employee(self):
        fetch_todays_separation =self.dbms.get_list("Employee_Seperation", filters={"docstatus": 1, "last_day_of_work": self.today}, privilege=True)
        if fetch_todays_separation.status ==utils.ok:
            core_hr = Core_Hr (dbms=self.dbms, obj=self.object,)
            for separation in fetch_todays_separation.data.rows:
                accept_sep =core_hr.accept_separation(utils.from_dict_to_object({"body": separation}))


        return utils.respond(utils.ok, utils.from_dict_to_object({}))
    @classmethod
    def update_emp_init(cls, dbms, object):
        instance =cls(dbms, object)
        return instance.update_employee()