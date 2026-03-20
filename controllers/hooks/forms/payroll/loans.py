from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.payroll import Core_Payroll
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
from datetime import datetime


dates = Dates ()

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

def validate_welfare (dbms, object):
    core_payroll = Core_Payroll (dbms=dbms)
    app = DataConversion.safe_get (object, "body")
    emp_id = DataConversion.safe_get (app, "employee")
    payment_method = DataConversion.safe_get (app, "payment_method")
    requested_amount = DataConversion.convert_to_float (DataConversion.safe_get (app, "welfare_expense", 0))
    repayment_period = DataConversion.convert_to_int (DataConversion.safe_get (app, "payment_length", 0))
    if not emp_id:
        throw ("Employee No is <strong class='text-rose-600'>required</strong>.")
    emp = core_payroll.get_doc ("Employee", emp_id)
    if not emp:
        throw (f"Employee with ID <strong class='text-rose-600'>{emp_id}</strong> does not exist.")
    if not requested_amount:
        throw ("Total Amount Utilized is <strong class='text-rose-600'>required</strong>.")
    if not repayment_period:
        throw ("Repayment Period is <strong class='text-rose-600'>required</strong>.")
    if repayment_period > 8:
        throw ("Repayment Period should not exceed <strong class='text-rose-600'>Eight (8) months</strong>.")
    if not payment_method:
        throw ("Payment Method is <strong class='text-rose-600'>required</strong>.")
    if DataConversion.safe_e (payment_method, "Cash", str, True):
        if not DataConversion.safe_get (app, "attach_receipt"):
            throw ("Receipt Attachment  is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "amount_in_words"):
        throw ("Amount in Words is <strong class='text-rose-600'>required</strong>.")

    covered_expense = requested_amount/2
    DataConversion.safe_set (object.body, "staff_covered_expense", covered_expense)
    DataConversion.safe_set (object.body, "company_covered_expense", covered_expense)
    DataConversion.safe_set (object.body, "monthly_repayment_amount", covered_expense/repayment_period)
    DataConversion.safe_set (object.body, "total_amount_repaid", 0)

def validate_tuition_advance (dbms, object):
    core_payroll = Core_Payroll (dbms=dbms)
    tuition_app = DataConversion.safe_get (object, "body")
    
    emp_id = DataConversion.safe_get (tuition_app, "employee")
    requested_amount = DataConversion.convert_to_float (DataConversion.safe_get (tuition_app, "maximum_loan_amount_requested", 0))
    repayment_period = DataConversion.convert_to_int (DataConversion.safe_get (tuition_app, "repayment_period", 0))
    if not emp_id:
        throw ("Employee No is <strong class='text-rose-600'>required</strong>.")
    emp = core_payroll.get_doc ("Employee", emp_id)
    if not emp:
        throw (f"Employee with ID <strong class='text-rose-600'>{emp_id}</strong> does not exist.")
    if not DataConversion.safe_get (tuition_app, "nrc_id"):
        throw ("NRC No is <strong class='text-rose-600'>required</strong>.")
    if not requested_amount:
        throw ("Requested Amount is <strong class='text-rose-600'>required</strong>.")
    if not repayment_period:
        throw ("Repayment Period is <strong class='text-rose-600'>required</strong>.")
    
    if repayment_period > 10:
        throw ("Repayment Period <strong class='text-rose-600'>cannot Greater than 10</strong>.")
    DataConversion.safe_set (object.body, "total_amount_repaid", 0)
    DataConversion.safe_set (object.body, "monthly_deduction_amount", requested_amount/repayment_period)

def house_loan_validations (dbms, object):
    core_payroll = Core_Payroll (dbms=dbms)
    cor_hr = Core_Hr (dbms)
    app = DataConversion.safe_get (object, "body")
    age_to_retirement = DataConversion.convert_to_int (DataConversion.safe_get (app, "age_to_retirement"))
    repayment_period = DataConversion.convert_to_int (DataConversion.safe_get (app, "repayment_period"))
    service_condition_type = DataConversion.safe_get (app, "service_condition_type")
    applicant_witness = DataConversion.safe_get (app, "applicant_witness")
    retirement_date = DataConversion.safe_get (app, "retirement_date")
    contract_expiration_date = DataConversion.safe_get (app, "contract_expiration_date")
    emp_id = DataConversion.safe_get (app, "employee")
    # if not contract_expiration_date:
    #     throw ("Contract Expiration Date is <strong class='text-rose-600'>required</strong>.")
    if not applicant_witness:
        throw ("Applicant Witness is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "nrc"):
        throw ("NRC No is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "date_of_engagement"):
        throw ("Date of engagement is <strong class='text-rose-600'>required</strong>.")
    if not service_condition_type:
        throw ("Condition of Service is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "requested_amount", 0):
        throw ("Requested Amount is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "requested_amount_words"):
        throw ("Requested Amount In Words is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "sketched_building_plan"):
        throw ("Sketched Building Plan is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "approved_house_plan"):
        throw ("Approved House Plan is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "proof_of_ownership"):
        throw ("Proof of Ownership is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "letter_of_sale"):
        throw ("Letter of Sale is <strong class='text-rose-600'>required</strong>.")
    if not emp_id:
        throw ("Employee No is <strong class='text-rose-600'>required</strong>.")
    emp = core_payroll.get_doc ("Employee", emp_id)
    if not emp:
        throw (f"Employee with ID <strong class='text-rose-600'>{emp_id}</strong> does not exist.")
    
    years_in_service_remaining = 0
    ld = dates.today ()
    if service_condition_type in ["Secondment", "Permanent and Pensionable"]:
        if not retirement_date:
            throw ("Retirement Date is <strong class='text-rose-600'>required</strong> for Permanent and Pensionable or Seconded Staff.")
        else:
            years_in_service_remaining = DataConversion.date_diff (retirement_date, dates.today (), unit="months")
            ld = retirement_date
            
    elif DataConversion.safe_e (service_condition_type, "Fixed Term", str, True):
        if not contract_expiration_date:
            throw ("Contract Expiration Date is <strong class='text-rose-600'>required</strong> for Contract Staff.")
        else:
            years_in_service_remaining = DataConversion.date_diff (contract_expiration_date, dates.today (), unit="months")
            ld = contract_expiration_date
    years = 0
    months = 0
    if DataConversion.safe_gt (repayment_period, 100, int):
        throw ("Repayment Period cannot be more than <strong class='text-rose-600'>100 months</strong>.")
    if DataConversion.safe_lt (years_in_service_remaining, repayment_period, int):
        repayment_period = repayment_period - years_in_service_remaining
    if years_in_service_remaining > 12:
        years_months = years_in_service_remaining/12
        months = years_in_service_remaining % 12
        years = years_months - months

    to_retirement = f"{years} year(s) {months} month(s)" if years > 0 else f"{years_in_service_remaining} month(s)" 
    
    egg = DataConversion.safe_get (emp, "date_of_joining")
    if not egg:
        throw (f"Employee <strong class='text-rose-600'>has no Date of Engagement</strong>.")
    if DataConversion.safe_lt (ld, egg, datetime):
        throw (f"Employee <strong class='text-rose-600'>has less time to retirement than time served</strong>.")
    dob = DataConversion.safe_get (emp, "d_o_b")
    hs = cor_hr.get_company_settings ()
    if not hs:
        throw ("Company HR Settings <strong class='text-rose-600'>Not Configured</strong>.")
    retirement_age_hs = DataConversion.convert_to_int (DataConversion.safe_get (hs, "retirement_age", 60))
    if not dob:
        throw (f"Employee has no <strong class='text-rose-600'>Date of Birth there is no way of knowing their age.</strong>.")
    rtm_age = DataConversion.date_diff (ld, dob, unit="years")
    
    if DataConversion.safe_gt (rtm_age, retirement_age_hs, int):
        throw (f"Employee <strong class='text-rose-600'>Retirement Age ({rtm_age} years) is greater than Council Retirement Age ({retirement_age_hs} years).</strong>.")
    DataConversion.safe_set (object.body, "age_to_retirement", retirement_age_hs - rtm_age)
    DataConversion.safe_set (object.body, "emp", emp)
    DataConversion.safe_set (object.body, "loan_entitlement", DataConversion.convert_to_float (DataConversion.safe_get (app, "requested_amount", 0)))
    DataConversion.safe_set (object.body, "total_amount_repaid", 0)
    DataConversion.safe_set (object.body, "years_in_service_remaining", to_retirement)
    DataConversion.safe_set (object.body, "repayment_period", repayment_period)
    # DataConversion.safe_set (object.body, "loan_entitlement", Re)

def long_term_sponsorship_validations (dbms, object):
    core_payroll = Core_Payroll (dbms)
    ltsa = DataConversion.safe_get (object, "body")
    emp_id = DataConversion.safe_get (ltsa, "employee")
    witness = DataConversion.safe_get (ltsa, "wittiness_staff")

    if not witness:
        throw ("Witness is <strong class='text-rose-600'>required</strong>.")
    witness_obj = core_payroll.get_doc ("Employee", witness)
    if not witness_obj:
        throw (f"Employee with No {witness} <strong class='text-rose-600'>Was Not Found</strong>.")
    
    if not emp_id:
        throw ("Employee No is <strong class='text-rose-600'>required</strong>.")
    emp = core_payroll.get_doc ("Employee", emp_id)
    if not emp:
        throw (f"Employee with No {emp_id} <strong class='text-rose-600'>Was Not Found</strong>.")
    date_of_birth = DataConversion.safe_get(emp, "d_o_b")
    if not date_of_birth:
        throw (f"Employee has no date <strong class='text-rose-600'>Date of Birth there is no way of knowing their age.</strong>.")
    expiry_date = DataConversion.safe_get (ltsa, "end_of_contract")
    course_duration = DataConversion.convert_to_float (DataConversion.safe_get (ltsa, "course_duration"))
    if not expiry_date:
        throw (f"Contract Expiration Date <strong class='text-rose-600'> is Required</strong>.")
    if not course_duration:
        throw (f"Course Duration <strong class='text-rose-600'> is Required</strong>.")
    year_expiration = DataConversion.convert_to_float (DataConversion.date_diff(expiry_date, dates.today (), unit="years"))
    if year_expiration < course_duration:
        throw (f"This Application Cannot Process <strong class='text-rose-600'> The Contract will End before the Course is Completed</strong>.")

    tuition_fees = DataConversion.safe_get (object.body, "tuition_fees", 0)
    if not tuition_fees:
        throw (f"Tuition Fees <strong class='text-rose-600'> are Required</strong>.")

    DataConversion.safe_set (object.body, "boarding_and_lodging", DataConversion.safe_get (object.body, "boarding_and_lodging", 0))
    DataConversion.safe_set (object.body, "travel_costs", DataConversion.safe_get (object.body, "travel_costs", 0))
    DataConversion.safe_set (object.body, "lunch_allowance", DataConversion.safe_get (object.body, "lunch_allowance", 0))
    DataConversion.safe_set (object.body, "books_allowance", DataConversion.safe_get (object.body, "books_allowance", 0))
    DataConversion.safe_set (object.body, "tuition_fees", tuition_fees)
    DataConversion.safe_set (object.body, "saved", 1)
    DataConversion.safe_set (object.body, "total_amount_repaid", 0)

    DataConversion.safe_set (object.body, "last_name", DataConversion.safe_get (ltsa, "last_name", DataConversion.safe_get (emp, 'last_name')))
    DataConversion.safe_set (object.body, "middle_name", DataConversion.safe_get (ltsa, "middle_name", DataConversion.safe_get (emp, 'middle_name')))
    DataConversion.safe_set (object.body, "first_name", DataConversion.safe_get (ltsa, "first_name", DataConversion.safe_get (emp, 'first_name')))
    DataConversion.safe_set (object.body, "designation", DataConversion.safe_get (ltsa, "designation", DataConversion.safe_get (emp, 'designation')))
    DataConversion.safe_set (object.body, "department", DataConversion.safe_get (ltsa, "section", DataConversion.safe_get (emp, 'section')))
    DataConversion.safe_set (object.body, "salary_grade", DataConversion.safe_get (ltsa, "salary_grade", DataConversion.safe_get (emp, 'employee_grade')))
    DataConversion.safe_set (object.body, "basic_pay", DataConversion.safe_get (ltsa, "basic_pay", DataConversion.safe_get (emp, 'basic_pay')))
    DataConversion.safe_set (object.body, "age", DataConversion.date_diff(dates.today (), date_of_birth, unit="years"))
    DataConversion.safe_set (object.body, "emp", emp)
    DataConversion.safe_set (object.body, "witness", witness_obj)

def validate_salary_advance (dbms, object, is_memo=False, is_saving=True):
    core_payroll = Core_Payroll (dbms=dbms)

    na = DataConversion.safe_get (object, "body")
    emp_id = DataConversion.safe_get (na, "employee_id")
    repayment_period = DataConversion.convert_to_int (DataConversion.safe_get (na, "repayment_period"))
    amount = DataConversion.convert_to_float (DataConversion.safe_get (na, "amount"))
    amount_in_words = DataConversion.safe_get (na, "amount_in_words")
    if not amount_in_words:
        throw ("Amount in Words is <strong class='text-rose-600'>required</strong>.")
    
    if not repayment_period or repayment_period == 0:
        throw ("Repayment Period is <strong class='text-rose-600'>required</strong> and must be greater than zero.")
    if repayment_period > 4:
        throw ("Repayment Period cannot be more than <strong class='text-rose-600'>4 months</strong> for Normal Advance.")
    if not amount or amount == 0.00:
        throw ("Amount is <strong class='text-rose-600'>required</strong> and must be greater than zero.")
    if not emp_id:
        throw ("Employee No is <strong class='text-rose-600'>required</strong>.")
    

    emp = core_payroll.get_doc ("Employee", emp_id)
    if not emp:
        throw (f"Employee with No {emp_id} <strong class='text-rose-600'>Was Not Found</strong>.")
    
    advance_f = {
        "employee_id": emp_id,
        "is_paid": 0,
        "is_approved": 0,
    }

    DataConversion.safe_set (object.body, "full_name", DataConversion.safe_get (na, "full_name", f"""{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}"""))
    DataConversion.safe_set (object.body, "designation", DataConversion.safe_get (na, "designation", DataConversion.safe_get (emp, 'designation')))
    DataConversion.safe_set (object.body, "department", DataConversion.safe_get (na, "section", DataConversion.safe_get (emp, 'section')))
    DataConversion.safe_set (object.body, "section", DataConversion.safe_get (na, "department", DataConversion.safe_get (emp, 'department')))
    DataConversion.safe_set (object.body, "employment_type", DataConversion.safe_get (na, "employment_type", DataConversion.safe_get (emp, 'employment_type')))
    DataConversion.safe_set (object.body, "employee_grade", DataConversion.safe_get (na, "employee_grade", DataConversion.safe_get (emp, 'employee_grade')))
    DataConversion.safe_set (object.body, "basic_pay", DataConversion.safe_get (na, "basic_pay", DataConversion.safe_get (emp, 'basic_pay')))
    DataConversion.safe_set (object.body, "total_amount_repaid", 0)
    DataConversion.safe_set (object.body, "is_approved", 0)

    at = DataConversion.safe_get (na, "advance_type")
    if not at:
        throw ("Advance Type is <strong class='text-rose-600'>required</strong>.")
    
    if at == "Normal Advance":
        DataConversion.safe_set (advance_f, "advance_type__in", ["Second Advance","Normal Advance"])
    else:
        DataConversion.safe_set (advance_f, "advance_type", "Second Advance")
        
    entries = core_payroll.get_list ("Advance_Application", filters=advance_f, order_by=['id'])
    if is_saving:
        s_entries = core_payroll.get_list ("Second_Salary_Advance_Application", filters=advance_f, order_by=['id'])

        if len (s_entries) > 0:
            throw (f"Employee <strong class='text-rose-600'>{DataConversion.safe_get (emp, 'full_name', emp_id)}</strong> has an existing unpaid {at}.")
    
    if len (entries) <= 0 and is_memo:
        has_normal_advance = False
        for entry in entries:
            if entry.advance_type == "Normal Advance" and entry.docstatus in [1,3,2]:
                has_normal_advance = True

            if entry.docstatus in [1,3,2]:
                throw (f"Employee <strong class='text-rose-600'>{DataConversion.safe_get (emp, 'full_name', emp_id)}</strong> has an existing unpaid {at}.")

            elif entry.name != na.name and entry.docstatus in [1,3,2]:
                throw (f"Employee <strong class='text-rose-600'>{DataConversion.safe_get (emp, 'full_name', emp_id)}</strong> has an existing unpaid {DataConversion.safe_get (entry, 'advance_type', at)}.")
                break
        if len (entries) > 0 and at == "Second Advance" and not has_normal_advance:
            throw ("Can't Initialize Second <strong class='text-rose-600'>Advance You have Not Yet Initialized Normal Advance</strong/")
    else:
        for entry in entries:

            if entry.docstatus in [1,3,2]:
                throw (f"Employee <strong class='text-rose-600'>{DataConversion.safe_get (emp, 'full_name', emp_id)}</strong> has an existing unpaid {at}.")

            elif entry.name != na.name and entry.docstatus in [1,3,2]:
                throw (f"Employee <strong class='text-rose-600'>{DataConversion.safe_get (emp, 'full_name', emp_id)}</strong> has an existing unpaid {DataConversion.safe_get (entry, 'advance_type', at)}.")
                break
        DataConversion.safe_set (object.body, 'emp_status', DataConversion.safe_get (emp, "status"))
        DataConversion.safe_set(object.body, "total_monthly_amount", amount / repayment_period) 

def on_normal_advance_save (dbms, object):
    validate_salary_advance (dbms, object)
    DataConversion.safe_set (object.body, "cleared", 0)

def on_second_advance_save (dbms, object):
    validate_salary_advance (dbms, object, is_saving=False)
    DataConversion.safe_set (object.body, "cleared", 0)
    object.doc_status = "Draft"

def on_normal_advance_update (dbms, object, ):
    validate_salary_advance (dbms, object)
    DataConversion.safe_set (object.body, "cleared", 0)

def on_second_advance_update (dbms, object):
    validate_salary_advance (dbms, object, is_saving=False)
    DataConversion.safe_set (object.body, "cleared", 0)
    object.doc_status = "Draft"

def on_normal_advance_submit (dbms, object):
    validate_salary_advance (dbms, object, is_saving=False)
    DataConversion.safe_set (object.body, "is_approved", 0)
    core_payroll = Core_Payroll (dbms)
    ad = DataConversion.safe_get (object, "body")
    repayment_period = DataConversion.safe_get (ad, "repayment_period", 1)
    
    # find if less than 30% of basic is take home

    result = core_payroll.notify_payroll (
        employee_number=DataConversion.safe_get (ad, "employee_id"),
        amount=DataConversion.safe_get (ad, "amount"),
        doc_type="Advance_Application",
        doc_name=DataConversion.safe_get (ad, "name"),
        length_or_period=repayment_period,
        effective_date=dates.get_last_date_of_current_month (),
        sc="Salary Advance",
        salary_advance_type="First"
    )
    if result.status != utils.ok:
        throw (f"{result.error_message}")

    DataConversion.safe_set(object.body, "disbursed_on", dates.today ()) 
    DataConversion.safe_set(object.body, "due_date", dates.add_days (dates.today (), 30 * repayment_period) ) 

def on_second_advance_submit (dbms, object):
    validate_salary_advance (dbms, object, is_saving=False)
    DataConversion.safe_set (object.body, "is_approved", 0)
    core_payroll = Core_Payroll (dbms)
    ad = DataConversion.safe_get (object, "body")
    repayment_period = DataConversion.safe_get (ad, "repayment_period", 1)
    
    # find if less than 30% of basic is take home

    result = core_payroll.notify_payroll (
        employee_number=DataConversion.safe_get (ad, "employee_id"),
        amount=DataConversion.safe_get (ad, "amount"),
        doc_type="Second_Salary_Advance_Application",
        doc_name=DataConversion.safe_get (ad, "name"),
        length_or_period=repayment_period,
        effective_date=dates.get_last_date_of_current_month (),
        sc="Salary Advance",
        salary_advance_type="Second"
    )
    if result.status != utils.ok:
        throw (f"{result.error_message}")

    DataConversion.safe_set(object.body, "disbursed_on", dates.today ()) 
    DataConversion.safe_set(object.body, "due_date", dates.add_days (dates.today (), 30 * repayment_period) ) 

def on_advance_memo_save (dbms, object):
    core_payroll = Core_Payroll (dbms)
    validate_salary_advance (dbms, object, is_memo=True)
    emp = core_payroll.get_doc ("Employee", DataConversion.safe_get (object.body, "employee_id"))
    DataConversion.safe_set (object.body, "employee_grade", DataConversion.safe_get (emp, "employee_grade"))
    entries = core_payroll.get_list ("Advance_Application", filters={"is_paid": 0, "is_approved": 1}, order_by=['id'])
    if DataConversion.safe_lt (len(entries), 0, int):
        throw ("Can Save Second Advance Memo you don't have <strong class='text-rose-500'>Any Salary Advance</strong>")

def on_advance_memo_update (dbms, object):
    validate_salary_advance (dbms, object, is_memo=True)

def on_advance_memo_submit (dbms, object):
    core_hr = Core_Hr (dbms)
    validate_salary_advance (dbms, object, is_memo=True)
    memo = DataConversion.safe_get (object, "body")
    emp = core_hr.get_doc ("Employee", DataConversion.safe_get (memo, "employee_id"))
    ssa = utils.from_dict_to_object ()
    DataConversion.safe_set (ssa, 'employee_id', DataConversion.safe_get (memo, "employee_id"))
    DataConversion.safe_set (ssa, 'full_name', DataConversion.safe_get (memo, "full_name")) 
    DataConversion.safe_set (ssa, 'department', DataConversion.safe_get (memo, "department")) 
    DataConversion.safe_set (ssa, 'designation', DataConversion.safe_get (memo, "designation")) 
    DataConversion.safe_set (ssa, 'employment_type', DataConversion.safe_get (memo, "employment_type")) 
    DataConversion.safe_set (ssa, 'emp_status', DataConversion.safe_get (memo, "emp_status"))
    DataConversion.safe_set (ssa, 'basic_pay', DataConversion.safe_get (memo, "basic_pay")) 
    DataConversion.safe_set (ssa, 'amount_in_words', DataConversion.safe_get (memo, "amount_in_words"))
    DataConversion.safe_set (ssa, 'section', DataConversion.safe_get (memo, "section"))
    DataConversion.safe_set (ssa, 'status', "Draft")
    DataConversion.safe_set (ssa, 'is_paid', 0)
    DataConversion.safe_set (ssa, 'show_totals', "Show")
    DataConversion.safe_set (ssa, 'amount', DataConversion.safe_get (memo, "amount"))
    DataConversion.safe_set (ssa, 'advance_type', DataConversion.safe_get (memo, "advance_type", "Second Advance"))
    DataConversion.safe_set (ssa, 'purpose', DataConversion.safe_get (memo, "purpose"))
    DataConversion.safe_set (ssa, 'repayment_period', DataConversion.safe_get (memo, "repayment_period"))
    DataConversion.safe_set (ssa, 'employee_grade', DataConversion.safe_get (memo, "employee_grade", DataConversion.safe_get (emp, "employee_grade")))
    DataConversion.safe_set (ssa, "cleared", 0)
    DataConversion.safe_set (ssa, "second_advance_memo", DataConversion.safe_get (memo, "name"))
    pp (ssa, "=================SSA DATA===================")
    r = dbms.create ("Second_Salary_Advance_Application", ssa)
    pp (r)
    if r.status != utils.ok:
        throw (f"{r.error_message}")
    
def on_house_loan_save (dbms, object):
    core_hr = Core_Hr (dbms)
    house_loan_validations (dbms, object)
    DataConversion.safe_set (object.body, "has_witnesses", 0)
    DataConversion.safe_set (object.body, "cleared", 0)
    hla = DataConversion.safe_get (object, "body")
    emp = DataConversion.safe_get (hla, "emp", {})
    if not emp:
        emp = core_hr.get_doc ("Employee", DataConversion.safe_get (hla, "employee"))

    n_hla = utils.from_dict_to_object ()
    DataConversion.safe_set (n_hla, "name", f"HLA-{DataConversion.safe_get (hla, 'name')}")
    DataConversion.safe_set (n_hla, "application", DataConversion.safe_get (hla, 'name'))
    DataConversion.safe_set (n_hla, "ref_doc", "House_Loan_Application")
    DataConversion.safe_set (n_hla, "applicant_witness", DataConversion.safe_get (hla, "applicant_witness"))
    DataConversion.safe_set (n_hla, "date_of_agreement", DataConversion.safe_get (hla, "date_of_engagement"))
    DataConversion.safe_set (n_hla, "borrower", DataConversion.safe_get (hla, "employee"))
    DataConversion.safe_set (n_hla, "borrowers_name", DataConversion.safe_get (hla, "full_name"))
    DataConversion.safe_set (n_hla, "advance_amount", DataConversion.safe_get (hla, "requested_amount"))
    DataConversion.safe_set (n_hla, "advance_amount_in_words", DataConversion.safe_get (hla, "requested_amount_words"))
    DataConversion.safe_set (n_hla, "status", "Pending Witness")

    r = dbms.create ("House_Loan_Agreement", n_hla)
    pp (r, "=))))))))))))========================PPPPPPPPP")
    if r.status == utils.ok:
        r = core_hr.send_mail_to_witnesses (
            doctype="House Loan Agreement",
            doc_name=DataConversion.safe_get (n_hla, "name"),
            applicant=emp,
            witness=DataConversion.safe_get (n_hla, "applicant_witness")
        )
        pp (r, "=========================PPPPPPPPP")
        if r:
            DataConversion.safe_set (object.body, "has_witnesses", 1)
    DataConversion.safe_set (object.body, "agreement", DataConversion.safe_get (n_hla, "name"))
    DataConversion.safe_set (object.body, "ref_doc", "House_Loan_Agreement")
    DataConversion.safe_set (object.body, "house_agreement", DataConversion.safe_get (n_hla, "name"))
    req_amt = DataConversion.convert_to_float (DataConversion.safe_get (hla, "requested_amount"))
    interest_amt = (req_amt/100)*5
    DataConversion.safe_set (object.body, "interest_amount", interest_amt)
    DataConversion.safe_set (object.body, "has_witnesses", 1)

def on_house_loan_submit (dbms, object):
    house_loan_validations (dbms, object)
    core_payroll = Core_Payroll (dbms)
    app = DataConversion.safe_get (object, "body")
    
    service_condition_type = DataConversion.safe_get (app, "service_condition_type")
    approved_amount = DataConversion.convert_to_float (DataConversion.safe_get (app, "approved_amount"))
    requested_amount = DataConversion.convert_to_float (DataConversion.safe_get (app, "requested_amount"))
    repayment_period = DataConversion.convert_to_int (DataConversion.safe_get (app, "repayment_period"))
    retirement_date = DataConversion.safe_get (app, "retirement_date")
    contract_expiration_date =  DataConversion.safe_get (app, "retirement_date") if  DataConversion.safe_get (app, "retirement_date") else DataConversion.safe_get (app, "contract_expiration_date")
    
    if not DataConversion.safe_get (app, "basic_pay"):
        throw ("Applicants Basic Pay  is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "is_amount_within_entitlement"):
        throw ("Is the applied for within entitlement is <strong class='text-rose-600'>required</strong>.")
    if not DataConversion.safe_get (app, "is_amount_within_entitlement"):
        DataConversion.safe_set (object.body, "submitted_date", dates.today ())
    if not repayment_period:
        throw ("Repayment Period is <strong class='text-rose-600'>required</strong>.")
    if not requested_amount:
        throw ("Requested amount  is <strong class='text-rose-600'>required</strong>.")
    if not approved_amount:
        throw ("Approved amount  is <strong class='text-rose-600'>required</strong>.")
    if not app.has_witnesses:
        throw(f"The document does not have a confirmed witness")

    if service_condition_type in ["Secondment", "Permanent and Pensionable"]:
        pass
    elif DataConversion.safe_e (service_condition_type, "Fixed Term", str, True):
        pass

    years = 0
    months = 0
    period_to_retirement = DataConversion.date_diff (dates.today (), contract_expiration_date, unit="months")
    
    if period_to_retirement > 12:
        years_months = period_to_retirement/12
        months = period_to_retirement % 12
        years = years_months - months

    to_retirement = f"{years} year(s) {months} month(s)" if years > 0 else f"{period_to_retirement} month(s)" 
    pp (to_retirement, "=================to_retirement===================")
    DataConversion.safe_set (object.body, "years_in_service_remaining", to_retirement)
    
    # throw ("HOUSE LOAN SUBMIT DISABLED FOR TESTING PURPOSES")
    try:
        req_amt = DataConversion.convert_to_float (DataConversion.safe_get (app, "requested_amount"))
        interest_amount = DataConversion.convert_to_float (DataConversion.safe_get (app, "interest_amount"))
        result_a = core_payroll.notify_payroll (
            employee_number=DataConversion.safe_get (app, "employee"),
            amount=req_amt,
            doc_type="House_Loan_Application",
            doc_name=DataConversion.safe_get (app, "name"),
            length_or_period=DataConversion.safe_get (app, "repayment_period"),
            effective_date=dates.get_last_date_of_current_month (),
            sc="House Loan"
        )
        result = core_payroll.notify_payroll (
            employee_number=DataConversion.safe_get (app, "employee"),
            amount=interest_amount,
            doc_type="House_Loan_Application",
            doc_name=DataConversion.safe_get (app, "name"),
            length_or_period=DataConversion.safe_get (app, "repayment_period"),
            effective_date=dates.get_last_date_of_current_month (),
            sc="Interest On House Loan"
        )
        DataConversion.safe_set (object.body, "is_approved", 1)
    except Exception as e:
        throw(f"An error occurred while adding info to payroll: {e}")

def long_term_sponsorship (dbms, object):
    long_term_sponsorship_validations (dbms, object)
    core_hr = Core_Hr (dbms)
    core_payroll = Core_Payroll (dbms)
    lts = DataConversion.safe_get (object, "body")
    DataConversion.safe_set (object.body, "has_witnesses", 0)
    DataConversion.safe_set (object.body, "cleared", 0)
    boarding_and_lodging = DataConversion.convert_to_float (DataConversion.safe_get (lts, "boarding_and_lodging", 0))
    travel_costs = DataConversion.convert_to_float (DataConversion.safe_get (lts, "travel_costs", 0))
    lunch_allowance = DataConversion.convert_to_float (DataConversion.safe_get (lts, "lunch_allowance", 0))
    books_allowance = DataConversion.convert_to_float (DataConversion.safe_get (lts, "books_allowance", 0))
    tuition_fees = DataConversion.convert_to_float (DataConversion.safe_get (lts, "tuition_fees", 0))
    others = DataConversion.convert_to_float (DataConversion.safe_get (lts, "others", 0))
    
    DataConversion.safe_set (object.body, "usage", [
        {
            "boarding_and_lodging" : boarding_and_lodging,
            "travel_costs" : travel_costs,
            "lunch_allowance" : lunch_allowance,
            "books_allowance" : books_allowance,
            "tuition_fees" : tuition_fees,
            "others": others,
        }
    ])

    amount = sum([
        boarding_and_lodging,
        travel_costs,
        lunch_allowance,
        books_allowance,
        tuition_fees
    ])

    DataConversion.safe_set (object.body, "amount", amount)
    lts_bp = utils.from_dict_to_object ()
    emp = DataConversion.safe_get (lts, "emp", {})
    if not emp:
        emp = core_payroll.get_doc ("Employee", DataConversion.safe_get (lts, "employee"))

    DataConversion.safe_set (lts_bp, "name", f"BPA-{DataConversion.safe_get (lts, 'name')}")
    DataConversion.safe_set (lts_bp, "application", DataConversion.safe_get (lts, 'name'))
    DataConversion.safe_set (object.body, "ref_doc", "Long_Term_Sponsorship")
    DataConversion.safe_set (lts_bp, "agreement_date", dates.today ())
    DataConversion.safe_set (lts_bp, "employee", DataConversion.safe_get (emp, "name"))
    DataConversion.safe_set (lts_bp, "applicant_names", DataConversion.safe_get (emp, "full_name"))
    DataConversion.safe_set (lts_bp, "nrc", DataConversion.safe_get (emp, "id_no"))
    DataConversion.safe_set (lts_bp, "program", DataConversion.safe_get (lts, "course_of_study"))
    DataConversion.safe_set (lts_bp, "qualification", DataConversion.safe_get (lts, "qualification_to_be_obtained"))
    DataConversion.safe_set (lts_bp, "start_date", DataConversion.safe_get (lts, "start_date"))
    DataConversion.safe_set (lts_bp, "end_date", DataConversion.safe_get (lts, "end_date"))
    DataConversion.safe_set (lts_bp, "wittiness_staff", DataConversion.safe_get (lts, "wittiness_staff"))
    DataConversion.safe_set (lts_bp, "status", "Pending Witness")

    r = dbms.create ("Long_Term_Sponsorship_Bonding_Period", lts_bp)
    if r.status == utils.ok:
        nw = core_hr.send_mail_to_witnesses (
            doctype="Long Term Sponsorship Bonding Period",
            doc_name=DataConversion.safe_get (lts_bp, "name"),
            applicant=emp,
            witness=DataConversion.safe_get (lts_bp, "wittiness_staff")
        )
    DataConversion.safe_set (object.body, "ref_doc", "Long_Term_Sponsorship_Bonding_Period")
    DataConversion.safe_set (object.body, "agreement", DataConversion.safe_get (lts_bp, "name"))
    DataConversion.safe_set (object.body, "bounding_period", DataConversion.safe_get (lts_bp, "name"))

def long_term_sponsorship_update (dbms, object):
    long_term_sponsorship_validations (dbms, object)

def long_term_sponsorship_submit (dbms, object):
    long_term_sponsorship_validations (dbms, object)
    lts = DataConversion.safe_get (object, "body")
    
    # if not lts.has_witnesses:
    #     throw(f"The document does not have a confirmed witness")

    DataConversion.safe_set (object.body, "is_approved", 1)

def long_term_sponsorship_req_fund (dbms, object):
    object.doc_status = "Draft"

def long_term_sponsorship_req_fund_submit (dbms, object):
    core_payroll = Core_Payroll (dbms)
    doc = core_payroll.get_doc ("Long_Term_Sponsorship", object.body.reference)
    if not doc:
        throw (f"Long Term Sponsorship with Reference {object.body.reference} was not <strong class='text-rose-600'>Found</strong>.")
    curr = DataConversion.safe_get (doc, "usage", [])

    additional = {}
    travel_costs = DataConversion.convert_to_float (DataConversion.safe_get (object.body, "travel_costs"))
    boarding_and_lodging = DataConversion.convert_to_float (DataConversion.safe_get (object.body, "boarding_and_lodging"))
    lunch_allowance = DataConversion.convert_to_float (DataConversion.safe_get (object.body, "lunch_allowance"))
    books_allowance = DataConversion.convert_to_float (DataConversion.safe_get (object.body, "books_allowance"))
    tuition_fees = DataConversion.convert_to_float (DataConversion.safe_get (object.body, "tuition_fees"))
    others = DataConversion.convert_to_float (DataConversion.safe_get (object.body, "others"))
    
    travel_costs_old = DataConversion.convert_to_float (DataConversion.safe_get (doc, "travel_costs", 0))
    boarding_and_lodging_old = DataConversion.convert_to_float (DataConversion.safe_get (doc, "boarding_and_lodging", 0))
    lunch_allowance_old = DataConversion.convert_to_float (DataConversion.safe_get (doc, "lunch_allowance", 0))
    books_allowance_old = DataConversion.convert_to_float (DataConversion.safe_get (doc, "books_allowance", 0))
    tuition_fees_old = DataConversion.convert_to_float (DataConversion.safe_get (doc, "tuition_fees", 0))
    others_old = DataConversion.convert_to_float (DataConversion.safe_get (doc, "others", 0))

    DataConversion.safe_set (doc, "travel_costs", sum([travel_costs, travel_costs_old]))
    DataConversion.safe_set (doc, "boarding_and_lodging", sum([boarding_and_lodging, boarding_and_lodging_old]))
    DataConversion.safe_set (doc, "lunch_allowance", sum([lunch_allowance, lunch_allowance_old]))
    DataConversion.safe_set (doc, "books_allowance", sum([books_allowance, books_allowance_old]))
    DataConversion.safe_set (doc, "tuition_fees", sum([tuition_fees, tuition_fees_old]))
    DataConversion.safe_set (doc, "others", sum([others, others_old]))

    DataConversion.safe_set (additional, "travel_costs", travel_costs)
    DataConversion.safe_set (additional, "boarding_and_lodging", boarding_and_lodging)
    DataConversion.safe_set (additional, "lunch_allowance", lunch_allowance)
    DataConversion.safe_set (additional, "books_allowance", books_allowance)
    DataConversion.safe_set (additional, "tuition_fees", tuition_fees)
    DataConversion.safe_set (additional, "others", others)

    DataConversion.safe_list_append (curr, additional)

    DataConversion.safe_set (doc, "usage", curr)
    
    object.body.is_approved = 1

    u = dbms.update ("Long_Term_Sponsorship", doc, update_submitted=True)
    pp (u)

def before_personal_loan_save(dbms, object):
    body =object.body
    witness = DataConversion.safe_get (body, "applicant_witness")
    emp_id = DataConversion.safe_get (body, "employee_no")
    DataConversion.safe_set (object.body, "total_amount_repaid", 0)

    if not body.date_of_application:
        throw(f"Date of Application is required")
    if not emp_id:
        throw(f"Employee No is required")
    if not body.current_basic:
        throw(f"Current Annum basic pay is required, provide it by picking an employee")
    if not body.job_title:
        throw(f"Job Title is required, provide it by picking an employee")
    if not witness:
        throw(f"applicant's witness is required, provide it by picking an employee")

    if DataConversion.safe_e (witness, emp_id, str, True):
        throw (f"applicant and witness can not be the same")

    object.body.cleared =0
    core_hr =Core_Hr(dbms, object)
    emp_data =utils.from_dict_to_object({})

    fetch_emp_data =dbms.get_doc("Employee", body.employee_no)
    if fetch_emp_data.status ==utils.ok:
        emp_data =DataConversion.safe_get (fetch_emp_data, "data") 
    else:
        throw(f"Failed to fetch employee {object.body.employee_no} data: {e}")

    personal_agreement =utils.from_dict_to_object({
        "name": f"PLA-{object.body.name}",
        "employee_full_name" : object.body.employee_full_name,
        "approved_loan": object.body.requested_loan_amount,
        "date_of_agreement": None,
        "ref_doc": "Personal_Loan_Agreement",
        "employee_no": object.body.employee_no, 
        "job_title": object.body.job_title, 
        "application": object.body.name,
        "department": object.body.department,
        "council_witness": object.body.council_witness,
        "applicant_witness": object.body.applicant_witness,
        "status": "Pending Witness"
    })

    DataConversion.safe_set (object.body, "agreement", f"PLA-{object.body.name}")
    DataConversion.safe_set (object.body, "ref_doc", "Personal_Loan_Agreement")

    DataConversion.safe_set (object.body, "personal_agreement", DataConversion.safe_get (personal_agreement, "name"))

    req_amt = DataConversion.convert_to_float (DataConversion.safe_get (body, "requested_loan_amount"))
    interest_amt = (req_amt/100)*5
    DataConversion.safe_set (object.body, "interest_amount", interest_amt)

    try:
        create_pla =dbms.create("Personal_Loan_Agreement", personal_agreement)
        if create_pla.status ==utils.ok:
            send_for_witness_approval =core_hr.send_mail_to_witnesses(
                doctype= object.model.replace("_", " "),
                doc_name =create_pla.data.name, 
                applicant =emp_data, 
                witness =DataConversion.safe_get (body, "applicant_witness")
            )
            
            if send_for_witness_approval:
                object.body.has_witnesses = 1
            else:
                throw(f"No witness was found to send the email to. Confirm both the council and applicant's witnesses.")
            object.body.agreement =create_pla.data.name
            object.doc_status ="Draft"

    except Exception as e:
        throw(f"An error occurred while generating the a personal loan agreement. Error =>{e}")
    
def before_personal_loan_submit(dbms, object):
    core_payroll =Core_Payroll(dbms, object)
    body =object.body

    if not body.date_of_application:
        throw(f"Date of Application is required")
    if not body.employee_no:
        throw(f"Employee No is required")
    if not body.current_basic:
        throw(f"Current Annum basic pay is required, provide it by picking an employee")
    if not body.job_title:
        throw(f"Job Title is required, provide it by picking an employee")
    if not body.applicant_witness:
        throw(f"applicant's witness is required, provide it by picking an employee")

    if not body.has_witnesses:
        throw(f"The document does not have a confirmed witness")

    # find if less than 30% of basic is take home 

    try:
        interest_amt = DataConversion.convert_to_float(DataConversion.safe_get (body, "interest_amount", 0))
        req_amt = DataConversion.convert_to_float (DataConversion.safe_get (body, "requested_loan_amount"))
        result_a = core_payroll.notify_payroll (
            employee_number=DataConversion.safe_get (body, "employee_no"),
            amount= req_amt,
            doc_type=DataConversion.safe_get (body, "doctype"),
            doc_name=DataConversion.safe_get (body, "name"),
            length_or_period=DataConversion.safe_get (body, "requested_repayment_period"),
            effective_date=dates.get_last_date_of_current_month (),
            sc="Personal Loan"
        )
        result = core_payroll.notify_payroll (
            employee_number=DataConversion.safe_get (body, "employee_no"),
            amount= interest_amt,
            doc_type=DataConversion.safe_get (body, "doctype"),
            doc_name=DataConversion.safe_get (body, "name"),
            length_or_period=DataConversion.safe_get (body, "requested_repayment_period"),
            effective_date=dates.get_last_date_of_current_month (),
            sc="Interest On Personal Loan"
        )

        DataConversion.safe_set (object.body, "is_approved", 1)

        pp (result, result_a)

    except Exception as e:
        throw(f"An error occurred while adding info to payroll: {e}")
    
def before_repayment_save(dbms, object):
    core_payroll = Core_Payroll(dbms, object)
    repayment = DataConversion.safe_get (object, "body")
    model = DataConversion.safe_get (repayment, "repayment_model")
    doc = DataConversion.safe_get (repayment, "repayment_reference")
    model_keys = {
        "Personal_Loan_Application": "employee_no",
        "House_Loan_Application": "employee",
        "Second_Salary_Advance_Application": "employee_id",
        "Advance_Application": "employee_id",
        "Professional_Membership_Subscription": "employee",
        "Long_Term_Sponsorship": "employee",
        "Medical_Recovery": "employee",
        "Tuition_Advance_For_Salary_Form": "employee",
    }
    if not DataConversion.safe_get (repayment, "repayment_type"):
        throw(f"Please provide the type of loan you are repaying for in the 'Repayment Type' field") 
    if not DataConversion.safe_get (repayment, "repayment_model"):
        if DataConversion.safe_get (repayment, "repayment_type") == "Medical Recovery":
            DataConversion.safe_set (repayment, "repayment_model", "Recovery_Of_Medical_Bills")
        else:
            repayment_type = str (DataConversion.safe_get (repayment, "repayment_type")).replace(" ", "_")
            DataConversion.safe_set (object.body, "repayment_model", repayment_type)

    if not DataConversion.safe_get (repayment, "repayment_reference"):
        throw(f"The 'Repayment Reference' field is empty. please provide the document you are repaying for in the previous field.")
    if not DataConversion.safe_get (repayment, "repayment"):
        throw(f"Please provide the amount you are repaying in the 'Repayment' field") 
    
    employee = DataConversion.safe_get (repayment, "repayer")
    if not employee:
        repayment_for = core_payroll.get_doc (model, doc)
        if not repayment_for:
            throw (f"Document For {model} with name/ID {doc} was not found")
        key = DataConversion.safe_get (model_keys, model)
        employee = DataConversion.safe_get (repayment_for, key)

    if not DataConversion.safe_get (repayment, "attachment"):
        throw (f"Receipt is missing")
    
    DataConversion.safe_set (object.body, "repayer", employee)

def before_repayment_submit(dbms, object):
    core_payroll = Core_Payroll(dbms, object)
    repayment = DataConversion.safe_get (object, "body")
    # pp (repayment)
    model = DataConversion.safe_get (repayment, "reference_model")
    doc = DataConversion.safe_get (repayment, "repayment_reference")
    model_keys = {
        "Personal_Loan_Application": "employee_no",
        "House_Loan_Application": "employee",
        "Second_Salary_Advance_Application": "employee_id",
        "Advance_Application": "employee_id",
        "Professional_Membership_Subscription": "employee",
        "Long_Term_Sponsorship": "employee",
        "Medical_Recovery": "employee",
        "Tuition_Advance_For_Salary_Form": "employee",
    }

    employee = DataConversion.safe_get (repayment, "repayer")
    if not employee:
        repayment_for = core_payroll.get_doc (model, doc)
        if not repayment_for:
            throw (f"Document For {model} with name/ID {doc} was not found")
        key = DataConversion.safe_get (model_keys, model)
        employee = DataConversion.safe_get (repayment_for, key)
    repayment_amount = DataConversion.safe_get (repayment, "repayment")
    if not DataConversion.safe_get (repayment, "attachment"):
        throw (f"Receipt is missing")
    if not employee:
        throw (f"Repayer is missing")
    if not repayment_amount:
        throw (f"Repayment amount is missing")
    fetch_doc = core_payroll.get_doc (model, doc)

    if not fetch_doc:
        throw (f"the Document {doc} was not found for {str (model).replace ("_", " ")}")
    repayment_data = core_payroll.repay_loan_and_other_deduction (repayment_method="Cash", repayment_amount=repayment_amount, ref=model, doc=doc, emp=employee)    

    if repayment_data.status != utils.ok:
        throw (f"{repayment_data.error_message}")
    
    repayment_amount = DataConversion.convert_to_float (DataConversion.safe_get (repayment, "repayment"))
    due_amount = DataConversion.convert_to_float(DataConversion.safe_get (repayment, "due_amount"))

    DataConversion.safe_set (object.body, "repayer", employee)
    DataConversion.safe_set (object.body, "repaid_amount", due_amount-repayment_amount)

    if DataConversion.convert_to_int (DataConversion.safe_get (fetch_doc, "cleared", 0)) == 0:
        due_amount = DataConversion.convert_to_float (DataConversion.safe_get (fetch_doc, "total_amount_repaid", 0))
        repayment_amount = DataConversion.convert_to_float (DataConversion.safe_get (repayment, "repayment", 0))
        DataConversion.safe_set (fetch_doc, "total_amount_repaid", sum ([due_amount, repayment_amount]))
        DataConversion.safe_set (fetch_doc, "due_amount", sum ([due_amount, repayment_amount]))
        if due_amount - repayment_amount == 0:
            DataConversion.safe_set (fetch_doc, "status", "Paid")
            DataConversion.safe_set (fetch_doc, "cleared", 1)
            DataConversion.safe_set (object, "docstatus", "Paid")
            DataConversion.safe_set (object.body, "status", "Paid")
            DataConversion.safe_set (object, "docstatus", "Paid")
        else:
            DataConversion.safe_set (fetch_doc, "status", "Partially Paid")
            DataConversion.safe_set (object.body, "status", "Partially Paid")
            DataConversion.safe_set (object, "docstatus", "Partially Paid")

        loan_update =dbms.update(model, fetch_doc, update_submitted=True)
        if loan_update.status != utils.ok:
            throw(f"An error occurred while updating the {model.replace("_", " ")} {doc}: {loan_update.error_message}")
        cr =dbms.update("Cash_Repayment", object.body, update_submitted=True)

def on_tuition_advance_save (dbms, object):
    validate_tuition_advance (dbms, object)

def on_tuition_advance_submit (dbms, object):
    validate_tuition_advance (dbms, object)
    core_payroll =Core_Payroll(dbms, object)
    body = DataConversion.safe_get (object, "body")
    
    # find if less than 30% of basic is take home

    try:
        result = core_payroll.notify_payroll (
            employee_number=DataConversion.safe_get (body, "employee"),
            amount=DataConversion.safe_get (body, "maximum_loan_amount_requested"),
            doc_type="Tuition_Advance_For_Salary_Form",
            doc_name=DataConversion.safe_get (body, "name"),
            length_or_period=DataConversion.safe_get (body, "repayment_period"),
            effective_date=dates.get_last_date_of_current_month (),
            sc="Tuition Advance"
        )
    except Exception as e:
        throw(f"An error occurred while adding info to payroll: {e}")
    
def on_emp_welfare_save (dbms, object):
    validate_welfare (dbms, object)

def on_emp_welfare_submit (dbms, object):
    validate_welfare (dbms, object)
    core_payroll =Core_Payroll(dbms, object)
    body = DataConversion.safe_get (object, "body")
    try:
        result = core_payroll.notify_payroll (
            employee_number=DataConversion.safe_get (body, "employee"),
            amount=DataConversion.safe_get (body, "staff_covered_expense"),
            doc_type="Recovery_Of_Medical_Bills",
            doc_name=DataConversion.safe_get (body, "name"),
            length_or_period=DataConversion.safe_get (body, "payment_length"),
            effective_date=dates.get_last_date_of_current_month (),
            sc="50% Medical Recovery"
        )
        pp(result)
    except Exception as e:
        throw(f"An error occurred while adding info to payroll: {e}")

def professional_membership_before_save(dbms, object):

    if not object.body.name:
        throw(f"The name field is required!")
    if not object.body.employee:
        throw(f"The employee field is required!")
    if not object.body.nrc:
        throw(f"The nrc field is required!")
    if not object.body.submittion_date:
        throw(f"The submission date field is required!")
    if not object.body.designation:
        throw(f"The designation field is required!")
    if not object.body.original_attachment:
        throw(f"The Invoice attachment field is required!")
    if not object.body.membership_type:
        throw(f"The membership type field is required!")
    if not object.body.name_of_professional_body:
        throw(f"The name of professional field is required!")
    if not object.body.invoice_number:
        throw(f"The invoice number field is required!")
    if not object.body.requested_amount:
        throw(f"The requested amount is required")
    if not object.body.desclaimer:
        throw(f"The please ensure that you check the consent field")
    if not object.body.instalments_period:
        throw(f"The instalment period field is required")

    object.body.cleared =0
    DataConversion.safe_set (object.body, "total_amount_repaid", 0)

def professional_membership_before_submit(dbms, object):
    professional_membership_before_save (dbms, object)
    core_payroll =Core_Payroll(dbms, object)
    body =object.body
    try:
        result = core_payroll.notify_payroll (
            employee_number=DataConversion.safe_get (body, "employee"),
            amount=DataConversion.safe_get (body, "requested_amount"),
            doc_type=DataConversion.safe_get (body, "doctype"),
            doc_name=DataConversion.safe_get (body, "name"),
            length_or_period=DataConversion.safe_get (body, "instalments_period"),
            effective_date=dates.get_last_date_of_current_month (),
            sc="Professional Membership Subscription"
        )
    except Exception as e:
        throw(f"An error occurred while adding info to payroll: {e}")