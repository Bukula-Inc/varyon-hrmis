from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll
from controllers.utils.data_conversions import DataConversion
from datetime import datetime

utils = Utils()
pp = utils.pretty_print


def paye_report(dbms, object):
    paye_data_result = []

    core_hr = Core_Hr(dbms=dbms)
    core_payroll = Core_Payroll (dbms=dbms)
    filter_obj = DataConversion.safe_get (object, "filters", utils.from_dict_to_object ())

    emp_name = DataConversion.safe_get (filter_obj, "employee")
    id_no = DataConversion.safe_get (filter_obj, "id_no")

    if emp_name:
        employee = {emp_name: core_hr.get_doc ("Employee", emp_name)}
    elif id_no:
        employee = utils.array_to_dict (core_hr.get_list ("Employee", {"id_no": id_no}, limit=1), "name")
    else:
        employee = utils.array_to_dict (core_hr.fetch_data_from_sql ("""
            SELECT
                employee.name,
                employee.tpin,
                employee.first_name,
                employee.last_name,
                employee.middle_name,
                employee.department_id,
                employee.employment_type_id,
                dd.name AS department,
                emp_ty.name AS employment_type
            FROM employee
            LEFT JOIN department dd ON employee.department_id = dd.id
            LEFT JOIN employment_type emp_ty ON employee.employment_type_id = emp_ty.id
                                                                    
        """), "name")
    
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
                payroll = DataConversion.safe_get (payroll_tracker, str (from_date_pp))
                payroll.append (payroll_proc)
                DataConversion.safe_set (payroll_tracker, str(from_date_pp), payroll)
    
    if payroll_tracker:
        latest_key = max(payroll_tracker.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
        latest_payroll = DataConversion.safe_get (payroll_tracker, latest_key)

        if latest_payroll and len (latest_payroll) > 0:
            track_emp = []
            for payroll_processor in latest_payroll:
                try:
                    from_date = DataConversion.safe_get (payroll_processor, "from_date")
                    to_date = DataConversion.safe_get (payroll_processor, "to_date")
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
                                        DataConversion.safe_set (report_row, "first_name", first_name)
                                        DataConversion.safe_set (report_row, "middle_name", DataConversion.safe_get (em, "middle_name", ''))
                                        DataConversion.safe_set (report_row, "last_name", last_name)
                                        DataConversion.safe_set (report_row, "employee", name)
                                        DataConversion.safe_set (report_row, "from_date", from_date)
                                        DataConversion.safe_set (report_row, "to_date", to_date)
                                        DataConversion.safe_set (report_row, "tpin", DataConversion.safe_get (em, "tpin", ''))
                                        DataConversion.safe_set (report_row, "total_tax", 0.00)
                                        DataConversion.safe_set (report_row, "tax_adjusted", 0.00)
                                        DataConversion.safe_set (report_row, "department", DataConversion.safe_get (em, "department", ''))
                                        DataConversion.safe_set (report_row, "employment_type", DataConversion.safe_get (em, "employment_type", ''))
                                        DataConversion.safe_set (report_row, "gross", DataConversion.safe_get (emp, "gross"))
                                        DataConversion.safe_set (report_row, "employee_names", DataConversion.safe_get (emp, "full_names"))
                                        DataConversion.safe_set (report_row, "tax_deducted", DataConversion.safe_get (emp, "PAYE"))
                                        paye_data_result.append (report_row)
                except Exception as err:
                    pp (f"{str (err)}")
                    pass

    return utils.respond(utils.ok, {'rows': paye_data_result})