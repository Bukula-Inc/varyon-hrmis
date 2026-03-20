from datetime import datetime
from controllers.utils import Utils

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

class Leave_commutation:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user

    @classmethod
    def recent_leave_commutation(cls, dbms, object):
        dashboard_instance = cls(dbms, object)

        return utils.respond(utils.ok, {
            "leave_commutation": dashboard_instance.recent_commutable(),
        })

    def recent_commutable(self):
        employees = self.dbms.get_list("Leave_Commutation", filters={"status__in": ["Submitted"]})
        if employees:
            summary = []
            for employee in employees.data.rows:
                if isinstance(employee, dict):
                    fullname = employee.get("fullname", "N/A")
                    commutable_days = employee.get("commutable_days", 0)
                    value = employee.get('amount', 0)

                    if fullname != "":
                        summary.append({
                            "name": fullname,
                            "total_commutable_days": commutable_days,
                            "total_value": value,
                        })

        return summary
