from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr
from controllers.utils.dates import Dates
from controllers.mailing import Mailing
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.mailing.templates.default_template import Default_Template



utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw
emailing_templates = Default_Templates()

def validate_job_application(body):
    if body:
        if not body.applicant_last_name:
            throw(f"""The field 'applicant's last name', is missing.""")
        if not body.applicant_first_name:
            throw(f"""The field 'applicant's first name', is missing.""")
        # if not body.applicant_middle_name:
        #     throw(f"""The field 'applicant's middle name', is missing.""")
        if not body.id_nrc:
            throw(f"""The field 'National Resignation Card / ID', is missing.""")
        if not body.job_advertisement:
            throw(f"""The field 'job advertisement', is missing.""")
        if not body.designation:
            throw(f"""The field 'designation', is missing.""")
        if not body.country:
            throw(f"""The field 'country', is missing.""")
        if not body.email:
            throw(f"""The field 'email', is missing.""")
        # if not body.postal_address:
        #     throw(f"""The field 'postal address', is missing.""")
        if not body.physical_address:
            throw(f"""The field 'physical address', is missing.""")
        if not body.date_of_birth:
            throw(f"""The field 'date of birth', is missing.""")
        if not body.marital_status:
            throw(f"""The field 'marital status', is missing.""")
        if not body.mobile:
            throw(f"""The field 'mobile', is missing.""")
        if not body.gender:
            throw(f"""The field 'gender', is missing.""")
        # if not body.applicant_attachement:
        #     throw(f"""The field 'applicant's attachement', is missing.""")
        # if not body.job_skills:
        #     throw(f"""The field 'job skills', is missing.""")
        if not body.letter:
            throw(f"""The field 'letter', is missing.""")
        
    return body

def on_job_application_save(dbms, object):
    object.body =validate_job_application(DataConversion.safe_get(object, "body", {}))

def on_job_application_submit(dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    emailing = Mailing(dbms, object)
    object.body.applicant_name = f"""{object.body.applicant_first_name} {object.body.applicant_middle_name or ''} {object.body.applicant_last_name}"""
    body =object.body
    job_opening =None
    fetch_job_advertisement =dbms.get_doc("Job_Advertisement", body.job_advertisement)
    if fetch_job_advertisement.status ==utils.ok:
        job_advertisement =fetch_job_advertisement.data


    email =Default_Template.template(
        emailing_templates.job_application(sender="", senders_job_title="", receiver=body.applicant_name, job_position=body.designation, contact="",)
    )
    # try:
    #     # send_email =emailing.send_mail(recipient=body.email, subject=f"Job Application FeedBack", body=email)
    # except Exception as e:
    #     pp(e)

    object.doc_status ="Applied"
    object.body.status ="Applied"
    object.body.attachments =[]
# def on_job_application_save(dbms, object):
#     delattr (object.body, "lower_range")
#     delattr (object.body, "upper_range")
    
   