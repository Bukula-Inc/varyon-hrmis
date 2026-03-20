from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.object_generator import Generate_Object, Extract_Object
from controllers.core_functions.hr import Core_Hr
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Staff_Payslip_Statistics:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_30_days = dates.add_days(dates.today(), -30)
        self.hr = Core_Hr(dbms,object.user,object)
        self.employee = None
        system_settings =  self.dbms.system_settings
        if system_settings:
            self.settings = utils.from_dict_to_object(system_settings)
            self.defaults =  self.settings.accounting_defaults
            comp = getattr(self.defaults, self.settings.default_company)
            cd = self.dbms.get_doc("Company",comp.name,fetch_linked_fields=True,privilege=True)
            cd.status == utils.ok or throw("Failed to fetch company info!")
            self.company = utils.from_dict_to_object(cd.data)
        

    @classmethod
    def staff_payslip_statistics(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        employee = cls.hr.get_list("Employee", filters={"user":dbms.current_user.name}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if employee:
                employee = employee[0]
        employee_data = {}

        emp = cls.hr.get_payslip_analytics(employee.id)
        if emp:
            employee_data = emp 
        return utils.respond(utils.ok, employee_data)