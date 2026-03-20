from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object, Object_To_Dict
from controllers.core_functions.hr import Core_Hr

utils = Utils()
pp = utils.pretty_print

def get_appraisal_content(dbms, object):
    open_ended_qs = dbms.get_list("Open_Ended_Question", user=object.user)
    closed_ended_qs = dbms.get_list("Closed_Ended_Question", user=object.user)
    closed_ended_qs_options = dbms.get_list("Appraisal_Question_Option", user=object.user)
    
    openqs = {}
    closedqs = {}
    closedqs_options = {}

    if open_ended_qs.status not in [utils.ok, utils.no_content]:
        return utils.respond(open_ended_qs.status, open_ended_qs.error_message)
    elif open_ended_qs.status == utils.ok:
        open_qns = open_ended_qs.data.rows
        openqs = utils.array_to_dict(open_qns, "name")

    if closed_ended_qs.status not in [utils.ok, utils.no_content]:
        return utils.respond(closed_ended_qs.status, closed_ended_qs.error_message)
    elif closed_ended_qs.status == utils.ok:
        closed_qns = closed_ended_qs.data.rows
        closedqs = utils.array_to_dict(closed_qns, "name")

    if closed_ended_qs_options.status not in [utils.ok, utils.no_content]:
        return utils.respond(closed_ended_qs_options.status, closed_ended_qs_options.error_message)
    elif closed_ended_qs_options.status == utils.ok:
        closed_qns_options = closed_ended_qs_options.data.rows
        closedqs_options = utils.array_to_dict(closed_qns_options, "name")

    return utils.respond(utils.ok, {
        "closedqs": closedqs,
        "openqs": openqs,
        "closedqs_options": closedqs_options,
    })



def behavioral_imperative (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    get_active_bhim = core_hr.get_list ("Performance_Behavioral_Imperative", filters={
        "is_current": 1,
    }, fetch_linked_tables=True, fetch_linked_fields=True,)
    behavior = []
    if get_active_bhim:
        for beha in get_active_bhim:
            behavior.append ({
                "desired_behavior": beha.name,
                "expected_behavior": beha.expected_behavior
            })

    return utils.respond (utils.ok, {"behavioral_imperative": behavior})

def eligible_for_bonus (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    get_eligible_employees = core_hr.get_list ("Appraise_Your_Self", filters={
        "self_app_total_score__gte": 80,
        "eligible_for_bonus": 1,
        "done": 1,
    }, fetch_linked_fields=True,)
    employees = []
    if get_eligible_employees:
        for emp in get_eligible_employees:
            pp (emp)
            employees.append ({
                "employee": emp.employee_id,
                "employee_name": emp.full_name,
                "employee_number": emp.employee_id,
                "employee_designation": emp.designation,
                "department": emp.department,
                "score": emp.self_app_total_score or '0.00',
                "bonus_amount": emp.bonus_amount,
            })

    return utils.respond (utils.ok, {"eligible_for_bonus": employees})