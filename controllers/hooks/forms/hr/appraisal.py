from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
utils = Utils()
dates = Dates()
throw = utils.throw
pp = utils.pretty_print

def used_performance_agreement (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    obj = DataConversion.safe_get (object, "body")
    self_app_total_score = DataConversion.convert_to_float (DataConversion.safe_get (obj, "self_app_total_score"))
    if self_app_total_score >= 80:
        emp = core_hr.get_doc ("Employee", DataConversion.safe_get (obj, "employee_id"))
        if not emp:
            throw ("Failed To Process Employee No is Missing")
        basic = DataConversion.convert_to_float (DataConversion.safe_get (emp, "basic_pay"))
        if not basic:
            throw ("Failed To Process Employee Basic Pay is Missing")
        DataConversion.safe_set (object.body, "bonus_amount", basic/2)
        DataConversion.safe_set (object.body, "eligible_for_bonus", 1)
    else:
        DataConversion.safe_set (object.body, "eligible_for_bonus", 0)
    DataConversion.safe_set (object.body, "done", 1)

    deactivate = core_hr.get_list ("Performance_Agreement", filters={
        "is_active": 1,
        "employee_id": object.body.employee_id
    })

    if deactivate:
        for pa in deactivate:
            pa.is_active = "0",
            pa.status = "Completed"
            r = dbms.update ("Performance_Agreement", pa, update_submitted=True)

def calculate_score (dbms, object):
    obj = object.body
    score_bi = 0.00
    score_bi_ro = 0
    score_po_ro = 0
    score_po = 0.00


    if DataConversion.safe_get (obj, "behavioral_imperative"):
        for b_itm in DataConversion.safe_get (obj, "behavioral_imperative"):
            score_bi_ro += 1
            score_bi +=  DataConversion.convert_to_int (b_itm.rating_b)

    if DataConversion.safe_get (obj, "performance_kpi"):
        for b_itm in DataConversion.safe_get (obj, "performance_kpi"):
            score_po_ro += 1
            score_po +=  DataConversion.convert_to_int (b_itm.rating_po)
    
    behavioral_imperatives_score = DataConversion.convert_to_float (score_bi/(score_bi_ro * 5) * 40)
    performance_objective_score = DataConversion.convert_to_float (score_po/(score_po_ro * 5) * 60)

    DataConversion.safe_get (object.body, "date_of_previous_assessment", DataConversion.safe_get (obj, "date_of_previous_assessment", dates.today ()))
    DataConversion.safe_set (object.body, "behavioral_imperatives_score", behavioral_imperatives_score)
    DataConversion.safe_set (object.body, "performance_objective_score", performance_objective_score)
    DataConversion.safe_set (object.body, "self_app_total_score", performance_objective_score + behavioral_imperatives_score)


def before_appraisal_save(dbms, object):
    pass


def after_appraisal_fetch(dbms, object,result):
    pass
    

def before_appraisal_update(dbms, object):
    # core = Core_Hr(dbms, object)
    # body = object.body
    # total_score = 0
    # open_ended_qns = core.get_appraisal_open_ended_questions()
    # closed = core.get_appraisal_closed_ended_questions(True)
    # closed_ended_qns = closed.questions
    # options = closed.options
    # options_rates = {option.name: option.rate for option in options}
    # open_keys = utils.get_object_keys(utils.array_to_dict(open_ended_qns, "name"))
    # closed_keys = utils.get_object_keys(utils.array_to_dict(closed_ended_qns, "name"))
    # if not object.body.open_ended_questions:
    #     object.body.open_ended_questions = []
    # if not object.body.closed_ended_questions:
    #     object.body.closed_ended_questions = []
    # for label, value in body.items():
    #     if label in open_keys:
    #         object.body.open_ended_questions.append({label: value})
    #     elif label in closed_keys:
    #         if value in options_rates:
    #             total_score += options_rates[value]
    #         object.body.total_closed_score = total_score
    #         object.body.closed_ended_questions.append({label: value})
    pass


def before_appraisal_submit(dbms, object):
    core = Core_Hr(dbms, object)
    openqs = {}