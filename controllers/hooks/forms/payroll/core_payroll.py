# core_payroll

from controllers.core_functions.payroll import Core_Payroll
from controllers.utils import Utils
from datetime import datetime

utils = Utils ()
pp = utils.pretty_print


def get_month_and_year (months_from_to_day=0):
    now = datetime.now()

    month_name = now.strftime('%B')
    year = now.strftime('%Y')
    return month_name, year


def check_for_payroll_affecting (dbms,document, employee, amount, reference, period, salary_component, settle=False, full_amount=0.00, full_interest=0.00, is_once_off=False):
    dt = get_month_and_year ()
    if not settle:
        entry = utils.from_dict_to_object ({
            "status": "Submitted",
            "employee": employee,
            "salary_component": salary_component,
            "is_used": 0,
            "month": dt[0],
            "year": dt[1],
            "full_amount": full_amount,
            "paid_amount": 0.00,
            "interest_amount": full_interest,
            "paid_interest_amount": 0.00,
            "remaining_period": period,
            "running_for": period,
            "reference": reference,
            "reference_doc": document,
            "amount": amount,
            "is_once_off": is_once_off,
        })
        dbms.create ("Payroll_Content_Per_Month", entry)
    elif settle:
        query = """
            SELECT * FROM payroll_content_per_months WHERE is_used = %s AND employee = %s AND reference = %s AND reference_doc LIMIT=1
        """
        employee_payroll_content = dbms.sql (query, [0, str({employee.get ("name", None)}), reference, document])
        if employee_payroll_content.status == utils.ok and len (employee_payroll_content.data) > 0:
            entry = employee_payroll_content.data[0]
            entry.amount -= float (amount)
            entry.is_used = 1 if entry.amount <= 0 else 0
            entry.remaining_period -= 1
            if not entry.is_once_off and entry.is_used == 1 and entry.remaining_period > 0:
                new_entry = entry.copy ()
                new_entry.is_used = 0
                new_entry.paid
                new_entry.amount = amount
                new_entry.paid_amount += amount
                new_entry.paid_interest_amount += entry.interest_amount / entry.running_for
                new_entry.remaining_period -= 1
                # new_entry.month = entry.month #resolve for the month so you can get the next month
                # new_entry.year = entry.year ##resolve for the year so you can get the next year
                dbms.create ("Payroll_Content_Per_Month", new_entry)
            dbms.update ("Payroll_Content_Per_Month", entry, update_submitted=True)