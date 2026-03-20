import os, subprocess, shutil
from django.core.management import call_command
import psycopg2
from django.db.utils import OperationalError
from controllers.utils import Utils
from controllers.utils.dates import Dates
from services.validation import Validation
from .raw import Raw
# from management.defaults.core.tenant_admin import tenant_admin
# from management.defaults.core.default_company import default_company



utils = Utils()
validation = Validation()
raw = Raw()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw
 
class Services:
    def __init__(self) -> None:
        self.config = raw.get_default_db_config() 
        del self.config["url"]
        
    def check_if_tenant_exists(self, name, email, tpin):
            try:
                with psycopg2.connect(**self.config) as conn:
                    with conn.cursor() as cursor:
                        queries = [
                            {"q": "select 1 from tenant where lower(name) = %s", "params": [name.lower()], "error": f"Client With name '{name}' already used!"},
                            {"q": "select 1 from customer where lower(name) = %s", "params": [name.lower()], "error": f"CST' with name '{name}' already used!"},
                            {"q": "select 1 from customer where lower(email) = %s", "params": [email.lower()], "error": f"CST'Email '{email}' already used!"},
                            {"q": "select 1 from user_pool where lower(name) = %s", "params": [email.lower()], "error": f"UP' Email '{email}' already used!"},
                            {"q": "select 1 from customer where tax_identification_no = %s and tax_identification_no != '1000000000'", "params": [tpin], "error": f"Tax Identification No '{tpin}' already used!"}
                        ]
                        for query in queries:
                            cursor.execute(query["q"], query["params"])
                            if cursor.fetchone():
                                return utils.respond(utils.found, query["error"])
            except psycopg2.Error as e:
                return utils.respond(utils.internal_server_error, f"Database error: {str(e)}")
            except Exception as e:
                return utils.respond(utils.internal_server_error, f"Unexpected error: {str(e)}")
            return utils.respond(utils.ok, "No duplicates found")


    def register_tenant(self, data, dbms):
        self.dbms = dbms
        data = data.body.data
        kyc = data.kyc
        name = kyc.name
        keys = [ "name", "email",  "contact_no", "tax_identification_no",  "physical_address", "country"]
        # validate tenant data
        validate = validation.validate_body_keys(kyc, keys)
        if validate.status != utils.ok:
            return validate
        # check if tenant exists
        tenant_exists = self.check_if_tenant_exists(name,kyc.email, kyc.tax_identification_no)
        if tenant_exists.status != utils.ok:
            return tenant_exists
        
        # create tenant database
        tenant_db = self.create_db_configuration_data(name)
        if tenant_db.status != utils.ok:
            return tenant_db
        
        tenant_as_customer = self.create_tenant_as_admin_customer(kyc)
        if tenant_as_customer.status != utils.ok:
            return tenant_as_customer
        customer = tenant_as_customer.data
        db_info = tenant_db.data
        db_info.customer = customer.id
        create_tenant_db_configs = self.create_tenant_db_configurations(db_info, data)

        if create_tenant_db_configs.status == utils.ok:
            db_info.tenant_id = create_tenant_db_configs.data.id
            db_info.license = data.kyc.license
            license = self.create_tenant_license(db_info)
            return utils.respond(utils.ok, f"""Tenant {name} Created Successfully""")
        
        # if not, delete the customer, db
        delete_customer = self.create_tenant_as_admin_customer(kyc,delete=True)
        return create_tenant_db_configs


    def create_db_configuration_data(self, tenant_name):
        cleaned = utils.replace_character( utils.remove_special_characters(tenant_name), ' ', '').lower()
        usr = utils.remove_special_characters(tenant_name)
        pwd = utils.generate_password(20)
        # con = psycopg2.connect(**self.config)
        return utils.respond(utils.ok, {
            "name": utils.remove_special_characters(tenant_name),
            "db_user": usr,
            "db_password": pwd,
            "db_name": cleaned,
            "db_host": "localhost",
            "db_port": "5432",
            "tenant_url": f"{cleaned}.startappsolutions.com",
            "status": "Initialized",
            "created_on": dates.today(),
            "expiry_date": dates.add_days(dates.today(), 30)
        })

    def create_or_drop_tenant_database(self, tenant_name, is_dropping=False):
        cleaned = utils.replace_character( utils.remove_special_characters(tenant_name), ' ', '').lower()
        usr = utils.remove_special_characters(tenant_name)
        pwd = utils.generate_password(20)
        con = psycopg2.connect(**self.config)
        con.autocommit = True
        cur = con.cursor()
        try:
            if is_dropping:
                cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) " f"FROM pg_stat_activity WHERE pg_stat_activity.datname = '{cleaned}' " f"AND pid <> pg_backend_pid();")
                cur.execute(f"DROP DATABASE IF EXISTS {cleaned};")
                con.commit()
                cur.execute(f"REASSIGN OWNED BY \"{usr}\" TO postgres;")
                cur.execute(f"DROP OWNED BY \"{usr}\";")
                con.commit()
                cur.execute(f"DROP ROLE IF EXISTS \"{usr}\";")
                con.commit()
                return utils.respond(utils.ok, "DB and role dropped successfully!")
            else:
                cur.execute(f'CREATE ROLE "{usr}" WITH LOGIN PASSWORD %s SUPERUSER', (pwd,))
                cur.execute(f"CREATE DATABASE {cleaned} WITH TEMPLATE template  OWNER '{usr}';")
                # subprocess.run(f"pg_dump --schema-only --clean startapp | psql {cleaned}", shell=True)
                con.commit()
                return utils.respond(utils.ok, {
                    "name": utils.remove_special_characters(tenant_name),
                    "db_user": usr,
                    "db_password": pwd,
                    "db_name": cleaned,
                    "db_host": "localhost",
                    "db_port": "5432",
                    "tenant_url": f"{cleaned}.startappsolutions.com",
                    "status": "Initialized",
                    "created_on": dates.today(),
                    "expiry_date": dates.add_days(dates.today(), 30)

                })
        except Exception as e:
            con.rollback()
            return utils.respond(utils.internal_server_error, f"Error: {str(e)}")
        finally:
            cur.close()
            con.close()

    def create_tenant_db_configurations(self, db_config, data):
        db_config.customer = data.kyc.name
        db_config.total_users = data.totals.additional_users.qty
        db_config.total_storage = data.totals.additional_storage.qty
        db_config.subscription_frequency = data.totals.freq
        db_config.status = "Initialized"
        db_config.modules = [{"module_price": mp} for mp in data.selected_modules]
        
        return self.dbms.create("Tenant", db_config, privilege=True)
        
       
    def create_tenant_license(self, data):
        from controllers.tenant import Tenant_Controller
        tc = Tenant_Controller()
        license = tc.create_tenant_license(data.name, data.license)
        update = tc.update_tenant_details(data.name, license)
        return license

    def create_tenant_subscription(self,data):
        from controllers.tenant import Tenant_Controller
        tc = Tenant_Controller()
        packages = []
        xt_packages = vars(data.packages)
        for l, v in xt_packages.items():
            for p_l, p_v in vars(v).items():
                packages.append(p_v.name)
        data.tenant_url = data.kyc.domain
        data.tenant = data.kyc.name
        data.packages = packages
        del data.license
        del data.kyc
        subscription = tc.create_tenant_subscription(data)
        return subscription

    def create_tenant_as_admin_customer(self,data, delete=False):
        data.status = "Active"
        data.registration_type = data.customer_type
        data.skip_submission_for_smart_invoice = True
        if self.dbms.tenant_db:
            if not delete:
                return self.dbms.create("Customer",data, privilege=True)
            else:
                customer = self.dbms.get_django_object("Customer",data.name)
                if customer.status == utils.ok:
                    return self.dbms.delete("Customer",[customer.data.id], privilege=True)
        else:
            utils.throw("Failed to connect to target tenant Database.")
            
    def migrate_tenant(self, data=None, tenant_url=None):
        tenant = tenant_url if tenant_url else data.xtenant
        if not tenant:
            return utils.respond(utils.not_found, f"xtenant key missing in the body!")
        include_in_list = raw.add_tenant_db_to_db_list(tenant)
        include_in_list.status == utils.ok or throw(include_in_list.get("error_message"))
        tenant_db = include_in_list.get("data").get("NAME")
        self.migrate(tenant_db,apps=data.apps or [], fake=data.fake)
        return utils.respond(utils.ok, f"{tenant_db} Migrated Successfully.")

    def full_migration(self, data):
        try:
            self.empty_apps()
            self.make_migrations()
            tenant_data = raw.get_tenant_configurations(data.body.xtenant)
            if tenant_data.get("status") == utils.ok:
                self.migrate(tenant_data.get("data").get("dbname"))
            
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{e}")
        return utils.respond(utils.ok, f"Migration for xtenant '{data.body.xtenant}' completed successfully!")

    def empty_apps(self):
        from multitenancy.settings import INSTALLED_APPS
        try:
            apps = [app.split('.')[-1] for app in INSTALLED_APPS if app.split('.')[-1] not in ["auth","admin","contenttypes","sessions","messages","staticfiles"]]
            apps.append("cron")
            apps.append("client_app")
            apps.append("management")
            call_command('makemigrations', '--empty', *apps)
        except Exception as e:
            throw(e)
        
    def make_migrations(self):
        try:
            call_command('makemigrations')
        except Exception as e:
            throw(e)
        
    def migrate(self, database, fake=False, apps = []):
        try:
            call_command('migrate', *apps, database=database, fake_initial=fake, fake=fake)
            return utils.respond(utils.ok, "Migration successful")
        except Exception as e:
            pp("Migration error:",str(e))

    def delete_module_migrations(self,data):
        module_path = os.path.join(utils.get_path_to_base_folder(), f"""client_app/{data.body.module}""")
        successful = []
        failed = []
        for root, dirs, files in os.walk(module_path, topdown=False):
            for name in dirs:
                if name == "migrations":
                    folder_to_delete_path = os.path.join(root, name)
                    try:
                        shutil.rmtree(folder_to_delete_path)
                        successful.append(folder_to_delete_path)
                    except OSError as e:
                        failed.append(folder_to_delete_path)
        return utils.respond(utils.ok, {"successful":successful, "failed": failed})

    # to delete module tables
    def get_models(self, module_path):
        pass
        # medels = utils.get____module_apps()
        # models_list = []
        # for root, _, files in os.walk(module_path):
        #     for file in files:
        #         if file == 'models.py':
        #             models_file_path = os.path.join(root, file)
        #             with open(models_file_path, 'r') as f:
        #                 file_contents = f.read()
        #                 try:
        #                     # Execute the file contents in a local namespace
        #                     local_namespace = {}
        #                     exec(file_contents, local_namespace)
        #                     for comp in local_namespace.values():
        #                         print(type(comp),comp.name)
        #                     models_in_file = [model for model in local_namespace.values() if isinstance(model, models.Model)]
        #                     models_list.extend(models_in_file)
        #                 except Exception as e:
        #                     print("Error executing file:", e)
        # return models_list
    
    def make_module_migrations(self, data):
        pass


    def delete_module_tables(self, data):
        # module = data.body.module.lower()
        # xtenant = data.body.xtenant
        # all_modules = utils.get_module________apps(group_by_module=True,only_models=True,fetch_model_objects=True)
        # if all_modules.get("data"):
        #     model_objects = all_modules.get("data").get(module)
        #     if len(model_objects):
        #         models = []
        #         for mo in model_objects:
        #             drop_table = raw.drop_model_table(xtenant, mo._meta.db_table)
        #             models.append(drop_table)
        #         return utils.respond(utils.ok, models)
        

        successful = []
        failed = []
        return
        models = self.get_models(module_path)
        return
        for root, dirs, files in os.walk(module_path, topdown=False):
            for name in dirs:
                if name == "migrations":
                    folder_to_delete_path = os.path.join(root, name)
                    try:
                        shutil.rmtree(folder_to_delete_path)
                        successful.append(folder_to_delete_path)
                    except OSError as e:
                        failed.append(folder_to_delete_path)
        return utils.respond(utils.ok, {"successful":successful, "failed": failed})


    # dealing with default data 
    def create_tenant_default_data(self,dbms,  data):
        from management.data_controller import Data_Controller
        xtenant = data.xtenant
        if not xtenant:
            return utils.respond(utils.not_found, f"xtenant key missing in the body!")
        include_in_list = raw.add_tenant_db_to_db_list(xtenant)
        include_in_list.status == utils.ok or throw(include_in_list.error_message)
        tenant = include_in_list.data.TENANT_INFO
        
        dc = Data_Controller(dbms)
        tenant_data = dc.admin_dbms.get_doc("Tenant", tenant.db_name, privilege=True, fetch_by_field="db_name")
        if tenant_data.status == utils.no_content and tenant.db_name == self.config.dbname:
            tenant.name = "ECZ"
            tenant.expiry_date = dates.add_days(dates.today(),365*2)
            tenant.total_users = 100
            tenant.total_storage = 100
            tenant.subscription_frequency = "Annually"
            tenant_data = dc.dbms.create("Tenant", tenant, privilege=True, fetch_if_exists=True)
        if tenant_data.status == utils.ok:
            tenant = tenant_data.data
        else:
            return utils.respond(utils.unprocessable_entity, f"Failed to fetch admin tenant for default data creation:{tenant_data.error_message}")
        tenant.is_admin = tenant.db_name == self.config.dbname
        create_defaults = dc.create_default_data(tenant)
        return utils.respond(utils.ok, {"message":f"Default data creation was successful for '{ tenant.tenant_url}'","data": create_defaults})
