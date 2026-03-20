from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.mailing import Mailing

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def before_offence_category_save(dbms, object):
    if not object.body.name:
        throw(f"The field 'name', is empty.") 
    if not object.body.title:
        throw(f"The field 'title', is empty.") 
    if not object.body.description:
        throw(f"The field 'description', is empty.")


def before_offence_save(dbms, object):

    if not object.body.name:
        throw(f"The field 'name', is empty.")
    if not object.body.first_breach:
        throw(f"The field 'first breach', is empty.")
    if not object.body.category:
        throw(f"The field 'category', is empty.")

def before_committee_save(dbms, object):
    body =object.body
    if not body.chairperson:
        throw("The chairperson field is not having a value ")
    if not body.internal_members and body.external_members:
        throw("The member list tables are empty")
    if len(body.internal_members) +len(body.external_members) <2:
        throw("The committee is required to have a minimum 3 members.")


def before_charge_form_submit(dbms, object):
    body =object.body
    mail =Mailing(dbms, object)
    email_templates =Default_Templates()
    accused =None    
    if body.linked_fields and body.employee:        
        accused =body.linked_fields.employee
    else:
        fetch_emp_data =dbms.get_doc("Employee", body.employee)
        if not fetch_emp_data:
            throw("The charged employee does not exist")
        accused =fetch_emp_data.data

    email_body =email_templates.charge_notice(sender =body.charging_officer, receiver =accused.full_name, company ="Examination Council of Zambia", offence=body.offence, charger_contact="")
    send_mail =mail.send_mail(accused.email or "", subject="Offence Charge", body=email_body)



    
