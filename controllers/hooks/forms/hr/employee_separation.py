from controllers.core_functions.payroll import Core_Payroll
from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates ()
throw = utils.throw
pp = utils.pretty_print

def fetch_doc(dbms, model, doc):
    if model and doc:
        fetch_doc =dbms.get_doc(model, doc)
        if fetch_doc.status ==utils.ok:
            return fetch_doc.data
        else:
            return None

def separation_submit (dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    mailing = Mailing(dbms=dbms)
    separation = object.body
    employee_info = core_hr.get_doc ("Employee", name=separation.employee)
    sub = None
    sup_msg = None
    emp_msg = None
    if employee_info:
        sub = separation.separation_type
        sup_msg = f""" {separation.separation_type} of {employee_info.full_name}  has been initialized Successfully"""
        emp_msg = f""" Your {separation.separation_type} process  has been initialized"""
        # mailing.send_mail (recipient=employee_info.email, subject=sub, body=emp_msg)
        supervisor = core_hr.get_doc ("Employee", name=employee_info.report_to)
        if supervisor:
            mailing.send_mail (recipient=supervisor.email, subject=sub, body=sup_msg)
        object.doc_status = "Pending Review"

def cancel_separation (dbms, object):
    canceled = object.body.linked_fields
    employee = DataConversion.safe_get (canceled, "employee")

    DataConversion.safe_set (employee, "status", "Active")
    DataConversion.safe_set (employee, "last_day_of_work", None)
    DataConversion.safe_set (employee, "docstatus", 0)
    DataConversion.safe_set (employee, "is_separated_emp_paid", "Unsettled")
    DataConversion.safe_set (employee, "is_separated", 0)
    dbms.update ("Employee", employee, update_submitted=True)


def accept_separation (dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object,)
    mailing = Mailing(dbms=dbms)
    separation = object.body
    user =dbms.current_user
    email_body =None

    employee_info = core_hr.get_doc ("Employee", name=separation.employee)
    if employee_info:
        if separation.separation_type == "Termination":
            status = "Terminated"
            msg = f"""
                We are writing to inform you that your employment with {employee_info.company} has been {status}, effective {separation.last_day_of_work}. 
                This decision has been made after careful consideration and in accordance with our company's policies and procedures.
                If you have any questions or concerns, please do not hesitate to reach out to our HR department.

                
            """

            email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Sincerely")
        elif separation.separation_type == "Retirement":
            status = "Retired"
            msg = f"""
                We are pleased to inform you that your retirement from {employee_info.company} has been officially processed, effective {separation.last_day_of_work}. 
                We wish you a happy and fulfilling retirement!
                Your dedication and contributions to our organization are greatly appreciated, and you will be missed. We hope you enjoy this new chapter in your life 
                and pursue all the things that bring you joy.
                If you have any questions or concerns, please don't hesitate to reach out to our HR department.
                <br/>
            """

            email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Best regards")
        elif separation.separation_type == "Resignation":
            status = "Resigned"
            msg = f"""
                This letter serves as formal confirmation that your resignation from {employee_info.company} has been accepted, effective {separation.resignation_date}. 
                Your decision to leave the company has been processed, and your employment with us will officially end on {separation.last_day_of_work}.
                We appreciate the contributions you made during your time with us and wish you the best in your future endeavors. 
                <br/>
                If you have any questions or concerns, please don't hesitate to reach out to our HR department.
                <br/>
            """

            email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Best regards")
        elif separation.separation_type == "Redundancy":
            status = "Redundant"
            msg = f"""
                We regret to inform you that your position at {employee_info.company} has been made redundant, effective {separation.last_day_of_work}.  
                This decision has been made after careful consideration and in accordance with our company's policies and procedures.

                We appreciate your contributions to the company and are grateful for your service.
                If you have any questions or concerns, please don't hesitate to reach out to our HR department.
                <br/>
            """

            email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Best regards")
        elif separation.separation_type == "End Of Contract":
            status = "Left"
            msg = f"""
                We are writing to inform you that your contract with {employee_info.company} has come to an end, 
                effective {separation.last_day_of_work}. We appreciate the work you have done during your time 
                with us and are grateful for your contributions. 
                <br/>
                <br/>
                <br/>
                If you have any questions or concerns, please don't hesitate to reach out to us. We wish you the best in your future endeavors.
                
            """
        else :
            status = "Separated"
            msg = f"""
                We am writing to inform you that your employment with {employee_info.company}  has been {separation.separation_type}, effective {separation.resignation_date} to {separation.last_day_of_work}. 
                This decision has been made after careful consideration and in accordance with our company's policies and procedures.
                If you have any questions or concerns, please do not hesitate to reach out to me or our HR department.
                <br/>
            """

            email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Best regards")
        employee_info.status = status
        employee_info.doc_status = status
        employee_info.is_separated = 1
        employee_info.last_day_of_work = separation.last_day_of_work

        dbms.update ("Employee", employee_info, update_submitted=True)
        if separation.skip_exit_interview:
            dbms.create ("Exit_Interview", utils.from_object_to_dict ({
                "employee": employee_info.name,
                "employee_name": employee_info.full_name,
                "department": employee_info.department,
                "designation": employee_info.designation,
                "date_of_joining": employee_info.date_of_joining,
                "status": "Pending"
            }))

    if employee_info:
        confirmation_mail =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=f"<h1> Separation of {employee_info.full_name} Has Been</h1><p> ")
        mailing.send_mail (recipient=user.email, subject="Separation Submission", body=confirmation_mail)
        if email_body !=None:
            mailing.send_mail (recipient=employee_info.email, subject="Separation Submission", body=email_body)

    object.doc_status = status



def before_clearance_submit(dbms, object):
    body =object.body
    core_payroll =Core_Payroll(dbms, object)

    # if not DataConversion.safe_get(body, "clearance_data", []):
    #     throw(f""" Please fill the list of items needed to be cleared. """)

    employee_data =dbms.get_doc("Employee", body.employee).data or throw(f"Failed to fetch the separating employee.")
    linked_fields =DataConversion.safe_get(body, "linked_field", "")
    employee_separation =DataConversion.safe_get(linked_fields, "employee_separation", {}) or fetch_doc(dbms, "Employee_Seperation", DataConversion.safe_get(body, "employee_separation", ""))

    employee_data.status ="Separated"
    employee_data.is_separated =1
    employee_data.last_day_of_work =DataConversion.safe_get(employee_separation, "last_day_of_work", dates.today())
    try:
        dbms.update("Employee", employee_data)
    except Exception as e:
        pp(e)
        throw(e)
    
    fetch_separation_type =dbms.get_doc("Separation_Type", DataConversion.safe_get(employee_separation, "separation_type", ""))
    if fetch_separation_type.status !=utils.ok:
        throw(f""" Failed to fetch separation type '<strong class="font-semibold text-red">{DataConversion.safe_get(employee_separation, "separation_type", "")}</strong>', {fetch_separation_type} """)
    separation_type =fetch_separation_type.data
    if DataConversion.safe_get(separation_type, "separation_package", []):
        fetch_allowance_and_benefits =dbms.get_list("Allowance_and_Benefit", fetch_linked_tables=True)
        if fetch_allowance_and_benefits.status !=utils.ok:
            throw(f""" Failed to fetch allowances and benefits """)
        all_nd_ben =DataConversion.safe_get(DataConversion.safe_get(fetch_allowance_and_benefits, "data"), "rows")
        group_aad =utils.group(all_nd_ben, "name")
        for benefit in DataConversion.safe_get(separation_type, "separation_package", []):
            amount =0
            package =group_aad[DataConversion.safe_get(benefit, "package_item", "")][0]
            if DataConversion.safe_get(package, "affects_payroll", 0):
                grouped_by_grade =utils.group(DataConversion.safe_get(package, "categories", []), "salary_grade")
                salary_grade_data =grouped_by_grade[DataConversion.safe_get(employee_data, "employee_grade", "")][0]
                if DataConversion.safe_get(package, "extra_fields", "None") in ["None", "Transportation Description"]:
                    amount +=DataConversion.safe_get(salary_grade_data, "amount")
                # elif DataConversion.safe_get(package, "extra_fields", "None") =="":

                add_to_payroll =core_payroll.notify_payroll(
                    employee_number=DataConversion.safe_get(employee_data, "name"),
                    amount= amount,
                    length_or_period=1,
                    doc_type=DataConversion.safe_get(body, "doctype", ""),
                    doc_name=body.name,
                    sc=DataConversion.safe_get(benefit, "package_item", ""),
                    entry_type ="Earning"
                )

