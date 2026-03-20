from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import date
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def separation_validation(body):

    if not body.employee:
        throw(f"The field 'Employee' is having an invalid value.")
    if not body.separation_type:
        throw(f"The field 'Separation Type' is having an invalid value.")
    if not body.department:
        throw(f"The field 'Department' is having an invalid value.")
    if not body.designation:
        throw(f"The field 'Designation' is having an invalid value.")
    if not body.resignation_date:
        throw(f"The field 'Notification Date' is having an invalid value.")
    if not body.notice_period:
        throw(f"The field 'Notice Period' is having an invalid value.")
    if not body.reason:
        throw(f"The field 'Reason' is having an invalid value.")
    if not body.last_day_of_work:
        throw(f"The field 'Last Day of Work' is having an invalid value.")
    return body

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

def separation_type_validation(body):
    if not body.name:
        throw("The field 'name' is having invalid data")
    if not body.description:
        throw("The field 'description' is having invalid data")
    return body

def fetch_doc(model, doc, dbms, object, required=0):
    if not doc:
        throw(f""" No name was provided for the model {model}, to fetch""")
    fetch_doc =dbms.get_doc(model, doc)
    if fetch_doc.status !=utils.ok:
        if required==1:
            throw(f"No {model.replace("_"," ")} by the Name '{doc}' was found!")
        else:
            return None
    return fetch_doc.data

def certificate_validation(body):
    if not body.employee_seperation:
        throw(f"The field 'employee separation' is missing or having invalid data")   
    if not body.employee_id:
        throw(f"The field 'employee' is missing or having invalid data")      
    if not body.nrc:
        throw(f"The field 'nrc' is missing or having invalid data")
    if not body.napsa_membership_number:
        throw(f"The field 'napsa membership number' is missing or having invalid data")
    if not body.employer_napsa_account_no:
        throw(f"The field 'employer_napsa_account_no' is missing or having invalid data")

    if not body.from_date:
        throw(f"The field 'from_date' is missing or having invalid data")
    if not body.to_date:
        throw(f"The field 'to_date' is missing or having invalid data")

    return body

def validate_csfte(body):
    if not body:
        throw(f""" No content was received for saving. Please filling in the fields. """)    
    if not body.name:
       throw(f""" The field 'name' was not provided. Please fill the field.""") 
    if not body.employee_name:
       throw(f""" The field 'employee name' was not provided. Please fill the field.""") 
    if not body.employee_id:
       throw(f""" The field 'employee' was not provided. Please fill the field.""") 
    if not body.nrc:
       throw(f""" The field 'NRC' was not provided. Please fill the field.""") 
    if not body.napsa_membership_number:
       throw(f""" The field 'NAPSA membership number' was not provided. Please fill the field.""") 
    if not body.employer_napsa_account_number:
       throw(f""" The field 'employee NAPSA account number' was not provided. Please fill the field.""") 
    if not body.designation:
       throw(f""" The field 'designation' was not provided. Please fill the field.""") 
    if not body.from_date:
       throw(f""" The field 'from date' was not provided. Please fill the field.""") 
    if not body.to_date:
       throw(f""" The field 'to date' was not provided. Please fill the field.""") 
    if not body.name_of_employer:
       throw(f""" The field 'name of employer' was not provided. Please fill the field.""") 
    if not body.address_of_employer:
       throw(f""" The field 'address of employer' was not provided. Please fill the field.""") 
    if not body.company:
       throw(f""" The field 'company' was not provided. Please fill the field.""") 
    if not body.employer_napsa_account_number:
       throw(f""" The field 'employer NAPSA account number' was not provided. Please fill the field.""") 
    if not body.employee_seperation:
       throw(f""" The field 'employee separation' was not provided. Please fill the field.""")

    return body


def before_separation_save(dbms, object):
    separation_validation(object.body)


def before_separation_submit(dbms, object):
    body =separation_validation(object.body)
    interview_question =None
    emp_data =body.linked_fields.employee if body.linked_field and body.linked_fields.employee else dbms.get_doc("Employee", body.employee).data or throw(f"Employee data was not found.")
    # DATES
    last_day_of_work =body.last_day_of_work if isinstance(body.last_day_of_work, str) else body.last_day_of_work.strftime("%Y-%m-%d")
    resignation_date =body.resignation_date if isinstance(body.resignation_date, str) else body.resignation_date.strftime("%Y-%m-%d")

    fetch_separation_type =dbms.get_doc("Separation_Type", body.separation_type)
    if fetch_separation_type.status !=utils.ok:
        throw(f"No Separation type by the Name '{body.separation_type}' was found!")
    separation_type =fetch_doc("Separation_Type", body.separation_type, dbms, object, required=0)
    if separation_type and separation_type.interview_question:
        interview_question =fetch_doc("Exit_Interview_Question", separation_type.interview_question, dbms, object,required=0)

    interview_questionnaire =utils.from_dict_to_object({
        "due_date": dates.add_days(last_day_of_work, 2),
        "email": "dragonheart@mail.com",
        "last_day": last_day_of_work,
        "designation": body.designation or emp_data.designation,
        "department": body.department or emp_data.department,
        "employee": body.employee,
        "open_ended_questions": interview_question.open_ended_questions if interview_question and interview_question.open_ended_questions else [],
        "closed_ended_questions": interview_question.closed_ended_questions if interview_question and interview_question.closed_ended_questions else [],
    })

    create_interview_questionnaire =dbms.create("Exit_Interview_Questionnair", interview_questionnaire)

    if create_interview_questionnaire.status !=utils.ok:
        pp(create_interview_questionnaire)


    clearance_form =utils.from_dict_to_object({
        "employee_name": emp_data.full_name,
        "engagement_date": emp_data.date_of_joining,
        "date_of_separation": body.resignation_date,
        "status": "Draft",
        "employee": emp_data.name,
        "job_title": emp_data.designation,
        "salary_grade": emp_data.salary_grade,
        "employee_separation": body.name,
        "clearance_data": []
    })

    create_clearance_form =dbms.create("Clearance_Form", clearance_form)
    if create_clearance_form.status !=utils.ok:
        throw(f"Failed to create a clearance form du to: {create_clearance_form}")


def before_certificate_of_service_save(dbms, object):
    # confirm_interview_and_clearnace
    body =certificate_validation(object.body)

    clearance_form = dbms.get_list("Clearance_Form", filters={"employee" :body.employee_id})
    if clearance_form.status ==utils.no_content:
        throw(f"No cleared clearance form was found for {body.employee_name} of id {body.employee_id}. Please have the clearance cleared before proceeding to the certificate.")
    elif clearance_form.status !=utils.ok:
        throw(f"No clearance form was found, the following error was mate. {clearance_form}")


def before_certificate_of_service_submit(dbms, object):    
    core_payroll =Core_Payroll(dbms, object)
    body =certificate_validation(object.body)
    employee_seperation =DataConversion.safe_get(body, "employee_seperation", None)
    fetch_separation_doc =None
    fetched_separation =None
    if not DataConversion.safe_get(body, "employee_seperation", None):
        fetch_separation_doc =dbms.get_list("Employee_Seperation", filters={"employee": body.employee_id})
    else:
        fetch_separation_doc =dbms.get_doc("Employee_Seperation", employee_seperation)
    if fetch_separation_doc.status !=utils.ok:
        throw(f"No separation doc was found related to {body.employee_name} of id {body.employee_id}")
    else:
        fetched_separation =DataConversion.safe_get(fetch_separation_doc, "data", None) if not DataConversion.safe_get(DataConversion.safe_get(fetch_separation_doc, "data", None), "rows", None) else DataConversion.safe_get(DataConversion.safe_get(fetch_separation_doc, "data", None), "rows", None)[0]
    
    emp_data =fetch_doc("Employee", body.employee_id, dbms, object, 1)
    separation_type =fetch_doc("Separation_Type", DataConversion.safe_get(fetched_separation, "separation_type", None), dbms, object, 1)
    if separation_type.separation_package:
        fetch_allowance_and_benefits =dbms.get_list("Allowance_and_Benefit", fetch_linked_tables=True)
        if fetch_allowance_and_benefits.status !=utils.ok:
            throw(f"Allowance and benefits were no found in the system.")
        grouped_by_name =utils.group(fetch_allowance_and_benefits.data.rows, "name")
        for package in separation_type.separation_package:
            grouped_benefit_categories =utils.group(grouped_by_name[package.package_item][0].categories, "salary_grade")
            add_to_payroll =core_payroll.notify_payroll(
                employee_number=body.employee_id,
                amount= grouped_benefit_categories[emp_data.employee_grade][0].amount,
                length_or_period=1,
                doc_type=body.doctype,
                doc_name=body.name,
                sc="Separation Package"
            )
    # throw(""" Check 1....""")
    # emp_data.status ="Separated"
    # update_employee =dbms.update("Employee", emp_data)
    # if update_employee.status !=utils.ok: 
    #     throw(f"An error occurred while trying to update the separating employee, {emp_data.name}")


def before_certificate_of_service_for_temporal_employee(dbms, object):
    object.body =validate_csfte(DataConversion.safe_get(object, "body"))




def before_certificate_of_service_submit(dbms, object):    
    core_payroll =Core_Payroll(dbms, object)
    body =certificate_validation(object.body)
    employee_seperation =DataConversion.safe_get(body, "employee_seperation", None)
    fetch_separation_doc =None
    fetched_separation =None
    if not DataConversion.safe_get(body, "employee_seperation", None):
        fetch_separation_doc =dbms.get_list("Employee_Seperation", filters={"employee": body.employee_id})
    else:
        fetch_separation_doc =dbms.get_doc("Employee_Seperation", employee_seperation)
    if fetch_separation_doc.status !=utils.ok:
        throw(f"No separation doc was found related to {body.employee_name} of id {body.employee_id}")
    else:
        fetched_separation =DataConversion.safe_get(fetch_separation_doc, "data", None) if not DataConversion.safe_get(DataConversion.safe_get(fetch_separation_doc, "data", None), "rows", None) else DataConversion.safe_get(DataConversion.safe_get(fetch_separation_doc, "data", None), "rows", None)[0]
    
    emp_data =fetch_doc("Employee", body.employee_id, dbms, object, 1)
    separation_type =fetch_doc("Separation_Type", DataConversion.safe_get(fetched_separation, "separation_type", None), dbms, object, 1)
    if separation_type.separation_package:
        fetch_allowance_and_benefits =dbms.get_list("Allowance_and_Benefit", fetch_linked_tables=True)
        if fetch_allowance_and_benefits.status !=utils.ok:
            throw(f"Allowance and benefits were no found in the system.")
        grouped_by_name =utils.group(fetch_allowance_and_benefits.data.rows, "name")
        for package in separation_type.separation_package:
            grouped_benefit_categories =utils.group(grouped_by_name[package.package_item][0].categories, "salary_grade")
            add_to_payroll =core_payroll.notify_payroll(
                employee_number=body.employee_id,
                amount= grouped_benefit_categories[emp_data.employee_grade][0].amount,
                length_or_period=1,
                doc_type=body.doctype,
                doc_name=body.name,
                sc="Separation Package"
            )

def before_exit_interview_questionnaire_save (dbms, object):
    object.body =exit_interview_questionnaire_validate(object.body)

def before_separation_type_save(dbms, object):
    object.body =separation_type_validation(object.body)

