from controllers.utils import Utils
import requests
from controllers.mailing import Mailing
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.print_controller import Print_Controller

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def on_save_job_offer(dbms,object):
    mailing = Mailing(dbms=dbms,object=object)
    
    application = object.body


    fetch_job_application =dbms.get_doc("Job_Application", application.job_application, fetch_by_field="name")
    if fetch_job_application.status ==utils.ok:
        fetch_job_application.data.status ="Accepted | Pending Confirmation"
        try:
            update_application =dbms.update("Job_Application", fetch_job_application.data, skip_hooks=True)
        except Exception as e:
            pp("An Error Occured :{e}")


def before_job_offer_submit(dbms, object):
    application = object.body
    link_to_appointment_letter =None
    mailing = Mailing(dbms=dbms,object=object)
    tenant_url =dbms.host+f"web/job_offer/?module=web&app=web&page=info&content_type=job_offer_confirmation&doc={application.id}"
    tenant_data =dbms.validation

    download_controller =Print_Controller(request=tenant_data, model="Job_Offer", print_format="ECZ Job Offer Letter", doc=application.id)

    generate_appointment_letter =download_controller.generate_print_doc(skip_validation=True, is_internal_processing=True)

    if generate_appointment_letter.status ==utils.ok:
        link_to_appointment_letter =generate_appointment_letter.data

    email_body =Default_Templates().joboffer_template(document_type=application.doctype.replace("_"," "), subject="", doc_body=application.terms_and_conditions, company=application.company, adressed_to=application.applicant_name, remark=None, emailers_name=f"{application.linked_fields.owner.applicant_email} {application.linked_fields.owner.first_name}", job_position=application.linked_fields.owner.main_role, include_link=tenant_url)
    
    sent = mailing.send_mail(application.applicant_email, subject=f"Job Offer For {application.designation}",body=email_body, attachment=link_to_appointment_letter)
    # throw("................................")
   
    # application.applicant_email  "https://www.startapperp.com"  http://0.0.0.0:8000/web/job_offer/ application.applicant_email


