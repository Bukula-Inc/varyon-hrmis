from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
import pandas as pd
import ast
import re
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def preprocess_list_string(s):
    if isinstance(s, str):
        s = re.sub(r'\[([^\]]+)\]', lambda m: '[' + ','.join(f"'{item.strip()}'" for item in m.group(1).split(',')) + ']', s)
    return s

def import_script_for_employees_grade (dbms, doc, doctype):
    success = []
    failed = []
    core_hr = Core_Hr (dbms=dbms)
    extract_employee_grade = doc.file_content
    ss = dbms.system_settings
    company = ss.default_company
    salary_components = core_hr.get_list ("Salary_Component")
    for employee_grade in extract_employee_grade:
        emp_grade = utils.from_dict_to_object ({})
        if employee_grade.earnings and employee_grade.deductions:
            emp_dict = utils.from_object_to_dict(employee_grade)
            df = pd.DataFrame([emp_dict])
            employee_grade.earnings_ = []
            employee_grade.deductions_ = []
            df['earnings'] = df['earnings'].apply(preprocess_list_string).apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            df['deductions'] = df['deductions'].apply(preprocess_list_string).apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            deductions_and_earnings = df[['earnings', 'deductions']].to_dict (orient="records")[0]
        if employee_grade:
            if not employee_grade.company:
                emp_grade.company = company
            if not employee_grade.payment_frequency:
                emp_grade.payment_frequency = "Monthly"
            for component in salary_components:
                if component.is_standard_component and component.component_type == "Earning":
                    employee_grade.earnings_.append({"component": component.name})
                elif component.is_standard_component and component.component_type == "Deduction":
                    employee_grade.deductions_.append({"component": component.name})
            
            for deduction in deductions_and_earnings['deductions']:
                pp ("============Deduction", deduction)
                get_deduc = core_hr.get_doc ("Salary_Component", deduction)
                pp ("=================== LIs Ded=======", get_deduc)
                if get_deduc.status != utils.ok:
                    employee_grade.deductions_.append({"component": deduction})
            for earning in deductions_and_earnings['earnings']:
                get_earn = core_hr.get_doc ("Salary_Component", earning)
                if get_earn.status != utils.ok:
                    employee_grade.earnings_.append({"component": earning})
            emp_grade.earnings = employee_grade.earnings_
            emp_grade.deductions = employee_grade.deductions_
            emp_grade.name = employee_grade.grade
            emp_grade.basic_pay = employee_grade.basic_pay if employee_grade.basic_pay else 0
            pp ("============= Emp Grade==================", emp_grade)
            emp_grade_created = dbms.create ("Employee_Grade", emp_grade, dbms.validation.user)
            pp ("==============Grade===========", emp_grade_created)
            if emp_grade_created.status == utils.ok:
                if not employee_grade.basic_pay:
                    emp_grade["error"] = " Success But Go Add Basic Pay To Grade "
                else:
                    emp_grade["error"] = " - "
                emp_grade['status'] = "Importation Successful"
                success.append (emp_grade)
            else:
                emp_grade["error"] = emp_grade_created.error_message
                emp_grade["status"] = "Importation Failed"
                failed.append (emp_grade)
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
    pp (update)
    return utils.respond(utils.ok, {"successful": success, "failed": failed})