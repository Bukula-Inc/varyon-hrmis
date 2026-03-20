from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
import math

utils = Utils()
pp = utils.pretty_print

def update_salary_components (dbms, object):
    core_hr = Core_Hr (dbms)
    count = 0
    sc = core_hr.get_list ("Salary_Component")
    if sc:
        for sa_c in sc:
            if not sa_c.is_type:
                is_type = ""
                if sa_c.for_commutation:
                    is_type = "Commutation"
                elif sa_c.is_commission:
                    is_type = "Commission"
                elif sa_c.is_private_pension:
                    is_type = "Private Pension"
                elif sa_c.is_overtime:
                    is_type = "Overtime"
                elif sa_c.is_advance:
                    is_type = "Advance"
                elif sa_c.is_welfare:
                    is_type = "Welfare"
                for key, value in sa_c.items():
                    if isinstance(value, float) and math.isnan(value):
                        sa_c[key] = 0.00
                sa_c.is_type = is_type
                sa = dbms.update ("Salary_Component", sa_c, update_submitted=True)
                if sa.status == utils.ok:
                    count += 1
    return utils.respond (utils.ok, response=f"Processed {count} Salary Component")