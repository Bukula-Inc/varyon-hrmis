from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()
pp =utils.pretty_print
throw = utils.throw

def exit_interview_questionnaire_validate (body):
    if not body.employee_seperation:
        throw("Please select Separation ID")
    if not body.employee:
        throw("Please select Employee")
    if not body.designation:
        throw("Please select Designation")
    if not body.department:
        throw("Please select Department")
    if body.open_ended_questions and not body.closed_ended_questions:
        throw("Please provide feedback for the questions in the questionnaire")

    return body

def before_exit_interview_questionnaire_save (dbms, object):
    object.body =exit_interview_questionnaire_validate(object.body)
