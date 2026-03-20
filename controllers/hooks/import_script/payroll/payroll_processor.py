from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.payroll import Core_Payroll
import ast
import re


utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

def payroll_import_script (dbms, doc, doctype):
    core = Core_Payroll(dbms,object)
    success = []
    failed = []
    total_basic = 0.00
    total_gross = 0.00
    total_net = 0.00
    total_earnings = 0.00
    total_deductions = 0.00
    total_paye = 0.00
    data = doc.file_content
    sc_c = utils.from_dict_to_object ({})
    sc = dbms.sql ("SELECT * FROM salary_component")
    if sc.data:
        sc_c = utils.array_to_dict (sc.data, "name")
    employees = []
    totals_row = {}
    if len(data) > 0:
        cols = utils.get_object_keys(data[0])
        ids = utils.get_list_of_dicts_column_field(data, "employee_number")
        emps = dbms.get_list("Employee", filters={"name__in":ids}, privilege=True)
        if emps.status == utils.ok:
            try:
                emps = utils.array_to_dict(emps.data.rows, "name")
                for emp in data:
                    employee = utils.from_dict_to_object ()
                    employee.employee = emp.basic or emp.basic_pay or 0.00
                    employee.basic_pay = emp.basic or emp.basic_pay or 0.00
                    employee.PAYE = emp.paye or 0.00
                    employee.net = emp.net or 0.00
                    employee.gross = emp.gross or 0.00
                    employee_number = emp.employee_number or emp.employee
                    emp_dict = emps.get (employee_number, None)
                    if emp_dict:
                        if employee.basic_pay > 0:
                            total_deductions += employee.PAYE
                            total_paye += employee.PAYE
                            total_gross += employee.gross
                            total_basic += float (employee.basic_pay)
                            total_net += employee.net
                            total_earnings += float (employee.basic_pay)
                            employee.employee = emp_dict.name
                            employee.designation = emp_dict.designation
                            employee.full_names = emp_dict.full_name or f"{emp_dict.first_name} {emp_dict.middle_name or ''} {emp_dict.last_name}"
                            for earning in emp_dict.earnings:
                                if earning.earning in sc_c:
                                    key = str(earning.earning).lower ().replace (" ", "_")
                                    if key in emp:
                                        if earning.earning in totals_row:
                                            totals_row[earning.earning] += emp[key] or 0.00
                                        else:
                                            totals_row[earning.earning] = emp[key] or 0.00
                                        employee[earning.earning] = emp[key] or 0.00
                                        total_earnings += employee[earning.earning]
                            for deduction in emp_dict.deductions:
                                if deduction.deduction in sc_c:
                                    key = str(deduction.deduction).lower ().replace (" ", "_")
                                    if key in emp:
                                        if key in totals_row:
                                            totals_row[deduction.deduction] += emp[key] or 0.00
                                        else:
                                            totals_row[deduction.deduction] = emp[key] or 0.00
                                        employee[deduction.deduction] = emp[key]
                                        total_deductions += employee[deduction.deduction]

                            employees.append (employee)
                            emp["error"] = " - "
                            emp['status'] = "Importation Successful"
                            success.append (emp)
                        else:
                            emp["error"] = "Employee Basic Pay Is Zero"
                            emp["status"] = "Importation Failed"
                            failed.append (emp)
                    else:
                        emp["error"] = "Employee Not Found"
                        emp["status"] = "Importation Failed"
                        failed.append (emp)
            except Exception as e:
                return utils.respond(utils.unprocessable_entity, {"successful": success, "failed": failed, "error_message": f"Failed To Import Due To: {e}"})
        else:
            emps["error"] = "All Employees Numbers Did Match Any Employees In The System Found"
            emps["status"] = "Importation Failed"
            failed.append (emp)
    if len (employees) > 0:

        totals_row["employee"] = "TOTALS"
        totals_row["full_names"] = "Totals"
        totals_row["PAYE"] = total_paye
        totals_row['net'] = total_net
        totals_row['basic_pay'] = total_basic
        totals_row['gross'] = total_gross
        employees.append (totals_row)
        pp (employees)
        p = dbms.create("Payroll_Processor",{
            "from_date":dates.get_first_date_of_current_month(),
            "to_date":dates.get_last_date_of_current_month(),
            "frequency":"Monthly",
            "company":dbms.system_settings.default_company,
            "currency":dbms.system_settings.default_currency,
            "convertion_rate":1,
            "total_employees":len(employees),
            "total_basic":total_basic,
            "total_gross":total_gross,
            "total_net":total_net,
            "total_earnings":total_earnings,
            "total_deductions":total_deductions,
            "employee_info":employees
        })
    else:
        throw("One or more emloyee validation has failed")
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
