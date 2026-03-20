from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils()
dates = Dates()
throw = utils.throw

class Salary_Componet:
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
    def salary_component(dbms, object):
        salary_component_data = dbms.get_list("Salary_Component", privilege=True)
        if salary_component_data.status == utils.ok:
            salary_component_list  = salary_component_data.data.rows
            total_salary_component = len(salary_component_list)
            component_grade = {} 
            stats = []
            for component in salary_component_list:
                component_name = component.name
                grade_data = dbms.get_list("Employee_Grade", filters={'employee_grade': component_name}, fetch_linked_tables = True, privilege=True)
                if grade_data.status == utils.ok:
                    grade_list = grade_data.data.rows
                    earnings_count = 0
                    deductions_count = 0
                    for grade in grade_list:
                        grade_earnings = grade.earnings
                        grade_deductions = grade.deductions
                        for earning in grade_earnings:
                            if earning.component == component_name:
                                earnings_count += 1

                        for deduction in grade_deductions:
                            if deduction.component == component_name:
                                deductions_count += 1

                    stats.append({
                        "component_name": component_name,
                        "total_grades": earnings_count + deductions_count,
                    })
                else:
                    stats.append({
                        "component_name": component_name,
                        "total_grades": 0,
                    })

            component_grade['grade_data'] = stats
        else:
            component_grade['grade_data'] = []

        return utils.respond(utils.ok, component_grade)