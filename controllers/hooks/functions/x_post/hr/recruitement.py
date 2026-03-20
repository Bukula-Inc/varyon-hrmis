from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def filled_sits_in_designation(dbms, object):
    data =object.body.data
    qty =0
    fetch_designation =dbms.get_list("Employee", filters={"designation": data.designation}, fields=["name","designation"])
    pp(fetch_designation)
    if fetch_designation.status ==utils.ok:
        qty =len(fetch_designation.data.rows)
    elif fetch_designation.status ==utils.no_content:
        pass
    else:
        throw(f"An error occurred: {fetch_designation}")
    
    return utils.respond(utils.ok, qty)


def update_job_advertisement(dbms, object):
    data =object.body.data
    return_obj =[]
    update_status =utils.unprocessable_entity
    fetch_job_advertisement =dbms.get_doc("Job_Advertisement", data.job_advertisement)
    if fetch_job_advertisement.status !=utils.ok:
        throw(f"The advertisement was not fetch successfully due to the following error: {fetch_job_advertisement}")
    job_advertisement =fetch_job_advertisement.data
    job_advertisement.description =data.description

    update_job_advertisement =dbms.update("Job_Advertisement", job_advertisement,  update_submitted=True, privilege=True)
    if update_job_advertisement.status ==utils.ok:
        return_obj =update_job_advertisement.data
        update_status =update_job_advertisement.status


    return utils.respond(update_status, return_obj)


def fetch_applicant_data_as_employee_obj(dbms, object):

    data =DataConversion.safe_get(DataConversion.safe_get(object, "body", {},), "data", None)
    if data:
        resource_doc =DataConversion.safe_get(data, "resource_doc", None)
        # is_on_probation =DataConversion.safe_get()
        # bank_name =DataConversion.safe_get(data, "bank_name", None)
        # account_no =DataConversion.safe_get(data, "account_no", None)
        # sort_code =DataConversion.safe_get(data, "sort_code", None)
        # branch =DataConversion.safe_get(data, "branch", None)
        # section =DataConversion.safe_get(data, "section", None)
        # probation =DataConversion.safe_get(data, "probation", "")

        if not resource_doc:
            return utils.respond(utils.unprocessable_entity, utils.from_dict_to_object({"error_message": f"The document name of the document having the reference data for the new employee was not provided in the 'X Post'."}))

        fetch_doc =dbms.get_doc("Job_Application", resource_doc)
        pp(fetch_doc)
        if fetch_doc.status !=utils.ok:
            return utils.respond(utils.unprocessable_entity, utils.from_dict_to_object({"error_message": f"The document '{resource_doc}' was not found."}))

        application =DataConversion.safe_get(fetch_doc, "data", {})
        fetch_job_advert =dbms.get_doc("Job_Advertisement", DataConversion.safe_get(application, "job_advertisement", ""))
        if fetch_job_advert.status !=utils.ok:
            (utils.unprocessable_entity, utils.from_dict_to_object({"error_message": f"The job advertisement document {DataConversion.safe_get(application, "job_advertisement", "")} was not found."}))

        job_advertisement =DataConversion.safe_get(fetch_job_advert, "data", None)

        fetch_grade =dbms.get_doc("Employee_Grade", DataConversion.safe_get(job_advertisement, "salary_grade", ""))
        grade =DataConversion.safe_get(fetch_grade, "data", {})

        fetch_hr_settings =dbms.get_doc("Employee_Grade", DataConversion.safe_get(job_advertisement, "salary_grade", ""))
        hr_settings =DataConversion.safe_get(fetch_hr_settings, "data", {})



        emp_data =utils.from_dict_to_object({                    
                "first_name": DataConversion.safe_get(application, "applicant_first_name", ""), 
                "middle_name": DataConversion.safe_get(application, "applicant_middle_name", ""), 
                "last_name": DataConversion.safe_get(application, "applicant_last_name", ""), 
                "full_name": DataConversion.safe_get(application, "applicant_name", ""), 
                "gender": DataConversion.safe_get(application, "gender", ""), 
                "d_o_b": DataConversion.safe_get(application, "date_of_birth", ""),
                "salutation": "Mr" if DataConversion.safe_get(application, "gender", "") =="Male" else "Ms", 
                "id_no": DataConversion.safe_get(application, "id_nrc", ""), 
                "date_of_joining": dates.today(), 
                "email": DataConversion.safe_get(application, "email", ""), 
				"company": DataConversion.safe_get(application, "company_id", "") or dbms.current_user.default_company or None,
				"designation": DataConversion.safe_get(application, "designation", ""),
				"department": DataConversion.safe_get(job_advertisement, "department", ""),
				"employee_grade": DataConversion.safe_get(job_advertisement, "salary_grade", ""),
				"employment_type": DataConversion.safe_get(job_advertisement, "employment_type", ""),
                "report_to": DataConversion.safe_get(job_advertisement, "supervisor", ""),
                "basic_pay": DataConversion.safe_get(grade, "basic_pay", ""),
                "deductions": [{"deduction": DataConversion.safe_get(component, "component", "")} for component in DataConversion.safe_get(grade, "deductions", []) if component],
                "earnings": [{"earning": DataConversion.safe_get(component, "component", "")} for component in DataConversion.safe_get(grade, "earnings", []) if component],
                "working_days":DataConversion.safe_get(hr_settings, "working_days", ""),
                "working_hours": DataConversion.safe_get(hr_settings, "working_hrs", ""),

        })    

        return utils.respond(utils.ok, emp_data)

def create_employee_from_job_offer(dbms, object):
    employee =DataConversion.safe_get(DataConversion.safe_get(object, "body", {}),  "data", None)
    return_object =utils.from_dict_to_object({"status": utils.unprocessable_entity, "data": None})
    if not employee:
       return_object.data =f"No data was provided to create the employee."
    
    create_employee =dbms.create("Employee", employee)  
    return_object.status =create_employee.status
    if create_employee.status !=utils.ok:
        return_object.data =create_employee.error_message
    else:
        return_object.data =create_employee.data

    return utils.respond(return_object.status, return_object.data)

def job_offer_status_update(dbms, object):
    body =DataConversion.safe_get(DataConversion.safe_get(object, "body" , {}), "data", None)
    return_obj =utils.from_dict_to_object({
        "status": utils.unprocessable_entity,
        "data": {},
        "error_message": ""
    })
    if body:
        response =DataConversion.safe_get(body, "response", None)
        if not response:
            throw(f"No response was provided for the job offer {job_offer_name} was not provided")        
        job_offer_name =DataConversion.safe_get(body, "job_offer", "")
        if not job_offer_name:
            throw(f"No job offer document {job_offer_name} was not provided")     
        fetch_job_offer =dbms.get_doc("Job_Offer", job_offer_name)
        if fetch_job_offer.status !=utils.ok:
            throw(f"No job offer document of the name {job_offer_name}")
        job_offer =DataConversion.safe_get(fetch_job_offer, "data", {})
        if not job_offer:
            throw(f"The document {job_offer_name} was not found")
        if response:
            if response =="Confirmed":
                DataConversion.safe_set(job_offer, "status", response)  
                update_job_offer =dbms.update("Job_Offer", job_offer, update_submitted=True)
                return_obj.status =DataConversion.safe_get(update_job_offer, "status", "")
                if update_job_offer.status ==utils:
                    return_obj.data =DataConversion.safe_get(update_job_offer, "data", "")
                else:
                    return_obj.error_message =DataConversion.safe_get(update_job_offer, "error_message", "")




    return utils.respond(return_obj.status, return_obj.data or return_obj.error_message)

