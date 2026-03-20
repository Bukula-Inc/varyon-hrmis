from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()

class Job_Application:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
    

    @classmethod
    def get_Applcations(self, dbms, object):
        self.__init__(self, dbms=dbms, object=object)
        application_list = []
        applications_per_designation = {}

        applications = self.dbms.get_list("Job_Application", user=self.user)
        if applications.get("status") == utils.ok:
            total_applications = 0
            successful_applications = 0
            rejected_applications = 0
            if len(applications.get("data").get("rows")) > 0:
                for application in applications.get("data").get("rows"):
                    total_applications += 1
                    if application["status"] == "Applied":
                        successful_applications += 1
                    if application["status"] == "Rejected":
                        rejected_applications += 1
                    designation = application.get("designation", "Unknown")
                    if designation not in applications_per_designation:
                        applications_per_designation[designation] = 0
                    applications_per_designation[designation] += 1
                    application_list.append({
                        "applicant_name": application["applicant_name"],
                        "application_date": application["created_on"],
                    })

        job_openings = self.dbms.get_list("Job_Advertisement", filters={"status__in": ["Submitted"]}, user=self.user)
        number_of_job_openings = 0
        if job_openings.get("status") == utils.ok:
            number_of_job_openings = len(job_openings.get("data").get("rows")) if len(job_openings.get("data").get("rows")) > 0 else 0

        job_application_stats = {
            "total_applications": total_applications,
            "successful_applications": successful_applications,
            "rejected_applications": rejected_applications,
            "number_of_job_openings": number_of_job_openings,
        }

        result = {
            "job_application_stats": job_application_stats,
            "applications_by_designation": applications_per_designation,
        }

        return utils.respond(utils.ok, result)
