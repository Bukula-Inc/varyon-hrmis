from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion
from datetime import datetime

utils = Utils()
pp = utils.pretty_print

def nhima_report(dbms, object):
    nhima_data_result = []
    core_hr = Core_Hr(dbms=dbms)
    core_payroll = Core_Payroll (dbms=dbms)
    filter_obj = DataConversion.safe_get (object, "filters", utils.from_dict_to_object ())
    hr_settings = core_hr.get_company_settings (core_hr.company)

    nhima = DataConversion.safe_get (filter_obj, "nhima")
    emp_name = DataConversion.safe_get (filter_obj, "employee")
    id_no = DataConversion.safe_get (filter_obj, "id_no")

    if emp_name:
        employee = {emp_name: core_hr.get_doc ("Employee", emp_name)}
    elif id_no:
        employee = utils.array_to_dict (core_hr.get_list ("Employee", {"id_no": id_no}, limit=1), "name")
    elif nhima:
        employee = utils.array_to_dict (core_hr.get_list ("Employee", {"nhima": nhima}, limit=1), "name")
    else:
        employee = utils.array_to_dict (core_hr.fetch_data_from_sql ("SELECT nhima, name, d_o_b, id_no, bank_name, account_no, sort_code, first_name, middle_name, last_name FROM employee"), "name")
    
    from_date = DataConversion.safe_get (filter_obj, "from_date")
    to_date = DataConversion.safe_get (filter_obj, "to_date")
    
    order_by = ['-id']
    
    filters = {}

    if from_date and to_date:
        DataConversion.safe_set (filters, "from_date", from_date)
        DataConversion.safe_set (filters, "to_date", to_date)

    payroll_processor = core_payroll.get_list ("Payroll_Processor", filters=filters, order_by=order_by, limit=15)

    payroll_tracker = {}

    if payroll_processor:
        for payroll_proc in payroll_processor:
            from_date_pp = DataConversion.safe_get (payroll_proc, "from_date")
            if from_date_pp not in payroll_tracker:
                DataConversion.safe_set (payroll_tracker, str (from_date_pp), [payroll_proc])
            else:
                payroll = DataConversion.safe_get (payroll_tracker, str(from_date_pp))
                payroll.append (payroll_proc)
                DataConversion.safe_set (payroll_tracker, str(from_date_pp), payroll)

    if payroll_tracker:
        latest_key = max(payroll_tracker.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
        latest_payroll = DataConversion.safe_get (payroll_tracker, latest_key)

        if latest_payroll and len (latest_payroll) > 0:
            track_emp = []
            for payroll_processor in latest_payroll:
                try:
                    date = DataConversion.safe_get (payroll_processor, "from_date")
                    employees = DataConversion.safe_get (payroll_processor, "employee_info", [])
                    if employees and len (employees) > 0:
                        for emp in employees:
                            name = DataConversion.safe_get (emp, "employee", '')
                            if name not in track_emp:
                                track_emp.append (name)
                                em = DataConversion.safe_get (employee, name)
                                if em:
                                    first_name = DataConversion.safe_get (em, "first_name")
                                    last_name = DataConversion.safe_get (em, "last_name")
                                    if first_name and last_name:
                                        report_row = utils.from_dict_to_object ()
                                        
                                        DataConversion.safe_set (report_row, "company_nhima_acc", DataConversion.safe_get (hr_settings, "company_nhima_acc", ""))
                                        DataConversion.safe_set (report_row, "first_name", first_name)
                                        DataConversion.safe_set (report_row, "middle_name", DataConversion.safe_get (em, "middle_name", ''))
                                        DataConversion.safe_set (report_row, "last_name", last_name)
                                        DataConversion.safe_set (report_row, "year", date.year)
                                        DataConversion.safe_set (report_row, "month", date.month)
                                        DataConversion.safe_set (report_row, "basic_pay", DataConversion.safe_get (em, "basic_pay", ''))
                                        DataConversion.safe_set (report_row, "bank_account_no", DataConversion.safe_get (em, "account_no", ''))
                                        DataConversion.safe_set (report_row, "employment_type", DataConversion.safe_get (em, "employment_type", ''))
                                        DataConversion.safe_set (report_row, "employee_share", DataConversion.safe_get (emp, "NAPSA"))
                                        DataConversion.safe_set (report_row, "employer_share", DataConversion.safe_get (emp, "NAPSA"))
                                        DataConversion.safe_set (report_row, "d_o_b", DataConversion.safe_get (em, "d_o_b"))
                                        DataConversion.safe_set (report_row, "nhima", DataConversion.safe_get (em, "nhima"))
                                        DataConversion.safe_set (report_row, "id_no", DataConversion.safe_get (em, "id_no"))
                                        nhima_data_result.append (report_row)
                except Exception as err:
                    pp (f"{str (err)}")
                    pass

    return utils.respond(utils.ok, {'rows': nhima_data_result})

