from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import datetime, date
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()

pp = utils.pretty_print

def medical_deductions_report (dbms, object):
    core_hr = Core_Hr  (dbms, object)
    sys_emp = core_hr.get_list ("Employee", filters={"status__in": ["On Leave", "Active", "Suspended"]})
    emp_flt_key = ''
    emp_flt_val = ''
    employees = {}
    emp_details = utils.array_to_dict (sys_emp, "name") 
    employees_df = utils.to_data_frame (sys_emp)

    return_data =[]
    total_welfare_expense = 0
    total_company_covered_expense = 0
    total_staff_covered_expense = 0
    total_monthly_welfare_expense = 0
    total_total_recovered_amount = 0
    total_staff_bill_balance = 0

    filters = {
        "salary_component__in": ["50% Medical Recovery"],
    }

    filters_obj = object.filters

    if DataConversion.safe_get (filters_obj, "cleared", None):
        cleared = 0
        if DataConversion.safe_e (DataConversion.safe_get (filters_obj, "cleared", None), "Closed", str, True):
            cleared = 1
        DataConversion.safe_set (filters, "cleared", cleared)

    if DataConversion.safe_get (filters_obj, "department", None):
        emp_flt_val = DataConversion.safe_get (filters_obj, "department")
        emp_flt_key = "department"
            
    if DataConversion.safe_get (filters_obj, "designation", None):
        emp_flt_val = DataConversion.safe_get (filters_obj, "designation")
        emp_flt_key = "designation"

    if DataConversion.safe_get (filters_obj, "reports_to", None):
        emp_flt_val = DataConversion.safe_get (filters_obj, "reports_to")
        emp_flt_key = "report_to"

    if DataConversion.safe_get (filters_obj, "to_date", None):
        DataConversion.safe_set (filters, "effective_date",  DataConversion.safe_get (filters_obj, "to_date"))

    if DataConversion.safe_get (filters_obj, "from_date", None):
        DataConversion.safe_set (filters, "last_payment_date",  DataConversion.safe_get (filters_obj, "from_date"))

    if emp_flt_key in employees_df.columns:
        employees = (
            employees_df.groupby(emp_flt_key)
            .apply(lambda x: x.to_dict(orient="records"))
            .to_dict()
        )
    
    # payroll_entries = core_hr.get_list ("Payroll_Activity_Entry", filters={})
    payroll_entries = core_hr.get_list ("Payroll_Activity_Entry", filters=filters)
    df = utils.to_data_frame (payroll_entries)
    if "reference" in df.columns:
        grouped_reference = (
            df.groupby("reference")
            .apply(lambda x: x.to_dict(orient="records"))
            .to_dict()
        )

        for ref, ref_docs in grouped_reference.items ():

            add_total = False
            report_row = {}
            count_elements = len (ref_docs)
            count_len = 0

            advance = DataConversion.safe_list_get (ref_docs, 0)
            amount = DataConversion.convert_to_float (DataConversion.safe_get (advance, "amount", 0))
            monthly_welfare_expense = DataConversion.convert_to_float (DataConversion.safe_get (advance, "monthly_payment", 0))
            applicant = DataConversion.safe_get (advance, "employee")
            emp_info = DataConversion.safe_get (emp_details, applicant)

            welfare_expense = amount * 2
            company_covered_expense = amount
            staff_covered_expense = amount
            total_recovered_amount = 0
            staff_bill_balance = amount

            DataConversion.safe_set (report_row, "employee", applicant)
            DataConversion.safe_set (report_row, "employee_name", DataConversion.safe_get (emp_info, "full_name", f"{DataConversion.safe_get (emp_info, 'first_name')} {DataConversion.safe_get (emp_info, 'middle_name', '')} {DataConversion.safe_get (emp_info, 'last_name')}"))
            DataConversion.safe_set (report_row, "department", DataConversion.safe_get (emp_info, "department", ''))
            DataConversion.safe_set (report_row, "welfare_expense", welfare_expense )
            DataConversion.safe_set (report_row, "payment_length", DataConversion.safe_get (advance, "length_or_period"))
            DataConversion.safe_set (report_row, "monthly_welfare_expense", monthly_welfare_expense)
            DataConversion.safe_set (report_row, "staff_covered_expense", staff_covered_expense)
            DataConversion.safe_set (report_row, "company_covered_expense", company_covered_expense)

            for doc in ref_docs:
                if DataConversion.safe_e (DataConversion.safe_get (doc, "cleared", 0), 1, int):
                    count_len += 1
                    total_recovered_amount += DataConversion.convert_to_float (DataConversion.safe_get (doc, "monthly_payment", 0))                   
                    staff_bill_balance -= DataConversion.convert_to_float (DataConversion.safe_get (doc, "monthly_payment", 0))
            DataConversion.safe_set (report_row, "remaining_months", count_elements - count_len)
            DataConversion.safe_set (report_row, "total_recovered_amount", total_recovered_amount)
            DataConversion.safe_set (report_row, "staff_bill_balance", staff_bill_balance)

            if not emp_flt_key:
                add_total = True
                DataConversion.safe_list_append (return_data, report_row)
            else:
                emp_df = utils.to_data_frame (DataConversion.safe_get (employees, emp_flt_val, []))
                if "name" in emp_df.columns:
                    emp_dict = (
                        emp_df.groupby("name")
                        .apply(lambda x: x.to_dict(orient="records"))
                        .to_dict()
                    )

                    if applicant in emp_dict:
                        add_total = True
                        DataConversion.safe_list_append (return_data, report_row)
                    else:
                        continue
            
            DataConversion.safe_list_append (return_data, report_row)
            
            if add_total:
                total_welfare_expense += welfare_expense
                total_company_covered_expense += company_covered_expense
                total_staff_covered_expense += staff_covered_expense
                total_monthly_welfare_expense += monthly_welfare_expense
                total_total_recovered_amount += total_recovered_amount
                total_staff_bill_balance += staff_bill_balance

    DataConversion.safe_list_append (return_data, {
        "employee": "TOTAL",
        "welfare_expense": total_welfare_expense,
        "company_covered_expense": total_company_covered_expense,
        "staff_covered_expense": total_staff_covered_expense,
        "monthly_welfare_expense": total_monthly_welfare_expense,
        "total_recovered_amount": total_total_recovered_amount,
        "staff_bill_balance": total_staff_bill_balance,
        "is_opening_or_closing": True,
    })

    return utils.respond(utils.ok, {'rows': return_data})