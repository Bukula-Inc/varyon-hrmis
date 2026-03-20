from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.dates import Dates
import pandas as pd
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates =Dates()


def get_employee_assets(dbms, object):
    core_hr = Core_Hr (dbms, obj=object)
    pp("Asset ====>",object)
    employee = core_hr.get_employee_separation (object.body.data.employee)
    return utils.respond (employee.status, response=employee)

def final_statement_calculated_totals(dbms, object):    
    calculated_totals =[]
    gratuity_amount =0.00
    last_pay =0.00
    redundancy_amount =0.00
    core_hr = Core_Hr (dbms, obj=object,) 
    
    separation = core_hr.get_employee_separation (object.body.data.employee)
    payslip =dbms.get_list("Payslip", filters={"employee":object.body.data.employee})

    if payslip.status == utils.ok:
        payslip_list = payslip.data.rows
        payslips =utils.sort(payslip_list, descend=True, sort_by="posting_date")
        last_pay =payslips[0].gross
        
    employee_data =core_hr.get_employee_info(employee_id=object.body.data.employee, get_advance=True, get_overtime=True,)
    gratuity =dbms.get_list("Graduate", filters={"employee":object.body.data.employee})
    if gratuity.status == utils.ok:
        gratuity_amount = float(gratuity.data.rows[0].gratuity_amount)
        
    seperation_date =None        
    seperation =dbms.get_list("Employee_Seperation", filters={"employee": object.body.data.employee})
    
    if seperation.status ==utils.ok:
        seperation_date =seperation.data.rows[0].resignation_date
    # pp("We Are Here....")
    
    if employee_data.status == utils.ok:
        employee_info = employee_data.data
        basic_pay = float(employee_info.basic_pay)
        working_days =float(employee_info.working_days)
        daily_pay = float(basic_pay) / float(working_days)
        remaining_leave_days =float(employee_info.leave_summary.overall_totals.remaining_days)
        date_of_joining =employee_info.date_of_joining
        unsettled_loan =employee_info.advance.balance if employee_info.advance and employee_info.advance.balance else 0.00
        
        years_saved =int((dates.calculate_days(date_of_joining, seperation_date))/ 365.25,)
        redundancy_amount =years_saved * (basic_pay * 2)
            
        calculated_totals.append(utils.from_dict_to_object({
            "salary": last_pay if last_pay else  0.00,
            "leave_days_amount": remaining_leave_days * daily_pay if remaining_leave_days and daily_pay else 0.00,
            "overtime_amount": employee_info.overtime.overtime if employee_info.overtime.overtime else 0.00,
            "unsettled_loan": unsettled_loan or 0.00,
            "redundancy_amount": redundancy_amount if redundancy_amount else 0.00,
            "gratuity_amount": gratuity_amount if gratuity_amount else 0.00,
        }))

    return utils.respond (utils.ok, calculated_totals)


    
    

