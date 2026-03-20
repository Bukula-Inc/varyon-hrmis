from controllers.utils import Utils
utils = Utils()


class Validation:
    def __init__(self) -> None:
        pass

    def validate_request(self, request, skip_xtenant=False):
        method = request.method
        headers = request.headers
        body = None
        data_obj = utils.from_dict_to_object()
        data_obj.body = {} or None
        try:
            body = request.body
            if not body:
                return utils.respond(utils.not_found, "Request missing body!")
            body = utils.string_to_json(body.decode('utf-8'))
            if not body.get("data"):
                return utils.respond(utils.not_found, "Request body missing data key!")
            data_obj.body = body.get("data")
            data_obj.xtenant = body.data.xtenant
            data_obj.method = method
            data_obj.apps = []
            data_obj.fake = False
            
            if data_obj.body.get("apps") and isinstance(data_obj.body.get("apps"), list):
                data_obj.apps  = data_obj.body.get("apps")
            if data_obj.body.get("fake"):
                data_obj.fake  = data_obj.body.get("fake")
            
            data_obj.host = utils.get_request_domain(request).get("data") or None
            data_obj.headers = dict(headers)
            data_obj.tenant_db = data_obj.xtenant
            return utils.respond(utils.ok, data_obj)

        except ValueError as e:
            raise ValueError(f"VALIDATION ERROR:, {e}")

    def validate_body_keys(self, body, keys):
        for k in keys:
            if not body.get(k):
                return utils.respond(utils.not_found, f"Body Missing {k} value!")
        return utils.respond(utils.ok, "Validation Passed!")
