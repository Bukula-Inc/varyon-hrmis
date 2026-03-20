from controllers.utils import Utils 
from controllers.core_functions.hr import Core_Hr
utils = Utils ()
pp = utils.pretty_print
def side_view_leave_type (dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    leaves = []
    leave_types = core_hr.get_list ("Leave_Type", filters={"status": "Active"}, limit=18)
    if leave_types:
        for leave_type in leave_types:
            leaves_ = core_hr.get_list ("Leave_Application", filters={"status": "Pending Approval", "leave_type": leave_type.name})
            if leaves_:
                leaves.append ({
                    "leave_type": leave_type.name,
                    "pending_count": len (leaves_)
                })
    return utils.respond (utils.ok, response={"status": utils.ok, "data": leaves})