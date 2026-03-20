from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.core_functions.hr import Core_Hr
from datetime import datetime


utils = Utils ()
pp = utils.pretty_print
throw =utils.throw

def on_submit_outcome (dbms, object):
    mailing = Mailing (dbms=dbms, object=object)
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    outcome = object.body
    check_box_validator ="1"
    offenders_email =""
    # pp (outcome)
    get_discipline = outcome.linked_fields.employee_disciplinary
    get_aggriever = outcome.linked_fields.subject
    issue = core_hr.get_doc ("Employee_Grievance", name=get_discipline.issue)
    get_aggrieved = core_hr.get_doc ("Employee", name=get_discipline.issue_raiser)
    get_offender =core_hr.get_doc("Employee", name=get_discipline.subject)
    user =dbms.current_user

    if get_offender.email:
        offenders_email =get_offender.email

    if outcome.written_warning:
        if isinstance(outcome.written_warning, int):
            check_box_validator =1

    if outcome.written_warning ==check_box_validator:
        if outcome.warning and offenders_email:
            warning_mail =Default_Templates.case_outcome_warning_mail(sender=user.first_name+" "+user.last_name, senders_job_title=user.role, receiver=get_offender.full_name or "", body=outcome.warning, company=None, document_type="Warning Letter")
            sent = mailing.send_mail (recipient=offenders_email, subject=get_discipline.violation_type, body=warning_mail)
        elif not offenders_email:
            throw("No Email is attached to the employee.")
        else:
            throw("No Message was provided for an email to be sent.")

    amsg = f"""
        <p>Your Issue Patterning {get_discipline.violation_type} has been <b>Resolved</b></p>
        <br />
    """
    email_body_aggrieved =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=get_aggrieved.full_name, company=None, body=amsg, final_greetings="Stay Safe!")
    sent = mailing.send_mail (recipient=get_aggrieved.email, subject=get_discipline.violation_type, body=email_body_aggrieved)
    msg = f"""
        <p>Your Issue Patterning {get_discipline.violation_type} has been <b>Resolved</b></p>
        <br />
    """
    email_body_get_aggriever =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=get_aggriever.full_name, company=None, body=msg, final_greetings="Stay Safe!")
    sent = mailing.send_mail (recipient=get_aggriever.email, subject=get_discipline.violation_type, body=email_body_get_aggriever)


    if issue: issue.status = "Resolved"
    
    dbms.update ("Employee_Grievance", issue, user_id=object.user)
    if outcome.suspension and outcome.start_date <= datetime.now ().date ():
        get_aggriever.status = "Suspended"
        get_aggriever.is_separated = 2
        get_aggriever.last_day_of_work = outcome.start_date
        dbms.update ("Employee", get_aggriever, user_id=object.user)
    elif outcome.termination and outcome.effective_date <= datetime.now ().date ():
        get_aggriever.status = "Terminated"
        get_aggriever.is_separated = 1
        get_aggriever.last_day_of_work = outcome.effective_date
        dbms.update ("Employee", get_aggriever, user_id=object.user)