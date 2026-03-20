from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

def staff_survey_feedback(dbms, object):
    survey = object.body.data
    get_survey_qs = dbms.get_doc("Employee_Welfare_Survey", name=survey, privilege=True)
    if get_survey_qs.status == utils.ok:
        qs = get_survey_qs.data['welfare_questions']
        qsnanair = get_survey_qs.data['employee_welfare_questionnair']
        
        result = []
        questionnair = []
        for q in qs:
            result.append({
                'question': q['question'],
            })
        for qsn in qsnanair:
            questionnair.append({
                'question': qsn['question'],  
            })
        return utils.respond(utils.ok, {"welfare_questions": result, "questionnaire": questionnair})