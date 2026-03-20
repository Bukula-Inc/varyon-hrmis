from controllers.core_functions.staff import Core_Staff

def applicant_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "applicant")

def raised_by_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "raised_by")

def issue_raiser_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "issue_raiser")

def employee_id_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "employee_id")

def employee_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "employee")

def planner_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "planner")

def initiator_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "initiator")

def employee_no_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "employee_no")

def user_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "user")

def subject_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "subject")

def appraisee_ref (dbms, obj):
    Core_Staff.validate_user (dbms, obj, "appraisee")