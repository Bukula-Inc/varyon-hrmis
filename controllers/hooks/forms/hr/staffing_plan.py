from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
utils = Utils ()
pp = utils.pretty_print
throw = utils.throw
def after_submit_staffing_plan(dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    data = object.body
    if data.create_job_offers == 1:
        if data.staffing_details and len (data.staffing_details) > 0:
            for opening in data['staffing_details']:
                job_opening = utils.from_dict_to_object ({})
                designation = core_hr.get_doc ("Designation", opening.designation)
                DataConversion.safe_set (job_opening, "lower_range", DataConversion.safe_get(opening, "estimated_cost", 0))
                DataConversion.safe_set (job_opening, "vacancies", DataConversion.safe_get(opening, "vacancies", 0))
                DataConversion.safe_set (job_opening, "designation", DataConversion.safe_get(opening, "designation"))
                DataConversion.safe_set (job_opening, "company", DataConversion.safe_get(data, "company"))
                DataConversion.safe_set (job_opening, "department", DataConversion.safe_get(opening, "department"))
                DataConversion.safe_set (job_opening, "currency", DataConversion.safe_get(core_hr, "reporting_currency"))
                if data.publish_salary == 1:
                    DataConversion.safe_set (job_opening, "publish_salary", 1)
                else:
                    DataConversion.safe_set (job_opening, "publish_salary", 0)
                if designation and designation.description:
                    DataConversion.safe_set (job_opening, "description", DataConversion.safe_get(designation, "description"))
                if data.publish_job_offer and job_opening.description:
                    DataConversion.safe_set (job_opening, "status", "Submitted")
                    DataConversion.safe_set (job_opening, "doc_status", "Submitted")
                    DataConversion.safe_set (job_opening, "publish", DataConversion.safe_get(data, "publish_job_offer"))
                else:
                    DataConversion.safe_set (job_opening, "status", "Draft")
                pp (job_opening)
                r = dbms.create ("Job_Advertisement", job_opening)
                pp (r)
    object.body.status = "Submitted"
    object.body.doc_status = "Submitted"