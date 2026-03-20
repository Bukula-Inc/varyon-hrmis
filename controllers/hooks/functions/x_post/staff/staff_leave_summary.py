from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

def get_staff_leave_summary (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    employee_leave_info = core_hr.get_employee_leave_days (object.body.data.name)
    leave_totals = employee_leave_info.overall_totals
    delattr (employee_leave_info, "overall_totals")
    return utils.respond (utils.ok, response={"overalls": leave_totals,
        "leave_breakdown": [
            {'leave_type': key, **value}
            for key, value in employee_leave_info.items()
        ]
    })
def interview_rating_by_staff(dbms, object):
    get_interview = dbms.get_doc("Interview", name=object.body.data.emp, fetch_linked_fields=True)
    if get_interview:
        applicant = get_interview.data.get('email')
        designation = get_interview.data.get('designation')

        get_competess = dbms.get_list("Competess_Assessment", filters={"parent": designation})
        get_practical = dbms.get_list("Practical_Assessment", filters={"parent": designation})
        get_applicant_details = dbms.get_list("Job_Application", filters={"email": applicant}, fetch_linked_tables=True)

        if get_applicant_details and get_applicant_details.data.rows:
            get_data = get_applicant_details.data.rows
            skills = set()
            attachments = []
            applicant_name = ''
            competess_rating = [{"competess": c['competess']} for c in get_competess.data.rows] if get_competess and get_competess.data.rows else []
            practical_rating = [{"practical_skill": p['practical_skill']} for p in get_practical.data.rows] if get_practical and get_practical.data.rows else []

            for sk in get_data:
                applicant_name = sk.get('applicant_name')
                for skl in get_interview.data.get('skills', []):
                    skills.add(skl.get('skill'))
                for ql in get_interview.data.get('qualifications', []):
                    attachments.append({"qualification_type": ql.get('qualification_type'), "qualification": ql.get('qualification')})

            skills = [{"skill": skill} for skill in skills] if skills else []

            if skills or attachments or competess_rating or practical_rating:
                return utils.respond(utils.ok, {
                    "data": skills,
                    "attachments": attachments,
                    "applicant_name": applicant_name,
                    "competess_rating": competess_rating,
                    "practical_rating": practical_rating
                })
        return None
    return None