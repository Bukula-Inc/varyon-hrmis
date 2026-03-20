from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.utils import Utils
from controllers.utils.dates import Dates 
from controllers.mailing import Mailing
from datetime import datetime
utils = Utils()
dates = Dates ()
throw = utils.throw
pp = utils.pretty_print

def training_program_before_save(dbms, object):
    body =object.body
    #TRAINING PROGRAM Status STRING
    scheduled ="scheduled"
    on_going ="on_going"
    rejected ="rejected"
    completed ="completed"

    body.current_state =scheduled

def on_training_program_submit(dbms, object):
    mailing = Mailing(dbms=dbms, object=object)
    # object.doc_status = "Pending Approval"
    tp = object.body
    trainer = tp.trainer
    owner = tp.linked_fields.owner
    owner_name = f"""{owner.first_name if owner.first_name else ''} {owner.middle_name if owner.middle_name else ''} {owner.last_name if owner.last_name else ''}"""
    if tp.initiator == "Company":
        
        if tp.time_date == "Date":
            period = f"<b>Dates:</b> {tp.start_date} - {tp.end_date}"
            duration = f"{dates.calculate_days (tp.start_date, tp.end_date)} days"
        else:
            period = f"<b>Time:</b> {tp.start_time} - {tp.end_time}"
            duration = "1 day"
        if tp.attendee:
            for attendee in tp.attendee:
                attendee_info = attendee.linked_fields.employee
                msg = f"""
                    <br />
                    We are pleased to inform you that you have been selected to participate 
                    in our upcoming Training and Development Program at {tp.company}. This 
                    program is designed to enhance your skills and knowledge, and equip you 
                    with the tools and expertise needed to excel in your role and contribute 
                    to the growth and success of our organization.
                    The Training will be delivered by {trainer}.
                    Below are the program details:
                    <br />
                    Program Title: {tp.name}
                    <br />
                    {period}
                    <br />
                    Location: {tp.location}
                    <br />
                    Duration: {duration}
                    <br />
                    {tp.description}
                    <br />
                    Congratulations again on your selection, and we wish you a rewarding learning experience.
                    <br />
                """
                email_body =Default_Templates().basic_template(sender=owner_name, receiver=attendee_info.full_name, company=None, body=msg, final_greetings="Best regards")
                # pp (msg)
                sent = mailing.send_mail (recipient=attendee.email, subject=tp.name, body=email_body)
    else:
        if tp.attendee:
            for attendee in tp.attendee:
                attendee_info = attendee.linked_fields.employee
                msg = f"""
                    <br />
                    We are pleased to inform you that your Submission for a training and development program has been accepted.
                    {tp.company} will keep to its end and provide the necessary help and provided you keep your end.
                    The Training will be delivered by {trainer}.
                    
                    Congratulations again on your Submission, and we wish you a rewarding learning experience.
                    <br />
                    Best regards,
                    
                    {tp.company}
                """
                email_body =Default_Templates().basic_template(sender=owner_name, receiver=attendee_info.full_name, company=None, body=msg)
                sent = mailing.send_mail (recipient=attendee.email, subject=tp.name, body=email_body)
    
def before_training_resources(dbms, object):

    pp(object)
    # throw("before_resource_storage")training_plan


def before_training_plan_save(dbms, object):

    start =datetime.strptime(object.body.from_date, '%Y-%m-%d')
    end =datetime.strptime(object.body.to_date, '%Y-%m-%d')
    today =datetime.strptime(dates.today(), '%Y-%m-%d')

    if start < today and end > today:
        object.body.use_status ="active"


