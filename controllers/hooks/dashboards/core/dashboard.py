from controllers.utils import Utils
from controllers.utils.dates import Dates
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw


# TAX INVOICE DASHBOARD
class Core_Dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.settings = self.dbms.system_settings
        self.defaults = self.settings.accounting_defaults
        self.default_company = self.settings.linked_fields.default_company

    @classmethod
    def core(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        return utils.respond(utils.ok,{
            "total_countries": cls.get_total_countries(cls).get("data"),
            "total_currencies": cls.get_total_currencies(cls).get("data"),
            "total_users": cls.get_total_users(cls).get("data"),
            "sectors": cls.get_sectors(cls).get("data"),
            "industries": cls.get_total_industries(cls).get("data"),
            "user_roles": cls.get_user_roles(cls).get("data"),
            "workflows": cls.get_workflows(cls).get("data"),
            "data_imports": cls.get_data_imports(cls).get("data"),
            "naming_series": cls.get_naming_series(cls).get("data"),
        })
    def get_total_countries(self):
        total = 0
        countries = self.dbms.get_list("Country",user=self.user, only_count=True)
        if countries.get("status") == utils.ok:
            total = countries.get("data")
        return utils.respond(utils.ok,total)
    
    def get_total_currencies(self):
        total = 0
        currencies = self.dbms.get_list("Currency",user=self.user, only_count=True)
        if currencies.get("status") == utils.ok:
            total = currencies.get("data")
        return utils.respond(utils.ok,total)
    
    def get_total_users(self):
        total = 0
        users = self.dbms.get_list("Lite_User",user=self.user, only_count=True)
        if users.get("status") == utils.ok:
            total = users.get("data")
        return utils.respond(utils.ok,total)
    
    def get_sectors(self):
        total = 0
        sectors = self.dbms.get_list("Sector",user=self.user, limit=9)
        if sectors.get("status") == utils.ok:
            total = sectors.get("data").get("rows")
        return utils.respond(utils.ok,total)
    
    def get_total_industries(self):
        total = 0
        industries = self.dbms.get_list("Industry",user=self.user, limit=9)
        if industries.get("status") == utils.ok:
            total = industries.get("data").get("rows")
        return utils.respond(utils.ok,total)
    
    def get_user_roles(self):
        total = 0
        user_roles = self.dbms.get_list("Role",user=self.user, limit=8)
        if user_roles.get("status") == utils.ok:
            total = user_roles.get("data").get("rows")
        return utils.respond(utils.ok,total)
    
    def get_workflows(self):
        total = 0
        workflows = self.dbms.get_list("Workflow",user=self.user, limit=8)
        if workflows.get("status") == utils.ok:
            total = workflows.get("data").get("rows")
        return utils.respond(utils.ok,total)
    
    def get_data_imports(self):
        total = []
        di = self.dbms.get_list("Data_Importation",user=self.user, limit=8)
        if di.get("status") == utils.ok:
            total = di.get("data").get("rows")
        return utils.respond(utils.ok,total)
    
    def get_naming_series(self):
        total = []
        series = self.dbms.get_list("Series",user=self.user, limit=8)
        if series.get("status") == utils.ok:
            total = series.get("data").get("rows")
        return utils.respond(utils.ok,total)