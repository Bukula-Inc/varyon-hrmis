from controllers.utils import Utils
from controllers.utils.dates import Dates
from management.data_controller import Data_Controller
from services import Services
from services.raw import Raw
from controllers.mailing import Mailing
from controllers.mailing.templates.default_template import Default_Template
from cron.controller.data_importation import Data_Importation
import psycopg2, subprocess, shutil
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw
services = Services()

raw = Raw()

class Controller_Background_Jobs:
    def __init__(self, dbms=None) -> None:
        self.dbms = dbms
        self.config = raw.get_default_db_config() 
        del self.config["url"]
        self.psql_path = shutil.which("psql")
    def __dump_db(self):
        self.dump_file_path = f"/tmp/startapp/template_dump.sql"
        self.pg_dump_command_path = shutil.which('pg_dump')
        if self.pg_dump_command_path is None:
            return utils.respond(utils.unprocessable_entity, "pg_dump command not found")
        
        # Explicitly create the file to avoid permission issues
        try:
            with open(self.dump_file_path, 'w') as f:
                pass
        except Exception as e:
            return utils.respond(utils.unprocessable_entity, f"Error creating dump file: {str(e)}")
        
        dump_cmd = [self.pg_dump_command_path, "-h", "localhost", "-U", "postgres", "-s", "-f", self.dump_file_path, self.config.dbname]
        env = {"PGPASSWORD": self.config.password}
        
        try:
            result = subprocess.run(dump_cmd, shell=False, capture_output=True, text=True, env=env)
            if result.returncode != 0:
                return utils.respond(utils.unprocessable_entity, f"{result.stderr}")
            return utils.respond(utils.ok, f"{result}")
        except Exception as e:
            return utils.respond(utils.unprocessable_entity, f"Error executing pg_dump: {str(e)}")


    # create the db role
    def __create_db_role(self, tenant):
        try:
            conn = psycopg2.connect(**self.config)
            conn.autocommit = True
            cur = conn.cursor()
            try:
                cur.execute(f"CREATE ROLE \"{tenant.db_user}\" WITH LOGIN PASSWORD '{tenant.db_password}' SUPERUSER")
                conn.commit()
                return utils.respond(utils.ok, "Role Created Successfully")
            except psycopg2.Error as e:
                return utils.respond(utils.internal_server_error, f"Failed to create role: {e}")
            finally:
                cur.close()
                conn.close()
        except Exception as e:
            pp(str(e))
            return utils.respond(utils.internal_server_error, f"An error occurred while creating the role:{str(e)}")
    
    # create the db
    def __create_db(self, tenant):
        try:
            conn = psycopg2.connect(**self.config)
            conn.autocommit = True
            cur = conn.cursor()

            # Create the database using psycopg2
            cur.execute(f"CREATE DATABASE \"{tenant.db_name}\" OWNER \"{tenant.db_user}\"")
            cur.close()
            conn.close()
            # Call the restore function after creating the DB
            return self.__restore_db_dump(self, tenant)
        except psycopg2.Error as e:
            drop = self.__drop_db_and_role(self, tenant)  # Clean up if there's an error
            return utils.respond(utils.internal_server_error, f"Failed to create DB: {e}")
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"An error occurred while creating the database: {str(e)}")
    
    # apply the dump on the new db
    def __restore_db_dump(self, tenant):
        restore_cmd = [self.psql_path, "-h", "localhost", "-U", tenant.db_user, "-d", tenant.db_name]
        try:
            env = {"PGPASSWORD": tenant.db_password}
            with open(self.dump_file_path, 'r') as dump_file:
                result = subprocess.run(restore_cmd, stdin=dump_file, capture_output=True, text=True,env=env)
            if result.returncode != 0:
                drop = self.__drop_db_and_role(self, tenant)
                return utils.respond(utils.internal_server_error, f"Failed to restore db:{result.stderr}")
            return utils.respond(utils.ok, "DB Created and Restored Successfully")
        except Exception as ex:
            return utils.respond(utils.internal_server_error, f"An error occurred while restoring DB: {str(ex)}")
    
    # should anything fail, drop the db and role to start afresh
    def __drop_db_and_role(self, tenant):
        try:
            con = psycopg2.connect(**self.config)
            con.autocommit = True
            cur = con.cursor()
            cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) " f"FROM pg_stat_activity WHERE pg_stat_activity.datname = '{tenant.db_name}' " f"AND pid <> pg_backend_pid();")
            cur.execute(f"DROP DATABASE IF EXISTS {tenant.db_name};")
            con.commit()
            cur.execute(f"REASSIGN OWNED BY \"{tenant.db_user}\" TO postgres;")
            cur.execute(f"DROP OWNED BY \"{tenant.db_user}\";")
            con.commit()
            cur.execute(f"DROP ROLE IF EXISTS \"{tenant.db_user}\";")
            con.commit()
            return utils.respond(utils.unprocessable_entity, f"DB and role dropped successfully")
        except Exception as ex:
            con.rollback()
            return utils.respond(utils.internal_server_error, f"Error: {str(ex)}")


    # initialize db creation process
    def __clone_template_db(self, tenant):
        try:
            new_role = self.__create_db_role(self,tenant)
            if new_role.status != utils.ok:
                return new_role
            new_db = self.__create_db(self,tenant)
            if new_db.status != utils.ok:
                return new_db
            return new_db
        except Exception as ex:
            pp("ROLE CREATION FAILED", str(ex))
            return utils.respond(utils.internal_server_error, f"DB Error: {str(ex)}")
            
                
    # create super admin account
    def create_super_admin_account(self, dbms, tenant):
        customer = tenant.linked_fields.customer
        modules = ""
        if tenant.modules and len(tenant.modules) > 0:
            for md in tenant.modules:
                modules += f""" <li> <div>{md.module_price}</div> </li>"""
        content = f"""
            <div style="width:100%; font-family: Helvetica, sans-serif; font-size: 12px; line-height: 1.3rem;">
                <h5 style="font-size: 25px; margin: 3px 0;">Hello {customer.name} </h5>
                <p style="font-size: 12px;">
                    <div style="font-size: 20px; font-weight: bolder; margin: 20px 0;">Congratulations!</div>
                    Your trial account with ECZ HRMIS has been created successfully! Your account will operate in trial version for the period of 
                    <div style="background-color: #151030; color: white; border-radius: 10px; padding: 10px 20px;width: 70px;margin: 10px 0;font-weight: bolder;text-align: center;">30 Days</div>
                    Below are your subscription details
                </p>
                <hr>
                <div>
                    <div style="font-size: 20px; font-weight: bolder;">Subscription Modules</div>
                    <ul style="list-style:circle;"> {modules} </ul>
                </div>
                <div>
                    To access the your portal, visit 
                    <a href="https://hrmis.exams-council.org.zm" style="background-color: #e8b3e8; color:white; border-radius: 5px; padding: 3px 5px; font-weight: bolder; font-size: 13px; text-decoration: none; margin: 0 5px;">
                        https://hrmis.exams-council.org.zm
                    </a> 
                    then click Sign In, provide the credentials sent to your second email as required by the system. <br>
                    Proceed to creating other users if necessary. <br>
                    Note: This is a super admin account.
                </div>
            </div>
        """
        mailing  = Mailing(dbms,None)
        try:
            # create super user for this tenant
            mail = tenant.linked_fields.customer.email
        
            new_user = dbms.create("Lite_User", utils.from_dict_to_object({
                "status": "Active",
                "name": mail,
                "first_name": tenant.name,
                "middle_name": "",
                "last_name": "",
                "email": mail,
                "contact_no": "0",
                "main_role": "Super Admin",
                "default_company": tenant.name
            }), privilege=True)
            if new_user.status == utils.ok:
                send = mailing.send_mail(mail,"Company Account Creation",Default_Template.template(content,"Company Account Creation"))
                return send
            else:
                return new_user
        except Exception as e:
            err = f"FAILED TO CREATE TENANT SUPER ADMIN ACCOUNT:{str(e)}"
            pp(err)
            return utils.respond(utils.internal_server_error, err)

    # MANAGE OVERDUE TRANSACTIONS
    @classmethod
    def initialize_tenants(cls, dbms, tc=None, all_tenants=[]):
        cls.__init__(cls,dbms)
        dump_db = cls.__dump_db(cls)
        if dump_db.status == utils.ok:
            tenants = tc.get_unprocessed_tenants()
            if tenants.status == utils.ok and tenants.data and len(tenants.data) > 0:
                data = tenants.data
                for tenant in data:
                    try:
                        clone_db = cls.__clone_template_db(cls, tenant)
                        if clone_db.status == utils.ok:
                            tenant_dbms = None
                            try:
                                tenant_dbms = tc.connect_tenant(tenant.db_name, skip_user_validation=True)
                            except Exception as e:
                                pp(f"AN ERROR OCCURRED WHILE CONNECTING TENANT DB:{str(e)}")
                            if not tenant_dbms:
                                pp("FAILED TO CONNECT TO TENANT")
                                drop = cls.__drop_db_and_role(cls,tenant)
                            else:
                                dc = Data_Controller(tenant_dbms)
                                try:
                                    migrate = services.migrate(tenant.db_name, fake=True)
                                    pp("MIGRATION CONCLUDED", migrate.status)
                                    if migrate.status == utils.ok:
                                        defaults = dc.create_default_data(tenant)
                                        if defaults.status == utils.ok:
                                            system_settings = tenant_dbms.get_system_settings()
                                            if system_settings.status == utils.ok:
                                                tenant_dbms.system_settings = system_settings.data
                                                tenant_dbms.host = "startappsolutions.com"
                                            else:
                                                pp(f"FAILED TO FETCH SYSTEM SETTINGS FOR TENANT {tenant.name}: {migrate}")
                                            super_user =  cls.create_super_admin_account(cls, tenant_dbms, tenant)
                                            pp(super_user)
                                        else:
                                            pp(f"DEFAULT CREATION FAILED FOR THE NEW TENANT {tenant.name}: {migrate}")
                                    else:
                                        drop = cls.__drop_db_and_role(cls, tenant)
                                        pp("||||||||||||| DB MIGRATION FAILED ||||||||||||||")
                                except Exception as e:
                                    pp(f"||||||||||||||||||||||| AN ERROR OCCURRED WHILE PREPARING TENANT:{str(e)}")
                                if defaults.status == utils.ok:
                                    tenant.status = "Active"
                                    update = dbms.update("Tenant", tenant, update_submitted=True, privilege=True)
                        else:
                            pp("|||||||||||||||||  TEMPLATE CLONING FAILED",clone_db.error_message)
                    except Exception as e:
                        pp(f"SOMETHING TERRIBLY WENT WRONG:{str(e)}")
        else:
            pp("PG DUMP FAILED:", dump_db.error_message,"================")

        

    # MANAGE AUTO INVOICING
    @classmethod
    def auto_invoicing(cls, dbms=None):
        pass


    @classmethod
    def initialize_data_importation(cls, dbms, tc):
        di = Data_Importation.initialize_data_importation(dbms,tc)