from controllers.utils import Utils
from datetime import datetime
from controllers.utils.dates import Dates
from analytics.payroll import Payroll_Analytics
from controllers.utils.data_conversions import DataConversion
utils = Utils()
dates = Dates()
pp = utils.pretty_print

class Core_Payroll:
    def __init__(self,dbms,object=None):
        self.dbms = dbms
        self.object = object
        self.payroll_analytics = Payroll_Analytics(dbms=dbms, object=object)
        
        self.system_settings = dbms.system_settings.linked_fields
        self.reporting_currency = self.system_settings.default_company.linked_fields.reporting_currency.name
        self.company = self.dbms.current_user.default_company if self.dbms.current_user.default_company else self.system_settings.default_company.name

    def payroll_config (self):
        return self.get_doc ("Payroll_Setup", self.company)

    def repay_loan_and_other_deduction (self, repayment_amount:float, emp:str, repayment_method:str="Payroll", ref=None, doc=None, sc=None):
        try: 
            get_dues = []
            r_dict = {}
            if repayment_method.lower () == "cash":
                get_dues = self.get_list ("Payroll_Activity_Entry", filters={
                    "cleared": 0,
                    "balance__gt": 0,
                    "reference_type": ref,
                    "reference": doc,
                    "employee": emp,
                })
            else:
                get_dues = self.get_list ("Payroll_Activity_Entry", filters={
                    "cleared": 0,
                    "balance__gt": 0,
                    "employee": emp,
                    "salary_component": sc,
                }, order_by=['id'])
            if len (get_dues) <= 0:
                return utils.respond (utils.unprocessable_entity, f"No Repayment to be made for {emp} on { str (ref).capitalize ().replace ("_", " ") if ref else sc}")
            balance = DataConversion.convert_to_float(repayment_amount)
            for due in get_dues:
                if DataConversion.safe_e (balance, 0, int):
                    break
                due_loan_amount = DataConversion.convert_to_float (DataConversion.safe_get (due, "balance", 0))
                
                if due_loan_amount > balance:
                    DataConversion.safe_set (due, "balance", due_loan_amount-balance)
                    balance = 0
                else:
                    balance -= due_loan_amount
                    DataConversion.safe_set (due, "balance", 0)
                    DataConversion.safe_set (due, "cleared", 1)

                r = self.dbms.update ("Payroll_Activity_Entry", due, update_submitted=True)
                if r.status == utils.ok:
                    DataConversion.safe_set (r_dict, "msg", "Successfully Repaid")
                    DataConversion.safe_set (r_dict, "remaining_period", DataConversion.convert_to_int (DataConversion.safe_get (due, "remaining_period", 0)))
                    DataConversion.safe_set (r_dict, "remaining_amount", DataConversion.convert_to_int (DataConversion.safe_get (due, "remaining_balance", 0)))

            return utils.respond (utils.ok, r_dict)

        except Exception as e:
            pp (f"ERROR in Loan Repayment: {e}")
            return utils.respond (utils.unprocessable_entity, f"{e}")

    def fetch_data_from_sql (self, query,params=None, fetch='all'):
        result = self.dbms.sql(query, params=params,fetch=fetch)
        return result.data if result.status == utils.ok else []

    def notify_payroll (
        self,
        employee_number,
        amount,
        sc,
        doc_type,
        doc_name,
        length_or_period=1,
        effective_date=dates.get_last_date_of_current_month (),
        allows_cash_repayment=True,
        posting_date=dates.today (),
        entry_type="Deduction",
        salary_advance_type="N/A"
    ):
        """
            1. employee_number ==> Employee ID/No
            2. amount ==> Requested Amount
            3. length_or_period ==> repayment period
            4. effective_date ==> repayment Start Date
            5. allows_cash_repayment ==>
            6. doc_type ==> Reference Type
            7. doc_name ==> referent Document/ID/Name
            8. sc ==> Salary Component
            9. posting_date ==> posting date
            10. entry_type ==> Deduction/Earning
            11. salary_advance_type ==> First/Second
        """
        try:
            amount = DataConversion.convert_to_float (amount)
            length_or_period = DataConversion.convert_to_int (length_or_period)
            if not employee_number:
                return utils.respond (utils.unprocessable_entity, "Employee No is <strong class='text-rose-600'>Required</strong>")
            emp = self.get_doc ("Employee", employee_number)
            if not emp:
                return utils.respond (utils.unprocessable_entity, f"Employee with No {employee_number} <strong class='text-rose-600'>Was Not Found</strong>")
            if not amount:
                return utils.respond (utils.unprocessable_entity, "Amount is <strong class='text-rose-600'>Required</strong>")
            if not sc:
                return utils.respond (utils.unprocessable_entity, "Salary Component is <strong class='text-rose-600'>Required</strong>")
            if not doc_type:
                return utils.respond (utils.unprocessable_entity, "Doc Type is <strong class='text-rose-600'>Required</strong>")
            if not doc_name:
                return utils.respond (utils.unprocessable_entity, "Doc Name is <strong class='text-rose-600'>Required</strong>")
            
            npo = utils.from_dict_to_object ()
            
            monthly_pay = amount / length_or_period
            last_payment_date = dates.add_days (dates.today (), 30 * length_or_period)
            track = 0

            for i in range(length_or_period):
                is_second = 0
                curr_per = (i+1)
                if DataConversion.safe_e (salary_advance_type, 'second', str, True):
                    is_second = 1
                acq_balance = amount - (monthly_pay * curr_per)
                DataConversion.safe_set (npo, "employee", employee_number)
                DataConversion.safe_set (npo, "salary_component", sc)
                DataConversion.safe_set (npo, "amount", amount)
                DataConversion.safe_set (npo, "monthly_payment", monthly_pay)
                DataConversion.safe_set (npo, "length_or_period", length_or_period)
                DataConversion.safe_set (npo, "effective_date", effective_date)
                DataConversion.safe_set (npo, "allows_cash_repayment", allows_cash_repayment)
                DataConversion.safe_set (npo, "reference_type", doc_type)
                DataConversion.safe_set (npo, "reference", doc_name)
                DataConversion.safe_set (npo, "remaining_balance", acq_balance)
                DataConversion.safe_set (npo, "balance", monthly_pay)
                DataConversion.safe_set (npo, "remaining_period", length_or_period - curr_per)
                DataConversion.safe_set (npo, "last_payment_date", last_payment_date)
                DataConversion.safe_set (npo, "posting_date", posting_date)
                DataConversion.safe_set (npo, "cleared", 0)
                DataConversion.safe_set (npo, "salary_advance_type", salary_advance_type)
                DataConversion.safe_set (npo, "is_second", is_second)
                DataConversion.safe_set (npo, "entry_type", entry_type)
                DataConversion.safe_set (npo, "month", DataConversion.get_date_part (posting_date))
                r = self.dbms.create ("Payroll_Activity_Entry", npo)
                pp(r)
                if r.status == utils.ok:
                    track += 1
            if track == length_or_period:
                return utils.respond (utils.ok, "Registered Successfully")
            return utils.respond (utils.unprocessable_entity, "An Error Occurred!")

        except Exception as e:
            pp (f"Error: {e}")
            return utils.respond (utils.unprocessable_entity, f"An Error Occurred!: {e}")

    def get_payroll_setup(self,company, fetch_linked_fields=False, fetch_linked_tables=False):
        return self.dbms.get_doc("Payroll_Setup", company, privilege=True, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)

    def get_list (self, model: str, filters={}, fetch_linked_tables=False, fetch_linked_fields=False,privilege=False, order_by=[], limit=None):
        list = self.dbms.get_list (model, filters=filters, fetch_linked_tables=fetch_linked_tables, fetch_linked_fields=fetch_linked_fields, privilege=privilege, order_by=order_by, limit=limit)
        if list.status == utils.ok:
            return list.data.rows
        return []
    def get_doc (self, model: str, name: str):
        list = self.dbms.get_doc (model, name)
        if list.status == utils.ok:
            return list.data
        return None
    def get_is_statutory_component (self):
        return self.get_list ("Salary_Component", {"is_statutory_component": 1, "disabled": 0, })

    def get_earning_components(self, fetch_linked_fields=False, fetch_linked_tables=False):
        comp = []
        components = self.dbms.get_list("Salary_Component",filters={ "component_type": "Earning", "disabled": 0 },fetch_linked_fields=fetch_linked_fields,fetch_linked_tables=fetch_linked_tables) 
        if components.status == utils.ok:
            comp = components.data.rows
        return comp
    
    def get_deduction_components(self, fetch_linked_fields=False, fetch_linked_tables=False):
        comp = []
        components = self.dbms.get_list("Salary_Component",filters={ "component_type": "Deduction", "disabled": 0 },fetch_linked_fields=fetch_linked_fields,fetch_linked_tables=fetch_linked_tables) 
        if components.status == utils.ok:
            comp = components.data.rows
        return comp
    
    def get_employee_leave_info(self,employee):
        res = {
            "current_leave_days": 0,
            "current_leave_value": 0,
            "ytd_leave_days": 0,
            "ytd_leave_value": 0
        }
                
        return utils.respond(utils.ok,res)
    
    def get_ytd_data(self, employee):
        first_date = dates.get_first_date_of_current_year()
        ytd = utils.from_dict_to_object({ "ytd_gross":0, "ytd_net":0, "ytd_earnings":0, "ytd_deductions":0, "ytd_tax":0, })
        ytd_slips = self.dbms.get_list("Payslip",filters={"created_on__gt":first_date,"employee":employee })
        if ytd_slips.status == utils.ok:
            for slip in ytd_slips.get("data").get("rows"):
                slp = utils.from_dict_to_object(slip)
                ytd.ytd_gross += slp.ytd_gross
                ytd.ytd_net += slp.ytd_net
                ytd.ytd_earnings += slp.ytd_earnings
                ytd.ytd_deductions += slp.ytd_deductions
                ytd.ytd_tax += slp.ytd_tax
        return utils.respond(utils.ok,utils.from_object_to_dict(ytd))
        

    def get_overall_accrued_overtime(self):
        total_hours = 0.00
        total_accrued_overtime = 0
        total_accrued_hour = 0  # Initialize total_accrued_hour here
        
        overtime_list = self.dbms.get_list("Overtime", filters={"docstatus": 1})
        if overtime_list.status == utils.ok:
            for overtime in overtime_list.data.rows:
                if overtime.is_paid == 0:
                    start_time = datetime.strptime(overtime.start_time, "%H:%M")
                    end_time = datetime.strptime(overtime.end_time, "%H:%M")
                    time_diff = end_time - start_time
                    total_hours += time_diff.total_seconds() / 3600
                total_accrued_hour = round(total_hours, 2)
            
            overtime_setup = self.dbms.get_list("Overtime_Configuration", filters={"docstatus": 0})
            if overtime_setup.status == utils.ok:
                for setup in overtime_setup.data.rows:
                    if setup.calculation_type == "Fixed Rate":
                        total_minutes_worked = total_hours * 60
                        total_accrued_overtime = total_minutes_worked * (int(setup.fixed_rate) / 60) 
                    elif setup.calculation_type == "Salary Based":
                        employees_info = self.dbms.get_list("Employee")
                        if employees_info.status == utils.ok:
                            for employee in employees_info.data.rows:
                                employee_salary = float(employee.get('basic_pay'))
                                working_days = float(employee.get('working_days'))
                                number_of_hours = float(employee.get('working_hours'))
                                overtimes = self.dbms.get_list("Overtime", filters={"applicant": employee['name'], "docstatus": 1})
                                if overtimes.status == utils.ok:
                                    for emp_overtime in overtimes.data.rows:
                                        if emp_overtime.is_paid == 0:
                                            start_time = datetime.strptime(emp_overtime.start_time, "%H:%M")
                                            end_time = datetime.strptime(emp_overtime.end_time, "%H:%M")
                                            time_diff = end_time - start_time
                                            total_hours += time_diff.total_seconds() / 3600
                                            total_hours_worked = working_days * number_of_hours
                                            per_rate = employee_salary / total_hours_worked
                                            earning = total_hours * per_rate
                                            total_accrued_overtime += earning
        else:
            total_accrued_hour = 0  
            total_accrued_overtime = 0 
            
        total_accrued = round(total_accrued_overtime, 2)
        res = {"total_accrued_hours": total_accrued_hour, "total_accrued_overtime": total_accrued}
        return utils.respond(utils.ok, res)


    def get_advance_stat (self):
        entries = self.get_list ("Payroll_Activity_Entry", filters={
            "salary_component": "Salary Advance",
        })
        if entries:
            advance = self.payroll_analytics.analyze_advance_data (data=entries)
            return advance
        return None
    
    def get_overtime_configuration(self):
        res = {}
        overtime_setup = self.dbms.get_list("Overtime_Configuration", filters={"docstatus": 1})
        if overtime_setup.status == utils.ok:
            data =  overtime_setup.data.rows
            res = data[0]
        return res
    
    def generate_payslips (self, refs):
        """
            refs = {
                reporting_currency,
                currency,
                from_date,
                to_date,
                convertion_rate,
                frequency,
                processor,
                decimals,
                earnings_data,
                deductions_data,
                employee:{
                    name,
                    first_name,
                    middle_name,
                    last_name,
                    department,
                    designation,
                    company,
                    employment_type,
                    bank_name,
                    account_no,
                    tpin,
                    tax_band,
                    working_days,
                    payslip_analytics,
                    leave_summary,
                }
                salary_info: {
                    basic_pay,
                    gross,
                    net,

                }
            }
        """
        refs = utils.from_dict_to_object (refs)
        payslip = utils.from_dict_to_object ({})
        payslip.status = "Submitted"
        payslip.docstatus = 1
        payslip.posting_date = dates.today()
        payslip.posting_time = dates.timestamp()
        payslip.from_date = refs.from_date
        payslip.to_date = refs.to_date
        payslip.reporting_currency = refs.reporting_currency
        payslip.currency = refs.currency
        payslip.convertion_rate = refs.convertion_rate
        payslip.employee = refs.employee.name
        payslip.company = refs.employee.company
        payslip.employee_names = f"{refs.employee.first_name or ''} {refs.employee.middle_name or ''} {refs.employee.last_name or ''}"
        payslip.department = refs.employee.department
        payslip.designation = refs.employee.designation
        payslip.employment_type = refs.employee.employment_type
        payslip.bank_name = refs.employee.bank_name
        payslip.bank_account_no = refs.employee.account_no
        payslip.tax_identification_no = refs.employee.tpin
        payslip.tax_band = refs.employee.tax_band
        payslip.payroll_frequency = refs.frequency
        payslip.working_days = refs.employee.working_days
        payslip.basic_pay = utils.fixed_decimals(float(refs.salary_info.basic_pay), refs.decimals)
        payslip.gross = utils.fixed_decimals(float(refs.salary_info.gross))
        payslip.net = utils.fixed_decimals(float(refs.salary_info.net))
        payslip.payroll_processor = refs.processor
        payslip.total_deductions = 0.00
        payslip.advance_amount = 0
        payslip.advance_repaid = 0
        payslip.total_advance_repaid = 0
        payslip.earnings = [{"earning":"Basic","amount":refs.salary_info.basic_pay}]
        payslip.deductions = []
        payslip.years_in_service = dates.calculate_time_period(str(refs.employee.date_of_joining),str(dates.today()))
        payslip.total_earnings = utils.fixed_decimals(float(payslip.basic_pay or 0), refs.decimals)
        payslip.total_tax_amount = 0
        leave_summary =  refs.employee.leave_summary.overall_totals
        remaining_days =  float(leave_summary.remaining_days or 0)
        emp_working_days =float(refs.employee.working_days or 0)
        emp_basic_salary =float(refs.salary_info.basic_pay or 0)
        leave_value_per_day = 0
        if leave_value_per_day > 0:
            leave_value_per_day = utils.fixed_decimals(emp_basic_salary / emp_working_days,refs.decimals)
        leave_value =  utils.fixed_decimals(leave_value_per_day * remaining_days,refs.decimals)
        rounded_leave_value = leave_value
        payslip.current_leave_days = leave_summary.remaining_days
        payslip.current_leave_value = rounded_leave_value
        payslip.ytd_leave_days = leave_summary.total_days
        ytd_leave_days =  float(leave_summary.total_days or 0)
        ytd_leave_days_value = utils.fixed_decimals(ytd_leave_days * leave_value_per_day, refs.decimals)
        payslip.ytd_leave_value = ytd_leave_days_value
        if refs.earnings_data:
            for earning in refs.earnings_data:
                en = getattr(refs.employee,earning.name, 0.00)
                if float(en or 0) >= 0:
                    payslip.total_earnings += float(en or 0)
                    payslip.earnings.append({"earning": earning.name, "amount":en or 0})
        if refs.deductions_data:
            for deduction in refs.deductions_data:
                ded = getattr(refs.employee, deduction.name, 0.00)
                if float(ded or 0) >= 0:
                    payslip.total_deductions += float(ded or 0)
                    payslip.deductions.append({"deduction":deduction.name,"amount":utils.fixed_decimals(float(ded or 0))})
        if refs.employee.tax_band:
            band = getattr(refs.employee, refs.employee.tax_band, 0.00)
            if float(band or 0) >= 0:
                payslip.total_tax_amount = utils.fixed_decimals(float(band or 0), refs.decimals)
                payslip.total_deductions += utils.fixed_decimals(float(band or 0), refs.decimals)
                payslip.deductions.append({"deduction": refs.employee.tax_band,"amount":utils.fixed_decimals(float(band or 0))} )

        payslip_analytics = refs.employee.payslip_analytics
        payslip.ytd_gross = utils.fixed_decimals(payslip_analytics.overall_gross + float(payslip.gross or 0), refs.decimals)
        payslip.ytd_net = utils.fixed_decimals(payslip_analytics.overall_net + float(payslip.net or 0), refs.decimals)
        payslip.ytd_earnings = utils.fixed_decimals(payslip_analytics.overall_earnings + float(payslip.total_earnings or 0), refs.decimals)
        payslip.ytd_deductions = utils.fixed_decimals(payslip_analytics.overall_deductions + float(payslip.total_deductions or 0), refs.decimals)
        payslip.ytd_tax = utils.fixed_decimals(payslip_analytics.overall_tax + float(payslip.total_tax_amount or 0), refs.decimals)

        return payslip

    def calculate_earning (self, earning_config, basic):
        vl = 0.00
        if earning_config and basic:
            vl = earning_config.fixed_amount if str (earning_config.value_type).lower () == "fixed amount" else (basic * earning_config.percentage) / 100
        return utils.fixed_decimals (vl, 2)
    
    def calculate_deduction (self, deduction, basic):
        vl = 0.00
        if deduction and basic:
            vl = deduction.fixed_amount if str (deduction.value_type).lower () == "fixed amount" else (basic * deduction.percentage) / 100
        return utils.fixed_decimals (vl, 2)

    def retirement_recalculation(self, body):
        salary_component ="Imprest Retirement"

        if body.retirement_type =="Petty Cash":
            doc_name ="petty_cash"
            salary_component ="Petty Cash Retirement"
        elif body.retirement_type =="Imprest Form-20-A":
            doc_name ="imprest_a"
        elif body.retirement_type =="Imprest Form-20-B":
            doc_name ="imprest_b"
        elif body.retirement_type =="Imprest Form-20-C":
            doc_name ="imprest_c"

        if not body[doc_name]: 
            utils.throw("no document was picked for the retirement, Please select the type 'Retirement Type' then the document on the newly displayed field.")

        model =body.retirement_type.replace(" ","_").replace("-","_")
        fetch_doc =self.dbms.get_doc(model, body[doc_name])
        if fetch_doc.status !=utils.ok:
            utils.throw(f"An error occerred while fetching the {body.retirement_type} document: {fetch_doc}")
        if not body.obtained_amount: 
            utils.throw("no document was picked for the retirement, Please select the type 'Retirement Type' then the document on the newly displayed field.")
        total_retired =0
        for item in body.areas_of_expense: 
            # if not item.expense_attachment: utils.throw(f"You must provide an attachment for each expense. {item.subsistance_allowance} has no attachment.")
            total_retired +=(float(item.usage_length) or 0* float(item.unit_price_of_usage) or 0)
        # pp(body)
        # utils.throw("......")
        # body.retired_amount =total_retired
        body.obtained_amount =float(fetch_doc.data.balance) or float(fetch_doc.data.requested_amount) 
        if not fetch_doc.data.requested_amount or fetch_doc.data.requested_amount ==0:
            utils.throw(f"You can not retire for a {model} that has an amount of 0.")
        body.balance_left =float(body.obtained_amount) -float(body.retired_amount)
        fetch_doc.data.balance = float(body.balance_left)


        if body.balance_left >0:
            fetch_doc.data.status ="Partially Retired"
            body.owed_to ="Examination Council of Zambia"
        elif body.balance_left <0:
            fetch_doc.data.status ="Over Retired"
            body.owed_to =f"Officer {body.employee_no}"
        else:
            fetch_doc.data.status ="Retired"
            DataConversion.safe_set (fetch_doc.data, "not_retired", 0)
            body.owed_to =""
        try:
            self.dbms.update(model, fetch_doc.data, update_submitted=True)
            if fetch_doc.data.status =="Partially Retired":
                notify_payroll =self.notify_payroll(
                    employee_number=DataConversion.safe_get (body, "employee_no"),
                    amount=DataConversion.safe_get (body, "balance_left"),
                    doc_type=DataConversion.safe_get (body, "retirement_type"),
                    doc_name=DataConversion.safe_get (body, doc_name),
                    length_or_period=DataConversion.safe_get (body, "requested_repayment_period", 1),
                    effective_date=dates.get_last_date_of_current_month (),
                    sc= salary_component
                )
        except Exception as e:
            utils.throw(f"An error occurred while updating the document, {body[doc_name]}: {e}" )

        return utils.from_dict_to_object({
            "status": fetch_doc.data.status,
            "body": body
        })