from controllers.core_functions.core import Core
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

class Data_Importation:
    def __init__(self) -> None:
        self.admin_dbms = tc.get_admin_dbms()
        self.admin = None
        admin = self.admin_dbms.get_administrator()
        if admin.status == utils.ok:
            self.admin = admin.data
        self.job = "Data Importation"
    @classmethod
    def init(cls):
        cls.__init__(cls)
        if tc.is_background_job_idle(cls.job):
            update = tc.update_background_job_status(cls.job, "Running")
            if update.status == utils.ok:
                data_importation = cls.admin_dbms.get_list("Data_Importation", filters={"status":"Submitted"}, privilege=True, fetch_linked_tables=True, fetch_linked_fields=False, limit=1)
                # tenants = tc.get_tenants()
                # if tenants.status == utils.ok:
                #     for tenant in tenants.data:
                #         # pp(tenant.name)
                #         pass
                if data_importation and data_importation.status == utils.ok:
                    core = Core(cls.admin_dbms,cls.admin.id)
                    for data in data_importation.data.rows:
                        core.start_data_importation(data)
                else:
                    pp(data_importation.error_message)
            update = tc.update_background_job_status(cls.job, "Idle")

            