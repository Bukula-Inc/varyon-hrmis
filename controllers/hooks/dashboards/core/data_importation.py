
# from controllers.core_functions.accounting import Core_Accounting
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.object_generator import Generate_Object, Extract_Object
# from controllers.dbms import DBMS
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw


# TAX INVOICE DASHBOARD
class Data_Importation_Dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        system_settings = self.dbms.get_system_settings()
        # self.core = Core_Accounting(dbms, self.user, self.object)
        if system_settings.get("status") == utils.ok:
            self.settings = Generate_Object(system_settings.get("data"))
            self.defaults = self.settings.accounting_defaults
            comp = getattr(self.defaults, self.settings.default_company)
            cd = self.dbms.get_doc("Company",comp.name,fetch_linked_fields=True,privilege=True)
            cd.get("status") == utils.ok or throw("Failed to fetch company info!")
            self.company = Generate_Object(cd.get("data"))

    @classmethod
    def dashboard(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        imports = dbms.get_list("Data_Importation",limit=12,user=cls.user)
        if imports.get("status") == utils.ok:
            return utils.respond(utils.ok, imports.get("data").get("rows"))
        return imports