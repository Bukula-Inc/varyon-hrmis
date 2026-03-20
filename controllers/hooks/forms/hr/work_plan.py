from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.default_template import Default_Template
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates

utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates ()

def activate_performance_agreement (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    object.body.is_active = 1
    deactivate = core_hr.get_list ("Performance_Agreement", filters={
        "is_active": 1,
        "employee_id": object.body.employee_id
    })
    if deactivate:
        for pa in deactivate:
            pa.is_active = 0,
            pa.status = "Completed"
            dbms.update ("Performance_Agreement", pa, update_submitted=True)
    r = dbms.update ("Performance_Agreement", object.body, update_submitted=True)
    performance_kpi = []
    if object.body.performance_kpi and len (object.body.performance_kpi) > 0:
        for kpi in object.body.performance_kpi:
            kpi.progress_tracker = "Pending"
            kpi.status = "Active"
            kpi.is_current = 1
            kpi.planer_of_work_plan = object.body.employee_id
            performance_kpi.append (kpi)
    object.body.performance_kpi = performance_kpi

def on_submit_work_plan (dbms, object):
    core_hr = Core_Hr (dbms=dbms, user=object.user, obj=object)
    mailing = Mailing (dbms=dbms,object=object)
    object.doc_status = "Pending Review"
    object.body.status = "Pending Review"
    if object.body.linked_fields.employee.report_to:
        recipient = core_hr.get_doc ("Employee", name=object.body.linked_fields.employee.report_to)
        if recipient:
            sub = f"{object.body.full_name} Work Plan Submission"
            msg = f"""<h3>Hello! </h3>, <br /> there has been a new submission of a work plan that is pending your review Or Approval """
            mailing.send_mail(recipient=recipient.email, subject=sub, body=Default_Template.template (msg, subject=sub))

def on_save_work_plan (dbms, object):
    planner = object.body.employee
    if not planner:
        throw ("Employee No is missing")
    for i, task in enumerate (object.body.work_plan_task):
        task.planer_of_work_plan = planner
        task.progress_tracker = "Pending"
        if not task.expected_start_date:
            throw (f"Task on Row #: {i+1} is missing expected start date")
        if not task.expected_end_date:
            throw (f"Task on Row #: {i+1} is missing expected end date")

def on_work_plan_issue (dbms, object):
    DataConversion.safe_set (object, "doc_status", "Draft")
    DataConversion.safe_set (object.body, "used", 0)

def submit_work_plan_issue (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    doc = DataConversion.safe_get (object.body, "work_plan")
    work_plan = core_hr.get_doc ("Performance_Agreement", doc)
    if  not work_plan:
        throw (f"Failed Targets Plan with name/ID {doc} not found")

    performance_kpi = DataConversion.safe_get (work_plan, "performance_kpi", [])
    from_date = DataConversion.safe_get (work_plan, "expected_start_date", dates.today ())
    end_date = DataConversion.safe_get (work_plan, "expected_end_date", dates.today ())
    if work_plan and len (performance_kpi) > 0:
        for task in performance_kpi:
            if DataConversion.safe_e (DataConversion.safe_get (work_plan, "title"), DataConversion.safe_get (task, "title"), str, True):
                # pp(work_plan,task)
                # if not DataConversion.safe_e (DataConversion.safe_get (work_plan, "description"), DataConversion.safe_get (task, "description"), str, True):
                DataConversion.safe_set (task, "expected_start_date", from_date)
                DataConversion.safe_set (task, "expected_end_date", end_date)
                DataConversion.safe_set (task, "started_on", from_date)
                DataConversion.safe_set (task, "completed_on", end_date)
                DataConversion.safe_set (task, "progress_tracker", "Adjusted")
        r = dbms.update ("Performance_Agreement", work_plan, update_submitted=True)
        if r.status != utils.ok:
            throw ("Some Thing Went Wrong")
        DataConversion.safe_set (object.body, "used", 1)