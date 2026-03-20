import datetime
from controllers.utils import Utils
from controllers.utils.dates import Dates

import pandas as pd

utils = Utils()
pp = utils.pretty_print
throw = utils.throw
dates =Dates()
              
            
def welfare_importation(dbms, doc, doctype):

    success = []
    failed = []
    ss =dbms.system_settings
    extracted_data =doc.file_content
    imp_emp_list =[x.employee_id for x in extracted_data]

    default_comany =ss.default_company
    default_welfare_type =None  


    grouped_emp_data =utils.from_dict_to_object({})
    fetch_welfare_type =dbms.get_doc("Welfare_Type", "Health")
    if fetch_welfare_type.status != utils.ok:
        throw("No welfare type was found that by the name Health")
    else:   
        default_welfare_type =fetch_welfare_type.data
    fetch_emp =dbms.get_list("Employee", filters={"name__in": imp_emp_list}, fetch_linked_fields =True)
    if fetch_emp.status !=utils.ok:
        throw(f"Error occurred when fetching Employees {fetch_emp}")
    else:
        grouped_emp_data =utils.array_to_dict(fetch_emp.data.rows, "name")

    for entry in extracted_data:  
        repayment_period =0
        repayment_unit =""
        if entry.pay_length_unit !="Year" or entry.pay_length_unit !="year":
            repayment_unit =entry.pay_length_unit
            repayment_period = default_welfare_type.limit_qty
        else:
            repayment_unit ="Months"
            repayment_period = default_welfare_type.limit_qty
                        
        welfare =utils.from_object_to_dict({
            "company_id": grouped_emp_data[entry.employee_id].linked_fields.company.id,
            "name": None,
            "employee_name": grouped_emp_data[entry.employee_id].full_name or "",
            "designation": grouped_emp_data[entry.employee_id].designation or "",
            "pay_length_unit": default_welfare_type.limit_unit or "Months",
            "payment_length": repayment_period or 8,
            "company_covered_expense": ((default_welfare_type.company_percentage /100) * entry.welfare_expense) or 0.00,
            "staff_covered_expense": ((default_welfare_type.employee_percentage /100) * entry.welfare_expense ) or 0.00,
            "welfare_expense": entry.welfare_expense,
            "attach_receipt": entry.attach_receipt or None,
            "payment_method": entry.payment_method or "Payroll",
            "employee": grouped_emp_data[entry.employee_id].name,
            "department": grouped_emp_data[entry.employee_id].department,
        })
           
                
        create = dbms.create("Recovery_Of_Medical_Bills", welfare, privilege=True)
        if create.status != utils.ok:
            failed.append(entry)
        else:
            success.append(entry)
                
            
    
    doc.file_content = [*success, *failed]
    if failed and len(failed) > 0 and success and len(success) > 0:
        doc.status = "Partially Imported"
        doc.doc_status = "Partially Imported"
    elif len(failed) > 0 and len(success) == 0:
        doc.status = "Importation Failed"
        doc.doc_status = "Importation Failed"
    elif len(failed) == 0 and len(success) > 0:
        doc.status = "Importation Successful"
        doc.doc_status = "Importation Successful"
    update = dbms.update("Data_Importation", doc, dbms.current_user_id, update_submitted=True)
    return utils.respond(utils.ok, {"successful": success, "failed": failed})                
