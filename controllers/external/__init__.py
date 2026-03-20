import requests, json
from controllers.utils import Utils
utils = Utils()
throw = utils.throw
pp = utils.pretty_print

class External_Handler:
    def __init__(self) -> None: 
        pass

    def post(self, url="", headers={'Content-Type': "application/json"},data={}):
        response = requests.post(url=url, headers=headers, data=json.dumps(data, default=utils.encode))
        try:
            if response.status_code == utils.ok:
                return utils.respond(utils.ok, response.json())
            return utils.respond(response.status_code, response.json())
        except Exception as e:
            return utils.respond(response.status_code, str(e)) 
        
