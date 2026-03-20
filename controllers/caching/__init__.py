from django.core.cache import caches
from controllers.utils import Utils
import pickle, json
utils = Utils()
pp = utils.pretty_print
throw = utils.throw
class Caching:
    def __init__(self):
        self.CACHING_EXPIRATION_TIME = 1000
        self.CACHING_EXPIRATION_TIME_FORM_MODELS = 1000
        self.cache  = None

    @classmethod
    def init(cls):
        instance = cls()
        instance.cache = caches["default"]
        return instance

    def get_cached_keys(self):
        return self.cache.keys('*')
    

    def clear_tenant_cache(self, tenant):
        try:
            self.cache.delete(tenant)
        except Exception as e:
            print(f"============================> Cache Clearing Failed:{ str(e)} <============================")

    def init_caching(self, tenant=None):
        defaults = {
            "tenant_info": {},
            "background_job_info": {},
            "user_pool_info": {},
            "models": {},
        }
        for key, value in defaults.items():
            if not self.cache.get(key):
                self.cache.set(key, value, self.CACHING_EXPIRATION_TIME)

    def cache_tenant_info(data):
        pass


    # DB CACHING
    def cache_tenant_db_info(self, data):
        try:
            name = data.get("db_name")
            if name:
                db_info = self.cache.get("db_info")
                if not db_info:
                    db_info = {f"{name}":data}
                    self.cache.set("db_info",db_info,self.CACHING_EXPIRATION_TIME)
                    return True
                else:
                    if db_info.get(name):
                        return True
                    else:
                        db_info[name] = data
                        return self.cache.set("db_info",db_info,self.CACHING_EXPIRATION_TIME)
            return False
        except Exception as e:
            # print("FAILED TO FETCH CACHED TENANT DB INFO",str(e))
            return False

    def get_tenant_db_info(self, tenant, fetch_by_field=None):
        self.cache.clear()
        try:
            db_info = self.cache.get("db_info")
            if db_info:
                if fetch_by_field:
                    by_id = utils.array_to_dict(utils.get_object_values(db_info), fetch_by_field)
                    if by_id.get(f"{id}"):
                        return by_id.get(id)
                    else:
                        return False

                config = db_info.get(tenant)
                if config:
                    return config
        except Exception as e:
            pp(f"FAILED TO GET TENANT DB INFO FROM CACHE:{str(e)}")
        return False


    def set_model_cache(self, model_name, value):
        models = self.cache.get("models")
        models[model_name] = value
        try:
            print(model_name)
            self.cache.set(model_name,pickle.dumps(value))
            self.cache.touch("models", self.CACHING_EXPIRATION_TIME_FORM_MODELS)
        except Exception as e:
            print(f"FAILED TO CACHE MODEL:{model_name}:{str(e)}\n\n")


    def get_model_cache(self, model):
        model_data = None
        if self.cache.get("models"):
            model_data = self.cache.get("models")
            if model_data and model_data.get(model):
                model_data = model_data.get(model)
        return model_data


    def set_tenant_cache(self, tenant, model, label, value):
        try:
            if value:
                tenant_cache_content = self.cache.get(tenant)
                if not tenant_cache_content: 
                    to_be_cached = {
                        f"{model}":{
                            f"{label}": value
                        }
                    }
                    tenant_cache_content = to_be_cached
                else:
                    if tenant_cache_content.get(model):
                        tenant_cache_content[model][label] = value
                    else:
                        tenant_cache_content[model] = {
                            f"{label}": value
                        }
                if tenant_cache_content:
                    self.cache.set(tenant,tenant_cache_content,self.CACHING_EXPIRATION_TIME)
                    self.cache.touch(tenant)
        except Exception as e:
            pass
            # print(f"============================> Caching setup failed for {tenant} : {model} : {label}:{ str(e)} | {self.cache} <============================")

        
    def update_tenant_cache(self, tenant, model, old_label, label, value):
        try:
            tenant_cache_content = self.cache.get(tenant)
            if not tenant_cache_content:
                to_be_cached = {
                    f"{model}":{
                        f"{label}": value
                    }
                }
                tenant_cache_content = to_be_cached
            else:
                if tenant_cache_content.get(model):
                    tenant_cache_content[model][label] = value
                    if tenant_cache_content.get(model).get(old_label):
                        try:
                            del tenant_cache_content[model][old_label]
                        except Exception as e:
                            pp(f"AN ERROR OCCURRED WHILE DELETING CACHE OLD CONTENT:{str(e)}")
                else:
                    tenant_cache_content[model] = {
                        f"{label}": value
                    }
            # pp(tenant_cache_content)
            self.cache.set(tenant,tenant_cache_content, self.CACHING_EXPIRATION_TIME)
            return self.cache.touch(tenant)
                
        except Exception as e:
            pass
            # print(f"============================> Caching update failed for {tenant} : {model} : {label}:{ str(e)} <============================")

    def get_tenant_cached_value(self, tenant, model, name):
        # return False
        try:
            if self.cache.get(tenant) and self.cache.get(tenant).get(model) and self.cache.get(tenant).get(model).get(name):
                return self.cache.get(tenant).get(model).get(name)
            else:
                return False
        except Exception as e:
            pass
            # print(f"============================> Cached data extraction failed for {tenant} : {model} : {name}:{str(e)} <============================")
        return False
        

    