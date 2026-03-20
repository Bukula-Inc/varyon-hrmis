from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.core_functions.hr import Core_Hr
utils = Utils()
throw = utils.throw
pp = utils.pretty_print


def on_training_feedback_save (dbms, object):
    mailing = Mailing (dbms=dbms,object=object)
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    feedback = object.body
    employee = core_hr.get_doc ("Employee", name=feedback.employee)
    user =dbms.current_user
    if employee:
        program = core_hr.get_doc ("Training_Program", name=feedback.training_program)
        if program:
            msg = f"""
                Thank you for Your Feedback on the that you participatraining programed in {program.name}
            """
            email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee.full_name, company=None, body=msg)
            sent = mailing.send_mail (employee.email, subject=program.name, body=email_body)
            # pp (sent)
