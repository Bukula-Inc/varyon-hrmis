from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.core_functions.hr import Core_Hr

utils = Utils ()
pp = utils.pretty_print
throw =utils.throw

def on_save_grievance (dbms, object):
    mailing = Mailing (dbms=dbms, object=object)
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    grievance = object.body
    get_siq = core_hr.get_doc ("Employee", name=grievance.grievance_against)
    if get_siq:
        grievance_email =Default_Templates().grievance(sender=grievance.raised_by, receiver=grievance.grievance_against, company=grievance.company, body=grievance.description)
        sent = mailing.send_mail (recipient=get_siq.email, subject=grievance.grievance_type, body=grievance_email)
    # throw("<<<...===...>>>")

def on_submit_of_grievance (dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    mailing = Mailing (dbms=dbms, object=object)
    user =dbms.current_user
    pp(user)
    grievance = object.body
    get_aggrieved = core_hr.get_doc ("Employee", name=grievance.raised_by)
    get_aggriever = core_hr.get_doc ("Employee", name=grievance.grievance_against)
    if grievance.escalation == "Escalate To Disciplinary":

        dsf = {}
        dsf['issue_raiser'] = get_aggrieved.name
        dsf['issue_raiser_name'] = get_aggrieved.full_name
        dsf['issue_raiser_department'] = get_aggrieved.department
        dsf['issue_raiser_reports_to'] = get_aggrieved.reports_to
        dsf['subject'] = get_aggriever.name
        dsf['subject_name'] = get_aggriever.full_name
        dsf['subject_department'] = get_aggriever.department
        dsf['subject_reports_to'] = get_aggriever.reports_to
        dsf['date_of_warning'] = grievance.grievance_date
        dsf['subject_statement'] = grievance.resolution_details
        dsf['issue'] = grievance.name
        dsf['violation_type'] = grievance.violation_type 
        dsf['status'] = "Draft"
        dsf['violation_date'] =grievance.grievance_date


        # emp_displine =utils.from_dict_to_object({
        #     # "company_id": null,
        #     "issue_raiser_name": "Nor aa Ron",
        #     "issue_raiser_reports_to": "euio esrdytfugui - 0014",
        #     "subject_name": "euio wertyu esrdytfugui",
        #     "subject_reports_to": "",
        #     "date_of_warning": "2025-01-21",
        #     "violation_date": "2025-01-21",
        #     "violation_location": "office",
        #     "description_of_violation": "<p>wetryiu</p>",
        #     "subject_statement": "<p>awetryuiuiop</p>",
        #     "owner": "admin1@startappsolutions.com",
        #     "modified_by": null,
        #     "status": "Draft",
        #     "issue": "EMP-GRV-Nor aa Ron-0001",
        #     "issue_raiser": "Nor Ron - 0026",
        #     "issue_raiser_department": "Development",
        #     "subject": "euio esrdytfugui - 0014",
        #     "subject_department": "Development",
        #     "violation_type": "Unfair treatment by supervisors or managers",
        # })



        created = dbms.create ("Employee_Disciplinary", utils.from_dict_to_object(dsf), user_id=object.user)
        if created.status == utils.ok: 
            disciplinary_data =created.data
            get_disciplinary_committee = core_hr.get_doc ("Disciplinary_Committee", name=grievance.company)
            if get_disciplinary_committee:
                members = get_disciplinary_committee.members
                for member in members:
                    disciplinary_email =Default_Templates().disciplinary(sender=user.first_name+ " "+user.last_name, receiver=disciplinary_data.subject_name, company=None, issue_date=disciplinary_data.violation_date, violation_type=disciplinary_data.violation_type)
                    sent = mailing.send_mail (recipient=member.member_email, subject=grievance.grievance_type, body=disciplinary_email)
           
            disciplinary_email =Default_Templates().disciplinary(sender=user.first_name+ " "+user.last_name, receiver=disciplinary_data.subject_name, company=None, issue_date=disciplinary_data.violation_date, violation_type=disciplinary_data.violation_type)
            sent = mailing.send_mail (recipient=get_aggrieved.email, subject=grievance.grievance_type, body=disciplinary_email)

        object.doc_status = "Escalated To Disciplinary"

    else:
        pass

        # amsg =Default_Templates().resolved_grievance(sender=user.first_name+ " "+user.last_name, receiver=get_aggrieved.full_name, company=None, body=grievance.resolution_details, grieve_data=grievance)

        # sent = mailing.send_mail (recipient=get_aggrieved.email, subject=grievance.grievance_type, body=amsg)

        # msg =Default_Templates().resolved_grievance(sender=user.first_name+ " "+user.last_name, receiver=get_aggriever.full_name, company=None, body=grievance.resolution_details, grieve_data=grievance)
        # sent = mailing.send_mail (recipient=get_aggriever.email, subject=grievance.grievance_type, body=msg)
        # object.doc_status = "Resolved"