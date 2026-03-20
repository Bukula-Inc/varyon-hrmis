from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw


def interview_score_sheet_report(dbms, object):
    filters = object.filters
    candidate_scores =[]
    if not filters:
        throw("Please provide the job advertisement in the filters")
    job_advertisement = DataConversion.safe_get(filters, "job_advertisement", "")
    fetch_interview =dbms.get_list("Interview_Schedule", filters=filters, fetch_linked_tables=True)
    if fetch_interview.status !=utils.ok:
        throw("No interview schedule found for the provided job advertisement")
    applicants_list = fetch_interview.data.rows[0].applicants_list if fetch_interview.data.rows[0].applicants_list else []
    if not applicants_list:
        throw("No applicants found for the provided job advertisement")

    interview_list =dbms.get_list("Interview", filters={"interview_schedule": fetch_interview.data.name})

    if interview_list.status !=utils.ok:
        throw("No interviews found for the provided job advertisement")
    
    for interview in interview_list.data.rows:
        total_score =(len(interview.technical_competence)*5) + (len(interview.behavioral_competence)*5)
        comment = " ".join(f"{feedback.interviewer_comments}, " for feedback in interview.other_relevant_information if feedback.interviewer_comments) or ""
        candidate_scores.append(utils.from_dict_to_object({
            "applicant": interview.applicant,
            "average_score": interview.overall_total,
            "percentage_score": f"{(float(interview.overall_total)/total_score if total_score >0 and float(interview.overall_total) >0 else 0) *100}%",
            "comments": comment
        }))

    return utils.respond(utils.ok, utils.from_dict_to_object({"rows": candidate_scores}))    
    # return [] 