from controllers.utils import Utils


utils = Utils ()
pp = utils.pretty_print

def on_submit_employee_discipline (dbms, object):
    discipline = object.body
    obj = {}
    obj['employee_disciplinary'] = discipline.name
    obj['subject'] = discipline.subject
    obj['subject_name'] = discipline.subject_name
    obj['subject_department'] = discipline.subject_department
    obj['subject_reports_to'] = discipline.subject_reports_to
    obj['violation_type'] = discipline.violation_type
    obj['violation_date'] = discipline.violation_date
    obj['violation_location'] = discipline.violation_location
    obj['status'] = "Draft"
    rr = dbms.create ("Case_Outcome", utils.from_dict_to_object (obj),)
    # object.doc_status = "Resolved"
    # object.doc_status = "Finalize In Case Outcome | Resolved"

