from controllers.utils import Utils
from controllers.mailing import Mailing

utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def on_scholarship_submit(dbms, object):
    object.doc_status ="Pending Approval"

def approve_application(dbms, object):
    scholarship = dbms.get_doc("Training_Program_Application",object.body.data.id, user=object.user)
    if scholarship.get("status") != utils.ok:
        return scholarship
    data = utils.from_dict_to_object(scholarship.get("data"))
    data.status = "Approved"
    update = dbms.update("Training_Program_Application", data, object.user, update_submitted=True)
    return update

def approved_scholarship(dbms, object):
    mailing = Mailing(dbms=dbms)
    id = object.body.id
    applicant = dbms.get_doc("Training_Program_Application", id, privilege=True)
    if applicant.get("status") != utils.ok:
        return applicant 
    else:
        applicant = applicant.get("data")
        applicant_email = applicant.get("email")
        applicant_name = applicant.get("first_name")
        subject = "Scholarship Approval"
        body = f"Hello {applicant_name} Your application for a scholarship training program has been successfully approved best wishes!!!]"
        mailing.send_mail(recipient=applicant_email, subject=subject, body=body)

