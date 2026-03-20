from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
utils = Utils()
dates = Dates()
from controllers.mailing import Mailing
throw = utils.throw
pp = utils.pretty_print

def before_qns_save_and_update(dbms, object):
    mailing = Mailing(dbms=dbms)
    question = object.body.name
    object.body.name = question.strip()
