from controllers.mailing.templates.crm_email_template import Crm_Templates
from controllers.mailing import Mailing
from controllers.utils import Utils
from controllers.core_functions.crm import Core_CRM
import pandas as pd
utils = Utils()
pp = utils.pretty_print
class CRM_Formats:
    def __init__(self)->None:
        pass
    def before_appointment_save(dbms, object):
        mailing = Mailing(dbms=dbms, object=object)
        appointment_body = object.body
        customer_name = appointment_body.customer
        customer_email = appointment_body.customer_email
        lead_name = appointment_body.lead
        lead_email = appointment_body.lead_email
        prospect_name = appointment_body.prospect
        prospect_email = appointment_body.prospect_email
        subject = appointment_body.name
        description = appointment_body.description
        appointment_date = appointment_body.appointment_date
        appointment_venue = appointment_body.venue
        company = appointment_body.company
        appointment_time = appointment_body.appointment_time
        content = {
            "customer": customer_name,
            "appointment_date": appointment_date,
            "appointment_venue": appointment_venue,
            "company": company,
            "appointment_time": appointment_time,
            "description": description,
        }
        email_content = Crm_Templates.appointment_schedule_template(
           content=content
        )
        if customer_name:
            mailing.send_mail(recipient=customer_email, subject=subject, body=email_content)
        elif lead_name:
            mailing.send_mail(recipient=lead_email, subject=subject, body=email_content)
        elif prospect_name:
            mailing.send_mail(recipient=prospect_email, subject=subject, body=email_content)
    
    def on_lead_update(dbms, object):
        mailing = Mailing(dbms=dbms)
        data = object.body
        sales_person = object.body.sales_person
        lead_name = object.body.name
        first_name = data.first_name
        last_name = data.last_name
        subject = f"Hello {last_name} {first_name}"
        body = "<p>We wish you luck on your new task</p>"
        email_content = Crm_Templates.appointment_schedule_template(
            content=(
                f"<p>You have been assigned to nature a lead:</p>"
                f"<p><strong>Lead To Be Natured:</strong> {lead_name}</p>"
                f"<p>{body}</p>"
            ),
            subject=subject
        )
        if sales_person:
            mailing.send_mail(recipient=sales_person, subject=subject, body=email_content)

    def after_submitting_ticket(dbms, object):
        mailing = Mailing(dbms=dbms, object=object)
        support_team = dbms.get_list("Support_Team", filters=None, limit=None, fetch_linked_tables=True, privilege=True)
        if support_team.status != utils.ok:
            return None
        support_data = support_team.data.rows
        if support_data:
            for team_name in support_data:
                team_name['name'] == team_name.name
                team_name['support_team_member'] == team_name.support_team_member

        ticket_doc = object.body
        customer_email = ticket_doc.email
        customer = ticket_doc.customer
        subject = ticket_doc.subject
        relation_manager_email = ticket_doc.relation_manager_email
        support_team = ticket_doc.support_team
        ticket_description = ticket_doc.description
        customer_subject = "Ticket Receipt Confirmation"
        relation_manager_subject = f"New Ticket From: {customer}"

        customer_body = Crm_Templates.template(
            content=(
                f"<p>Dear {customer},</p>"
                f"<p>Thank you for submitting your ticket. We have received your request and our team will get back to you soon.</p>"
                f"<p><strong>Ticket ID:</strong> {ticket_doc.name}</p>"
                f"<p><strong>Ticket Subject:</strong> {ticket_doc.subject}</p>"
                f"<p>We appreciate your patience and will be in touch shortly.</p>"
            ),
            subject=customer_subject
        )
        if relation_manager_email:
            relation_manager_body = Crm_Templates.template(
                subject=relation_manager_subject,
                content=(
                    f"<p>Dear {ticket_doc.relation_manager},</p>"
                    f"<p>A new ticket has been submitted by {customer} please look into the matter as soon as possible.</p>"
                    f"<p><strong>Customer Email:</strong> {customer_email}</p>"
                    f"<p><strong>Ticket ID:</strong> {ticket_doc.name}</p>"
                    f"<p><strong>Ticket Subject:</strong> {ticket_doc.subject}</p>"
                    f"<p><strong>Support Team:</strong> {ticket_doc.support_team}</p>"
                    f"<p><strong>Service:</strong> {ticket_doc.service}</p>"
                    f"<p><strong>Ticket Description:</strong> {ticket_description}</p>"
                )
            )
        else:
            relation_manager_body = None

        mailing.send_mail(recipient=customer_email, subject=customer_subject, body=customer_body)
        if relation_manager_email:
            mailing.send_mail(recipient=relation_manager_email, subject=relation_manager_subject, body=relation_manager_body)
    def on_prospect_save(dbms, object):
        object.doc_status="Pending Conversion"

        
    def on_contract_submit(dbms, object):
        mailing = Mailing(dbms=dbms)
        object.doc_status="Active Contract"
        data = object.body
        customer_name = data["customer"]
        customer_email = data["email"]
        company = data["company"]
        effective_from = data["start_date"]
        effective_to = data["end_date"]
        subject = f"New Contract: {customer_name}"
        email_content = Crm_Templates.template(
            content=(
                f"<p>Dear {customer_name},</p>"
                f"<p>We are excited to inform you that you have a new contract with <strong>{company}</strong>.</p>"
                f"<p><strong></strong>Effective From: {effective_from} <strong>To</strong> {effective_to}.</p>"
                f"<p>Thank you for choosing our services. We value your trust and look forward to working with you.</p>"
                f"<p>If you have any questions or need further assistance, please do not hesitate to reach out to us.</p>"
                f"<p>Best regards,</p>"
                f"<p>Yours {company}</p>"
            ),
            subject=subject
        )
        mailing.send_mail(recipient=customer_email, subject=subject, body=email_content)
        

    def before_submitting_news_letter(dbms, object):
        mailing = Mailing(dbms=dbms, object=object)
        doc_body = object.body
        subject = doc_body.subject
        details = doc_body.email_body
        ss_provider =object.body.company
        data_list = [
            dbms.get_list("Email_Group_Member", filters={"parent": object.body.email_group}),
            dbms.get_list("Lead_Email_Group", filters={"parent": object.body.email_group}),
            dbms.get_list("Prosect_Email_Group", filters={"parent": object.body.email_group}),
        ]

        recipients = [
            {"email": row["email"], "member": row["member"]}
            for data in data_list
            if data.status == utils.ok
            for row in data.get("data", {}).get("rows", [])
            if row.get("email")
            
        ]
        for recipient in recipients:
            member = f"Dear {recipient['member']},"
            email_body = Crm_Templates.news_letter_email_template(content=details, subject=subject, member = member, ssp=ss_provider)
            mailing.send_mail(recipient=recipient["email"], subject=subject, body=email_body)
            

    def email_campaign(dbms, object):
        mailing = Mailing(dbms=dbms, object=object)
        data = object.body
        subject = data.subject
        contact_no = data.contact_no
        company = data.company
        description = data.content
        if data is not None:
            customer_campaign = data.customer_campaign
            prospect_campaign = data.prospect_campaign
            lead_campaign = data.lead_campaign
            improved_content = """
            <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <h2 style="color: #2e1065;">Hello {name},</h2>
                <p style="font-size: 16px;">We are excited to introduce our latest campaign: 
                    <strong style="color: #2e1065;">{subject}</strong>.
                </p>
                <p style="font-size: 14px; color: #555;">If you'd like to learn more, feel free to contact us at:
                    <strong>{contact_no}</strong>.
                </p>
                <p style="font-size: 14px; color: #555;">You can also email us at:
                    <a href="mailto:{email}" style="color: #2196F3; text-decoration: none;">{email}</a>.
                </p>
                <div style="margin-top: 15px; padding: 15px; background-color: #f9f9f9; border-radius: 6px; text-align: center;">
                    <strong>Topic Content:</strong>
                    <p style="font-size: 14px; padding: 10px 15px; background-color: #f1f1f1; border-radius: 4px; color: #333;">
                        {description}
                    </p>
                </div>
                <p style="margin-top: 25px; font-size: 14px;">Best Regards,</p>
                <p style="font-size: 16px; color: #2e1065;"><strong>{company}</strong></p>
            </div>
            """
            if customer_campaign:
                for customer in customer_campaign:
                    customer_email = customer['email']
                    customer_name = customer['customer']
                    if customer_name:
                        email_content = Crm_Templates.template(
                            content=improved_content.format(name=customer_name, subject=subject, contact_no=contact_no, email=customer_email, description=description, company=company
                            ),
                            subject=subject
                        )
                        mailing.send_mail(recipient=customer_email, subject=subject, body=email_content)

            if prospect_campaign:
                for prospect in prospect_campaign:
                    prospect_email = prospect['email']
                    prospect_name = prospect['prospect']
                    if prospect_name:
                        email_content = Crm_Templates.template(
                            content=improved_content.format(name=prospect_name, subject=subject, contact_no=contact_no, email=prospect_email, description=description, company=company),
                            subject=subject
                        )
                        mailing.send_mail(recipient=prospect_email, subject=subject, body=email_content)

            # Send emails to leads
            if lead_campaign:
                for lead in lead_campaign:
                    lead_email = lead['email']
                    lead_name = lead['lead']
                    if lead_name:
                        email_content = Crm_Templates.template(
                            content=improved_content.format(name=lead_name, subject=subject, contact_no=contact_no, email=lead_email, description=description, company=company),
                            subject=subject
                        )
                        mailing.send_mail(recipient=lead_email, subject=subject, body=email_content)
    def relation_manager(dbms, object):
        mailing = Mailing(dbms=dbms, object=object)
        data = object.body
        if data is not None:
            rm_name = data.get("name")
            email = data.get("email")
            subject = "New Customer Relation Manager Assignment"
            supervisor_first_name = data.get("supervisor_first_name")
            supervisor_last_name = data.get("supervisor_last_name")
            customers = data.get("crm_customers")
            crm_customers = [customer['crm_customer'] for customer in customers if customer.get('crm_customer') is not None]
            customer_list = "\n".join(f"<strong style='color: #2e1065;'>{customer}</strong>." for customer in crm_customers)
            email_template = Crm_Templates.template(
                content= (f"""<div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <h2 style="color: #2e1065;">Hello {rm_name},</h2>
                            <p style="font-size: 16px;">We are excited to inform you that you have been given a role of customer relation manager for the following customers: 
                                <strong style="color: #2e1065;">{customer_list}</strong>.
                            </p>
                            <p style="font-size: 14px; color: #555;">Your Supervisor is: :
                                <strong>{supervisor_last_name} {supervisor_first_name}</strong>.
                            </p>
                            <p style="margin-top: 25px; font-size: 14px;">Best Regards,</p>
                        </div>"""
                )
            )
            mailing.send_mail(recipient=email, subject=subject, body=email_template)