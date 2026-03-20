from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.object_generator import Generate_Object, Extract_Object
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw


# TAX INVOICE DASHBOARD
class Payroll_Processor:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.system_settings()
        if system_settings.status == utils.ok:
            self.settings = utils.from_dict_to_object(system_settings.data)
            self.defaults = self.settings.accounting_defaults
            comp = getattr(self.defaults,self.settings.default_company)
            cd = self.dbms.get_doc("Company",comp.name,fetch_linked_fields=True,privilege=True)
            cd.status == utils.ok or throw("Failed to fetch company info!")
            self.company = utils.from_dict_to_object(cd.data)

    @classmethod
    def payroll_history(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        res = []
        recent_payments_data = cls.dbms.get_list("Payroll_Processor",user=cls.user,limit=11,filters={"docstatus":1})
        if recent_payments_data.status == utils.ok:
            res = recent_payments_data.data.rows

        return utils.respond(utils.ok,res)
    
    