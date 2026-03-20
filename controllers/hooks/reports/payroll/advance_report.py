import numpy as np
from controllers.utils import Utils
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()
pp = utils.pretty_print

def advance_report(dbms, object):
    core_payroll = Core_Payroll (dbms)
    advance_data_result = []
    total_paid_amount = 0
    total_recently_settled_amount = 0
    total_balance = 0
    total_is_paid = 0
    total_amount = 0
    total_unpaid = 0
    total_normal = 0
    total_second = 0

    advance_filters = object.filters
    filters = {
        "salary_component": "Salary Advance",
    }
    if DataConversion.safe_get (advance_filters, "employee", None):
        DataConversion.safe_set (filters, "employee", DataConversion.safe_get (advance_filters, "employee"))
    if DataConversion.safe_get (advance_filters, "cleared", None):
        cleared = 0
        if DataConversion.safe_e (DataConversion.safe_get (advance_filters, "cleared", None), "Closed", str, True):
            cleared = 1
        DataConversion.safe_set (filters, "cleared", cleared)
        
    payroll_entries = core_payroll.get_list ("Payroll_Activity_Entry", filters=filters)
    df = utils.to_data_frame (payroll_entries)
    if "reference" in df.columns:
        grouped_reference = (
            df.groupby("reference")
            .apply(lambda x: x.to_dict(orient="records"))
            .to_dict()
        )

        for ref, ref_docs in grouped_reference.items ():
            report_row = {}
            DataConversion.safe_set (report_row, "reference", ref)
            count_elements = len (ref_docs)
            advance = DataConversion.safe_list_get (ref_docs, 0)
            amount = DataConversion.convert_to_float (DataConversion.safe_get (advance, "amount", 0))
            DataConversion.safe_set (report_row, "applicant", DataConversion.safe_get (advance, "employee"))
            DataConversion.safe_set (report_row, "effective_date", DataConversion.safe_get (advance, "effective_date"))
            DataConversion.safe_set (report_row, "last_payment_date", DataConversion.safe_get (advance, "last_payment_date"))
            recently_settled_amount = 0
            type_a = "Second Advance"
            if DataConversion.safe_e (DataConversion.safe_get (advance, "salary_advance_type"), "first", str, True):
                type_a = "Normal Advance"
                total_normal += 1
            else:
                total_second += 1
            
            DataConversion.safe_set (report_row, "advance_type", type_a)
            DataConversion.safe_set (report_row, "amount", amount)
            paid_amount = 0
            balance = amount
            count_len = 0
            for i, doc in enumerate(ref_docs):
                if DataConversion.safe_e ((i+1), count_elements, int) and DataConversion.safe_e (DataConversion.safe_get (doc, "cleared", 0), 1, int):
                    recently_settled_amount = DataConversion.safe_get (doc, "monthly_payment", 0.00)
                    total_recently_settled_amount += recently_settled_amount
                if DataConversion.safe_e (DataConversion.safe_get (doc, "cleared", 0), 1, int):
                    count_len += 1
                    paid_amount += DataConversion.convert_to_float (DataConversion.safe_get (doc, "monthly_payment", 0))
                    balance -= DataConversion.convert_to_float (DataConversion.safe_get (doc, "monthly_payment", 0))

            is_paid = "Still Open"
            if DataConversion.safe_e (count_elements, count_len, int):
                is_paid = "Closed"
                total_is_paid += 1
            else:
                total_unpaid += 1
            
            repayment_method = "Payroll"
            if DataConversion.safe_e (DataConversion.safe_get (advance, "allows_cash_repayment", 0), 1, int):
                repayment_method = "Payroll / Cash"

            DataConversion.safe_set (report_row, "remaining_months", count_elements - count_len)
            DataConversion.safe_set (report_row, "repayment_method", repayment_method)
            DataConversion.safe_set (report_row, "is_paid", is_paid)
            DataConversion.safe_set (report_row, "paid_amount", paid_amount)
            DataConversion.safe_set (report_row, "balance", balance)
            DataConversion.safe_set (report_row, "recently_settled_amount", recently_settled_amount)

            DataConversion.safe_list_append (advance_data_result, report_row)

            total_balance += balance
            total_amount += amount
    
    DataConversion.safe_list_append (advance_data_result, {
        "effective_date": "TOTALS",
        "paid_amount": total_paid_amount,
        "recently_settled_amount": total_recently_settled_amount,
        "balance": total_balance,
        "is_paid": f"{total_unpaid} (OPEN) AND {total_is_paid} (CLOSED)",
        "amount": total_amount,
        "advance_type": f"{total_normal} (NORMAL) AND {total_second} (SECOND)",
        "is_opening_or_closing": True,
    })

    return utils.respond(utils.ok, {
        'rows': advance_data_result,
    })

def ecz_loan_report(dbms, object):
    core_payroll = Core_Payroll(dbms, object)
    emp_flt_key = ''
    emp_flt_val = ''
    employees = {}
    employees_df = utils.to_data_frame (core_payroll.get_list ("Employee", filters={"status__in": ["On Leave", "Active", "Suspended"]}))

    return_data =[]
    total_paid = 0
    total_balance = 0
    total_monthly_payments = 0
    total_interest = 0
    total_interest_paid = 0
    total_loan_amount = 0

    filters = {
        "salary_component__in": ["House Loan", "Personal Loan", "Tuition Advance", "Professional Membership Subscription"],
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

    if emp_flt_key in employees_df.columns:
        employees = (
            employees_df.groupby(emp_flt_key)
            .apply(lambda x: x.to_dict(orient="records"))
            .to_dict()
        )

    payroll_entries = core_payroll.get_list ("Payroll_Activity_Entry", filters=filters)

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
            monthly_payments = DataConversion.convert_to_float (DataConversion.safe_get (advance, "monthly_payment", 0))
            applicant = DataConversion.safe_get (advance, "employee")

            paid = 0
            balance = amount
            interest = 0
            interest_paid = 0

            DataConversion.safe_set (report_row, "loan_id", ref)
            DataConversion.safe_set (report_row, "employee", applicant)
            DataConversion.safe_set (report_row, "loan_amount", amount)
            DataConversion.safe_set (report_row, "disbursement_date", DataConversion.safe_get (advance, "posting_date"))
            DataConversion.safe_set (report_row, "loan_type", DataConversion.safe_get (advance, "salary_component"))
            DataConversion.safe_set (report_row, "interest_total", DataConversion.safe_get (advance, "interest_total"))
            DataConversion.safe_set (report_row, "due_date", DataConversion.safe_get (advance, "last_payment_date"))
            DataConversion.safe_set (report_row, "repayment_period", DataConversion.safe_get (advance, "length_or_period"))
            DataConversion.safe_set (report_row, "monthly_repayment", monthly_payments)

            for doc in ref_docs:
                if DataConversion.safe_e (DataConversion.safe_get (doc, "cleared", 0), 1, int):
                    count_len += 1
                    paid += DataConversion.convert_to_float (DataConversion.safe_get (doc, "monthly_payment", 0))
                    balance -= DataConversion.convert_to_float (DataConversion.safe_get (doc, "monthly_payment", 0))
            
            DataConversion.safe_set (report_row, "remaining_months", count_elements - count_len)
            DataConversion.safe_set (report_row, "paid", paid)
            DataConversion.safe_set (report_row, "balance", balance)
            
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
            if add_total:
                total_loan_amount += amount
                total_paid += paid
                total_balance += balance
                total_monthly_payments += monthly_payments
                total_interest += interest
                total_interest_paid += interest_paid

    DataConversion.safe_list_append (return_data, {
        "employee": "TOTAL",
        "loan_amount": total_loan_amount,
        "paid": total_paid,
        "balance": total_balance,
        "monthly_repayment": total_monthly_payments,
        "interest_total": total_interest,
        "interest_total": total_interest_paid,
        "is_opening_or_closing": True,
    })

    return utils.respond(utils.ok, {'rows': return_data})