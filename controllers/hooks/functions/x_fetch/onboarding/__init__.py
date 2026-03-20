from controllers.utils import Utils
import itertools

utils = Utils()
pp = utils.pretty_print
throw = utils.throw
class Onboarding:
    def __init__(self,dbms, object) -> None:
        self.dbms = dbms
        self.object = object

    @classmethod
    def get_onboarding_content(cls, dbms, object):
        cls.__init__(cls, dbms, object)
        if dbms.current_user:
            user = utils.from_dict_to_object(dbms.current_user)
            del user["password"]
            data = utils.from_dict_to_object({"user": user, "onboarding": {}, "role": {}, "company":{}})
            onboarding = cls.get_onboarding_data(cls)
            role = cls.dbms.user_controller.get_user_allowed_menu_items()
            company = cls.dbms.get_doc("Company", user.default_company, privilege=True)
            if onboarding.status == utils.ok:
                data.onboarding = onboarding.data
            if role.status == utils.ok:
                data.update(role.data)
            if company.status == utils.ok:
                data.company = company.data
            return utils.respond(utils.ok, data)
        else:
            return utils.respond(utils.unauthorized, "User id required to fetch onboarding info!")

    def get_onboarding_data(self):
        onboarding = self.dbms.get_doc("Onboarding", f"{self.dbms.current_user.name}", privilege=True)
        if onboarding.status == utils.ok:
            return onboarding
        else:
            create = self.dbms.create("Onboarding", {"name": self.dbms.current_user.name, "user": None, "current_stage":1}, privilege=True)
            return create


        

        
