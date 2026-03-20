from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
utils = Utils()
dates = Dates()
throw = utils.throw
pp = utils.pretty_print

def on_submissions_of_Leave_policy (dbms, object):
    obj = object.body
    if obj.enable_single_accrual:
        ent = utils.from_dict_to_object ({})
        ent.name = obj.accruing_leave_type
        ent.reference = obj.name
        atc = []
        if obj.attached_leave_types and len (obj.attached_leave_types) > 0:
            for lt in obj.attached_leave_types:
                lt1 = utils.from_dict_to_object ({})
                lt1.leave_type = lt.leave_type
                atc.append (lt1)

        ent.attached_leave_types = atc

        pp (ent)
        r = dbms.create ("EnabledSingleAccrual", ent, submit_after_create=True)
        pp (r)
    object.body.is_active =1