from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import *
from controllers.mailing.templates.hr_email_template import Default_Templates
utils = Utils()



def remove_special_character (string):
    return string.replace("_", " ")

def memos(dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    mailing = Mailing(dbms=dbms)
    memo = object.body
    user = dbms.current_user
    if not DataConversion.safe_get (object.body, "sender"):
        DataConversion.safe_set (object.body, "sender", f"""{user.first_name} {user.middle_name or ''} {user.last_name}""")
    
    remark_text = ""
    remark_title = 0
    attachment_path =None
    cc_init = str (DataConversion.safe_get (memo, "cc"))
    
    key = str (DataConversion.safe_get (memo, "to")).lower ()
    custom = DataConversion.safe_get (memo, "custom", [])
    filters = utils.from_dict_to_object ()
    recipients = []
    if not key:
        throw ("to is required")
    match key:
        case 'individual':
            to = DataConversion.safe_get (memo, "ind")
            if not to:
                throw ("An Individual is required.")
            DataConversion.safe_set (filters, "name", to)
        case 'designation':
            to = DataConversion.safe_get (memo, "desig")
            if not to:
                throw ("Designation is required")
            DataConversion.safe_set (filters, "designation", to)
        case 'department':
            to = DataConversion.safe_get (memo, "dept")
            if not to:
                throw ("Department is required")
            DataConversion.safe_set (filters, "department", to)
        case 'role':
            to = DataConversion.safe_get (memo, "role")
            if not to:
                throw ("Role is required")
            recipients = core_hr.get_list ("Lite_User", filters={"main_role": to})
        case 'all':
            emps = core_hr.get_list ("Employee", filters={"status__in": ["Active", "On Leave", "Suspended"]})
            if emps:
                recipients = emps
        case "custom":
            if not custom or custom and len (custom) <= 0:
                throw ("Please Select Recipients")
            for recipient in custom:
                doc = DataConversion.safe_get (recipient, "recipient")
                if doc:
                    emp = core_hr.get_doc ("Employee", doc)
                    DataConversion.safe_list_append (recipients, emp)
        case _:
            recipients = None
            filters = None
    if not recipients and filters:
        DataConversion.safe_set (filters, "status__in", ["Active", "On Leave", "Suspended"])
        recipients = core_hr.get_list("Employee", filters=filters)
    
    remark = DataConversion.safe_get (memo,"remarks")
    if utils.get_text_from_html_string (remark):
        remark_text = remark
        remark_title = 1
    attach = DataConversion.safe_get (memo, "attachment")
    if attach:
        if type(attach) ==str:
            attachment_path = attach.strip()
    if recipients:
        for recipient in recipients:
            if DataConversion.safe_get (user, "email") != DataConversion.safe_get (recipient, "email"):
                # if cc_init:
                #     cc = cc_init.split (',')
                email_body =Default_Templates().internal_communications(document_type=object.model, subject=memo.subject, doc_body=memo.body, company=recipient.company, adressed_to=recipient.full_name, remark=remark_text, emailers_name=memo.sender, job_position=memo.role, remark_title=remark_title, logo=None,)
                sent =mailing.send_mail(recipient=recipient.email, subject=memo.subject, body=email_body, attachment=attachment_path)
                pp(".....")
                print(sent)
                pp(".....") 

def announcement(dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    mailing = Mailing(dbms=dbms)
    announcement = object.body
    recipients = []
    key = str (DataConversion.safe_get (announcement, "to")).lower ()
    filters = utils.from_dict_to_object ()
    user = dbms.current_user
    if not DataConversion.safe_get (object.body, "sender"):
        DataConversion.safe_set (object.body, "sender", f"""{user.first_name} {user.middle_name or ''} {user.last_name}""")
    if not key:
        throw ("to is required")
    match key:
        case 'individual':
            to = DataConversion.safe_get (announcement, "ind")
            if not to:
                throw ("An Individual is required.")
            DataConversion.safe_set (filters, "name", to)
        case 'designation':
            to = DataConversion.safe_get (announcement, "desig")
            if not to:
                throw ("Designation is required")
            DataConversion.safe_set (filters, "designation", to)
        case 'department':
            to = DataConversion.safe_get (announcement, "dept")
            if not to:
                throw ("Department is required")
            DataConversion.safe_set (filters, "department", to)
        case 'role':
            to = DataConversion.safe_get (announcement, "role")
            if not to:
                throw ("Role is required")
            recipients = core_hr.get_list ("Lite_User", filters={"main_role": to})
        case 'all':
            emps = core_hr.get_list ("Employee", filters={"status__in": ["Active", "On Leave", "Suspended"]})
            if emps:
                recipients = emps
        case _:
            recipients = None
            filters = None
    if not recipients and filters:
        DataConversion.safe_set (filters, "status__in", ["Active", "On Leave", "Suspended"])
        recipients = core_hr.get_list("Employee", filters=filters)
    
    attachment_path = None
    remark = DataConversion.safe_get (announcement,"announcement_context")
    if utils.get_text_from_html_string (remark):
        remark_text = remark
        remark_title = 1
    attach = DataConversion.safe_get (announcement, "attachment")
    if attach:
        if type(attach) ==str:
            attachment_path = attach.strip()
    pp (recipients)
    if recipients:
        for recipient in recipients:
            if DataConversion.safe_get (user, "email") != DataConversion.safe_get (recipient, "email"):
                announcement_template = Default_Templates().internal_communications(document_type=object.model, subject=announcement.subject or announcement.name, doc_body=remark, company=recipient.company, adressed_to=recipient.full_name, remark="", emailers_name=announcement.sender, job_position=announcement.dept, remark_title=0, logo=None,)
                r = mailing.send_mail(recipient=recipient.email, subject=announcement.name, body=announcement_template, attachment=None)
                pp (r)

def bulletin(dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    mailing = Mailing(dbms=dbms)  
    bulletin = object.body
    recipients = core_hr.get_list("Employee")
    
    if bulletin.attachment:
        if type(bulletin.attachment) ==str:
            attachment_path =bulletin.attachment.strip()

    if recipients:
        for recipient in recipients:
            bulletin_template = Default_Templates().internal_communications(document_type=object.model, subject=bulletin.name, doc_body=bulletin.bulletin_context, company=recipient.company, adressed_to=recipient.full_name, remark="", emailers_name="", job_position="", remark_title=0, logo=None,)
            mailing.send_mail(recipient=recipient.email, subject="Newsletter", body=bulletin_template, attachment=None)
            

def get_appraisars(dbms, object):
        mailing = Mailing(dbms=dbms)
        id = object.body.id
        appraisers_list = dbms.get_doc("Appraisal_Setup", id, privilege=True)
        if appraisers_list.status != utils.ok:
            return appraisers_list
        else:
            appraisals = appraisers_list
            appraisers = appraisals.data.appraisers
            for appraiser in appraisers:
                appraiser_email = appraiser.appraiser_email
                appraisal_name = appraiser.appraiser_name
                subject="Appraisal Awaits"
                body="<p>You Have Been Selected To Appraise</p>"
                appraisers_notification_template = Default_Templates.internal_communications(document_type=remove_special_character(object.model), subject=policy.name, doc_body=body, company=receiver.company, adressed_to=receiver.full_name, remark="", emailers_name="", job_position="", remark_title=0, logo=None,)
                utils.pretty_print(appraisers_notification_template)
                if appraiser_email:
                    utils.pretty_print(appraiser_email)
                    mailing.send_mail(recipient=appraiser_email, subject=subject, body=appraisers_notification_template, attachment=None)

def on_company_policy (dbms, object):
    core_hr = Core_Hr (dbms=dbms, user=object.user, obj=object)
    mailing = Mailing(dbms=dbms)
    policy = object.body
    receivers = core_hr.get_list("Employee", filters={"status__in": ["Active", "On Leave", "Suspended"]})
    if receivers:
        for receiver in receivers:   
            policy_template =Default_Templates().internal_communications(document_type=remove_special_character(object.model), subject=policy.name, doc_body=policy.policy_context, company=receiver.company, adressed_to=receiver.full_name, remark="", emailers_name="", job_position="", remark_title=0, logo=None,)
            mailing.send_mail(recipient=receiver.email, subject=policy.name, body=policy_template, attachment=None)
            