from controllers.utils.data_conversions import DataConversion
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.payroll import Core_Payroll
from controllers.core_functions.hr import Core_Hr
from controllers.print_controller import Print_Controller
from dateutil.relativedelta import relativedelta

from datetime import timedelta
from controllers.mailing import Mailing
from calendar import monthrange

utils = Utils ()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw

class Process_Payroll:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.core_payroll = Core_Payroll (self.dbms)
        self.core_hr = Core_Hr (self.dbms)
        # self.config = self.core_payroll.payroll_config ()
        self.payroll_processor = object.body
        self.from_date = self.payroll_processor.from_date
        self.to_date = self.payroll_processor.to_date
        self.failed_employees = []
        self.number_of_gen_payslips = 0
        self.created_payslips = 0
        self.number_of_payslips = 0
        self.email_queue = []
        self.employee_query = """
            SELECT
                CAST(replace(employee.basic_pay::text, ',', '') AS numeric) AS basic_pay,
                employee.name,
                employee.id,
                employee.full_name,
                employee.first_name,
                employee.middle_name,
                employee.email,
                employee.last_name,
                employee.bank_name,
                employee.account_no,
                employee.sort_code,
                employee.tpin,
                employee.date_of_joining,
                employee.last_day_of_work,
                employee.department_id,
                employee.employment_type_id,
                employee.employee_grade_id,
                employee.working_days,
                employee.working_hours,
                employee.designation_id,
                employee.inable_probation,
                employee.is_separated,
                employee.is_separated_emp_paid,
                jsonb_path_query_array(employee.deductions, '$[*].deduction') AS deductions,
                jsonb_path_query_array(employee.earnings, '$[*].earning') AS earnings,
                d.name AS designation,
                dept.name AS department,
                emptype.name AS employment_type,
                sg.name AS employee_grade,
                tb.name AS tax_band
            FROM employee
            LEFT JOIN designation d ON employee.designation_id = d.id
            LEFT JOIN employment_type emptype ON employee.employment_type_id = emptype.id
            LEFT JOIN employee_grade sg ON employee.employee_grade_id = sg.id
            LEFT JOIN department dept ON employee.department_id = dept.id
            LEFT JOIN income_tax_band tb ON employee.tax_band_id = tb.id;
        """

        self.employees = self.fetch_data_from_sql (self.employee_query)
        self.employee_dict = utils.array_to_dict (self.employees or [], "name")
        self.deductions_data = self.core_payroll.get_deduction_components (fetch_linked_tables=True)
        self.earnings_data = self.core_payroll.get_earning_components (fetch_linked_tables=True)
        self.decimals = dbms.system_settings.currency_decimals
        hr_settings = self.core_hr.get_company_settings (self.core_hr.company)
        self.hr_settings_working_days = DataConversion.safe_get (hr_settings, "working_days", 22)
        self.successful = 0
        self.failed = 0

    def fetch_data_from_sql (self, query):
        result = self.dbms.sql(query)
        return result.data if result.status == utils.ok else []

    def validate_date_range(self, from_date, to_date, frequency):

        if not from_date or not to_date or from_date > to_date:
            raise throw ("Invalid date range")

        days_diff = (to_date - from_date).days + 1

        if frequency == "Weekly":
            if from_date.weekday() != 0 or to_date.weekday() != 6:
                return False

            total_weeks = days_diff // 7
            if days_diff % 7 != 0:
                return False

            for week_start in (from_date + timedelta(days=7 * i) for i in range(total_weeks)):
                week_days = [week_start + timedelta(days=i) for i in range(7)]
                working_days = [d for d in week_days if d.weekday() < 5]
                if len(working_days) < self.hr_settings_working_days_per_week:
                    return False

            return True
        elif frequency == "Monthly":
            current = from_date
            while current <= to_date:
                start_day = current.replace(day=1)
                end_day = current.replace(day=monthrange(current.year, current.month)[1])

                actual_start = max(from_date, start_day)
                actual_end = min(to_date, end_day)

                days_in_month = (actual_end - actual_start).days + 1
                if days_in_month < self.hr_settings_working_days:
                    return False

                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)
            return True
        else:
            throw("Invalid frequency: expected 'Weekly' or 'Monthly'")

    def process_payroll(self, curr_from_date, curr_to_date):
        number_of_payslips = 0
        number_of_gen_payslips = 0
        created_payslips = []

        for emp_salary_info in self.payroll_processor.employee_info:
            emp_name = emp_salary_info.employee

            if str(emp_name).lower() == "totals":
                continue

            basic_pay = DataConversion.convert_to_float(DataConversion.safe_get(emp_salary_info, "basic_pay", 0.00))
            if basic_pay <= 0.00:
                self.failed_employees.append({
                    "employee": emp_name,
                    "reason": "Zero Basic Pay",
                    "error_occurred": f"{emp_name}'s basic pay is zero or not found"
                })
                continue

            employee = self.employee_dict.get(emp_name)
            if not employee:
                self.failed_employees.append({
                    "employee": emp_name,
                    "reason": "Employee Not Found",
                    "error_occurred": f"{emp_name} not active or missing in the system"
                })
                continue

            try:
                existing = self.dbms.get_list(
                    "Payslip",
                    filters={"status__in": ["Submitted"], "employee": emp_name, "from_date": curr_from_date, "to_date": curr_to_date},
                )

                if existing.status != utils.no_content:
                    self.failed_employees.append({
                        "employee": emp_name,
                        "reason": "Payslip Already Exists",
                        "error_occurred": f"{emp_name} already has a payslip for this period"
                    })
                    continue

                number_of_payslips += 1

                if not (employee.date_of_joining <= curr_to_date):
                    self.failed_employees.append({
                        "employee": emp_name,
                        "reason": "Date of Joining",
                        "error_occurred": f"{emp_name} joined after current period"
                    })
                    continue

                employee.leave_summary = self.core_hr.emp_leave_annual_days(emp_name)
                employee.payslip_analytics = utils.from_dict_to_object(self.core_hr.get_payslip_analytics(emp_name))
                payslip = utils.from_dict_to_object({})

                payslip.status = "Submitted"
                payslip.docstatus = 1
                payslip.posting_date = dates.today()
                payslip.posting_time = dates.timestamp()
                payslip.from_date = curr_from_date
                payslip.to_date = curr_to_date
                payslip.reporting_currency = "ZMW"
                payslip.currency = self.payroll_processor.currency
                payslip.convertion_rate = self.payroll_processor.convertion_rate
                payslip.years_in_service = dates.calculate_time_period(DataConversion.convert_datetime_to_string (DataConversion.safe_get (employee, "date_of_joining", dates.today ()), fmt="%Y-%m-%d"),dates.today())
                payslip.employee = emp_name
                payslip.company = self.core_hr.company
                payslip.employee_names = DataConversion.safe_get (employee, "full_name", f"""{DataConversion.safe_get (employee, 'first_name', '')} {DataConversion.safe_get (employee, 'middle_name', '')} {DataConversion.safe_get (employee, 'last_name', '')}""")
                payslip.department = employee.department
                payslip.designation = employee.designation
                payslip.employment_type = employee.employment_type
                payslip.bank_name = employee.bank_name
                payslip.bank_account_no = employee.account_no
                payslip.tax_identification_no = employee.tpin
                payslip.tax_band = employee.tax_band
                payslip.payroll_frequency = self.payroll_processor.frequency
                payslip.working_days = DataConversion.convert_to_float(DataConversion.safe_get(employee, "working_days", self.hr_settings_working_days))
                payslip.basic_pay = utils.fixed_decimals(basic_pay, self.decimals)
                payslip.gross = utils.fixed_decimals(DataConversion.convert_to_float(DataConversion.safe_get(emp_salary_info, "gross", 0.00)))
                payslip.net = utils.fixed_decimals(DataConversion.convert_to_float(DataConversion.safe_get(emp_salary_info, "net", 0.00)))
                payslip.payroll_processor = self.payroll_processor.name
                payslip.total_earnings = basic_pay
                payslip.total_deductions = 0.00
                payslip.advance_amount = 0
                payslip.advance_repaid = 0
                payslip.overtime = 0
                payslip.total_advance_repaid = 0
                payslip.earnings = [{"earning": "Basic", "amount": basic_pay}]
                if self.earnings_data:
                    for earning in self.earnings_data:
                        name = DataConversion.safe_get (earning, "resenting")
                        val = DataConversion.convert_to_float(getattr(emp_salary_info, earning.name)) or 0.00
                        if val > 0:
                            r = self.core_payroll.repay_loan_and_other_deduction (repayment_amount=ded, emp=emp_name, sc=earning.name)
                            rp_trp = 0
                            remaining_amount = 0
                            if r and isinstance (r, dict):
                                rp_trp = DataConversion.safe_get (r, "remaining_period")
                                remaining_amount = DataConversion.safe_get (r, "remaining_amount")
                            payslip.earnings.append({"earning": name if name else earning.name, "amount": val, "units": DataConversion.safe_get (earning, "units", "")})
                            payslip.total_earnings += utils.fixed_decimals (DataConversion.convert_to_float(val), self.decimals)

                payslip.deductions = []
                if self.deductions_data:
                    for deduction in self.deductions_data:
                        ded = DataConversion.convert_to_float(getattr(emp_salary_info, deduction.name)) or 0.00
                        if ded > 0:
                            r = self.core_payroll.repay_loan_and_other_deduction (repayment_amount=ded, emp=emp_name, sc=deduction.name)
                            rp_trp = 0
                            remaining_amount = 0
                            if r and isinstance (r, dict):
                                rp_trp = DataConversion.safe_get (r, "remaining_period")
                                remaining_amount = DataConversion.safe_get (r, "remaining_amount")
                            if DataConversion.safe_get (deduction, "name") == "Pension (PLA)":
                                payslip.ytd_pla = ded
                            if DataConversion.safe_get (deduction, "is_advance", 0) or DataConversion.safe_get (deduction, "is_private_pension", 0):
                                r = self.dbms.create ("Advance_And_Pension_Entries", utils.from_dict_to_object ({
                                    "posting_date": str (self.to_date),
                                    "ref_doc": "Payroll_Processor",
                                    "ref": DataConversion.safe_get (self.payroll_processor, "name"),
                                    "salary_component": DataConversion.safe_get (deduction, "name"),
                                    "amount_saved": ded,
                                    "is_recovered": 0
                                }))

                                if DataConversion.safe_get (deduction, "is_advance", 0):
                                    DataConversion.safe_set (payslip, "advance_repaid", utils.fixed_decimals (DataConversion.convert_to_float(ded), self.decimals))
                                else:
                                    DataConversion.safe_set (payslip, "pension_paid", utils.fixed_decimals (DataConversion.convert_to_float(ded), self.decimals))
                            name = DataConversion.safe_get (earning, "resenting")
                            payslip.deductions.append({"deduction": name if name else deduction.name, "amount": utils.fixed_decimals(ded), "outstanding": rp_trp, "balance": remaining_amount, "units": DataConversion.safe_get (deduction, "unites")})
                            payslip.total_deductions += utils.fixed_decimals (DataConversion.convert_to_float(ded), self.decimals)

                if employee.tax_band:
                    tax = DataConversion.convert_to_float(getattr(emp_salary_info, employee.tax_band))
                    if tax >= 0:
                        payslip.total_tax_amount = utils.fixed_decimals(tax, self.decimals)
                        payslip.total_deductions += payslip.total_tax_amount
                        payslip.deductions.append({"deduction": employee.tax_band, "amount": payslip.total_tax_amount})

                remaining_days = DataConversion.convert_to_float (DataConversion.safe_get(employee.leave_summary, "remaining_leave_days", 0.00))
                working_days = DataConversion.convert_to_float (DataConversion.safe_get(employee, "working_days", self.hr_settings_working_days))
                leave_value_per_day = DataConversion.convert_to_float (payslip.basic_pay) / working_days

                payslip.current_leave_days = remaining_days
                payslip.current_leave_value = utils.fixed_decimals(leave_value_per_day * remaining_days, self.decimals)

                ytd_days = DataConversion.convert_to_float(DataConversion.safe_get(employee.leave_summary, "total_days", 0.00))
                payslip.ytd_leave_days = ytd_days
                payslip.ytd_leave_value = utils.fixed_decimals(ytd_days * leave_value_per_day, self.decimals)

                analytics = employee.payslip_analytics
                payslip.ytd_gross = utils.fixed_decimals(float(analytics.get("overall_gross", 0)) + float(payslip.gross), self.decimals)
                payslip.ytd_net = utils.fixed_decimals(float(analytics.get("overall_net", 0)) + float(payslip.net), self.decimals)
                payslip.ytd_earnings = utils.fixed_decimals(float(analytics.get("overall_earnings", 0)) + float(payslip.total_earnings), self.decimals)
                payslip.ytd_deductions = utils.fixed_decimals(float(analytics.get("overall_deductions", 0)) + float(payslip.total_deductions), self.decimals)
                payslip.ytd_tax = utils.fixed_decimals(float(analytics.get("overall_tax", 0)) + float(payslip.total_tax_amount), self.decimals)
                
                new_payslip = self.dbms.create("Payslip", payslip)
                # pp(payslip)
                if new_payslip.status == utils.ok:
                    created_payslips.append(new_payslip.name)
                    number_of_gen_payslips += 1

                    email = DataConversion.safe_get(employee, "email", None)
                    if email:
                        self.email_queue.append (utils.from_dict_to_object ({
                            "email": email,
                            "doc": new_payslip.data
                        }))
                else:
                    self.failed_employees.append({
                        "employee": emp_name,
                        "reason": "Payslip Creation Failed",
                        "error_occurred": str(new_payslip.message)
                    })

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.failed_employees.append({
                    "employee": emp_name,
                    "reason": "Unhandled Exception",
                    "error_occurred": str(e)
                })

        self.successful = number_of_gen_payslips
        self.failed = number_of_payslips - number_of_gen_payslips if number_of_payslips > number_of_gen_payslips else 0
        pp (self.failed_employees)
        pp(f"Payslips processed: {number_of_payslips}, created: {number_of_gen_payslips}, failed: {len(self.failed_employees)}")

    def send_emails (self):
        # if self.config:
        # DataConversion.convert_to_float (DataConversion.safe_get (self.config, "auto_send_emails", 0)):
        mailing = Mailing(self.dbms)
        if self.email_queue and len (self.email_queue) > 0:
            for doc in self.email_queue:
                payslip = doc.doc
                email = doc.email
                try:
                    core_print = Print_Controller(
                        request=self.dbms.validation,
                        model="Payslip",
                        print_format="Payslip Standard Format",
                        doc=payslip.name
                    )
                    # etry = entry = "app" if md.wrapper_module == "client_app" else "app"
                    # payslip.doc_url = f"""https://{self.dbms.host}/{etry}/{md.module}/{md.app}?module={md.module}&app={md.app}&page=info&content_type={md.content_type}&doc={doc_name}"""
                    doc_print = core_print.generate_print_doc(skip_validation=True, is_internal_processing=True)
                    pp(doc_print)
                    formatted = payslip.to_date.strftime("%B %Y")
                    company = payslip.linked_fields.company
                    content = f"""
                        <div style="max-width: 100%;">
                            <h2 style="color: {company.default_theme_color}; font-size: 1.5rem">Dear {payslip.employee_names},</h2>
                            <p style="font-size: 15px; line-height: 1.6; margin-top: 20px;">
                                We are pleased to inform you that your salary for the period <strong style="color: {company.default_secondary_color}">{payslip.from_date} - {payslip.to_date}</strong> has been successfully processed.
                                <br />
                                Your payslip for this period has been attached to this email. It includes a breakdown of your basic pay, total earnings, deductions, and net pay.
                                <br />
                                Please review the attached document carefully. If you have any questions or notice any discrepancies, feel free to reach out to the Human Resources department for assistance.
                                <br />
                                We sincerely appreciate your hard work, dedication, and the value you continue to bring to the organization.
                                <br />
                                <br />
                                <br />
                                Warm regards,
                                <p>Human Resources Department</p>
                            </p>
                        </div>
                    """
                    # mail = mailing.send_mail(email, f"Payslip - {payslip.from_date}", body=Default_Template.template(content,f"Payslip – {formatted}",company), attachment=doc_print.data,model="Payslip", skip_queuing=True)
                    # pp("Mail =>",mail.status)
                except Exception as e:
                    self.failed_employees.append({
                        "employee": payslip.employee,
                        "reason": "Email Sending Failed",
                        "error_occurred": str(e)
                    })

    def on_payroll_processor_cancel(self):
        payroll_processor = object.body
        payslips = self.core_hr.get_list ("Payslip", filters={"payroll_processor": payroll_processor.name})
        if payslips:
            payslip_ids =  utils.get_list_of_dicts_column_field(payslips, "id")
            self.dbms.cancel_doc ("Payslip", payslip_ids)

        if payroll_processor.employee_info and len (payroll_processor.employee_info) > 0:
            for emp in payroll_processor.employee_info:
                employee = self.core_hr.get_doc ("Employee", emp.employee)
                if employee:
                    if str (employee.status).lower () != "active":
                        employee.is_separated_emp_paid = "Unsettled"
                        self.dbms.update ("Employee", employee, update_submitted=True)

    @classmethod
    def payroll_processor_initializer(cls, dbms, obj, payslips=True):
        instance = cls(dbms, obj)

        stats = utils.from_dict_to_object({
            "failed": 0,
            "successful": 0,
            "failed_employees": [],
        })

        if not instance.employees and not instance.employee_dict:
            throw ("Failed: No Employees Found! Create Some Employees")
        
        if not payslips:
            return None

        freq = instance.payroll_processor.frequency

        if freq == "Monthly":
            if instance.validate_date_range(instance.payroll_processor.from_date, instance.payroll_processor.to_date, "Monthly"):
                from_date = instance.payroll_processor.from_date
                to_date = instance.payroll_processor.to_date

                rd = relativedelta(to_date, from_date)
                months_between = rd.years * 12 + rd.months + 1

                for i in range(months_between):
                    current_from_date = from_date + relativedelta(months=i)
                    current_to_date = min(
                        to_date,
                        current_from_date + relativedelta(months=1) - timedelta(days=1)
                    )
                    instance.process_payroll(current_from_date, current_to_date)
                    # instance.send_emails ()
                    stats.failed += int(instance.failed)
                    stats.successful += int(instance.successful)
                DataConversion.safe_set (stats, "failed_employees", instance.failed_employees)
                return stats
            else:
                instance.on_payroll_processor_cancel ()
                throw ("Invalid date range for Monthly payroll. The range should be greater than working days.")
        else:
            instance.on_payroll_processor_cancel ()
            throw (f"Invalid payroll frequency: {freq}")

        return stats