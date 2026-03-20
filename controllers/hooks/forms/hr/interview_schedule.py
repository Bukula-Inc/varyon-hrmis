from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.core_functions.hr import DataConversion
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.mailing import Mailing

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def get_application_details(dbms, application_id):
    application = dbms.get_doc("Job_Application", application_id)
    pp(application)
    if application.status != utils.ok:
        return
    return application.data

def interview_schedule_validation(body):
    # MAIN BODY
    if not body.name:
        throw(f"The field 'Name', is missing.")
    if not body.schedule:
        throw(f"The field 'Schedule', is missing.")
    if body.physical_interview:
        if not body.location:
            throw(f"The field 'Location', is missing.")
    if body.virtual_interview:
        if not body.link_to_virtual_meeting:
            throw(f"The field 'Link to Virtual Meeting', is missing.")
    if not body.panel_type:
        throw(f"The field 'Panel Type', is missing.")
    else:
        if body.panel_type =="Pre Defined Panel":
            if not body.link_panel:
                throw(f"The field 'Link Panel', is missing.")
        elif body.panel_type =="Use Defined Panel":
            if not body.chairperson:
                throw(f"The field 'Chairperson', is missing.")

    if not body.schedule_for:
        throw(f"The field 'Schedule For', is missing.")
    else:
        if body.schedule_for =="For Single Applicant":
            if not body.designation:
                throw(f"The field 'Designation', is missing.")
            if not body.from_time:
                throw(f"The field 'From Time', is missing.") 
            if not body.to_time:
                throw(f"The field 'To Time', is missing.")
            if not body.application:
                throw(f"The field 'Application', is missing.")
            if not body.applicant:
                throw(f"The field 'Applicant', is missing.")

    # EXTERNAL INTERVIEWER
    if not body.external_Interviewers:
        pass
    else:
        row_no =0
        if isinstance(body.external_Interviewers, list):
            for row in body.external_Interviewers:
                if not row.interviewer_last_name:
                    throw(f"The field 'Interviewer Last Name', is missing at row {row_no +1}.")
                if not row.interviewer_first_name:
                    throw(f"The field 'Interviewer First Name', is missing at row {row_no +1}.")
                if not row.interviewer_email:
                    throw(f"The field 'Interviewer Email', is missing at row {row_no +1}.")
                row_no +=1

    # INTERNAL INTERVIEWER
    if not body.internal_interviewer:
        pass
    else:
        row_no =0
        if isinstance(body.internal_interviewer, list):
            for row in body.internal_interviewer:
                if not row.interviewer_last_name:
                    throw(f"The field 'Interviewer Last Name', is missing at row {row_no +1}.")
                if not row.interviewer_first_name:
                    throw(f"The field 'Interviewer First Name', is missing at row {row_no +1}.")
                if not row.interviewer_email:
                    throw(f"The field 'Interviewer Email', is missing at row {row_no +1}.")
                row +=1

    # APPLICANTS SCHEDULED LIST
    if not body.applicants_list:
        pass
    else:
        row_no =0
        if isinstance(body.applicants_list, list):
            for row in body.applicants_list:
                if not row.application:
                    throw(f"The field 'Application', is missing at row {row_no +1}.")
                if not row.position:
                    throw(f"The field 'Position', is missing at row {row_no +1}.")
                if not row.interview_date:
                    throw(f"The field 'Interview Date', is missing at row {row_no +1}.")
                if not row.form_time:
                    throw(f"The field 'Form Time', is missing at row {row_no +1}.")
                else:
                    body.applicants_list[row_no].form_time =str(body.applicants_list[row_no].form_time)
                if not row.to_time:
                    throw(f"The field 'To Time', is missing at row {row_no +1}.")
                else:
                    body.applicants_list[row_no].to_time =str(body.applicants_list[row_no].to_time)
                # if not row.applicant:
                #     throw(f"The field 'Applicant', is missing at row {row_no +1}.")
                if not row.applicant_email:
                    throw(f"The field 'Applicant Email', is missing at row {row_no +1}.")
                row_no +=1

    return body
        



def on_save_interview_schedule(dbms, object):
    object.body =interview_schedule_validation(object.body)

        
def pending(dbms, object):
    object.body.status = "Pending"

def before_interview_schedule_submit(dbms, object):
    core_hr = Core_Hr(dbms=dbms)
    mailing = Mailing(dbms=dbms, object=object)
    data = object.body
    interview_location =data['location']
    interview_link =data['link_to_virtual_meeting']
    schedule_for = DataConversion.safe_get(data, 'schedule_for', '')
    
    if schedule_for == "For Single Applicant":
        applicant_name = DataConversion.safe_get(data, 'applicant', 'Applicant')
        applicant_email = DataConversion.safe_get(data, 'applicant_email', '')
        position_name = DataConversion.safe_get(data, 'position_name', 'N/A')
        interview_date = DataConversion.safe_get(data, 'schedule', 'TBD')
        from_time = DataConversion.safe_get(data, 'from_time', 'TBD')  
        to_time = DataConversion.safe_get(data, 'to_time', 'TBD')
        interview_location = data['location']
        
        interview_link = DataConversion.safe_get(data, 'link_to_virtual_meeting', '')
        
    elif schedule_for == "Multiple Applicants":
        applicants_list = DataConversion.safe_get(data, 'applicants_list', [])
        external_Interviewers =DataConversion.safe_get(data, 'external_Interviewers', [])
        internal_interviewers =DataConversion.safe_get(data, 'internal_interviewers', [])

        external_Interviewers =external_Interviewers if isinstance(external_Interviewers, list) else []
        internal_interviewers =internal_interviewers if isinstance(internal_interviewers, list) else []

        interviewers = [*internal_interviewers,*external_Interviewers]
        for applicant in applicants_list:  
            applicant_id = DataConversion.safe_get(applicant, 'application')
            applicant_email = DataConversion.safe_get(applicant, 'applicant_email')
            position_name = DataConversion.safe_get(applicant, 'position')
            interview_date = DataConversion.safe_get(applicant, 'interview_date')
            from_time = DataConversion.safe_get(applicant, 'form_time')
            to_time = DataConversion.safe_get(applicant, 'to_time')
            short_list_data =DataConversion.safe_get(DataConversion.safe_get(applicant, "linked_fields", None), "application", None)
            applicant_data =get_application_details(dbms, DataConversion.safe_get(short_list_data, "application", None)) or {}
            if applicant_email:
                interviewee_content = Default_Templates.interview_schedule_inverviewee_email_template({
                    "applicant": applicant_id,
                    "position_name": position_name,
                    "interview_date": interview_date,
                    "from_time": from_time,
                    "to_time": to_time,
                    "applicant_email": applicant_email,
                    'interview_location': interview_location,
                })
                send_email = mailing.send_mail(recipient=applicant_email, subject="Interview Invitation", body=interviewee_content)

                interview_object =utils.from_dict_to_object({
                    # "name": "INT-APPLICANT -Jack-Peterson- 0008-0007",
                    "email": applicant_data.applicant_email or "",
                    "contact_no": applicant_data.contact_no or "",
                    "interview_type": None,
                    # "application_outcome": None,
                    "interview_schedule": data.name,
                    "from_time": from_time,
                    "to_time": to_time,
                    "applicant": f"{applicant_data.applicant_first_name} {applicant_data.applicant_middle_name} {applicant_data.applicant_last_name}",
                    "interview_summary": "",
                    "applicant_email": applicant_email,
                    "nationality_registration_number": applicant_data.id_nrc or None,
                    "technical_total": 0,
                    "behavioral_total": 0,
                    "overall_total": 0,
                    "candidates_suitability": None,
                    "technical_competence": [],
                    "behavioral_competence": [],
                    "other_relevant_information": [],
                    "schedule":  interview_date,
                    "offered_job_title": applicant.position or "",
                    "short_listed_applicant": applicant.application
                })
                # pp(interview_object)
                # throw(".....")

                try:
                    create_interview =dbms.create("Interview", interview_object)
                    pp(create_interview)
                except Exception as e:
                    pp(e)
                    pass

        for interviewer in interviewers:
            interviewer_email = DataConversion.safe_get(interviewer, 'interviewer_email')
            if interviewer_email:
                interviewer_subject = "Interview Panel Notification"
                
                content = Default_Templates.interview_schedule_inverviewer_template({'owner_name': interviewer.get('interviewer_first_name', '') + " " + interviewer.get('interviewer_last_name', ''),
                    'applicant': [
                        {
                            'name': applic['application'].replace("APPLICANT -", "").split()[0].rstrip('-'),
                            'form_time': DataConversion.safe_get(applic, 'form_time', ''),
                            'to_time': DataConversion.safe_get(applic, 'to_time', ''),
                            'interview_date': DataConversion.safe_get(applic, 'interview_date', ''),
                        } 
                        for applic in applicants_list
                    ],
                    'interview_location': interview_location,
                    'interview_link': interview_link if interview_link else "N/A",
                })
                send_email = mailing.send_mail(recipient=interviewer_email, subject=interviewer_subject, body=content)
    object.doc_status = "Scheduled"
