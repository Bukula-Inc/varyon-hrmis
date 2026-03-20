from middleware.middleware import get_db_config_for_domain
from controllers.utils import Utils

utils = Utils()
throw = utils.throw
pp = utils.pretty_print


class TenantRouter:
    def db_for_read(self, model, **hints):
        db_name = get_db_config_for_domain()
        if db_name:
            return db_name
        
        
    def db_for_write(self, model, **hints):
        db_name = get_db_config_for_domain()
        if db_name:
            return db_name

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
    
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db != obj2._state.db:
            obj2._state.db = obj1._state.db
        return True