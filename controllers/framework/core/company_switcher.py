from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
throw = utils.throw
from controllers.authentication import Authentication
class Company_Switcher:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.auth = Authentication()

    @classmethod
    def switch_company(cls, dbms, object):
        cls.__init__(cls, dbms, object)
        data = object.body.data
        if not data.company:
            throw("Please select the company you'd like to switch to!")
        if not data.confirm_password:
            throw("Please provide your password!")
        if not dbms.current_user or not dbms.current_user.email:
            throw("Please login before switching the company!")
        data.email = dbms.current_user.email
        data.password = data.confirm_password
        authenticate = cls.auth.login(dbms, data, is_company_switching=True,company=data.company)
        if authenticate.status != utils.ok:
            throw(f"Failed to switch company: {authenticate.error_message}!")
        return authenticate

