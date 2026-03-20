from controllers.utils import Utils
from controllers.utils.dates import Dates
from services import Services
from controllers.tenant import Tenant_Controller

utils = Utils()
dates = Dates()
services = Services()
tc = Tenant_Controller()

pp = utils.pretty_print
throw = utils.throw

class Tenant_Services:
    @classmethod
    def init_tenant_services(cls):
        tenants = tc.get_tenants()
        pp(tenants)

      