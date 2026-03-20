
import psycopg2
from django.db import connections
from multitenancy.settings import DATABASES, TENANT_ADMIN
from controllers.utils import Utils
from controllers.caching import Caching
utils = Utils()

pp = utils.pretty_print
throw = utils.throw

class Raw:
    def __init__(self) -> None:
        self.admin_db_config = DATABASES.get("default")
        self.tenant_admin = TENANT_ADMIN
        self.admin_url = self.tenant_admin.get("DOMAIN")

    def get_default_db_config(self):
        default_db = DATABASES.get("default")
        connection_params = {
            "dbname": default_db.get("NAME"),
            "user": default_db.get("USER"),
            "password": default_db.get("PASSWORD"),
            "host": default_db.get("HOST"),
            "port": default_db.get("POST"),
            "url": TENANT_ADMIN.get("DOMAIN")
        }
        return utils.from_dict_to_object(connection_params)

    def connect_to_admin(self):
        config = self.get_default_db_config()
        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cursor:
                    return utils.respond(utils.ok, cursor)
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"Failed to connect to admin: {e}")
        
    def connect_tenant(self,host=TENANT_ADMIN.get("DOMAIN"),admin=False):
        from controllers.dbms import DBMS
        if admin:
            host = TENANT_ADMIN.get("DOMAIN")
        dbms = DBMS(init_admin=True,skip_user_validation=host==TENANT_ADMIN.get("DOMAIN"))
        return dbms
    
    def get_tenant_configurations(self, tenant, fetch_by_db_name=True, fetch_by_db_url=False):
        self.caching = Caching.init()
        cached_tenant =self.caching.get_tenant_db_info(tenant)
        data = utils.from_dict_to_object()
        if cached_tenant:
            data = cached_tenant
        else:
            config = self.get_default_db_config()
            if tenant == TENANT_ADMIN.get("DB"):
                self.caching.cache_tenant_db_info( config)
                data = config
            try:
                if config.get("url"):
                    del config["url"]
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cursor:
                        q = ""
                        if fetch_by_db_name:
                            q = "select * from tenant where db_name = %s"
                        else:
                            q = "select * from tenant where name = %s"
                        cursor.execute(q, [tenant])
                        db_conf = cursor.fetchone()
                    if db_conf:
                        columns = [col[0] for col in cursor.description]
                        values = [str(val).strip() if val is not None else None for val in db_conf]
                        data = utils.from_dict_to_object(dict(zip(columns, values)))
                    else:
                        if tenant == TENANT_ADMIN.get("DB"):
                            data = utils.from_dict_to_object({
                                "db_name": config.dbname,
                                "db_user": config.user,
                                "db_password": config.password,
                                "db_host": config.host,
                                "db_port": config.port,
                            })
                        else:
                            return utils.respond(utils.unprocessable_entity, "DB configurations not found for the selected tenant.")

                # pp("TENANT WAS FETCHED FROM THE DATABASE====>>><<<<<")
            except Exception as e:
                return utils.respond(utils.internal_server_error, f"{e}")
            self.caching.cache_tenant_db_info(data)
        if data:
            config = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': data.get("db_name"),
                'USER': data.get("db_user"),
                'PASSWORD': data.get("db_password"),
                'HOST': data.get("db_host"),
                'PORT': data.get("db_port") or 5432,
                'ATOMIC_REQUESTS': False,
                'AUTOCOMMIT': True,
                'CONN_MAX_AGE': 0,
                'CONN_HEALTH_CHECKS': False,
                'OPTIONS': {},
                'TIME_ZONE': None,
                'TEST': {
                    'CHARSET': None,
                    'COLLATION': None,
                    'MIGRATE': True,
                    'MIRROR': None,
                    'NAME': None
                },
                "TENANT_INFO": data
            }
            return utils.respond(utils.ok, config)
        return utils.respond(utils.not_found, None)




    def add_tenant_db_to_db_list(self, tenant=TENANT_ADMIN.get("DB")):
        config = self.get_tenant_configurations(tenant, fetch_by_db_name=True)
        if config.get("status") == utils.ok:
            cf = utils.from_dict_to_object(config.get("data"))
            if cf.get("TENANT_INFO"):
                del cf["TENANT_INFO"]
            if not cf.get("NAME"):
                return utils.respond(utils.unprocessable_entity, f"Failed to properly fetch config for tenant db: {tenant}")
            if not connections.databases.get(cf.get("NAME")):
                connections.databases[cf.get("NAME")] = cf
            return config
        else:
            return utils.respond(utils.internal_server_error, f"Failed to add DB to the list: {config.get('error_message') or 'Database configurations not found!!'}")
        

    def drop_model_table(self, tenant, table_name):
        add_tenant = self.add_tenant_db_to_db_list(tenant)
        config = add_tenant.get("data")
        del config["TENANT_INFO"]
        if add_tenant.get("status") == utils.ok:
            try:
                with psycopg2.connect(
                    dbname=config.get("NAME"), 
                    user=config.get("USER"),
                    password = config.get("PASSWORD"),
                    host = config.get("HOST"),
                    port = config.get("PORT")
                ) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(f"DROP  TABLE IF EXISTS {table_name} CASCADE;")
                        conn.commit()
                        # cursor.close()
                        # conn.close()
                        return utils.respond(utils.ok, f"{table_name} Dropped successfully.")
            except Exception as e:
                return utils.respond(utils.internal_server_error, f"{e}")
            
        else:
            return add_tenant