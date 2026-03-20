from itertools import zip_longest
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.payroll import Core_Payroll
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll.Payroll_calc import EarningCalculator

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def fetch_employee_data(dbms, emp: str="", fields: list=[]):
    if emp:
        fetch_emp =dbms.get_doc("Employee", emp)
        if fetch_emp.status !=utils.ok:
            return
        # if not fields:
        return fetch_emp.data
        

def validate_acting_memo(body):
    if not DataConversion.safe_get(body, "position_owner"):
        throw("""The field 'position owner', was not provided.""") 
    if not DataConversion.safe_get(body, "acting_officer"):
        throw("""The field 'acting officer', was not provided.""") 
    if not DataConversion.safe_get(body, "start_date"):
        throw("""The field 'start date', was not provided.""") 
    if not DataConversion.safe_get(body, "end_date"):
        throw("""The field 'end date', was not provided.""") 
    if not DataConversion.safe_get(body, "acting_period"):
        throw("""The field 'acting period', was not provided.""") 
    if not DataConversion.safe_get(body, "reason"):
        throw("""The field 'reason', was not provided.""") 
    if not DataConversion.safe_get(body, "acting_officer_name"):
        throw("""The field 'acting officer name', was not provided.""")
    if not DataConversion.safe_get(body, "position_owner_name"):
        throw("""The field 'position owner name', was not provided.""")
    if not DataConversion.safe_get(body, "salary_grade"):
        throw("""The field 'salary grade', was not provided.""") 
    if not DataConversion.safe_get(body, "job_title"):
        throw("""The field 'job title', was not provided.""") 

def validate_acting_appointment(dbms, body):
    emp_owner =None
    emp_acting =None
    if body:
        if not DataConversion.safe_get(body, "position_owner", ""):
            throw(""" The field 'position owner', was not provided for. """)
        else:
            fetch_emp =dbms.get_doc("Employee", DataConversion.safe_get(body, "position_owner"))
            if fetch_emp.status ==utils.ok:
                emp_owner =fetch_emp.data
            else:
                throw(f""" No employee was retrived by by the ID {DataConversion.safe_get(body, "position_owner", "")}, for the position holding officer  """)
        if not DataConversion.safe_get(body, "acting_officer", ""):
            throw(""" The field 'acting officer', was not provided for. """)
        else:
            fetch_emp =dbms.get_doc("Employee", DataConversion.safe_get(body, "acting_officer"))
            if fetch_emp.status ==utils.ok:
                emp_acting =fetch_emp.data
            else:
                throw(f""" No employee was retrived by by the ID {DataConversion.safe_get(body, "acting_officer", "")}, for the acting officer """)
        if not DataConversion.safe_get(body, "start_date", ""):
            throw(""" The field 'start date', was not provided for. """)
        if not DataConversion.safe_get(body, "end_date", ""):
            throw(""" The field 'end date', was not provided for. """)

        if not DataConversion.safe_get(body, "acting_period", ""):
            throw(""" The field 'acting period', was not provided for. """)
        if not DataConversion.safe_get(body, "holders_location", ""):
            throw(""" The field 'Holder's Location ', was not provided for. """)

        # Owner's Details
        if not DataConversion.safe_get(body, "job_title", ""):
            throw(""" The field 'job title', was not provided for. """)
        if not DataConversion.safe_get(body, "department", ""):
            throw(""" The field 'department', was not provided for. """)
        if not DataConversion.safe_get(body, "salary_grade", ""):
            throw(""" The field 'salary grade', was not provided for. """)
        if not DataConversion.safe_get(body, "salary_components", ""):
            DataConversion.safe_set(body, "salary_components", DataConversion.safe_get(emp_owner, "earnings", []))
        # if not DataConversion.safe_get(body, "reason", ""):
        #     throw(""" The field 'reason', was not provided for. """)
        if not DataConversion.safe_get(body, "owner_name", ""):
            throw(""" The field 'owner name', was not provided for. """)
        if not DataConversion.safe_get(body, "basic_pay", ""):
            throw(""" The field 'basic pay', was not provided for. """)

        # Filler's Details
        if not DataConversion.safe_get(body, "acting_officer_job_title", ""):
            throw(""" The field 'acting officer job title', was not provided for. """)
        if not DataConversion.safe_get(body, "acting_officer_department", ""):
            throw(""" The field 'acting officer department', was not provided for. """)
        if not DataConversion.safe_get(body, "acting_officer_salary_grade", ""):
            throw(""" The field 'acting officer salary grade', was not provided for. """)
        if not DataConversion.safe_get(body, "acting_officer_salary_components", ""):
            DataConversion.safe_set(body, "acting_officer_salary_components", DataConversion.safe_get(emp_acting, "earnings", []))
        if not DataConversion.safe_get(body, "acting_officer_name", ""):
            throw(""" The field 'acting officer name', was not provided for. """)
        if not DataConversion.safe_get(body, "acting_officer_basic_pay", ""):
            throw(""" The field 'acting officer basic pay', was not provided for. """)

    return body

def validate_acting_appointment_settings(body):
    if body:
        if not body.position_holder_in_country:
            throw(""" The field <strong class="text-red font-bold text-[2rem]">'name'</strong>, was not provided """) 
        if not body.position_holder_outside_country:
            throw(""" The field <strong class="text-red font-bold text-[2rem]">'maturity period'</strong>, was not provided """) 
        if not body.grade_exceptions:
            throw(""" The field <strong class="text-red font-bold text-[2rem]">'grade exception'</strong>, was not provided """)

def calculate_pay_for_acting(dbms, body):
    acting_appointment =validate_acting_appointment(dbms, body)
    sys_setting =dbms.system_settings

    # FETCH NEED DOCS
    fetch_appointment_settings =dbms.get_doc("Acting_Appointment_Settings", DataConversion.safe_get(sys_setting, "default_company") or "ECZ")
    if fetch_appointment_settings.status !=utils.ok:
        throw(f""" No acting appointment settings where found. The returned value was {fetch_appointment_settings}. """)
    fetch_component =dbms.get_list("Salary_Component", filters={"component_type": "Earning",})
    if fetch_component.status !=utils.ok:
        throw(f""" Failed to fetch the list of salary components. {fetch_component} """)
    fetch_hr_setting =dbms.get_doc("Hr_Setting", sys_setting.default_company or "ECZ")
    if fetch_hr_setting.status !=utils.ok:
        throw(f""" No HR settings were found in the system. {fetch_hr_setting} """)

    # GET COMPANY WORKS DAYS
    hr_settings =fetch_hr_setting.data
    working_days =int(hr_settings.working_days) or 22

    grouped_salary_components =utils.group(DataConversion.safe_get(DataConversion.safe_get(fetch_component, "data"), "rows"), "name")

    # DAYS OF ACTING
    acting_period =float(DataConversion.safe_get(acting_appointment, "acting_period", 0))

    # BASIC PAYS
    holder_basic_pay =DataConversion.safe_get(acting_appointment, "basic_pay", 0)
    acting_basic_pay =DataConversion.safe_get(acting_appointment, "acting_officer_basic_pay", 0)

    # ACTING APPOINTMENT SETTINGS AND GRADE THAT DO NOT WORK WITH THE DEFAULT CONFIGURATIONS
    aa_setings =DataConversion.safe_get(fetch_appointment_settings, "data", {})
    grade_exceptions= DataConversion.safe_get(aa_setings, "grade_exceptions", None)
    group_grade =utils.group(grade_exceptions, "employee_grade")
    
    # INIT VARIABLES FOR THE CALCULATION
    matured =None # FOR A CHECK IF PAYMENT IS REQUIRED
    maturity_by_location =None # HOLD DEFAULT MATURITY FIELD NAME
    exception_maturity_field =None # HOLD THE APPLICABLE FIELD NAME FOR THE APPLICABLE MATURITY LENGTH
    maturity_period_length =0 # HOLD THE APPLICABLE MATURITY LENGTH 

    # IDENTIFY THE LOCATION TO THE HOLDING OFFICER IS GOING

    if DataConversion.safe_get(acting_appointment, "holders_location", "") =="Outside the Country":
        maturity_by_location ="position_holder_outside_country"
        exception_maturity_field ="out_side_country" 
    else:
        maturity_by_location ="position_holder_in_country" 
        exception_maturity_field ="within_country" 

    # CHECK IF THE HOLDERS GRADE IS THE LIST OF EXCEPTION GRADES
    if grade_exceptions and DataConversion.safe_get(acting_appointment, "salary_grade", None) in list(group_grade.keys()):
        maturity_period_length =float(group_grade[DataConversion.safe_get(acting_appointment, "salary_grade", None)][0][exception_maturity_field])
        if maturity_period_length >0 and acting_period >= maturity_period_length:
            matured =1

    # CHECK IF THE ACTING PERIOD IS GREATOR THAN THE APPLICABLE MATURITY LENGTH IN THE DEFAULT
    elif acting_period >=float(DataConversion.safe_get(aa_setings, maturity_by_location, 0)):
        matured =1

    # GROUPING SALARY COMPONENTS BY VALUE TYPE
    grouped_by_value_type =utils.from_dict_to_object({
        "Fixed Amount": [],
        "Percentage": [],
        "System Value": [],
        "Custom": [],
    })
    for component in DataConversion.safe_get(DataConversion.safe_get(fetch_component, "data"), "rows"):
        grouped_by_value_type[DataConversion.safe_get(component, "value_type", "Custom") or "Custom"].append(component)
    
    direct_calculation_component =utils.group(DataConversion.safe_get(grouped_by_value_type, "Fixed Amount", []) + DataConversion.safe_get(grouped_by_value_type, "Percentage", []), "name")
    holders_unstandardized_components =fetch_employee_data(dbms, DataConversion.safe_get(acting_appointment, "position_owner"))
    # [comp for comp in DataConversion.safe_get(acting_appointment, "acting_officer_salary_components", []) if not comp in direct_calculation_component]
    acting_unstandardized_components =fetch_employee_data(dbms, DataConversion.safe_get(acting_appointment, "acting_officer"))
    # [comp for comp in DataConversion.safe_get(acting_appointment, "acting_officer_salary_components", []) if not comp in direct_calculation_component]
    
    holding_records =[]
    acting_records =[]
    # CALCULATION 
    total_holding_gross =holder_basic_pay
    total_acting_gross =acting_basic_pay

    holding_amt =[{"basic":total_holding_gross}]
    acting_amt =[{"basic":total_acting_gross}]

    if DataConversion.safe_get(acting_appointment, "acting_officer_salary_components", []) and DataConversion.safe_get(acting_appointment, "salary_components", []):     
        for holding, acting in zip_longest(DataConversion.safe_get(acting_appointment, "salary_components", []), DataConversion.safe_get(acting_appointment, "acting_officer_salary_components", []), fillvalue=utils.from_dict_to_object({"earning": ""})):
            total_holding_gross +=EarningCalculator.calc_earning(DataConversion.safe_get(acting_appointment, "position_owner"), holder_basic_pay, direct_calculation_component[DataConversion.safe_get(holding, "earning", "")][0]) if DataConversion.safe_get(holding, "earning", "") and DataConversion.safe_get(holding, "earning", "") in direct_calculation_component else 0.0     
            total_acting_gross +=EarningCalculator.calc_earning(DataConversion.safe_get(acting_appointment, "acting_officer"), acting_basic_pay, direct_calculation_component[DataConversion.safe_get(acting, "earning", "")][0]) if DataConversion.safe_get(acting, "earning", "") and DataConversion.safe_get(acting, "earning", "") in direct_calculation_component else 0.0
          
            holding_amt.append({DataConversion.safe_get(holding, "earning", "") :EarningCalculator.calc_earning(DataConversion.safe_get(acting_appointment, "position_owner"), holder_basic_pay, direct_calculation_component[DataConversion.safe_get(holding, "earning", "")][0]) if DataConversion.safe_get(holding, "earning", "") and DataConversion.safe_get(holding, "earning", "") in direct_calculation_component else 0.0})
            acting_amt.append({DataConversion.safe_get(acting, "earning", "") :EarningCalculator.calc_earning(DataConversion.safe_get(acting_appointment, "acting_officer"), acting_basic_pay, direct_calculation_component[DataConversion.safe_get(acting, "earning", "")][0]) if DataConversion.safe_get(acting, "earning", "") and DataConversion.safe_get(acting, "earning", "") in direct_calculation_component else 0.0})

        for holding, acting in zip_longest(DataConversion.safe_get(holders_unstandardized_components, "unstandardized_components", []), DataConversion.safe_get(acting_unstandardized_components, "unstandardized_components", []), fillvalue=utils.from_dict_to_object({"component_name": "", "component_type":"", "main_value": 0.00, "component_value": 0.00, "component_value_employer": 0.00})):
            total_holding_gross +=DataConversion.safe_get(holding, "component_value", 0.00)
            total_acting_gross +=DataConversion.safe_get(acting, "component_value", 0.00)
            
            holding_amt.append({holding.component_name: DataConversion.safe_get(holding, "component_value", 0.00)})
            acting_amt.append({acting.component_name: DataConversion.safe_get(acting, "component_value", 0.00)})


        # holding_amt.append({"gross": total_holding_gross})
        # acting_amt.append({"gross": total_acting_gross})


        daily_pay =(total_holding_gross -total_acting_gross) /working_days if (total_holding_gross -total_acting_gross) >0 else 0.0
        acting_pay =daily_pay *acting_period

        # pp("holding_amt =>", holding_amt, "acting_amt =>",acting_amt, acting_pay)
        # pp({"difference": total_holding_gross - total_acting_gross})
    
    return utils.from_dict_to_object({
        "holders_gross": total_holding_gross,
        "actors_gross": total_acting_gross,
        "daily_pay": daily_pay,
        "acting_payment": acting_pay,
        "payable": "Yes" if matured ==1 else "No"
    })
        


def fetch_doc_data(dbms, model, doc):
    if model and doc:
        fetch_doc =dbms.get_doc(model, doc)
        if fetch_doc.status ==utils.ok:
            return fetch_doc.data
    return None

def before_acting_appointment_settings_save(dbms, object):
    pass


def before_acting_appointment_memo_save(dbms, object):
    validate_acting_memo(object.body)

def calc_earings (dbms, emp, earnings, basic, emp_role, paye):
    components = []
    core_hr = Core_Hr (dbms)
    unstandardized_components_dict = {}
    emp_data = core_hr.get_doc ("Employee", DataConversion.safe_get (emp, "name"))

    if not emp_data:
        throw (f"{emp_role} No Found in the system")

    unstandardized_components = DataConversion.safe_get (emp_data, "unstandardized_components")
    if not unstandardized_components:
        unstandardized_components = []
    unstandardized_components_dict = utils.array_to_dict (unstandardized_components, "component_name")

    gross = DataConversion.convert_to_float (basic)
    for earning in earnings:
        component = DataConversion.safe_get (earning.linked_fields, "component", {})
        if not DataConversion.safe_e (DataConversion.safe_get (component, "component_type"), "Earning", str, True):
            continue
        if DataConversion.safe_get (component, "value_type") in ["Percentage", "Fixed Amount"]:
            if DataConversion.safe_e (DataConversion.safe_get (component, "unstandardized", 0), 1, int):
                component_data = DataConversion.safe_get (unstandardized_components_dict, DataConversion.safe_get (component, "name"))
                if not component_data:
                    throw (f"Employee Whose {emp_role} has unstandardized Salary Component {DataConversion.safe_get (component, 'name')} Make Sure You Specify the Values In the Employee Document")
                if DataConversion.safe_e (DataConversion.safe_get (component_data, 'component_type'), "Fixed Amount", str, True):
                    DataConversion.safe_set (component, "fixed_amount", DataConversion.convert_to_float (DataConversion.safe_get (component_data, "component_value", 0)))
                elif DataConversion.safe_e (DataConversion.safe_get (component_data, 'component_type'), "Percentage", str, True):
                    DataConversion.safe_set (component, "percentage", DataConversion.convert_to_float (DataConversion.safe_get (component_data, "component_value", 0)))
                else:
                    throw (f"Employee Whose {emp_role} has unstandardized Salary Component {DataConversion.safe_get (component, 'name')} Value type is unknown make sure its Either <b class='text-blue-600'>Fixed Amount</b> or <b class='text-emerald-600'>Percentage</b>")
            gross += EarningCalculator.calc_earning (emp, basic, component, paye)
            DataConversion.safe_list_append (components, utils.from_dict_to_object({
                "earning": DataConversion.safe_get (component, "name")
            }))
    return gross, components

def before_acting_appointment_save(dbms, object):
    pass

def before_acting_memo_submit(dbms, object):
    core_hr = Core_Hr (dbms)
    memo = DataConversion.safe_get(object, "body", {})
    validate_acting_memo(memo)

    acting_setup = core_hr.get_doc ("Acting_Appointment_Settings", core_hr.company)
    if not acting_setup:
        throw ("Define Acting Appointment Settings To Process Acting Appointment Memo")

    paye = core_hr.get_list ("Income_Tax_Band", filters={"is_current": 1}, limit=1)
    if not paye:
        throw ("Define Income Tax Bands To Process With Calculations")
    paye = DataConversion.safe_list_get (paye, 0)

    acting_appointment = utils.from_dict_to_object ()
    position_owner = DataConversion.safe_get(memo.linked_fields, "position_owner", {})
    acting_officer = DataConversion.safe_get(memo.linked_fields, "acting_officer", {})

    acting_grade = DataConversion.safe_get (acting_officer, "employee_grade")
    owner_grade = DataConversion.safe_get (position_owner, "employee_grade")

    owner = core_hr.get_doc ("Employee_Grade", owner_grade)
    acting = core_hr.get_doc ("Employee_Grade", acting_grade)
    if not owner:
        throw ("Owner Officer's Salary Grade is Not Found")
    if not acting:
        throw ("Acting Officer's Salary Grade is Not Found")

    acting_components = DataConversion.safe_get (acting, "earnings", [])
    owner_components = DataConversion.safe_get (owner, "earnings", [])
    owner_basic = DataConversion.convert_to_float (DataConversion.safe_get (owner, "basic_pay", 0))
    acting_basic = DataConversion.convert_to_float (DataConversion.safe_get (acting, "basic_pay", 0))
    location = DataConversion.safe_get (memo, "holders_location")
    
    holders_gross, owner_salary_components  = calc_earings (dbms, position_owner, owner_components, owner_basic,  "Position Owner", paye)
    actors_gross, acting_salary_components = calc_earings (dbms, acting_officer, acting_components, acting_basic, "Acting Officer", paye)
    acting_period = DataConversion.convert_to_float (DataConversion.safe_get (memo, "acting_period", 0))
    wd = DataConversion.convert_to_float(DataConversion.safe_get (acting_officer, "working_days", 22))
    diff = holders_gross - actors_gross
    dp = diff / wd
    payable = dp * acting_period
    is_payable = 0
    grade_exceptions = utils.array_to_dict (DataConversion.safe_get (acting_setup, "grade_exceptions", []), "employee_grade")
    is_excluded = DataConversion.safe_get (grade_exceptions, owner_grade)
    
    if is_excluded:
        within_country = DataConversion.convert_to_float (DataConversion.safe_get (is_excluded, "within_country"))
        outside_country = DataConversion.convert_to_float (DataConversion.safe_get (is_excluded, "out_side_country"))
        if DataConversion.safe_e (location, "Within the Country", str, True) and DataConversion.safe_ge (acting_period, within_country, int):
            is_payable = 1
        elif DataConversion.safe_e (location, "Outside the Country", str, True) and DataConversion.safe_ge (acting_period, outside_country, int):
            is_payable = 1
    else:
        position_holder_in_country = DataConversion.convert_to_float (DataConversion.safe_get (acting_setup, "position_holder_in_country"))
        position_holder_outside_country = DataConversion.convert_to_float (DataConversion.safe_get (acting_setup, "position_holder_outside_country"))
        if DataConversion.safe_e (location, "Within the Country", str, True) and DataConversion.safe_ge (acting_period, position_holder_in_country, int):
            is_payable = 1
        elif DataConversion.safe_e (location, "Outside the Country", str, True) and DataConversion.safe_ge (acting_period, position_holder_outside_country, int):
            is_payable = 1

    DataConversion.safe_set (acting_appointment, "daily_pay", dp)
    DataConversion.safe_set (acting_appointment, "difference_payment", diff)
    DataConversion.safe_set (acting_appointment, "payable", is_payable)
    DataConversion.safe_set (acting_appointment, "acting_payment", payable)
    DataConversion.safe_set (acting_appointment, "position_owner", DataConversion.safe_get (position_owner, "name"))
    DataConversion.safe_set (acting_appointment, "job_title", DataConversion.safe_get (position_owner, "designation"))
    DataConversion.safe_set (acting_appointment, "department", DataConversion.safe_get (position_owner, "department"))
    DataConversion.safe_set (acting_appointment, "basic_pay", DataConversion.safe_get (position_owner, "basic_pay"))
    DataConversion.safe_set (acting_appointment, "owner_name", DataConversion.safe_get (position_owner, "full_name"))
    DataConversion.safe_set (acting_appointment, "salary_grade", owner_grade)
    DataConversion.safe_set (acting_appointment, "holders_gross", holders_gross)
    DataConversion.safe_set (acting_appointment, "salary_components", owner_salary_components)

    DataConversion.safe_set (acting_appointment, "acting_officer", DataConversion.safe_get (acting_officer, "name"))
    DataConversion.safe_set (acting_appointment, "acting_officer_job_title", DataConversion.safe_get (acting_officer, "designation"))
    DataConversion.safe_set (acting_appointment, "acting_officer_department", DataConversion.safe_get (acting_officer, "department"))
    DataConversion.safe_set (acting_appointment, "acting_officer_name", DataConversion.safe_get (acting_officer, "full_name"))
    DataConversion.safe_set (acting_appointment, "acting_officer_basic_pay", DataConversion.safe_get (acting_officer, "basic_pay"))
    DataConversion.safe_set (acting_appointment, "acting_officer_salary_grade", acting_grade)
    DataConversion.safe_set (acting_appointment, "acting_officer_salary_components", acting_salary_components)
    DataConversion.safe_set (acting_appointment, "actors_gross", actors_gross)

    DataConversion.safe_set (acting_appointment, "start_date", str (DataConversion.safe_get (memo, "start_date")))
    DataConversion.safe_set (acting_appointment, "end_date", str (DataConversion.safe_get (memo, "end_date")))
    DataConversion.safe_set (acting_appointment, "acting_period", acting_period)
    DataConversion.safe_set (acting_appointment, "holders_location", location)
    DataConversion.safe_set (acting_appointment, "reason", DataConversion.safe_get (memo, "reason"))
    DataConversion.safe_set (acting_appointment, "status", "Draft")

    try:
        create_aa =dbms.create("Acting_Appointment", acting_appointment)
        if create_aa.status != utils.ok:
            throw(f""" Failed to create an acting appointment document. {create_aa.error_message}""")
    except Exception as e:
        throw(f""" Failed to create an acting appointment document. {e} """)
   
def before_acting_appointment_submit(dbms, object):
    core_payroll =Core_Payroll(dbms)
    acting_appointment = DataConversion.safe_get(object, "body", {})
    validate_acting_appointment(dbms, acting_appointment)

    if DataConversion.safe_e (DataConversion.safe_get (acting_appointment, "payable", 0), 1, int): 
        add_to_payroll =core_payroll.notify_payroll(
            employee_number=DataConversion.safe_get(acting_appointment, "acting_officer"),
            amount= DataConversion.safe_get(acting_appointment, "acting_payment"),
            length_or_period=1,
            doc_type=DataConversion.safe_get(acting_appointment, "doctype", "Acting_Appointment"),
            doc_name=DataConversion.safe_get (acting_appointment, "name"),
            sc="Acting Allowance",
            entry_type ="Earning"
        )