from controllers.utils import Utils
from collections import defaultdict

utils = Utils()
throw = utils.throw

def before_staff_feedback_submit(dbms, object):
    survey = object.body['survey']    
    hr_survey = dbms.get_doc("Employee_Welfare_Survey", name=survey)
    if not hr_survey:
        utils.throw("Survey not found.")
    
    get_all_ans = dbms.get_list("Staff_Feedback", filters={"survey": survey}, privilege=True, fetch_linked_tables=True)
    if not get_all_ans:
        utils.throw("No answers found for the given survey.")
    
    vote_counts = defaultdict(lambda: {'total_yes': 0, 'total_no': 0})
    for ans in get_all_ans.data.rows:
        for answer in ans['question_ans']:
            vote_counts[answer['question']]['total_yes'] += answer['yes']
            vote_counts[answer['question']]['total_no'] += answer['no']    
    for question in hr_survey['data']['welfare_questions']:
        try:
            if question['question'] in vote_counts:
                question['total_yes'] = vote_counts[question['question']]['total_yes']
                question['total_no'] = vote_counts[question['question']]['total_no']
                print(f"Updated question {question['id']}: total_yes={question['total_yes']}, total_no={question['total_no']}")
            else:
                print(f"Skipping question {question['id']}: No votes found.")
        except KeyError as e:
            print(f"Error updating question {question.get('id', 'unknown')}: {str(e)}")
            continue
    
    update_response = dbms.update("Employee_Welfare_Survey", hr_survey['data'])
    if update_response.status != 200:
        utils.throw(f"Failed to update the survey document. Response: {update_response}")
    
    return utils.respond(utils.ok, {"data":"Survey updated successfully"})