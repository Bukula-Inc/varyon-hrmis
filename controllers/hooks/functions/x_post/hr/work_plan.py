from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion


utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw
def save__ (dbms, object):
    pass

# def activate_performance_agreement (dbms, object):
#     core_hr = Core_Hr (dbms=dbms)
#     object.body.is_active = 1
#     deactivate = core_hr.get_list ("Performance_Agreement", filters={
#         "is_active": 1,
#         "employee_id": object.body.employee_id
#     })
#     if deactivate:
#         for pa in deactivate:
#             pa.is_active = 0,
#             pa.status = "Completed"
#             dbms.update ("Performance_Agreement", pa, update_submitted=True)
#     r = dbms.update ("Performance_Agreement", object.body, update_submitted=True)
#     pp (r)

# def work_plan_process_task_work (dbms, object):
#     core_hr = Core_Hr (dbms)
#     status = utils.unprocessable_entity
#     msg = "Failed"
#     work_plan = core_hr.get_doc ("Work_Plan", object.body.data.doc)
#     if work_plan and len (work_plan.work_plan_task) > 0:
#         for task in work_plan.work_plan_task:
#             pp (task)
#             pp (object.body.data.type)
#             utils.throw ()
#             if task.title == object.body.data.title:
#                 if str (object.body.data.type).lower() == "start":
#                     task.progress_tracker = "In Progress"
#                     task.started_on = dates.today ()
#                 elif str (object.body.data.type).lower() == "complete":
#                     task.completed_on = dates.today ()
#                     task.progress_tracker = "Completed"
#                 elif str (object.body.data.type).lower() == "issue":
#                     task.progress_tracker = "Need Some More Time"
#         r = dbms.update ("Work_Plan", work_plan, update_submitted=True)
#         if r.status == utils.ok:
#             status = utils.ok
#             msg = "Successful"
#     return utils.respond (status, msg)

def work_plan_process_task_work (dbms, object):
    core_hr = Core_Hr (dbms)
    status = utils.unprocessable_entity
    msg = "Failed"
    work_plan = core_hr.get_doc ("Performance_Agreement", object.body.data.doc)
    performance_kpi = DataConversion.safe_get (work_plan, "performance_kpi", [])
    type_ = DataConversion.safe_get (object.body.data, "type")
    tfe = DataConversion.safe_get (object.body.data, "obj", {})
    if work_plan and len (performance_kpi) > 0 and tfe:
        kra = DataConversion.safe_get (tfe, "key_result")
        sg = DataConversion.safe_get (tfe, "strategic_goal")
        ta = DataConversion.safe_get (tfe, "thematic_area")
        if not kra:
            throw ("key performance area is required")
        if not kra:
            throw ("key performance area is required")
        for task in performance_kpi:
            type_ = DataConversion.safe_get (object.body.data, "type")
            t_kra = DataConversion.safe_get (task, "key_result")
            # t_sg = DataConversion.safe_get (task, "strategic_goal")
            # t_ta = DataConversion.safe_get (task, "thematic_area")
            # if DataConversion.safe_e (t_kra, kra, str, True) and DataConversion.safe_e (t_sg, sg, str, True) and DataConversion.safe_e (t_ta, ta, str, True):
            if DataConversion.safe_e (t_kra, kra, str, True):
                if DataConversion.safe_e (type_, "start", str, True):
                    DataConversion.safe_set (task, "progress_tracker", "In Progress")
                    DataConversion.safe_set (task, "started_on", dates.today ())
                elif DataConversion.safe_e (type_, "complete", str, True):
                    DataConversion.safe_set (task, "completed_on", dates.today ())
                    DataConversion.safe_set (task, "progress_tracker", "Completed")
                elif DataConversion.safe_e (type_, "issue", str, True):
                    DataConversion.safe_set (task, "progress_tracker", "Need Some More Time")
        r = dbms.update ("Performance_Agreement", work_plan, update_submitted=True)
        if r.status == utils.ok:
            status = utils.ok
            msg = "Successful"
    return utils.respond (status, msg)

def get_work_plan (dbms, object):
    core_hr = Core_Hr (dbms)
    status = utils.unprocessable_entity
    msg = "No Performance Agreement"
    # work_plan = core_hr.get_list ("Performance_Agreement_KPIs")
    # work_plan = core_hr.get_list ("Performance_Agreement_KPIs", filters={"progress_tracker__in": ["In Progress", "Pending", "Need Some More Time"], "is_current": 1, "status": "Active", "planer_of_work_plan": object.body.data.emp})
    work_plan = core_hr.get_list ("Performance_Agreement_KPIs", filters={"progress_tracker__in": ["In Progress", "Pending", "Need Some More Time"], "planer_of_work_plan": object.body.data.emp})
    pp (work_plan)
    if work_plan:
        msg = []
        for  task in work_plan:
            msg.append ({
                "task": task.title,
                "description": task.description
            })
        status = utils.no_content
    return utils.respond (status, msg)

def activate_work_plan (dbms, object):
    core_hr = Core_Hr (dbms)
    status = utils.unprocessable_entity
    msg = "Failed"
    work_plan = core_hr.get_doc ("Work_Plan", object.body.data.doc)
    if work_plan:
        work_plan.is_current = 0
        work_plan.status = "Active"
        r = dbms.update ("Work_Plan", work_plan)
        if r.status == utils.ok:
            msg = "success"
            status = utils.ok
    return utils.respond (status, msg)

def request_adjustment (dbms, object):
    status = utils.ok
    msg = "Success"
    core_hr = Core_Hr (dbms)
    obj = DataConversion.safe_get (object.body, "data")
    title = DataConversion.safe_get (obj, "title")
    expected_start_date = DataConversion.safe_get (obj, "expected_start_date")
    expected_end_date = DataConversion.safe_get (obj, "expected_end_date")
    description = DataConversion.safe_get (obj, "description")
    work_plan = DataConversion.safe_get (obj, "work_plan")
    reason = DataConversion.safe_get (obj, "reason")

    if not work_plan:
        throw ("Target is <strong class='text-rose-600'> missing </strong>")
    
    if not title:
        throw ("Title is <strong class='text-rose-600'> missing </strong>")
    
    if not expected_start_date:
        throw ("Expected start date is <strong class='text-rose-600'> missing </strong>")
    
    if not expected_end_date:
        throw ("Expected end date is <strong class='text-rose-600'> missing </strong>")
    
    if not description:
        throw ("Task description is <strong class='text-rose-600'> missing </strong>")
    
    if not reason:
        throw ("Reason for adjustment is <strong class='text-rose-600'> missing </strong>")
    work_plan_doc = core_hr.get_doc ("Performance_Agreement", work_plan)
    if not work_plan_doc:
        throw (f"Targets with name/ID {work_plan} <strong class='text-rose-600'> was not found </strong>")
    
    task_adjustment = utils.from_dict_to_object ()

    DataConversion.safe_set (task_adjustment, "work_plan", work_plan)
    DataConversion.safe_set (task_adjustment, "title", title)
    DataConversion.safe_set (task_adjustment, "expected_start_date", expected_start_date)
    DataConversion.safe_set (task_adjustment, "expected_end_date", expected_end_date)
    DataConversion.safe_set (task_adjustment, "description", description)
    DataConversion.safe_set (task_adjustment, "status", "Draft")
    DataConversion.safe_set (task_adjustment, "reason", reason)

    r = dbms.create ("Request_Task_Adjustment", task_adjustment, submit_after_create=True)
    if r.status != utils.ok:
        status = utils.unprocessable_entity
        msg = "Failed"

    return utils.respond (status, msg)

def get_appraisal_for (dbms, object):
    ret_data = utils.from_dict_to_object ()
    core_hr = Core_Hr (dbms=dbms)
    previous_app = core_hr.get_list ("Appraise_Your_Self", order_by=['-id'], filters={
        "employee_id": object.body.data.emp,
        "done": 1,
    }, limit=1)

    if previous_app:
        DataConversion.safe_set (ret_data, "date_of_previous_assessment", DataConversion.safe_get (previous_app[0], "date_of_previous_assessment"))
        DataConversion.safe_set (ret_data, "self_app_total_score", DataConversion.safe_get (previous_app[0], "self_app_total_score"))
        
    get_active_appraisal = core_hr.get_list ("Performance_Agreement", filters={
        "is_active": 1,
        "employee_id": object.body.data.emp,
        "status__in": ["Submitted", "Approved"],
    }, fetch_linked_tables=True, fetch_linked_fields=True, limit=1)

    if get_active_appraisal:
        DataConversion.safe_set(ret_data, "targets", get_active_appraisal[0] or {})

    return utils.respond (utils.ok, ret_data)