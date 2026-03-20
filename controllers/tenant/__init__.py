from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.dbms import DBMS
# from controllers.core_functions.accounting import Core_Accounting
from services.raw import Raw
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class Tenant_Controller:
    def __init__(self):
        self.dbms = DBMS(init_admin=True)
        self.admin_db_name = self.dbms.tenant_db
        self.admin = self.dbms.get_administrator().get("data",None)
        self.raw = Raw()

    def get_admin_dbms(self):
        return self.dbms
        
    def get_background_jobs(self,filters={}):
        job = self.dbms.get_list("Background_Job", filters=filters, privilege=True,as_dict=True,lower_dict_keys=True)
        return job 
    
    def get_background_job_content(self,job_name):
        job = self.dbms.get_doc("Background_Job",job_name,privilege=True)
        return job 
    
    def is_background_job_idle(self,job_name):
        job = self.dbms.get_doc("Background_Job",job_name,privilege=True)
        return job and job.status == utils.ok and job.data.status == "Idle"
    
    def update_background_job_status(self,job_name, status):
        job = self.dbms.get_doc("Background_Job",job_name,privilege=True)
        if job.status == utils.ok:
            data = job.data
            data.status = status
            update = self.dbms.update("Background_Job",data,privilege=True)
            return update 
        return utils.respond(utils.internal_server_error, "Failed to Update Background Job Status")

    def get_unprocessed_tenants(self):
        return self.dbms.get_tenants(filters={"status": "Initialized"})
    
    def get_tenants(self, filters={}):
        return self.dbms.get_tenants(filters=filters)
    
    def get_tenant(self, tenant, fetch_by_field=None):
        return self.dbms.get_doc("Tenant", tenant, fetch_by_field=fetch_by_field, privilege=True)
    
    def get_billing_config(self):
        return self.dbms.get_doc("Billing_Config", "Billing Config", privilege=True)
    
    def get_module_pricing(self):
        return self.dbms.get_list("Module_Pricing", privilege=True)
    
    def get_module_pricing_package(self, name):
        return self.dbms.get_doc("Module_Pricing", name, privilege=True)

    def connect_tenant(self, tenant_url, skip_user_validation=False):
        connect = self.raw.add_tenant_db_to_db_list(tenant_url)
        if connect.status == utils.ok:
            return DBMS(utils.from_dict_to_object({ "host": tenant_url, "tenant_db":tenant_url }), skip_user_validation=skip_user_validation)
        return False
    
    def create_tenant_license(self, tenant, license):
        return self.dbms.create("License", utils.from_dict_to_object({"tenant":tenant,"content":license }), privilege=True)
    

    def update_tenant_details(self, tenant, license):
        tenant_data = self.dbms.get_doc("Tenant", tenant, privilege=True)
        if tenant_data.status == utils.ok:
            tnt = tenant_data.data
            tnt.api_key = utils.generate_client_api_key({"tnt":f"{tnt.db_name}&%{tnt.id}"})
            if license.status == utils.ok:
                tnt.license_no = license.data.name
            return self.dbms.update("Tenant", tnt, privilege=True)

    
    def create_tenant_subscription(self, data, is_new_tenant = True):
        tenant = self.get_tenant(data.tenant)
        lst = []

        if tenant.status == utils.ok:
            tnt = data
            package_details = []
            if is_new_tenant:
                sub = utils.from_dict_to_object({
                    "tenant": tnt.name,
                    "is_active": 1,
                    "docstatus":1,
                    "status":"Submitted",
                    "total_users": data.additional_users,
                    "total_storage": data.additional_storage,
                    "quotation": self.create_subscription_quotation(data),
                    "payment_reference": None,
                    "subscription_from": dates.today(),
                    "subscription_to": dates.add_days(dates.today(),30 if data.frequency == "Monthly" else 365),
                    "frequency": data.frequency,
                    "subscription_modules": [],
                })
                
                for pack in data.packages:
                    pkg_data = self.get_module_pricing_package(pack)
                    if pkg_data.get("status") == utils.ok:
                        p = utils.from_dict_to_object(pkg_data.get("data"))
                        package_details.append(p)
                        for pm in p.price_modules:
                            lst.append(pm.module)
                unq = list(set(lst))
                for mod in unq:
                    sub.subscription_modules.append({ "module_name" :mod })
                create = self.dbms.create("Subscription", sub, privilege=True)
                return create

        return utils.respond(utils.internal_server_error, "An error occurred white subscribing tenant")
    
    def create_subscription_quotation(self,data):
        # core = Core_Accounting(self.dbms, self.admin.id)
        # core.calculate_invoice_totals
        return None