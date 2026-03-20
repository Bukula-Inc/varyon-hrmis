import requests, json
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.dbms import DBMS
from .config import header_content
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw
class Domain_Controller:
    def __init__(self) -> None:
        self.dbms = DBMS(init_admin=True)
        pass

    def get_domain_configurations(self):
        return self.dbms.get_doc("Domain_Controller", "Domain Controller", privilege=True)

    def register_subdomain(self,subdomain_name):
        dc = self.get_domain_configurations()
        if dc.get("status") != utils.ok:
            return dc
        conf = dc.data
        header = header_content
        header["Authorization"] = f"sso-key {conf.domain_host_api_key}:{conf.domain_host_secret_key}"
        data = [{"data": conf.domain_ip, "name": subdomain_name, "ttl": int(conf.domain_default_ttl), "type": conf.domain_default_record_type}]
        try:
            response = requests.patch(conf.domain_host_url, data=json.dumps(data), headers=header)
            return utils.respond(utils.ok, f"Subdomain {subdomain_name} registered successfully!")
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"Failed to register subdomain: {e}")
