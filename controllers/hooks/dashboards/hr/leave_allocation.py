from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
pp = utils.pretty_print
dates = Dates()
class Leave_Allocation_Dashboard:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.core = Core_Hr(dbms, self.object)
        
    @classmethod
    def leave_allocation(cls, dbms, object):
        instance = cls(dbms, object)
        return utils.respond(utils.ok, {
            "leave_allocated": instance.allocated_leave()
        })
    def allocated_leave(self):
        allocations = self.core_hr.get_leave_allocated()
    