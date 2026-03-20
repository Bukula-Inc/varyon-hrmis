import threading, json
from client_app.controller.tenant.models import Tenant
from client_app.controller.user_pool.models import User_Pool
from controllers.utils import Utils
from services.raw import Raw
from django.shortcuts import render
from controllers.authentication import Authentication
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from controllers.caching import Caching

utils = Utils()
raw = Raw()
auth = Authentication()
pp = utils.pretty_print
throw = utils.throw
THREAD_LOCAL = threading.local()


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.caching = Caching.init()

    def init_middleware_validation(self, request):
        self.request = request
        self.path = self.request.META.get("PATH_INFO")
        self.request.path = self.path
        self.url = self.request.build_absolute_uri()
        self.db_name = raw.tenant_admin.get("DB")
        self.request.tenant_db = self.db_name
        self.config = raw.add_tenant_db_to_db_list()

    def validate_service_request(self):
        if self.request.body:
            body = utils.from_dict_to_object(json.loads(self.request.body))
            if not body.xtenant:
                if "/new-tenant/" not in self.path:
                    return utils.json_respond(utils.not_found, "xtenant missing in body!")
                else:
                    body.xtenant = self.db_name
            
            try:
                tenant = utils.from_dict_to_object()
                cached_tenant = self.caching.get_tenant_db_info(body.xtenant)
                if cached_tenant:
                    tenant = cached_tenant
                else:
                    try:
                        tenant = Tenant.objects.using(self.db_name).get(db_name=body.xtenant)
                    except ObjectDoesNotExist as e:
                        pp("An error occurred while configuring this tenant:", str(e))
                
                if tenant:
                    self.db_name = tenant.db_name
                    self.request.tenant_db = self.db_name
                    self.request.tenant_id = f"{self.db_name}&%{tenant.id}"
            except ObjectDoesNotExist as e:
                pass
                # return utils.json_respond(utils.unprocessable_entity,f"Tenant name provided does not exist: {str(e)}")
        else:
            return utils.json_respond(utils.unprocessable_entity,"Request missing body.")
        return True
   
    # normal user authentication
    def init_user_authentication(self):
        try:
            body = json.loads(self.request.body)
            if body.get("email"):
                try:
                    user = User_Pool.objects.using(self.db_name).get(name__iexact=body.get("email"))
                    if user:
                        try:
                            tenant = utils.from_dict_to_object()
                            cached_tenant = self.caching.get_tenant_db_info( self.db_name,fetch_by_field="id")
                            if cached_tenant:
                                tenant = cached_tenant
                            else:
                                tenant = Tenant.objects.using(self.db_name).get(pk=user.tenant_id)
                            if tenant:
                                self.db_name = tenant.db_name
                                self.request.tenant_db = self.db_name
                                self.request.tenant_id = f"{self.db_name}&%{tenant.id}"
                                return True
                        except ObjectDoesNotExist:
                            return utils.json_respond(utils.not_found,"Tenant not found!")
                except ObjectDoesNotExist:
                    return utils.json_respond(utils.unprocessable_entity,"User Email Not Recognized")
        except Exception as e:
                return utils.json_respond(utils.unprocessable_entity,f"Failed to extract authentication body: {str(e)}")



    # to authenticate supplier or customer on the portal
    def authenticate_supplier_or_customer(self):
        if "request-otp" in self.path:
            if self.request.body:
                body = utils.from_dict_to_object(json.loads(self.request.body))
                if not body.trader_type:
                    return utils.json_respond(utils.not_found, "Trader Type is required!")
                if not body.email:
                    return utils.json_respond(utils.not_found, "Email is required!")
                if not body.product_or_service_provider:
                    return utils.json_respond(utils.not_found, "Service/Product provider is required!")
                try:
                    tenant = utils.from_dict_to_object()
                    cached_tenant = self.caching.get_tenant_db_info( body.product_or_service_provider, fetch_by_field="name")
                    if cached_tenant:
                        tenant = cached_tenant
                    else:
                        tenant = Tenant.objects.using(self.db_name).get(name=body.product_or_service_provider)
                    if tenant:
                        self.request.service_provider = tenant.name
                        self.db_name = tenant.db_name
                        self.request.tenant_db = self.db_name
                        self.request.tenant_id = f"{self.db_name}&%{tenant.id}"
                except ObjectDoesNotExist:
                    return utils.json_respond(utils.unprocessable_entity,"Service/Product provider not found! Ensure to select the correct service provider.")
        else:
            cookie = self.request.headers.get("Cookie")
            if cookie:
                splited = cookie.split("key=")
                if splited and len(splited) > 1:
                    decoded = utils.from_dict_to_object()
                    try:
                        self.request.api_key = splited[1]
                        decoded = utils.decode_client_api_key(splited[1])

                        # to add tenant from the tenant token for port access
                        if decoded and decoded.api_key:
                            decoded_tenant_api_key = utils.decode_client_api_key(decoded.api_key)
                            if decoded_tenant_api_key and decoded_tenant_api_key.tnt:
                                decoded.tnt = decoded_tenant_api_key.tnt

                        client_key = utils.decode_client_api_key(decoded.api_key)
                        if client_key.tnt:
                            tnt = client_key.tnt.split("&%")
                            if tnt and len(tnt) > 0:
                                self.db_name = tnt[0]
                                self.request.tenant_db = tnt[0]
                        decoded.api_key = self.request.api_key
                    except Exception as e:
                        return utils.json_respond(utils.unprocessable_entity,f"Validation failed:{str(e)}")
                    if not decoded:
                        return utils.json_respond(utils.unprocessable_entity,"Invalid client portal cookie. Please Login in once more!")
                    self.request.api_key = decoded.api_key
                    self.request.party = decoded.party
        return True


    # MAIN INTERCEPTOR
    def __call__(self, request):
        self.init_middleware_validation(request)
        
        if self.path:
            # authenticate user
            if "/api/authenticate" in self.path.lower():
                user_auth = self.init_user_authentication()
                if user_auth != True:
                    return user_auth
            
            # authenticate customer/supplier
            elif "/portal/" in self.path:
                portal = self.authenticate_supplier_or_customer()
                if portal != True:
                    return portal
            elif "/services/" in self.path:
                services = utils.from_dict_to_object()
                try:
                    services = self.validate_service_request()
                except Exception as e:
                    pp(f"An error occurred while connecting tenant {self.db_name}:", str(e))
                if services != True:
                    return services
            else:
                validate = auth.validate_request(request)
                if not validate or validate.get("status") != utils.ok:
                    if validate.status == utils.unauthorized:
                        return JsonResponse("Authorization Failed: Invalid API-KEY", status=utils.unauthorized, safe=False)
                    return render(request, "authentication/unauthorized.html", {"prev_url": self.url})
                else:
                    if validate.status == utils.ok:
                        if validate.data.tenant_db:
                            self.db_name = validate.data.tenant_db
                            self.request.tenant_db = self.db_name
                            self.request.tenant_id = validate.data.tenant_id
                        else:
                            if (
                                "/api/"       in self.path or 
                                "/portal/"    in self.path or 
                                "/auth/"      in self.path or 
                                "/media/"     in self.path or 
                                self.path ==     "/"       or
                                "/web/"       in self.path 
                            ):
                                self.request.tenant_db = self.db_name
                            else:
                                return render(request, "authentication/unauthorized.html", {"prev_url": self.url})
                            
        if not self.db_name:
            return JsonResponse("Failed to connect tenant. Something went wrong!", status=utils.unprocessable_entity, safe=False)
        setattr(THREAD_LOCAL, "db", self.db_name)
        config = raw.add_tenant_db_to_db_list(self.db_name)
        if config.status != utils.ok:
            return JsonResponse("Failed to connect tenant", status=utils.unprocessable_entity, safe=False)
        response = self.get_response(self.request)
        return response
    
def get_db_config_for_domain():
    return getattr(THREAD_LOCAL, "db", None) 
