from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.core_functions.hr import Core_Hr

utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def on_save_appointment_letter_offer(dbms,object):
    mailing = Mailing(dbms=dbms,object=object)
    core_hr = Core_Hr (dbms=dbms, obj=object)
    letter = object.body
    # email_body= Default_Templates().default_template(document_type=letter.doc_type, subject=letter.designation+" "+"Job Offer", doc_body=letter.appointment_context, company=letter.company, adressed_to=letter.applicant, emailers_name=letter.linked_fields.owner.first_name, job_position=letter.linked_fields.owner.role,)
    # sent = mailing.send_mail(letter.applicant_email, subject="Appointment Letter",body=email_body)
    offer = core_hr.get_doc ("Job_Offer", name=letter.job_offer)
    if offer and offer.accepted:
        application = offer.linked_fields.job_application
        if application:
            employee = utils.from_dict_to_object ({})
            employee.first_name = application.applicant_first_name
            employee.middle_name = application.applicant_middle_name
            employee.last_name = application.applicant_last_name
            employee.email = application.email
            employee.mobile = application.mobile
            employee.designation = application.designation
            employee.company = core_hr.company
            employee.status = "Pending"
            dbms.create ("Employee", employee)

def on_submit_appointment_letter_offer(dbms, object):
    mailing = Mailing(dbms=dbms, object=object)
    core_hr = Core_Hr (dbms=dbms, obj=object)
    letter = object.body
    tenant_url =dbms.host+"web/appointment_letter/"


    email_body= Default_Templates().default_template(document_type=letter.doc_type, subject=letter.designation+" "+"Job Offer", doc_body=letter.appointment_context, company=letter.company, adressed_to=letter.applicant, emailers_name=letter.linked_fields.owner.first_name, job_position=letter.linked_fields.owner.role, include_link=tenant_url)
    sent = mailing.send_mail(letter.applicant_email, subject="Appointment Letter",body=email_body)
    # throw(">>>>>......")

