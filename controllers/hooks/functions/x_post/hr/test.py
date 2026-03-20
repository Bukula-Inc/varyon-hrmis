from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def tests(dbms, object):
    pp(object)
    name ="APP-2025-0003"
    pp(dbms.get_doc("Leave_Application", name))
    
    throw(".....")