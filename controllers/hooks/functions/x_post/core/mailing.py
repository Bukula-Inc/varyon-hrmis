
from controllers.core_functions.core import Core
from controllers.mailing import Mailing
from controllers.mailing.templates.default_template import Default_Template
from controllers.mailing.templates.default_templates import Default_Templates
dt = Default_Templates()
from controllers.utils import Utils
# from controllers.dbms import DBMS
utils = Utils()
throw = utils.throw
pp = utils.pretty_print


from services.raw import Raw

def test_email_config(dbms, object):
    mailing = Mailing(dbms, object)
    user = Default_Templates.new_user_template("ECZ HRMIS","startappsolutions.com","chikolabruce23@gmail.com","377529","Bruce","")
    throw("This feature is disabled!")
    # send = mailing.send_mail(
    #     "esskayyoungesser@gmail.com", 
    #     "TESTING EMAILS",Default_Template.template(user, "New User Account Creation"))
    # return send
