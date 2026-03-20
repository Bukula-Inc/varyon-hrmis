from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.tenant import Tenant_Controller


utils = Utils()
date = Dates()
tc = Tenant_Controller()

pp = utils.pretty_print
throw = utils.throw


utils = Utils ()
pp = utils.pretty_print
dates = Dates ()

class Employee_Discipline_Controller:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def init_employee_discipline (cls, dbms, tc=None):
        core_hr = Core_Hr (dbms=dbms)

        get_case_outcome = core_hr.get_list ("")
                                         