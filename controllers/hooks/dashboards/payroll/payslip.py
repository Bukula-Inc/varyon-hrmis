from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils()
dates = Dates()
throw = utils.throw

class PaySlip:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.system_settings()
        if system_settings.status == utils.ok:
            self.settings = Dict_To_Object(system_settings.data)

    @staticmethod
    def payslip(dbms, object):
        submitted_payslips = []
        status = []
        payslip_data = dbms.get_list("Payslip", user=object.user)
        if payslip_data.status == utils.ok:
            payslip_list = payslip_data.data.rows
            status.append({
                "submitted": sum(1 for slip in payslip_list if slip['status'] == 'Submitted'),
                "draft": sum(1 for slip in payslip_list if slip['status'] == 'Draft'),
                "total": len(payslip_list),
            })
          

    
            employee_payslip = dbms.get_list("Payslip", filters={"status__in": ["Submitted"]}, user=object.user)
            if employee_payslip.status == utils.ok:
                for slip in employee_payslip.data.rows:
                    submitted_payslips.append({
                        "employee_name": slip["name"],
                    })
            results = {
                "payslip_stats": status,
                "submitted_payslip": submitted_payslips,
            }
            return utils.respond(utils.ok, results)