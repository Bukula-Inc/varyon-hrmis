from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def staff_requisition_before_save(dbms, object):    
    core_hr =Core_Hr(dbms, object)
    # validation =core_hr.validate_staff_requisition(object.body)

def staff_requisition_before_submit(dbms, object):    
    core_hr =Core_Hr(dbms, object)
    # validation =core_hr.validate_staff_requisition(object.body)
    employee_grade =None
    job_title =None
    if object.body.linked_fields and object.body.linked_fields.employee_grade:
        employee_grade =object.body.linked_fields.employee_grade
    else:
        fetch_employee_grade =dbms.get_doc("Employee_Grade", object.body.employee_grade)
        if fetch_employee_grade.status !=utils.ok:
            throw(f"The grade {object.body.employee_grade} was not found.")        
        employee_grade =fetch_employee_grade.data

    fetch_job_title =dbms.get_doc("Designation", object.body.staffing_job_title)
    if fetch_job_title.status ==utils.ok:
        job_title =fetch_job_title.data
    
    

    job_advertisement =utils.from_dict_to_object({
        "designation": object.body.staffing_job_title,
        "company": core_hr.company,
        "department": object.body.staffing_department,
        "vacancies": object.body.variance or 0,
        "number_required": object.body.number_required,
        "publish": 1 if object.body.source_of_recruitment =="Externally" else 0,
        "source_of_recruitment": object.body.source_of_recruitment or "",
        "employment_type": object.body.employment_type or object.body.contract_type or "", 
        "publish_salary": 0,
        "description": DataConversion.safe_get(job_title, "description", "") or "",
        "currency": "ZMW",
        "lower_range": employee_grade.basic_pay,
        "status": "Draft",
        "origin": object.body.doctype or ""
    })
    create_ja =dbms.create("Job_Advertisement", job_advertisement)
    if create_ja.status !=utils.ok:
        throw(f"An error occurred while generating an advertisement: {create_ja}")


def graduate_development_enrollment_before_save(dbms, object):    
    core_hr =Core_Hr(dbms, object)
    validation =core_hr.validate_graduate_development_enrollment(object.body)

def graduate_development_enrollment_before_submit(dbms, object):    
        core_hr =Core_Hr(dbms, object)
        employee_grade =None
        job_title =None
        if object.body.linked_fields and object.body.linked_fields.employee_grade:
            employee_grade =object.body.linked_fields.employee_grade
        else:
            fetch_employee_grade =dbms.get_doc("Employee_Grade", DataConversion.safe_get(DataConversion.safe_get(object, "body", {}), "employee_grade", {}))
            if fetch_employee_grade.status !=utils.ok:
                throw(f"The grade {object.body.employee_grade} was not found.")        
            employee_grade =fetch_employee_grade.data

        fetch_job_title =dbms.get_doc("Designation", DataConversion.safe_get(DataConversion.safe_get(object, "body", {}), "position", ""))
        if fetch_job_title.status ==utils.ok:
            job_title =fetch_job_title.data
        
        job_advertisement =utils.from_dict_to_object({
            "designation": DataConversion.safe_get(DataConversion.safe_get(object,"body", {}),"position", ""),
            "company": core_hr.company,
            "department": DataConversion.safe_get(DataConversion.safe_get(object,"body", {}),"department", ""),
            "vacancies": DataConversion.safe_get(DataConversion.safe_get(object, "body", {}),"number_required", 0) or 0,
            "number_required": DataConversion.safe_get(DataConversion.safe_get(object, "body", {}), "number_required", ""),
            "publish": 1,
            "publish_salary": 0,
            "description": DataConversion.safe_get(job_title, "description", "") or "",
            "currency": "ZMW",
            "lower_range": DataConversion.safe_get(employee_grade,"basic_pay", 0),
            "upper_range": 0,
            "status": "Draft",
            "origin": DataConversion.safe_get(DataConversion.safe_get(object, "body", {}), "doctype", ""),
            "employment_type": DataConversion.safe_get(DataConversion.safe_get(object, "body", {}), "employment_type", "") or DataConversion.safe_get(DataConversion.safe_get(object, "body", {}), "contract_type", "") or "", 
            "supervisor": DataConversion.safe_get(DataConversion.safe_get(object,"body", {}),"supervisor", ""),
            "source_of_recruitment": "Externally",
            "salary_grade": DataConversion.safe_get(DataConversion.safe_get(object, "body", {}), "employee_grade", "")
        })

        
        create_ja =dbms.create("Job_Advertisement", job_advertisement)
        if create_ja.status !=utils.ok:
            throw(f"An error occurred while generating an advertisement: {create_ja}")


def before_short_list_submission(dbms, object):
    # validation
    if object.body.application:
        fetch_application =dbms.get_doc("Job_Application", object.body.application)
        if fetch_application.status !=utils.ok:
            throw(f"the source application was not found, the error returned is {fetch_application}")
        fetch_application.data.status ="Short Listed"
        fetch_application.data.docstatus =1
        update_application =dbms.update("Job_Application", fetch_application.data, update_submitted=True)
        if update_application.status !=utils.ok:
            throw(f"The source application was not successfully updated. The returned error is: {update_application}")
        if fetch_application.data.docstatus ==0:
            submit_application =dbms.submit_doc("Job_Application", update_application.data)

def before_job_offer_save(dbms, object):
    body =DataConversion.safe_get(object, "body", {})
    fetch_interview =dbms.get_doc("Interview", DataConversion.safe_get(body, "interview", None))

    if fetch_interview.status ==utils.ok:
        object.body.job_application =DataConversion.safe_get(DataConversion.safe_get(DataConversion.safe_get(fetch_interview, "linked_fields", {}), "short_listed_applicant", {}), "short_listed_applicant", "")