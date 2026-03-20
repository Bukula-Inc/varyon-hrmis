from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils()
dates = Dates()
throw = utils.throw

class Employee_Grade:
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
    def employee_grade(dbms, object):

        emp_grade_data = dbms.get_list("Employee_Grade", fetch_linked_tables = True, privilege=True)
        if emp_grade_data.status == utils.ok:
            emp_grade_list = emp_grade_data.data.rows
            total_grades = len(emp_grade_list)
            employee_drade = {} 
            stats = []
            status = []
            for grade_data in emp_grade_list:
                grade_name = grade_data.name
                grade_deductions = len(grade_data.deductions)
                grade_earnings = len(grade_data.earnings)
                employees_data = dbms.get_list("Employee", filters={'employee_grade': grade_name},  privilege=True)
                if employees_data.status == utils.ok:
                    employees_list = employees_data.data.rows
                    status.append({
                        "grade_name": grade_name,
                        "total_grade_emp": len(employees_list),
                    })
                    employee_drade['grade_data'] = status

        else:
            status = []
        return utils.respond(utils.ok, employee_drade)