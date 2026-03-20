from controllers.utils import Utils
from controllers.core_functions.hr.hr_extension import HR_Extension
from controllers.core_functions.payroll.payroll_extension import Payroll_Extension

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

class Staff_Dashboard:        

    def __init__(self, dbms, obj) -> None:
        self.dbms = dbms
        self.obj = obj
        self.settings = {}
        self.hr = HR_Extension(dbms,obj)
        self.payroll = Payroll_Extension(dbms, self.obj)

    @classmethod
    def dashboard(cls, dbms, obj):
        instance = cls( dbms, obj)
        return utils.respond(utils.ok,{
            "hr": instance.hr.get_staff_hr_related_stats(dbms.current_user.name),
            "payroll": instance.payroll.get_staff_payroll_related_stats(dbms.current_user.name)
        })