from datetime import datetime
import logging
from controllers.mailing.templates.payroll_email_template import Default_Templates
from controllers.utils import Utils
from controllers.mailing import Mailing

utils = Utils()
pp =utils.pretty_print

def notify_employees(dbms, object):
    mailing = Mailing(dbms=dbms)
    grade_name = object.body.name
    grade_data = object.body

    employees_data = dbms.get_list("Employee", filters={'employee_grade': grade_name},fetch_linked_tables = True, privilege=True)
    if employees_data.status == utils.ok:
        for employee  in employees_data.data.rows:
            employee.basic_pay = grade_data.basic_pay
            employee.earnings = grade_data.earnings
            employee.deductions = grade_data.deductions
            update = dbms.update("Employee", employee, privilege=True)
       

   
        


























































































