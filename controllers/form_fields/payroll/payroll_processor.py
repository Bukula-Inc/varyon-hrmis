from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from collections import defaultdict
import time

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

def get_fields (dbms):
    
    company = dbms.current_user.default_company or dbms.system_settings.default_company

    return [
            {
                "id": "has_error",
                "fieldlabel": "Has Errors",
                "fieldname": "has_error",
                "fieldtype": "check",
                "columns": 1,
                "required": False,
                "hidden": True,
                "placeholder": "There Are Errors",
            },
            {
                "id": "payroll_processor_error",
                "fieldlabel": "Payroll Processor Errors",
                "fieldname": "payroll_processor_error",
                "fieldtype": "rich",
                "columns": 1,
                "height": 300,
                "required": False,
                "hidden": False,
                "displayon": ["has_error", 1],
                "placeholder": "There where Processor Errors in this Payroll Period",
            },
            {
                "id": "ff",
                "fieldlabel": "Processed Payroll",
                "fieldname": "ff",
                "fieldtype": "section-break",
                "columns": 12,
                "required": False,
                "hidden": False,
                "addborder": True,
                "placeholder": "The payroll that was processed starts here above are the errors that occred",
            },
            {
                "id": "from-date",
                "fieldlabel": "From Date",
                "fieldname": "from_date",
                "fieldtype": "date",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "Select From Date",
                "default": dates.get_first_date_of_current_month()

            },
            {
                "id": "to-date",
                "fieldlabel": "To Date",
                "fieldname": "to_date",
                "fieldtype": "date",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "Select To Date",
                "default": dates.get_last_date_of_current_month()
            },
            {
                "id": "company",
                "fieldlabel": "Company",
                "fieldname": "company",
                "fieldtype": "link",
                "model":"Company",
                "columns": 1,
                "required": True,
                "hidden": True,
                "placeholder": "Select Company",
                "default": company
            },
            {
                "id": "frequency",
                "fieldlabel": "Payment Frequency",
                "fieldname": "frequency",
                "fieldtype": "read-only",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "Select Payment Frequency",
                "options": ["Monthly", "Weekly"],
                "default":"Monthly"
            },
            {
                "id": "currency",
                "fieldlabel": "Currency",
                "fieldname": "currency",
                "fieldtype": "read-only",
                # "model":"Currency",
                "columns": 1,
                "required": True,
                "hidden": False,
                "fetchfrom":"company",
                "fetchfield":"reporting_currency",
                "placeholder": "Select Currency",
                "default": "ZMW"
            },
            {
                "id": "convertion-rate",
                "fieldlabel": "Convertion Rate",
                "fieldname": "convertion_rate",
                "fieldtype": "float",
                "columns": 1,
                "required": True,
                "hidden": True,
                "placeholder": "Enter Convertion Rate",
                "default":"1.0"
            },
            {
                "id": "bank-account",
                "fieldlabel": "Cash/Bank Account",
                "fieldname": "bank_account",
                "fieldtype": "link",
                "model":"Bank_Account",
                "columns": 1,
                "required": False,
                "hidden": True,
                "placeholder": "Select Bank Account",
                "default": None
            },
            {
                "id": "total_employees",
                "fieldlabel": "Total Employees",
                "fieldname": "total_employees",
                "fieldtype": "read-only",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "",
                "default":'0',
            },
            {
                "id": "break",
                "fieldlabel": "Employee Details",
                "fieldname": "ed",
                "fieldtype": "section-break",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "",
                "addborder":True
            },
            {
                "id": "employee-info",
                "fieldlabel": "Employee Info",
                "fieldname": "employee_info",
                "fieldtype": "table",
                "model":"Employee Info",
                "required": True,
                "hidden": False,
                "placeholder": "",
                "addemptyrow": False,
                "fields":[
                    {
                        "id": "employee",
                        "fieldlabel": "Employee",
                        "fieldname": "employee",
                        "fieldtype": "link",
                        "model":"Employee",
                        "columns": 1,
                        "required": True,
                        "hidden": False,
                        "placeholder": "Select Employee",
                        "default":0
                    },
                    {
                        "id": "employee-names",
                        "fieldlabel": "Full Names",
                        "fieldname": "full_names",
                        "fieldtype": "read-only",
                        "columns": 1,
                        "required": True,
                        "hidden": False,
                        "placeholder": "Full Names",
                        "default":0
                    },
                    {
                        "id": "designation",
                        "fieldlabel": "Designation",
                        "fieldname": "designation",
                        "fieldtype": "read-only",
                        "columns": 1,
                        "required": False,
                        "hidden": False,
                        "placeholder": ""
                    },
                    {
                        "id": "basic-pay",
                        "fieldlabel": "Basic Pay",
                        "fieldname": "basic_pay",
                        "fieldtype": "read-only",
                        "columns": 1,
                        "required": True,
                        "hidden": False,
                        "placeholder": "",
                        "alwaysfetch":False,
                        "default":"0.00",
                        "is_figure":True
                    },
                ]
            },
            {
                "id": "totals",
                "fieldlabel": "Overrall Totals",
                "fieldname": "ot",
                "fieldtype": "section-break",
                "addborder": True,
            },
            {
                "id": "total-basic",
                "fieldlabel": "Total Basic",
                "fieldname": "total_basic",
                "fieldtype": "read-only",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "",
                "default":"0.00",
                "is_figure":True
            },
            {
                "id": "total-earnings",
                "fieldlabel": "Total Earnings",
                "fieldname": "total_earnings",
                "fieldtype": "read-only",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "",
                "default":"0.00",
                "is_figure":True
            },
            {
                "id": "total-deductions",
                "fieldlabel": "Total Deductions",
                "fieldname": "total_deductions",
                "fieldtype": "read-only",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "",
                "default":"0.00",
                "is_figure":True,
            },
            {
                "id": "total-gross",
                "fieldlabel": "Total Gross",
                "fieldname": "total_gross",
                "fieldtype": "read-only",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "",
                "default":"0.00",
                "is_figure":True
            },

            {
                "id": "total__earnings_with_excluded",
                "fieldlabel": "Total Gross",
                "fieldname": "total__earnings_with_excluded",
                "fieldtype": "read-only",
                "columns": 1,
                "required": True,
                "hidden": True,
                "placeholder": "",
                "default":"0.00",
                "is_figure":True
            },
            {
                "id": "total-net",
                "fieldlabel": "Total Net",
                "fieldname": "total_net",
                "fieldtype": "read-only",
                "columns": 1,
                "required": True,
                "hidden": False,
                "placeholder": "",
                "default":"0.00",
                "is_figure":True
            },

        ]

def fetch_data(query, dbms, params=False):
    result = utils.from_dict_to_object
    if params:
        result = dbms.sql(query, params)
    else:
        result = dbms.sql(query)
    return result.data if result.status == utils.ok else []

def fetch_payroll_processor_fields(dbms, object):
    core_hr = Core_Hr (dbms)
    temp_employees = {}
    initial_emp_fetch = []
    separations = []
    is_pp = False


    extra_params = DataConversion.safe_get (object, "extra_params", {})
    if extra_params:
        if DataConversion.safe_get (extra_params, "pp", False):
            separations = str (DataConversion.safe_get (extra_params, "sep", '')).split ("_")
            if len (separations) > 0:
                is_pp = True

    emp = []
    sc = []
    tb = []

    fields = get_fields (dbms)
    fields = utils.array_to_dict(fields,"fieldname")
    if fields.company:
        fields.company.default = dbms.current_user.default_company

    employee_query = """
        SELECT
            CAST(replace(employee.basic_pay::text, ',', '') AS numeric) AS basic_pay,
            employee.name,
            employee.id,
            employee.full_name,
            employee.first_name,
            employee.middle_name,
            employee.last_name,
            employee.date_of_joining,
            employee.last_day_of_work,
            employee.working_days,
            employee.working_hours,
            employee.napsa,
            employee.account_no,
            employee.bank_name,
            employee.id_no,
            employee.employment_type_id,
            employee.employee_grade_id,
            employee.designation_id,
            employee.department_id,
            employee.inable_probation,
            employee.tax_band_id,
            employee.status_id,
            employee.is_separated,
            employee.is_separated_emp_paid,
            jsonb_path_query_array(employee.unstandardized_components, '$[*]') AS unstandardized_components,
            jsonb_path_query_array(employee.deductions, '$[*].deduction') AS deductions,
            jsonb_path_query_array(employee.earnings, '$[*].earning') AS earnings,
            dd.name AS designation,
            et.name AS employment_type,
            dept.name AS department,
            tb.name AS tax_band,
            ss.name AS employee_grade,
            sta.name AS status
        FROM employee
        LEFT JOIN employment_type et ON employee.employment_type_id = et.id
        LEFT JOIN department dept ON employee.department_id = dept.id
        LEFT JOIN designation dd ON employee.designation_id = dd.id
        LEFT JOIN employee_grade ss ON employee.employee_grade_id = ss.id
        LEFT JOIN income_tax_band tb ON employee.tax_band_id = tb.id
        LEFT JOIN doc_status sta ON employee.status_id = sta.id
        ORDER BY name ASC
    """

    salary_component_query = """
        SELECT
            name,
            component_type,
            percentage,
            value_type,
            shared_deduction_custom_company,
            shared_deduction_custom_emp,
            shared_deduction_custom,
            apply_on,
            grossable,
            fixed_amount,
            has_ceiling,
            unstandardized,
            is_statutory_component,
            ceiling_amount,
            shared_deduction,
            for_commutation,
            is_private_pension,
            is_advance,
            is_overtime,
            exclude_on_statutory_deductions,
            is_commission,
            unites,
            resenting
        FROM salary_component;
    """

    tax_band_query = """
        SELECT
            itb.name,
            itb.deduct_on,
            itb.tax_free_amount,
            itb.take_home_percentage,
            itb.zra_percentage,
            tsb.amount_from,
            tsb.amount_to,
            tsb.deduction_percentage
        FROM income_tax_band itb
        LEFT JOIN income_tax_band_salary_bands itbsb ON itb.id = itbsb.income_tax_band_id
        LEFT JOIN taxable_salary_band tsb ON tsb.id = itbsb.taxable_salary_band_id
        WHERE itb.is_current::integer = 1;
    """
    

    
    if is_pp and len (separations) > 0:
        for sep in separations:
            if not sep:
                continue
            query = """
                SELECT
                    CAST(replace(employee.basic_pay::text, ',', '') AS numeric) AS basic_pay,
                    employee.name,
                    employee.id,
                    employee.full_name,
                    employee.first_name,
                    employee.middle_name,
                    employee.last_name,
                    employee.date_of_joining,
                    employee.last_day_of_work,
                    employee.working_days,
                    employee.working_hours,
                    employee.napsa,
                    employee.account_no,
                    employee.bank_name,
                    employee.id_no,
                    employee.employment_type_id,
                    employee.employee_grade_id,
                    employee.designation_id,
                    employee.department_id,
                    employee.inable_probation,
                    employee.tax_band_id,
                    employee.status_id,
                    employee.is_separated,
                    employee.is_separated_emp_paid,
                    jsonb_path_query_array(employee.deductions, '$[*].deduction') AS deductions,
                    jsonb_path_query_array(employee.earnings, '$[*].earning') AS earnings,
                    dd.name AS designation,
                    et.name AS employment_type,
                    dept.name AS department,
                    tb.name AS tax_band,
                    ss.name AS employee_grade,
                    sta.name AS status
                FROM employee
                LEFT JOIN employment_type et ON employee.employment_type_id = et.id
                LEFT JOIN department dept ON employee.department_id = dept.id
                LEFT JOIN designation dd ON employee.designation_id = dd.id
                LEFT JOIN employee_grade ss ON employee.employee_grade_id = ss.id
                LEFT JOIN income_tax_band tb ON employee.tax_band_id = tb.id
                LEFT JOIN doc_status sta ON employee.status_id = sta.id
                WHERE employee.name = %s;
            """

            emp_fetch = fetch_data (query, dbms=dbms, params=[sep])
            if emp_fetch and len (emp_fetch) > 0:
                initial_emp_fetch.extend (emp_fetch)
    else:
        initial_emp_fetch = fetch_data (query=employee_query, dbms=dbms)

    temps = core_hr.get_list ("Pay_For_Temps_Or_Seasonal_Employee", {"is_current": 1}, limit=1)
    if temps:
        temps = DataConversion.safe_list_get (temps, 0)
        temp_emp = DataConversion.safe_get (temps, "employee")
        if temp_emp:
            temp_employees = utils.array_to_dict (temp_emp, "employee_no")

    initial_sc_fetch = fetch_data (query=salary_component_query, dbms=dbms)
    tax_band = fetch_data (query=tax_band_query, dbms=dbms)

    df = utils.to_data_frame (initial_emp_fetch)
    filtered_df = df[df['status'] != 'Disabled']
    initial_emp_fetch = filtered_df.to_dict(orient='records')
    
    sly_comp = utils.array_to_dict (initial_sc_fetch, 'name')
    if initial_sc_fetch:
        sc = utils.group (initial_sc_fetch, "component_type")

    if initial_emp_fetch and len (initial_emp_fetch) > 0:
        for em in initial_emp_fetch:
            leave_days = core_hr.emp_leave_annual_days (DataConversion.safe_get (em, "name"))
            cd = DataConversion.convert_to_float (DataConversion.safe_get (leave_days, "remaining_days"))
            em = core_hr.get_emp_last_pay (em)
            DataConversion.safe_set (em, "leave_days", cd)
            is_separated = DataConversion.safe_get (em, "is_separated")
            is_separated_emp_paid = DataConversion.safe_get (em, "is_separated_emp_paid")
            basic_pay = DataConversion.convert_to_float(DataConversion.safe_get (em, "basic_pay", 0.00))
            if DataConversion.safe_get (em, "employment_type") in ["Temporal", "Seasonal Employment"]:
                emp_info = DataConversion.safe_get (temp_employees, DataConversion.safe_get (em, "name"))
                if emp_info:
                    basic_pay = DataConversion.convert_to_float (DataConversion.safe_get (emp_info, "pay", 0))
            if basic_pay > 0:
                if not is_separated or (is_separated and is_separated_emp_paid != "Settled"): 
                    DataConversion.safe_set (em, "basic_pay", basic_pay)
                    emp.append (core_hr.get_employee_payroll_content (em, sly_comp))
    grouped = defaultdict(list)

    required_fields = [
        "name",
        "deduct_on",
        "tax_free_amount",
        "zra_percentage",
        "take_home_percentage",
        "amount_from",
        "amount_to",
        "deduction_percentage",
    ]

    for entry in tax_band:
        for field in required_fields:
            if field not in entry:
                raise KeyError(f"Missing field in tax_band entry: {field}")
        key = (
            entry["name"],
            entry["deduct_on"],
            entry["tax_free_amount"],
            entry["zra_percentage"],
            entry["take_home_percentage"]
        )

        grouped[key].append({
            "amount_from": entry["amount_from"],
            "amount_to": entry["amount_to"],
            "zra_percentage": entry["zra_percentage"],
            "take_home_percentage": entry["take_home_percentage"],
            "deduction_percentage": entry["deduction_percentage"]
        })

    tax_band = []
    for (name, deduct_on, tax_free_amount, zra_percentage, take_home_percentage), bands in grouped.items():
        tax_band.append({
            "name": name,
            "deduct_on": deduct_on,
            "take_home_percentage": take_home_percentage,
            "zra_percentage": zra_percentage,
            "tax_free_amount": tax_free_amount,
            "salary_bands": bands
        })

    if tax_band:
        tb = utils.from_dict_to_object(tax_band[0])
        DataConversion.safe_set (tb, "name", "PAYE")
        DataConversion.safe_set (tb, "take_home_percentage", 100 - DataConversion.convert_to_float (DataConversion.safe_get (tb, "zra_percentage", 0)))

    if sc:
        new_fields = []
        if sc.Earning:
            new_fields.extend(sc.Earning)
        if sc.Deduction:
            new_fields.extend(sc.Deduction)
        for cmp in new_fields:
            fields.employee_info.fields.append({
                "id": cmp.name,
                "fieldlabel": cmp.name,
                "fieldname": cmp.name,
                "fieldtype": "read-only" if cmp.is_standard_component == 1 or cmp.value_type in ["Fixed Amount", "Percentage", "System Value"] or cmp.fixed_amount != 0 else "currency",
                "columns": 1,
                "required": False,
                "hidden": False,
                "placeholder": f"Enter {cmp.name}",
                "default":"0.00",
                "is_figure":True
            })
        if tb:
            fields.employee_info.fields.append({
                "id": tb.name,
                "fieldlabel": tb.name,
                "fieldname": tb.name,
                "fieldtype": "read-only",
                "columns": 1,
                "required": False,
                "hidden": False,
                "placeholder": "Income Tax Bank",
                "default":"0.00",
                "is_figure":True
            })

        fields.employee_info.fields.extend([
            {
                "id": "gross",
                "fieldlabel": "Total Gross",
                "fieldname": "gross",
                "fieldtype": "read-only",
                "columns": 1,
                "required": False,
                "hidden": False,
                "placeholder": "Total Gross",
                "default":"0.00",
                "is_figure":True
            },
            {
                "id": "total_un_taxable_gross",
                "fieldlabel": "Total Gross",
                "fieldname": "total_un_taxable_gross",
                "fieldtype": "read-only",
                "columns": 1,
                "required": False,
                "hidden": True,
                "placeholder": "Total Gross",
                "default":"0.00",
                "is_figure":True
            },
            {
                "id": "net",
                "fieldlabel": "Net",
                "fieldname": "net",
                "fieldtype": "read-only",
                "columns": 1,
                "required": False,
                "hidden": False,
                "placeholder": "Net",
                "default":"0.00",
                "is_figure":True
            }
        ])

    return utils.respond(utils.ok, {
        "fields": utils.get_object_values(fields),
        "data":{
            "employees": emp,
            "salary_components": sc,
            "tax_band": tb
        }
    })