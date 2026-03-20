from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
class Staffing_Plan:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}

    @classmethod
    def get_departments(self, dbms, object):
        self.__init__(self, dbms=dbms, object=object)
        departments_list = []

        departments = self.dbms.get_list("Department", filters={"status__in": ["Active"]}, user=self.user)
        if departments.status == utils.ok:
            if len(departments.data.rows) > 0:
                for department in departments.data.rows:
                    staffing_plans = self.dbms.get_list("Staffing_Plan", filters={"department": department["name"], "status__in": ["Submitted"]}, user=self.user)
                    if staffing_plans.status == utils.ok:
                        departments_list.append({
                            "department_name": department["name"],
                            "number_of_departments": len(staffing_plans.data.rows),
                        })

        return utils.respond(utils.ok, departments_list)
       
