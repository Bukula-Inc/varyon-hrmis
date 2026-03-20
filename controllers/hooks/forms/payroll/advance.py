from controllers.utils import Utils
from controllers.utils.dates import Dates
import datetime
from controllers.mailing import Mailing
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion


dates = Dates ()

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw
def long_term_sponsorship(dbms, object):
    core_payroll = Core_Payroll(dbms)
    app = object.body

    if not app.type_of_advance:
        return utils.respond(utils.error, "Loan type is required")

    loan_type = app.linked_fields.type_of_advance
    get_ads = core_payroll.get_list("Salary_Advance_Entries", filters={"is_active": "yes", "applicant": app.employee, "source_type": app.type_of_advance})

    entry = utils.from_dict_to_object({})
    entry.applicant = app.employee
    entry.full_name = f"{app.first_name} {app.middle_name or ''} {app.last_name}"
    entry.repayment_period = loan_type.repayment_period_length
    entry.disbarment_date = app.disbursed_on
    entry.due_date = app.due_date
    entry.entry_type = app.deduction_type
    entry.total_repaid = 0.00
    entry.interest_repaid = 0.00
    entry.amount = (app.boarding_and_lodging + app.travel_costs + app.lunch_allowance + app.books_allowance + app.tuition_fees)
    entry.balance = entry.amount
    entry.reference = app.name
    entry.paid = 0
    entry.source = app.name
    entry.is_active = "yes" if not get_ads else "pending"
    entry.source_type = app.type_of_advance
    entry.repayment_start_date = None
    entry.reference_type = app.doctype
    entry.monthly_repayment = entry.amount / loan_type.repayment_period_length
    entry.interest_total = (entry.amount / 100) * loan_type.interest_rate if loan_type.is_interest_applicable else 0.00
    entry.advance_amount_with_interest = entry.amount + entry.interest_total

    r = dbms.create("Salary_Advance_Entries", entry, submit_after_create=True)

    # bounding_period = utils.from_dict_to_object ({})
    # bounding_period.employee = entry.applicant
    # bounding_period.enabled_on = True
    # bounding_period.ending_on
    # b = dbms.create ("Enabled_Bonding_Period", bounding_period, submit_after_create=True)
    # pp (b)

def validate_loan (dbms, object):
    pp (object)
    loan_application =object.body
    if not loan_application.type_of_advance: throw("Advance type is missing, please provide one!")
    # throw ("--------------")
    pass

def house_loan (dbms, object):
    core_payroll = Core_Payroll (dbms)
    app = object.body
    loan_type = app.linked_fields.type_of_advance if app.type_of_advance else None
    get_ads = core_payroll.get_list ("Salary_Advance_Entries", filters={"is_active": "yes", "applicant": app.employee, "source_type": app.type_of_advance})
    # pp(loan_type, get_ads, app)
    if loan_type and get_ads:
        if loan_type.maximum_open_advances >= len (get_ads) or 0:
            throw (f"Maximum Limit for {loan_type.name} has been Hit")
    entry = utils.from_dict_to_object ({})
    entry.applicant = app.employee
    entry.full_name = app.full_name
    entry.repayment_period = loan_type.repayment_period_length or 0
    entry.disbarment_date = dates.today ()
    entry.due_date = app.due_date
    entry.entry_type = app.type_of_advance
    entry.total_repaid = 0.00
    entry.interest_repaid = 0.00
    entry.amount = 0.00
    entry.balance = entry.amount
    entry.reference = app.name
    entry.paid = 0
    entry.source = app.name
    entry.is_active = "yes" if not get_ads else "pending"
    entry.source_type = loan_type.name
    entry.repayment_start_date = None
    entry.reference_type = app.doctype
    entry.monthly_repayment = entry.amount / loan_type.repayment_period_length
    entry.interest_total = (entry.amount/loan_type.interest_rate) * 100 if loan_type.is_interest_applicable else 0.00
    entry.advance_amount_with_interest = entry.amount + entry.interest_total
    r = dbms.create ("Salary_Advance_Entries", entry, submit_after_create=True)
    pp (r)

def professional_sponsorship (dbms, object):
    app = object.body
    employee = DataConversion.safe_get (app, "employee")
    pp(app)
    doc = DataConversion.safe_get (app, "name")
    if not doc:
        throw (f"Reference is <strong class='text-rose-600'> missing</strong>")
    if not employee:
        throw (f"Applicant/Employee No is <strong class='text-rose-600'> required</strong>")
    instalments_period = DataConversion.convert_to_float (DataConversion.safe_get (app, "instalments_period"))
    amount = DataConversion.convert_to_float (DataConversion.safe_get (app, "amount"))
    entry = utils.from_dict_to_object ({})
    DataConversion.safe_set (entry, "applicant", employee)
    DataConversion.safe_set (entry, "repayment_period", instalments_period)
    DataConversion.safe_set (entry, "fullname", DataConversion.safe_get (app, "fullname"))
    DataConversion.safe_set (entry, "due_date", dates.add_days (dates.today (), 30 * instalments_period))
    DataConversion.safe_set (entry, "disbarment_date", dates.today ())
    DataConversion.safe_set (entry, "entry_type", "Professional Membership Subscription")
    DataConversion.safe_set (entry, "fullname", DataConversion.safe_get (app, "fullname"))
    DataConversion.safe_set (entry, "total_repaid", 0.00)
    DataConversion.safe_set (entry, "paid", 0.00)
    DataConversion.safe_set (entry, "interest_repaid", 0.00)
    DataConversion.safe_set (entry, "interest_total", 0.00)
    DataConversion.safe_set (entry, "advance_amount_with_interest", 0.00)
    DataConversion.safe_set (entry, "amount", amount)
    DataConversion.safe_set (entry, "balance", amount)
    DataConversion.safe_set (entry, "reference", doc)
    DataConversion.safe_set (entry, "source", doc)
    DataConversion.safe_set (entry, "is_active", "yes")
    DataConversion.safe_set (entry, "source_type", "deduction")
    DataConversion.safe_set (entry, "repayment_start_date", None)
    DataConversion.safe_set (entry, "reference_type", DataConversion.safe_get (app, "doctype"))
    DataConversion.safe_set (entry, "monthly_repayment", amount / instalments_period or 0.00)

    r = dbms.create ("Salary_Advance_Entries", entry, submit_after_create=True)
    pp (r)

def apply_for_advance (dbms, object):
    validate_advance (dbms, object)


def approve_for_advance (dbms, object):
    core_payroll = Core_Payroll (dbms)
    validated_data = validate_advance (dbms, object, True)
    if validated_data:
        advance_type = core_payroll.get_doc ("Salary_Advance_Configuration", object.body.type_of_advance)
        due_date = dates.add_days (dates.today (), 30)
        repstart_date = due_date
        if advance_type:
            if (advance_type.grace_period):
                repstart_date = dates.add_days(dates.today (), (30 * int (advance_type.grace_period)))
            if str (advance_type.repayment_plan).lower () == "over a period of time":
                due_date = dates.add_days(repstart_date, (30 * int (advance_type.repayment_period_length)))

        get_ads = core_payroll.get_list ("Salary_Advance_Entries", filters={"is_active": "yes", "applicant": object.body.applicant, "source_type": object.body.type_of_advance})

        object.body.due_date = due_date
        object.body.disbursed_on = dates.today ()
        send_mail = Mailing (dbms=dbms, object=object)
        entry = utils.from_dict_to_object ({})
        entry.applicant = object.body.applicant
        entry.full_name = object.body.full_name
        entry.repayment_period = object.body.repayment_period
        entry.disbarment_date = object.body.disbursed_on
        entry.due_date = object.body.due_date
        entry.entry_type = advance_type.advance_type
        entry.total_repaid = 0.00
        entry.interest_repaid = 0.00
        entry.amount = validated_data.advance_amount
        entry.balance = entry.amount
        entry.reference = object.body.name
        entry.paid = 0
        entry.source = object.body.name
        entry.is_active = "yes" if not get_ads else "pending"
        entry.source_type = object.body.type_of_advance
        entry.repayment_start_date = repstart_date
        entry.reference_type = object.body.doctype
        entry.monthly_repayment = validated_data.total_monthly_payment
        entry.interest_total = validated_data.interest_amount
        entry.advance_amount_with_interest = validated_data.advance_amount_with_interest
        entry = dbms.create ("Salary_Advance_Entries", entry, submit_after_create=True)
        if entry.status == utils.ok:
            applicant_info = entry.data.linked_fields.applicant
            if applicant_info and applicant_info.email:
                se = send_mail.send_mail (recipient=applicant_info.email, subject="ADVANCE APPROVAL", body=f"<h1>Dear {applicant_info.full_name},</h1><p>Your advanced request was approved</p>")
                pp(se)

def validate_advance (dbms, object, submission=False):
    core_payroll = Core_Payroll (dbms=dbms)
    object.body.is_paid = 0
    advance = object.body
    pp("............",advance)
    advance_type = advance.type_of_advance
    valid_amount = 0.00
    advance_amount = 0.00
    interest_amount = 0.00
    total_monthly_payment = 0.00
    advance_amount_with_interest = 0.00
    if not advance.applicant:
        throw ("Applicant is missing on the application")
    emp = core_payroll.get_doc ("Employee", advance.applicant)
    pp("emp ===>",emp)
    if not advance_type:
        throw ("Choose a valid valid advance type")
    advance_type = core_payroll.get_doc ("Salary_Advance_Configuration", advance_type)
    if str(advance_type.amount_value).lower () == "percentage of basic pay":
        valid_amount =  (float(utils.remove_special_characters(advance_type.amount_rate))/100) * float (advance.basic_pay)
    elif str(advance_type.amount_value).lower () == "employee's full basic":
        valid_amount = float (utils.remove_special_characters (advance.basic_pay))
    else:
        throw ("Choose a valid valid advance type")
    advance_amount = float (utils.remove_special_characters (advance.amount))
    if advance_amount > valid_amount:
        throw (f"Cannot apply for {advance_amount} for it is Greater than your threshold {valid_amount}")
    if str (advance_type.eligibility_type).lower () != "all":
        if advance_type.eligibility and len(advance_type.eligibility) > 0:
            eligible = False
            for eligibility in advance_type.eligibility:
                if eligibility.employment_type == emp.employment_type:
                    if eligibility.time_measure == "Months":
                        eligibility_date = dates.calculate_days (to_date=datetime.strptime(dates.today (), "%Y-%m-%d").date(), from_date=emp.date_of_joining)
                        if eligibility_date >= eligibility.period_of_service:
                            eligible = True
                    elif eligibility.time_measure == "Years":
                        if dates.years_since (emp.date_of_joining, eligibility.period_of_service):
                            eligible = True
                    elif eligibility.time_measure == "Days":
                        if dates.days_since (emp.date_of_joining, eligibility.period_of_service):
                            eligible = True
                    elif eligibility.time_measure == "Months":
                        if dates.months_since (emp.date_of_joining, eligibility.period_of_service):
                            eligible = True
                    elif eligibility.time_measure == "Weeks":
                        if dates.weeks_since (emp.date_of_joining, eligibility.period_of_service):
                            eligible = True
            if not eligible:
                throw (f"Your Are Not Eligible For {advance_type.name} {advance_type.advance_type}!")
    if advance_type.is_interest_applicable:
        interest_amount = (float(utils.remove_special_characters(advance_type.interest_rate))/100) * float (advance_amount)
        advance_amount_with_interest = advance_amount + interest_amount
    open_advances = core_payroll.get_list ("Salary_Advance_Entries", filters={"applicant": emp.name,"paid": 0})
    if str (advance_type.repayment_plan).lower () == "over a period of time":
        total_monthly_payment = (advance_amount_with_interest / advance_type.repayment_period_length) if advance_type.is_interest_applicable else (advance_amount / advance_type.repayment_period_length)
    if open_advances:
        open_amount = total_monthly_payment
        take_Home_pen = (float(utils.remove_special_characters(advance_type.max_take_home))/100) * float (advance.basic_pay)
        pp (advance_type.maximum_open_advances, len(open_advances))
        if not submission and len (open_advances) + 1 > advance_type.maximum_open_advances:
            throw (f"Cannot apply for {advance_type.name} you've reach the maximum open threshold {advance_type.maximum_open_advance}")
        for open_adv_amount in open_advances:
            open_amount += open_adv_amount.monthly_repayment
        if open_amount > take_Home_pen:
            throw (f"Cannot apply for {advance_type.name} you've due to maximum take home threshold {advance_type.max_take_home}% of Your Basic")
    response = utils.from_dict_to_object ({
        "advance_amount": advance_amount,
        "total_monthly_payment": total_monthly_payment,
        "interest_amount": interest_amount,
        "advance_amount_with_interest": advance_amount_with_interest,
    })
    return response