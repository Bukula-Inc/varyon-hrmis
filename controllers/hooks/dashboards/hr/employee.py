from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Employee:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.system_settings = self.dbms.system_settings
        # pp(self.system_settings)

    def update_designation_count(self, employees_designation, designation):
        """Helper function to increment or add a designation."""
        existing_designation = next((d for d in employees_designation if d["label"] == designation), None)

        if existing_designation:
            existing_designation["value"] += 1
        else:
            employees_designation.append({
                "label": designation,
                "value": 1,
            })


    def get_gender_counts(self, employees):
        """Helper function to count males and females."""
        male_count = sum(1 for emp in employees if str(emp.gender).lower() == "male")
        female_count = sum(1 for emp in employees if str(emp.gender).lower() == "female")
        return [male_count, female_count]


    def process_employees_data(self, employees):
        """Process the employee data to get gender and designation counts."""
        employees_designation = []

        for emp in employees:
            self.update_designation_count(employees_designation, emp.designation)

        return employees_designation


    def employee(self):
        """Main function to handle employee data and return the results."""
        employees = self.dbms.get_list("Employee", filters={"status__in": ["Active", "Probation"]})

        if employees.status != utils.ok or len(employees.data.rows) == 0:
            return utils.respond(utils.error, "No active or probation employees found")

        employees_designation = self.process_employees_data(employees.data.rows)
        gender_counts = self.get_gender_counts(employees.data.rows)

        results = utils.from_dict_to_object({
            "gender": gender_counts,
            "employees_designation": employees_designation,
        })
        return utils.respond(utils.ok, results)


    @classmethod
    def employee_sv(cls, dbms, object):
        cls = cls (dbms, object)
        return cls.employee()