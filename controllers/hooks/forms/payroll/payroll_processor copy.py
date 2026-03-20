from controllers.utils import Utils
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import timedelta
from controllers.utils.dates import Dates
from controllers.core_functions.accounting import Core_Accounting
from controllers.core_functions.payroll import Core_Payroll
from controllers.core_functions.hr import Core_Hr
utils = Utils()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw


def on_payroll_processor_save(dbms, object):
    pass

def on_payroll_processor_update(dbms, object):
    pass


def on_payroll_processor_cancel(dbms, object):
    core_hr = Core_Hr (dbms)
    payroll_processor = object.body
    core = Core_Accounting(dbms, object.user, object)
    payslips = core_hr.get_list ("Payslip", filters={"payroll_processor": payroll_processor.name})
    if payslips:
        payslip_ids =  utils.get_list_of_dicts_column_field(payslips, "id")
        dbms.cancel_doc ("Payslip", payslip_ids)

    if payroll_processor.employee_info and len (payroll_processor.employee_info) > 0:
        for emp in payroll_processor.employee_info:
            employee = core_hr.get_doc ("Employee", emp.employee)
            if employee:
                if str (employee.status).lower () != "active":
                    employee.is_separated_emp_paid = "Unsettled"
                    dbms.update ("Employee", employee, update_submitted=True)

    if payroll_processor.transaction_journal:
        cancel_payroll_gl = core.cancel_journal_entry(payroll_processor.transaction_journal)
        pp (cancel_payroll_gl)


class Process_Payroll:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.core = Core_Accounting(dbms, object)
        self.core_payroll = Core_Payroll(dbms, object)
        self.core_hr = Core_Hr(dbms=dbms)
        self.payroll_processor = object.body
        self.failed_employees = []
        self.deductions_data = self.core_payroll.get_deduction_components (fetch_linked_tables=True)
        self.earnings_data = self.core_payroll.get_earning_components (fetch_linked_tables=True)
        self.decimals = dbms.system_settings.currency_decimals
        hr_settings = self.core_hr.get_company_settings (self.core_hr.company)
        self.hr_settings_working_days = 22 if not hr_settings else hr_settings.working_days
        self.successful = 0
        self.failed = 0


    def validate_date_range(self, from_date, to_date, frequency):
        days_diff = (to_date - from_date).days + 1

        if frequency == "Weekly":
            is_valid = (days_diff % 7 == 0)
        elif frequency == "Monthly":
            is_valid = (days_diff >= self.hr_settings_working_days )
        else:
            raise ValueError("Invalid frequency")

        return is_valid

    def calc_overtime (self, emp):
        return_val = 0.00
        overtime = float(getattr(emp, 'Overtime', 0.0) or 0.0)
        if overtime > 0.0:
            ov_data = self.core_hr.get_unsettled_overtime_data(employee=emp.employee)
            if ov_data:
                for ot in ov_data:
                    ot.total_earning = utils.fixed_decimals((float (ot.total_earning) - float (overtime)), self.decimals)
                    if ot.total_earning <= 0:
                        ot.status = "Paid"
                        ot.is_paid = 1
                    else:
                        return_val =  ot.total_earning
                    ot.is_paid = 1
                    update = self.dbms.update("Overtime", ot, privilege=True)

        return return_val

    def calc_advance (self, emp):
        advance = float(getattr(emp, 'Advance', 0.0) or 0.0)
        return_val = 0.00
        if advance > 0.0:
            ad_data = self.core_hr.get_unsettled_advance_data(employee=emp.employee)
            if ad_data:
                for repayment_data in ad_data:
                    if repayment_data.repayments.doctype == "Salary_Advance_Partial_Payments":
                        repayment_date = datetime.fromisoformat(repayment_data.repayments.month.replace('Z', '+00:00'))
                        if repayment_date.year == datetime.now().year and repayment_date.month == datetime.now().month:
                            if repayment_data.repayments.state == "Unsettled":
                                settlement = repayment_data.repayments.payment
                                repayment_data.repayments.balance -= settlement
                                repayment_data.repayments.state = "Settled"
                                self.dbms.update("Advance_Application", repayment_data.doc, privilege=True)
                        if repayment_data.repayments.balance <= 0:
                            repayment_data.doc.is_paid = 1
                            self.dbms.update("Advance_Application", repayment_data.doc, privilege=True)
                    else:
                        repayment_data.doc.amount = utils.fixed_decimals (float (repayment_data.doc.amount) - float (advance), self.decimals)
                        if repayment_data.doc.amount <= 0:
                            repayment_data.doc.is_paid = 1
                            repayment_data.doc.status = "Paid"
                        else:
                            return_val = repayment_data.doc.amount
                        self.dbms.update("Advance_Application", repayment_data.doc, privilege=True)
        return return_val

    def calc_commission (self, emp, commission):
        pass

    def clear_separated_employees (self, emp, curr_to_date):
        curr_to_date = curr_to_date if not isinstance (curr_to_date, str) else dates.string_to_date (curr_to_date)
        last_day_of_work = emp.last_day_of_work if not isinstance (emp.last_day_of_work, str) else dates.string_to_date (emp.last_day_of_work)
        if emp.is_separated == 1 and last_day_of_work <= curr_to_date:
            emp.is_separated_emp_paid = "Settled"
            self.dbms.update ("Employee", emp, update_submitted=True)
        return

    def process_payroll (self, curr_from_date, curr_to_date):
        number_of_payslips = 0
        number_of_gen_payslips = 0
        for emp_salary_info in self.payroll_processor.employee_info:
            if float(emp_salary_info.basic_pay) == 0.00:
                self.failed_employees.append ({"employee": emp_salary_info.employee, "reason": "Employee Basic Pay", "error_occurred": f"{emp_salary_info.employee}'s basic pay is zero"})
            if str (emp_salary_info.employee).lower () != "totals":
                employee = None
                emp = self.core_hr.get_employee(employee_id=emp_salary_info.employee,get_leave_days=True, get_payslip_analytics=True)
                if emp.status == utils.ok:
                    employee = emp.data
                else:
                    self.failed_employees.append ({"employee": emp_salary_info.employee, "reason": "Field To Fetch Employee", "error_occurred": f"{emp.error_message}"})
                if employee:
                    current_payslip_data =  self.dbms.get_list("Payslip", filters={"status__in": ["Submitted"], "employee": employee.name, "from_date": curr_from_date, "to_date": curr_to_date }, user=self.object.user)
                    if  current_payslip_data.status == utils.no_content:
                        number_of_payslips += 1
                        self.calc_overtime (emp_salary_info)
                        self.calc_advance (emp=emp_salary_info)
                        date_of_joining = employee.date_of_joining
                        if (date_of_joining <= curr_to_date and date_of_joining >= curr_from_date) or date_of_joining < curr_from_date :
                            payslip = utils.from_dict_to_object({})
                            payslip.status = "Submitted"
                            payslip.docstatus = 1
                            payslip.posting_date = dates.today()
                            payslip.posting_time = dates.timestamp()
                            payslip.from_date = curr_from_date
                            payslip.to_date = curr_to_date
                            payslip.reporting_currency = self.core.system_settings.default_currency
                            payslip.currency = self.payroll_processor.currency
                            payslip.convertion_rate = self.payroll_processor.convertion_rate
                            payslip.employee = employee.name
                            payslip.company = employee.company
                            payslip.salary_grade = employee.employee_grade
                            payslip.employee_names = f"{employee.first_name or ''} {employee.middle_name or ''} {employee.last_name or ''}"
                            payslip.department = employee.department
                            payslip.designation = employee.designation
                            payslip.employment_type = employee.employment_type
                            payslip.bank_name = employee.bank_name
                            payslip.bank_account_no = employee.account_no
                            payslip.tax_identification_no = employee.tpin
                            payslip.tax_band = employee.tax_band
                            payslip.payroll_frequency = self.payroll_processor.frequency
                            payslip.working_days = employee.working_days
                            payslip.basic_pay = utils.fixed_decimals(float(emp_salary_info.basic_pay), self.decimals)
                            payslip.gross = utils.fixed_decimals(float(emp_salary_info.gross))
                            payslip.net = utils.fixed_decimals(float(emp_salary_info.net))
                            payslip.payroll_processor = self.payroll_processor.name
                            payslip.total_deductions = 0.00
                            payslip.advance_amount = 0
                            payslip.advance_repaid = 0
                            payslip.total_advance_repaid = 0
                            payslip.earnings = [{"earning":"Basic","amount":emp_salary_info.basic_pay}]
                            payslip.deductions = []
                            payslip.years_in_service = dates.calculate_time_period(str(employee.date_of_joining),str(dates.today()))
                            payslip.total_earnings = utils.fixed_decimals(float(payslip.basic_pay or 0), self.decimals)
                            payslip.total_tax_amount = 0
                            leave_summary =  employee.leave_summary.overall_totals
                            remaining_days =  float(leave_summary.remaining_days or 0)
                            emp_working_days =float(employee.working_days or 0)
                            emp_basic_salary =float(emp_salary_info.basic_pay or 0)
                            leave_value_per_day = 0
                            if leave_value_per_day > 0:
                                leave_value_per_day = utils.fixed_decimals(emp_basic_salary / emp_working_days,self.decimals)
                            leave_value =  utils.fixed_decimals(leave_value_per_day * remaining_days,self.decimals)
                            rounded_leave_value = leave_value
                            payslip.current_leave_days = leave_summary.remaining_days
                            payslip.current_leave_value = rounded_leave_value
                            payslip.ytd_leave_days = leave_summary.total_days
                            ytd_leave_days =  float(leave_summary.total_days or 0)
                            ytd_leave_days_value = utils.fixed_decimals(ytd_leave_days * leave_value_per_day, self.decimals)
                            payslip.ytd_leave_value = ytd_leave_days_value

                            if self.earnings_data:
                                for earning in self.earnings_data:
                                    en = getattr(emp_salary_info,earning.name, 0.00)
                                    if float(en or 0) >= 0:
                                        payslip.total_earnings += float(en or 0)
                                        payslip.earnings.append({"earning": earning.name, "amount":en})
                            if self.deductions_data:
                                for deduction in self.deductions_data:
                                    ded = getattr(emp_salary_info,deduction.name, 0.00)
                                    if float(ded) >= 0:
                                        if deduction.is_private_pension:
                                            payslip.private_pension = float(ded)
                                        if str(deduction.name).lower () == "napsa":
                                            payslip.napsa = float(ded)
                                        payslip.total_deductions += float(ded)
                                        payslip.deductions.append({"deduction":deduction.name,"amount":utils.fixed_decimals(float(ded))})
                            if employee.tax_band:
                                band = getattr(emp_salary_info, employee.tax_band, 0.00)
                                if float(band or 0) >= 0:
                                    payslip.total_tax_amount = utils.fixed_decimals(float(band or 0), self.decimals)
                                    payslip.total_deductions += utils.fixed_decimals(float(band or 0), self.decimals)
                                    payslip.deductions.append({"deduction":employee.tax_band,"amount":utils.fixed_decimals(float(band))} )

                            payslip_analytics = employee.payslip_analytics
                            payslip.ytd_gross = utils.fixed_decimals(payslip_analytics.overall_gross + float(payslip.gross or 0), self.decimals)
                            payslip.ytd_net = utils.fixed_decimals(payslip_analytics.overall_net + float(payslip.net or 0), self.decimals)
                            payslip.ytd_earnings = utils.fixed_decimals(payslip_analytics.overall_earnings + float(payslip.total_earnings or 0), self.decimals)
                            payslip.ytd_deductions = utils.fixed_decimals(payslip_analytics.overall_deductions + float(payslip.total_deductions or 0), self.decimals)
                            payslip.ytd_tax = utils.fixed_decimals(payslip_analytics.overall_tax + float(payslip.total_tax_amount or 0), self.decimals)
                            payslip.ytd_napsa = utils.fixed_decimal (payslip_analytics.overall_napsa + float(payslip.NAPSA or 0), self.decimals)
                            payslip.ytd_private_pension = utils.fixed_decimal (payslip_analytics.overall_private_pension + float(payslip["Private Pension"] or 0), self.decimals)
                            new_payslip = self.dbms.create("Payslip", payslip, self.object.user)
                            if new_payslip.status == utils.ok:
                                number_of_gen_payslips += 1
                                self.successful = number_of_gen_payslips
                                self.failed = number_of_payslips - number_of_gen_payslips if (number_of_payslips - number_of_gen_payslips) > 0 else 0
                                self.clear_separated_employees (emp=employee, curr_to_date=curr_to_date)

    @classmethod
    def payroll_processor_initializer (cls, dbms, object):
        cls = cls (dbms, object)
        transactions_journal = cls.core.post_payroll_control_transactions(cls.payroll_processor, cls.earnings_data, cls.deductions_data)
        if transactions_journal.status != utils.ok:
            throw(f"Failed to post payroll transactions: {transactions_journal.error_message}")
        journal = transactions_journal.data.name

        stats = utils.from_dict_to_object ({
            "failed": 0,
            "successful": 0,
            "journal": journal,
        })
        if cls.payroll_processor.frequency == "Weekly":
            result = cls.validate_date_range(cls.from_date, cls.to_date, cls.payroll_processor.frequency)
            if result:
                weeks_between = (cls.to_date - cls.from_date).days // 7 + 1
                for i in range(weeks_between):
                    current_from_date = cls.from_date + timedelta(weeks=i)
                    current_to_date = current_from_date + timedelta(days=6)
                    cls.process_payroll (current_from_date, current_to_date)
                    stats.failed += int (cls.failed)
                    stats.successful += int (cls.successful)
                return stats
            else:
                throw("Invalid date range for Weekly payroll. The range should be a multiple of 7.")

        elif cls.payroll_processor.frequency == "Monthly":
            result = cls.validate_date_range(cls.payroll_processor.from_date, cls.payroll_processor.to_date, cls.payroll_processor.frequency)
            if result:
                days_diff = (cls.payroll_processor.to_date - cls.payroll_processor.from_date).days + 1
                if 20 <= days_diff <= 30 or days_diff > 30 and cls.payroll_processor.to_date.year == cls.payroll_processor.from_date.year and cls.payroll_processor.to_date.month == cls.payroll_processor.from_date.month:
                    months_between = relativedelta(cls.payroll_processor.to_date, cls.payroll_processor.from_date).months + 1
                elif 20 <= days_diff <= 32:
                    months_between = relativedelta(cls.payroll_processor.to_date, cls.payroll_processor.from_date).months or 1
                elif days_diff > 32:
                    months_between = relativedelta(cls.payroll_processor.to_date, cls.payroll_processor.from_date).months + 1
                if months_between >= 1:
                    for i in range(months_between):
                        current_from_date = cls.payroll_processor.from_date + relativedelta(months=i)
                        current_to_date = current_from_date + relativedelta(months=1) - timedelta(days=1)
                        cls.process_payroll (current_from_date, current_to_date)
                        stats.failed += int (cls.failed)
                        stats.successful += int (cls.successful)
                    return stats
            else:
                return throw("Invalid date range for Monthly payroll.The range should be greater than working days")
        return None





def on_payroll_processor_submit(dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    processor = Process_Payroll.payroll_processor_initializer (dbms=dbms, object=object)
    if not processor:
        return throw ("Something went wrong while processing Payroll")
    object.body.total_successful_payslips = processor.successful
    object.body.total_failed_payslips = processor.failed
    object.body.transaction_journal = processor.journal
    object.body.is_previous = 1
    active_processors = core_hr.get_list ("Payroll_Processor", filters={"is_previous": 1, "status": "Submitted"})
    if active_processors:
        for ap in active_processors:
            ap.is_previous = 2
            r =dbms.update ("Payroll_Processor", update_submitted = True)
            pp ("<<<<<<<<<<========================>>>>>>>>>>>>>>>>UPDATATATE", r)
    pp (object.body)

