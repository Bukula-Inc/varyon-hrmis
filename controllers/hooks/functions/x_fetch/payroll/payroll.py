from datetime import datetime, timedelta
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
# import pandas as pd
from itertools import groupby
from operator import attrgetter
from controllers.core_functions.hr import Core_Hr

utils = Utils()
dates = Dates ()

pp = utils.pretty_print

def get_payroll_processor_content(dbms, object):
    core_hr = Core_Hr(dbms,object.user,object)
    components = dbms.get_list("Salary_Component",filters={"disabled":0}, fetch_linked_tables=True, fetch_linked_fields=True, user=object.user, order_by=["id"])
    tax_bands = dbms.get_list("Income_Tax_Band",fetch_linked_tables=True,fetch_linked_fields=True,user=object.user,order_by=["-id"],limit=1)
    employee = core_hr.get_employee(get_advance=True, get_overtime=True, get_all=True, order_by=["id"])
    tb = None
    emp = None
    earnings = {}
    deductions = {}

    if components.status == utils.ok:
        data = utils.group(components.data.rows, "component_type")
        earnings = data.get("Earning")
        if earnings and  len(earnings) > 0:
            earnings = utils.array_to_dict(earnings, "name")
        deductions = data.get("Deduction")
        if deductions and  len(deductions) > 0:
            deductions = utils.array_to_dict(deductions, "name")
        
    if tax_bands.status == utils.ok:
        tb = tax_bands.data.rows[0]
    if employee.status == utils.ok:
        emp = utils.array_to_dict(employee.data,"name")
    
    return utils.respond(utils.ok, {
        "employee":emp,
        "income_tax_band":tb,
        "earnings":earnings,
        "deductions":deductions,
    })

def compare_payrolls (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    data  =[]
    status = False
    cols = [{"l": "employee", "t": "Employee ID"}]
    cols.append ({"l": "basic_pay", "t": "Basic Pay"})
    current_payroll = object.body.data
    processors = core_hr.get_list ("Payroll_Processor", filters={"is_previous": 1}, limit=1)
    sc = core_hr.get_list ("Salary_Component")
    if sc:
        for com in sc:
            cols.append ({"l": com.name, "t": com.name})
    cols.append ({"l": "net", "t": "Net Pay"})
    cols.append ({"l":"gross", "t": "Gross Pay"})
    if processors:
        previous_payroll = processors[0]
        # if current_payroll.total_net != previous_payroll.total_net:
        if previous_payroll and previous_payroll.employee_info and current_payroll and current_payroll.employee_info:
            status =True
            previous_employees = utils.array_to_dict (previous_payroll.employee_info, "employee")
            for emp_info in current_payroll.employee_info:
                if emp_info.employee != "TOTALS":
                    data.append ({
                        "old": emp_info,
                        "new": previous_employees.get (emp_info.employee, {})
                    })
            
    return utils.respond (status=utils.ok, response={"cols": cols, "status": status, "data": data})