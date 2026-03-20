from controllers.utils import Utils
from controllers.utils.dates import Dates 
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

def amendments_report (dbms, object):
    return_data = []

    core_payroll = Core_Payroll  (dbms, object)
    sys_emp = core_payroll.get_list ("Employee", filters={"status__in": ["On Leave", "Active", "Suspended"]})
    emp_flt_key = ''
    emp_flt_val = ''
    employees = {}
    emp_details = utils.array_to_dict (sys_emp, "name") 
    employees_df = utils.to_data_frame (sys_emp)
    ov_total_monthly_amount = 0
    ov_total_amount = 0
    return_data = []

    filters = {
        "month": DataConversion.get_date_part (part="month"),
    }

    filters_obj = object.filters

    if filters_obj.employee:
        DataConversion.safe_set (filters, "employee", DataConversion.safe_get (filters_obj, "employee"))

    if DataConversion.safe_get (filters_obj, "department", None):
        emp_flt_val = DataConversion.safe_get (filters_obj, "department")
        emp_flt_key = "department"
            
    if DataConversion.safe_get (filters_obj, "designation", None):
        emp_flt_val = DataConversion.safe_get (filters_obj, "designation")
        emp_flt_key = "designation"

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

    DataConversion.safe_list_append (return_data, {
        "employee_no": str(DataConversion.safe_get (filters, "month")).upper (),
        "is_opening_or_closing": True,
    })
    DataConversion.safe_list_append (return_data, {
        "is_opening_or_closing": True,
    })
    
    payroll_entries = core_payroll.get_list ("Payroll_Activity_Entry", filters=filters)
    # pp (payroll_entries)
    df = utils.to_data_frame (payroll_entries)
    if "salary_component" in df.columns:
        grouped_salary_component = (
            df.groupby("salary_component")
            .apply(lambda x: x.to_dict(orient="records"))
            .to_dict()
        )

        for ref, ref_docs in grouped_salary_component.items ():
            
            DataConversion.safe_list_append (return_data, {
                "employee_no": str(ref).upper (),
                "is_opening_or_closing": True,
            })

            ref_docs_df = utils.to_data_frame (ref_docs)
            if "reference" in ref_docs_df.columns:
                grouped_reference = (
                    ref_docs_df.groupby("reference")
                    .apply(lambda x: x.to_dict(orient="records"))
                    .to_dict()
                )

                total_amount = 0
                total_monthly = 0

                for key, docs in grouped_reference.items ():
                    report_row = {}
                    add_row = True
                    
                    doc = DataConversion.safe_list_get (docs, 0)
                    emp_id =  DataConversion.safe_get (doc, "employee")
                    emp_info = DataConversion.safe_get (emp_details, emp_id)
                    amount = DataConversion.convert_to_float (DataConversion.safe_get (doc, "amount", 0))
                    ma = DataConversion.convert_to_float (DataConversion.safe_get (doc, "monthly_payment"))
                    
                    DataConversion.safe_set (report_row, "reference", key)
                    DataConversion.safe_set (report_row, "employee_no", emp_id)
                    DataConversion.safe_set (report_row, "full_name", DataConversion.safe_get (emp_info, "full_name"))
                    DataConversion.safe_set (report_row, "designation", DataConversion.safe_get (emp_info, "designation"))
                    DataConversion.safe_set (report_row, "department", DataConversion.safe_get (emp_info, "department"))
                    DataConversion.safe_set (report_row, "effective_date", DataConversion.safe_get (doc, "effective_date"))
                    DataConversion.safe_set (report_row, "last_payment_date", DataConversion.safe_get (doc, "last_payment_date"))
                    DataConversion.safe_set (report_row, "length_or_period", DataConversion.safe_get (doc, "length_or_period"))
                    DataConversion.safe_set (report_row, "monthly_payment", ma)
                    DataConversion.safe_set (report_row, "amount", amount)
                    
                    if emp_flt_key:
                        emp_df = utils.to_data_frame (DataConversion.safe_get (employees, emp_flt_val, []))
                        if "name" in emp_df.columns:
                            emp_dict = (
                                emp_df.groupby("name")
                                .apply(lambda x: x.to_dict(orient="records"))
                                .to_dict()
                            )

                            if emp_id not in emp_dict:
                                add_row = False

                    if add_row:
                        total_monthly += ma
                        total_amount += amount
                    DataConversion.safe_list_append (return_data, report_row)

            DataConversion.safe_list_append (return_data, {
                "employee_no": "Total",
                "amount": total_amount,
                "monthly_payment": total_monthly,
                "is_opening_or_closing": True,
            })

            DataConversion.safe_list_append (return_data, {})
            
            ov_total_amount += total_amount
            ov_total_monthly_amount += total_monthly

    DataConversion.safe_list_append (return_data, {
        "employee_no": "TOTALS",
        "amount": ov_total_amount,
        "monthly_payment": ov_total_monthly_amount,
        "is_opening_or_closing": True,
    })
    
    return utils.respond(utils.ok, {'rows': return_data})