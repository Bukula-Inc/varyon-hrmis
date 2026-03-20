from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.mailing import Mailing
from controllers.core_functions.hr import Core_Hr

utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def get__job_application_details(dbms, object):
    tenant_url = f"{dbms.host}:8000/web/medical_clearance/"
    tenant_upload = f"{dbms.host}:8000/web/upload_medical_clearance/?applicant={object.body.data.application}"
    mailing = Mailing(dbms=dbms)
    core_hr = Core_Hr(dbms=dbms)
    return_dict = {}
    doc = dbms.get_list("Interview", filters={"applicant": object.body.data.application})
    get_hr_settings = dbms.get_doc("Hr_Setting", name=core_hr.company)
    get_medical_doc = get_hr_settings.data['medical_clearance'] if get_hr_settings.data['medical_clearance'] is not None else None
    oath_of_secrecy = get_hr_settings.data['oath_of_secrecy'] if get_hr_settings.data['oath_of_secrecy'] is not None else None

    if doc.status == utils.ok:
        data = doc.data.rows
        if isinstance(data, list) and data:  
            data_dict = data[0]  
            return_dict['job_application'] = data_dict.get('applicant')
            return_dict['applicant_email'] = data_dict.get('email')
            return_dict['designation'] = data_dict.get('designation')
            email_body = Default_Templates.recruitment_and_selection(
                document_type="Job Consideration",
                subject="Job Application Consideration",
                doc_body="We are pleased to inform you about your job application progress.",
                company=core_hr.company,
                adressed_to=data_dict.get('applicant'),
                emailers_name="HR Team",
                job_position=data_dict.get('designation'),
                remark_title=1,
                logo="",
                include_link=tenant_url,
                uplodLink=tenant_upload,
                oath_of_secrecy = str(oath_of_secrecy),
                remark=str(get_medical_doc)
            )
            mailing.send_mail(recipient=data_dict.get('email'), subject="Job Consideration", body=email_body)
    return utils.respond(doc.get("status"), return_dict)

def get_job_advertisement_application (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    get_opening = core_hr.get_doc ("Job_Advertisement", object.body.data.job_advertisement)
    return_data = utils.from_dict_to_object ({})
    if not get_opening:
        return_data.status = utils.no_content
        return_data.error_message = f"Job Advertisement {object.body.data.job_advertisement} Is Not Available"
    else:
        skills = []
        qualifications = []
        get_designation = core_hr.get_doc ("Designation", get_opening.designation)
        if get_designation:
            if get_designation.qualification and len (get_designation.qualification) > 0:
                for des_qli in get_designation.qualification:
                    qualifications.append ({"qualification_type": des_qli.qualification,})

            if get_designation.skill and len (get_designation.skill) > 0:
                for des_skill in get_designation.skill:
                    skills.append ({"skill": des_skill.skills,})

        return_data.qualification = qualifications
        return_data.skill = skills
    return utils.respond (status=utils.ok, response=return_data)

def applicants_job_offer(dbms, object):
    returned_data =utils.from_dict_to_object({})
    applicant_details =object.body.data.applicant_details
    full_name =applicant_details.first_name +" "+ applicant_details.other_names
    new_full_name =full_name.replace("  ", " ")
    
    fetch_job_offer =dbms.get_list("Job_Offer", filters={"applicant_name": new_full_name, "applicant_email": applicant_details.applicat_email, "designation":applicant_details.job_designation, "accepted": "" })
    if fetch_job_offer.status ==utils.ok:
        returned_data =fetch_job_offer.data.rows[0]
    else:
        return utils.respond(fetch_job_offer.status, fetch_job_offer.error_message)
    return utils.respond(utils.ok, returned_data)

def job_offer_confirmation(dbms, object):
    return_data =utils.from_dict_to_object({})
    status =utils.ok
    data =object.body.data
    job_application =None
    fetch_job_offer =dbms.get_doc("Job_Offer", data.id)
    if fetch_job_offer.status ==utils.ok: 
        job_offer =fetch_job_offer.data
        fetch_job_application =dbms.get_doc("Job_Application", job_offer.job_application, fetch_by_field="name")
        if fetch_job_application.status ==utils.ok:
            job_application =fetch_job_application.data
        if data.response == "Accept":
            job_offer.status ="Confirmed"
            job_offer.docstatus =1
            job_application.status ="Confirmed"
            job_application.docstatus =1
        else:
            job_offer.status ="Rejected"
            job_offer.docstatus =3
            job_offer.accepted ="Confirmed"
            job_application.status ="Rejected"
            job_application.docstatus =3

        try:
            update_offer =dbms.update("Job_Offer", job_offer, update_submitted=True)
            update_application =dbms.update("Job_Application", job_application, update_submitted=True)
            if update_offer.status:
                status =update_offer.status
            if update_offer.data:
                return_data =update_offer.data
            else:
                return_data =update_offer.error_message
        except Exception as e:
            pp("An Erro Occurred : {e}")

    else:
        status =fetch_job_application.status
        if fetch_job_application.data:
            return_data =fetch_job_application.data
        else:
            return_data =fetch_job_application.error_message


    return utils.respond(utils.ok, {"rows": return_data})

def appointment_letter_approval(dbms, object):
    returned_data =utils.from_dict_to_object({})
    applicant_details =object.body.data
    full_name =applicant_details.first_name +" "+ applicant_details.other_names
    new_full_name =full_name.replace("  ", " ")
    
    fetch_job_offer =dbms.get_list("Appointment_Letter", filters={"applicant_name": new_full_name, "applicant_email": applicant_details.applicat_email, "designation":applicant_details.job_designation })
    if fetch_job_offer.status ==utils.ok:
        returned_data =fetch_job_offer.data.rows[0]
    else:
        return utils.respond(fetch_job_offer.status, fetch_job_offer.error_message)
    return utils.respond(utils.ok, returned_data)

def appointment_letter_confirmation(dbms,object):
    returned_data =utils.from_dict_to_object({})
    applicant_details =object.body.data

    fetch_appointment_letter =dbms.get_doc("Appointment_Letter", applicant_details.id)
    if fetch_appointment_letter.status ==utils.ok:
        appointment_letter =fetch_appointment_letter.data

        if applicant_details.response == "Accept":
            appointment_letter.status ="Confirmed"
            appointment_letter.reporting_date =applicant_details.date
        else:
            appointment_letter.status ="Rejected"
            appointment_letter.docstatus =3

        try:
            update_appointment_letter =dbms.update("Appointment_Letter", appointment_letter, update_submitted=True)
            if update_appointment_letter.status:
                status =update_appointment_letter.status
            if update_appointment_letter.data:
                returned_data =update_appointment_letter.data
            else:
                returned_data =update_appointment_letter.error_message
        except Exception as e:
            pp("An Erro Occurred : {e}")

    else:
        status =fetch_appointment_letter.status
        if fetch_appointment_letter.data:
            returned_data =fetch_appointment_letter.data
        else:
            returned_data =fetch_appointment_letter.error_message

    return utils.respond(utils.ok, returned_data)


def create_short_(dbms, object):
    id = object.body.data.id
    get_Applicant = dbms.get_doc("Job_Application", id)
    if get_Applicant:
        applic_data = get_Applicant.data
        short_list = utils.from_dict_to_object({})        
        short_list.application =applic_data.name
        short_list.applicant_first_name = applic_data.applicant_first_name
        short_list.applicant_middle_name = applic_data.applicant_middle_name
        short_list.applicant_last_name = applic_data.applicant_last_name
        short_list.applicant_email = applic_data.email
        short_list.contact_no = applic_data.mobile
        short_list.job_position = applic_data.designation
        short_list.application_date = applic_data.created_on
        short_list.salary_expectation = applic_data.salary_expectation
        short_list.applicant = applic_data.applicant_first_name + " " + applic_data.applicant_last_name
        short_list.status ="Draft"
        short_list.job_advertisement = applic_data.job_advertisement
        short_list.applicant_skills = []
        for skill in applic_data.job_skills:
            short_list_skill = utils.from_dict_to_object({})
            short_list_skill.skill = skill.skill
            short_list_skill.has_skill = skill.has_skill
            short_list.applicant_skills.append(short_list_skill)
        short_list.document_files = []
        for document in applic_data.applicant_attachement:
            short_list_document = utils.from_dict_to_object({})
            short_list_document.qualification = document.qualification
            short_list_document.qualification_type = document.qualification_type
            short_list.document_files.append(short_list_document)
        create = dbms.create("Applicant_Short_List", short_list, submit_after_create=True)
        if create.status == utils.ok:
            # applic_data.status ="ShortListed"
            # dbms.update("Job_Application", applic_data, update_submitted=True)
            return utils.respond(utils.ok, {"data": create})
        
        return utils.respond(utils.unprocessable_entity,"Failed To Short List This Applicant")
    
def get_designation_description(dbms, object):
    get_desig = object.body.data
    get_doc = dbms.get_list("Designation", filters={"name": get_desig})
    if get_doc:
        df = utils.to_data_frame(get_doc.data.rows)
        pass
        # description = df['description']
        # return utils.respond(utils.ok, {"data": description})
def get_applicant_data(dbms, object):
    get_applicant = dbms.get_list("Interview", filters = {"applicant":object.body.data['applicant_details']})
    if get_applicant.status == utils.ok:
        app_data = get_applicant.data.rows[0]
        get_data = {"applicant": app_data['applicant'],"email": app_data['email'],"contact_no": app_data['contact_no'],}
        return utils.respond(utils.ok, {"applicant": get_data})
def reverse_job_consideration(dbms, object):
    mailing = Mailing(dbms=dbms)
    get_applicant = dbms.get_list("Interview", filters = {"applicant":object.body.data['application']})
    if get_applicant.status == utils.ok:
        df = utils.to_data_frame(get_applicant.data.rows)
        applicant = df['applicant'].iloc[0]
        email = df['email'].iloc[0]
        position = df['designation'].iloc[0]
        body_data = {
            "applicant_name": applicant,
            "email": email,
            "company": dbms.current_user.default_company,
            "position": position,
        }
        subject = "Reverse Job Consideration"  
        body = Default_Templates.reverse_consideration(subject, body_data)
        mailing.send_mail(recipient=email, body=body, subject=subject)
def creating_employee_from_applicant(dbms, object):
    pp(object)
def get_applicant_submitted_documenst(dbms, object):
    pass
        
