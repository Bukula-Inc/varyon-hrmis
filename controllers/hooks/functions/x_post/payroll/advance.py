from controllers.utils import Utils
from controllers.utils.dates import Dates
import datetime
import math
from controllers.core_functions.payroll import Core_Payroll

dates = Dates ()

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

def advance_calc (dbms, object):
    core_payroll = Core_Payroll (dbms=dbms)
    filters = object.body.data
    get_lst = core_payroll.get_list ("Advance_Application", filters=filters)
    if not get_lst:
        get_lst = "no Advances"
    return utils.respond (utils.ok, get_lst)

# def apply_for_advance (dbms, object):
#     core_payroll = Core_Payroll (dbms=dbms)
#     object.body.is_paid = 0
#     advance = object.body
#     advance_type = advance.type_of_advance
#     valid_amount = 0.00
#     advance_amount = 0.00
#     interest_amount = 0.00
#     total_monthly_payment = 0.00
#     advance_amount_with_interest = 0.00
#     if not advance.applicant:
#         throw ("Applicant is missing on the application")
#     emp = core_payroll.get_doc ("Employee", advance.applicant)
#     if not advance_type:
#         throw ("Choose a valid valid advance type")
#     advance_type = core_payroll.get_doc ("Salary_Advance_Configuration", advance_type)
#     if str(advance_type.amount_value).lower () == "percentage of basic pay":
#         valid_amount =  (float(utils.remove_special_characters(advance_type.amount_rate))/100) * float (advance.basic_pay)
#     elif str(advance_type.amount_value).lower () == "employee's full basic":
#         valid_amount = float (utils.remove_special_characters (advance.basic_pay))
#     else:
#         throw ("Choose a valid valid advance type")
#     advance_amount = float (utils.remove_special_characters (advance.amount))
#     if advance_amount > valid_amount:
#         throw (f"Cannot apply for {advance_amount} for it is Greater than your threshold {valid_amount}")
#     if str (advance_type.eligibility_type).lower () != "all":
#         if advance_type.eligibility and len(advance_type.eligibility) > 0:
#             eligible = False
#             for eligibility in advance_type.eligibility:
#                 if eligibility.employment_type == emp.employment_type:
#                     if eligibility.time_measure == "Months":
#                         eligibility_date = dates.calculate_days (to_date=datetime.strptime(dates.today (), "%Y-%m-%d").date(), from_date=emp.date_of_joining)
#                         if eligibility_date >= eligibility.period_of_service:
#                             eligible = True
#                     elif eligibility.time_measure == "Years":
#                         if dates.years_since (emp.date_of_joining, eligibility.period_of_service):
#                             eligible = True
#                     elif eligibility.time_measure == "Days":
#                         if dates.days_since (emp.date_of_joining, eligibility.period_of_service):
#                             eligible = True
#                     elif eligibility.time_measure == "Months":
#                         if dates.months_since (emp.date_of_joining, eligibility.period_of_service):
#                             eligible = True
#                     elif eligibility.time_measure == "Weeks":
#                         if dates.weeks_since (emp.date_of_joining, eligibility.period_of_service):
#                             eligible = True
#             if not eligible:
#                 throw (f"Your Are Not Eligible For {advance_type.name} {advance_type.advance_type}!")
#     if advance_type.is_interest_applicable:
#         interest_amount = (float(utils.remove_special_characters(advance_type.interest_rate))/100) * float (advance_amount)
#         advance_amount_with_interest = advance_amount + interest_amount
#     open_advances = core_payroll.get_list ("Advance_Application", filters={"is_paid": 0})
#     if str (advance_type.repayment_plan).lower () == "over a period of time":
#         total_monthly_payment = (advance_amount_with_interest / advance_type.repayment_period_length) if advance_type.is_interest_applicable else (advance_amount / advance_type.repayment_period_length)
#     if open_advances:
#         open_amount = total_monthly_payment
#         take_Home_pen = (float(utils.remove_special_characters(advance_type.max_take_home))/100) * float (advance.basic_pay)
#         if len (open_advances) + 1 > advance_type.maximum_open_advances:
#             throw (f"Cannot apply for {advance_type.name} you've reach the maximum open threshold {advance_type.maximum_open_advance}")
#         for open_adv_amount in open_advances:
#             open_amount += open_adv_amount.total_monthly_amount
#         if open_amount > take_Home_pen:
#             throw (f"Cannot apply for {advance_type.name} you've due to maximum take home threshold {advance_type.max_take_home}% of Your Basic")


def loan_calculator(principal, rate, time, method='amortized', payments_per_year=12):
    """
        Calculate loan payments or interest using various methods.
        Parameters:
            principal (float): The loan amount (initial principal).
            rate (float): Annual interest rate as a decimal (e.g., 0.05 for 5%).
            time (float): Time in years (or months depending on the rate).
            method (str): The method for calculation ('simple', 'compound', 'amortized',
                        'declining_balance', 'balloon', 'equal_principal', 'graduated').
            payments_per_year (int): The number of payments per year (default is 12 for monthly payments).

        Returns:
            float: The calculated payment or interest.
    """
    rate_per_period = rate / payments_per_year

    if str (method).lower () == 'simple':
        interest = principal * rate * time
        return interest

    elif str (method).lower () == 'compound':
        # Compound Interest Method
        amount = principal * (1 + rate_per_period) ** (payments_per_year * time)
        return amount - principal

    elif str (method).lower () == 'amortized':
        # Amortized Loan (Fixed-rate) Method
        num_payments = payments_per_year * time
        payment = principal * (rate_per_period * (1 + rate_per_period) ** num_payments) / ((1 + rate_per_period) ** num_payments - 1)
        return payment

    elif str (method).lower () == 'declining_balance':
        # Declining Balance Method
        # Calculate the interest for each period based on the outstanding balance
        total_interest = 0
        outstanding_balance = principal
        for _ in range(int(payments_per_year * time)):
            interest = outstanding_balance * rate_per_period
            total_interest += interest
            # Assuming principal payments are the same each period
            outstanding_balance -= (principal / (payments_per_year * time))
        return total_interest

    elif str (method).lower () == 'balloon':
        # Balloon Loan Method
        # Assuming equal payments for most of the term, then a large lump sum at the end
        monthly_payment = principal * (rate_per_period * (1 + rate_per_period) ** (payments_per_year * (time - 1))) / \
                          ((1 + rate_per_period) ** (payments_per_year * (time - 1)) - 1)
        balloon_payment = principal * (1 + rate_per_period) ** (payments_per_year * (time - 1))
        return monthly_payment, balloon_payment

    elif str (method).lower () == 'equal_principal':
        # Equal Principal Payment Method
        num_payments = payments_per_year * time
        principal_payment = principal / num_payments
        total_interest = 0
        outstanding_balance = principal
        payments = []
        for _ in range(num_payments):
            interest_payment = outstanding_balance * rate_per_period
            total_payment = principal_payment + interest_payment
            payments.append(total_payment)
            outstanding_balance -= principal_payment
            total_interest += interest_payment
        return payments, total_interest

    elif str (method).lower () == 'graduated':
        # Graduated Payment Loan Method (payments increase annually by 5%)
        payments = []
        initial_payment = principal * rate_per_period * (1 + rate_per_period) / (1 - (1 + rate_per_period) ** -payments_per_year)
        payments.append(initial_payment)
        # Increase the payment by 5% annually
        for i in range(1, int(time)):
            increased_payment = payments[-1] * 1.05
            payments.append(increased_payment)
        total_payments = sum(payments)
        return payments, total_payments

    else:
        raise ValueError("Unsupported loan calculation method.")
