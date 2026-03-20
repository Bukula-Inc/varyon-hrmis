from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()

class Job_Opening:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}

    @classmethod
    def get_job_openings(self, dbms, object):
        self.__init__(self, dbms=dbms, object=object)
        jb_opening = self.dbms.get_list("Job_Advertisement", privilege=True, filters={"docstatus":1})
        if jb_opening:
            opening_data = jb_opening.data.rows
            total_vacancies = 0
            closed_job_openins =0 
            total_openings = len(opening_data)
            department_vacancies = {}

            for job in opening_data:
                if job['status'] == "Closed":
                    closed_job_openins += 1
                department = job.get("department")
                vacancies = int(job.get("vacancies", 0))
                total_vacancies += vacancies
                department_vacancies[department] = department_vacancies.get(department, 0) + vacancies

            departments_list = [{"department_name": dept, "number_of_vacancies": vac} for dept, vac in department_vacancies.items()]
            return utils.respond(utils.ok, {"total_vacancies": total_vacancies, "total_openings": total_openings, "departments": departments_list})

        return utils.respond(utils.ok, {"total_vacancies": 0, "total_openings": 0, "departments": []})
