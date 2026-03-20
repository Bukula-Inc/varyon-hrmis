from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw


class User_Dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.settings = self.dbms.system_settings
        self.defaults = self.settings.accounting_defaults
        self.default_company = self.settings.linked_fields.default_company

    @classmethod
    def user(cls, dbms, object):
        cls.__init__(cls, dbms, object)
        recent_users = []
        disable_users = []
        recent_users_data = cls.dbms.get_list("Lite_User", limit=4,user=cls.user)
        if recent_users_data.status == utils.ok:
            rows = recent_users_data.data.rows[:4]
            for ru in rows:
                recent_users.append(ru)
        disabled_users_data = cls.dbms.get_list("Lite_User", filters={"disabled": 1}, user=cls.user, limit=4)
        if disabled_users_data.status == utils.ok:
            rows = disabled_users_data.data.rows[:4]
            for ru in rows:
                disable_users.append(ru)

        return utils.respond(utils.ok,{
            "recent_users": recent_users,
            "disabled_users": disable_users,
        })
    