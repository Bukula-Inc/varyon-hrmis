from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def witness (dbms, object):
    core_hr = Core_Hr (dbms)
    doc = DataConversion.safe_get (object.body.data, "doc")
    if not doc:
        throw ("<strong class='text-rose-600'>Unrecognized Document</strong>")
    
    a_doc = core_hr.get_doc ("Witnesses_Doc", doc)
    if not a_doc:
        throw ("<strong class='text-rose-600'>Unknown Document</strong>")

    return utils.respond (utils.ok, a_doc)