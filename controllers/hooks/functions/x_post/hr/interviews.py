from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.mailing import Mailing
from controllers.utils.data_conversions import DataConversion

utils = Utils ()
pp = utils.pretty_print
throw =utils.throw

def get_job_application (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    applicant_details =None
    job_application = dbms.get_doc("Applicant_Short_List", name=object.body.data.name)
    if job_application:
        fetch_application =dbms.get_doc("Job_Application", job_application.data.application, fetch_linked_fields=False, fetch_linked_tables=False,)
        if fetch_application.status ==utils.ok:
            applicant_details =fetch_application.data

        get_interview_schedule = dbms.get_list("Applicants_Schedule_List", filters={"application": job_application.data['name']})
        pp(applicant_details)
        if get_interview_schedule:
            df = utils.to_data_frame(get_interview_schedule.data.rows)
            interview_schedule_time = {
                "from_time": df['form_time'].tolist(),
                "to_time": df['to_time'].tolist(),
            }
        short_listed = job_application.get("data", {})
        document_files = short_listed.get('document_files', [])
        _skills = []
        qualifications = []
        if short_listed and document_files:
            for skill in short_listed.get('applicant_skills', []):
                _skills.append({"skill": skill.get('skill')})

            for doc in document_files:
                qualifications.append({
                    "qualification": doc.get('qualification'),
                    "qualification_type": doc.get('qualification_type')
                })

        return utils.respond(utils.ok, {"_skills": _skills, "documents": qualifications, "interview_schedule_times": interview_schedule_time, "applicant_details":applicant_details})
    else:
        return utils.respond(utils.ok, {"_skills": [], "documents": []}) 
    
def reject(dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    interview = core_hr.get_doc("Interview",object.body.data.id)
    if interview:
        data = utils.from_dict_to_object(interview)
        data.status = "Conduct"
        update = dbms.update("Interview", data, object.user, update_submitted=True)
    else:
        utils.throw ("An Error Occurred")
    return update

def questions(dbms, object):
    fecth_questions = dbms.get_list("Exit_Interview_Questionnair", fetch_linked_tables=True, filters={"designation":object.body.data.name},  privilege=True)
    if fecth_questions.status !=utils.ok:
        return utils.respond(utils.unprocessable_entity, "No Questionnaire For This Designation")
    # filters={"parent": object.body.data.name}
    get_questions =fecth_questions.data.rows[0].questions
    q_data = get_questions
    ques = []
    questions_list = set()  
    
    for q in q_data:
        if q['question'] not in questions_list:
            questions = {
                "question": q['question'],
                "answer": q['answer'],
            }
            ques.append(questions)
            questions_list.add(q['question'])  
            
    return utils.respond(utils.ok, ques)

def pull_question(dbms, object):
    pull_questions = dbms.get_list("Questions", privilege=True)
    if pull_questions is None:
        return None 
    q_data = pull_questions.data.rows
    ques = []
    seen_questions = set()  
    for qs in q_data:
        if qs['question'] not in seen_questions:
            questions = {
                "question": qs['question'],
                "choice": qs['choice'],
            }
            ques.append(questions)
            seen_questions.add(qs['question'])  
            
    return utils.respond(utils.ok, ques)

def interview_rating(dbms, object):
    get_interview = dbms.get_doc("Interview", name=object.body.data.emp, fetch_linked_fields=True)
    applicant = get_interview.data['email']
    designation = get_interview.data['designation']
    pp(get_interview)
    

        # # return utils.respond(utils.ok, {
        # #     # "applicant_details": 
        # #     "data": skills, 
        # #     "attachments": attachments, 
        # #     "applicant_name": applicant_name,
        # #     "competess_rating": competess_rating,
        # #     "practical_rating": practical_rating
        # })
def submit_job_application_(dbms, object):
    mailing = Mailing(dbms=dbms, object=object)
    data = object.body.data
    if data:
        job_application = utils.from_dict_to_object({})
        job_application.applicant_first_name = data.applicant_first_name
        job_application.applicant_last_name = data.applicant_last_name
        job_application.email = data.email
        job_application.mobile = data.phone
        job_application.country = data.country
        job_application.designation = data.designation
        job_application.job_opening = data.job_opening
        job_application.cover_letter = data.cover_letter
        job_application.job_skills = data.job_skills
        job_application.documents = data.documents
        create = dbms.create("Job_Application", job_application, submit_after_create=True)
        if create:
            return utils.respond(utils.ok, {"data": create})
        return utils.respond(utils.unprocessable_entity, "Application Submission Failed Please Enter Correct Details")

