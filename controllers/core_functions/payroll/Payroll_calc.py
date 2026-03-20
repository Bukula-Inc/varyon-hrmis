from controllers.utils.data_conversions import DataConversion
from controllers.utils import Utils
from controllers.core_functions.payroll import Core_Payroll
# from controllers.core_functions.hr import Core_Hr
from datetime import datetime, timedelta
from collections import defaultdict
import json
import copy
import time

utils = Utils ()
pp = utils.pretty_print

def count_week_days(start_date, end_date, week_day=5):
    day_count = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < week_day:
            day_count += 1
        current += timedelta(days=1)
    return day_count


class DeductionCalculator:
    def calc_deduction(self, employee, employee_row, deduction):
        try:
            deduction_value = 0.0
            percentage = DataConversion.convert_to_float (DataConversion.safe_get(deduction, "percentage", 0.0))
            fixed_amount = DataConversion.convert_to_float (DataConversion.safe_get(deduction, "fixed_amount", 0.0))
            custom_share = DataConversion.convert_to_float (str(DataConversion.safe_get (deduction, "shared_deduction_custom")).lower ())
            if custom_share:
                percentage_offset = percentage or fixed_amount
                shared_emp_percent = DataConversion.convert_to_float (DataConversion.safe_get(deduction, "shared_deduction_custom_emp"))
                percentage = (percentage_offset / 100.0) * shared_emp_percent
            if DataConversion.safe_get (deduction, "has_ceiling") == 1:
                deduction_value = self.calculate_ceiling_deduction(
                    employee_row,
                    percentage,
                    DataConversion.safe_get (deduction, "apply_on"),
                    DataConversion.convert_to_float (DataConversion.safe_get(deduction, "ceiling_amount"))
                )
            elif custom_share and not fixed_amount:
                deduction_value = self.calculate_shared_deduction(
                    employee_row,
                    percentage,
                    custom_share,
                    DataConversion.safe_get (deduction, "apply_on")
                )
            else:
                if fixed_amount:
                    deduction_value = percentage if percentage else fixed_amount
                elif percentage:
                    base = self.get_base_value(employee_row, DataConversion.safe_get (deduction, "apply_on"))
                    deduction_value = (base * percentage) / 100.0

            return DataConversion.convert_to_float (deduction_value)

        except Exception as e:
            print("Error in calc_deduction:", str(e))
            return 0.0

    def calculate_shared_deduction(self, emp_row, deduction_percentage, shared_deduction_custom, apply_on):
        try:
            pp (deduction_percentage, shared_deduction_custom, apply_on)
            if not shared_deduction_custom:
                return 0.0

            base = self.get_base_value(emp_row, apply_on)
            return DataConversion.convert_to_float ((base * deduction_percentage) / 100.0)

        except Exception as e:
            print("Error in calculate_shared_deduction:", str(e))
            return 0.0

    def calculate_ceiling_deduction(self, employee_row, deduction_percentage, apply_on, ceiling_amount):
        try:
            if ceiling_amount <= 0:
                return 0.0

            base = self.get_base_value(employee_row, apply_on)
            ceiling = (base * deduction_percentage) / 100.0
            return min(ceiling, ceiling_amount)

        except Exception as e:
            print("Error in calculate_ceiling_deduction:", str(e))
            return 0.0

    def get_base_value(self, row, key):
        try:
            if key == "Basic":
                return getattr(row, "basic_pay", 0.0)
            elif key == "Gross":
                return getattr(row, "gross", 0.0)
            elif key == "Net":
                return getattr(row, "net", 0.0)
            else:
                return 0.0
        except Exception as e:
            print("Error getting base value:", str(e))
            return 0.0

class IncomeTaxCalculator:
    @staticmethod
    def calculate_income_tax_band(employee, employee_row, band):
        """
        Calculate income tax deduction based on salary bands and tax-free amount.

        Parameters:
            employee        : Dictionary containing employee data (must include 'tax_band')
            employee_row    : Dictionary containing employee's salary details
            band : Dictionary containing 'tax_band' info and bands

        Returns:
            Tax deduction amount (float)
        """
        if not DataConversion.safe_get (employee, 'tax_band', None) or not band:
            return 0.0

        tax_free_amount = DataConversion.convert_to_float (DataConversion.safe_get (band, 'tax_free_amount', 0))
        salary_bands = DataConversion.safe_get (band, 'salary_bands', [])

        if not isinstance(salary_bands, list) or not salary_bands:
            return 0.0

        sorted_bands = sorted(
            salary_bands,
            key=lambda b: DataConversion.convert_to_float (DataConversion.safe_get(b,'amount_from', 0))
        )

        deduct_on = DataConversion.safe_get(band, 'deduct_on', '').lower()
        deductible_amount = DataConversion.convert_to_float (DataConversion.safe_get (employee_row, deduct_on))

        if deductible_amount <= tax_free_amount:
            return 0.0

        deduction = 0.0
        cash_on_hand = deductible_amount - tax_free_amount
        end_calculations = False
        total_bands = len(sorted_bands) - 1

        for i, b in enumerate(sorted_bands):
            if end_calculations:
                break

            perc = DataConversion.convert_to_float (DataConversion.safe_get(b,'deduction_percentage', 0)) / 100.0

            amount_from = DataConversion.convert_to_float (DataConversion.safe_get(b,'amount_from', 0)) if DataConversion.is_number(DataConversion.safe_get(b,'amount_from')) else 0.0
            amount_to = DataConversion.safe_get(b,'amount_to', 0)
            if DataConversion.is_number(amount_to) and str(amount_to).lower() != "above":
                amount_to = DataConversion.convert_to_float (amount_to)
            else:
                amount_to = 0.0

            difference = utils.fixed_decimals (abs(amount_to - amount_from), 4)

            if cash_on_hand >= difference and i < total_bands:
                taxable_amount = difference
                cash_on_hand -= difference
            else:
                taxable_amount = cash_on_hand
                end_calculations = True

            tax_amount = taxable_amount * perc
            deduction += tax_amount

        return utils.fixed_decimals(deduction, 2)


class EarningCalculator:
    @staticmethod
    def calc_earning(emp, basic_pay, earning, paye):
        """
        Calculate earning for an employee based on percentage or fixed amount.

        Parameters:
            emp         : Employee object (not used here, kept for compatibility)
            basic_pay   : Basic pay amount (number)
            earning     : Dictionary with optional 'percentage' and 'fixed_amount' keys

        Returns:
            Calculated earning (float)
        """
        if not isinstance(basic_pay, (int, float)) or basic_pay < 0:
            raise ValueError("basic_pay must be a non-negative number.")

        if not isinstance(earning, dict):
            earning = {}

        percentage = DataConversion.convert_to_float (DataConversion.safe_get (earning, 'percentage', 0))
        fixed_amount = DataConversion.convert_to_float (DataConversion.safe_get (earning, 'fixed_amount', 0))

        if percentage > 0:
            earning_value = (basic_pay * percentage) / 100
        elif fixed_amount > 0:
            earning_value = fixed_amount
        else:
            earning_value = 0.0
        
        if DataConversion.safe_e (DataConversion.safe_get (earning, "exclude_on_statutory_deductions", 0), 1, int) and DataConversion.safe_e (DataConversion.safe_get (earning, "grossable", 0), 1, int):
            take_home = DataConversion.safe_get(paye, "take_home_percentage")
            earning_value = earning_value/(DataConversion.convert_to_float (take_home or 63)/100)
        return utils.fixed_decimals (earning_value, 2)

class PayrollCalculator:

    def __init__(self, dbms, data, from_date, to_date):
        self.dbms = dbms
        self.tb = []
        self.from_date = from_date
        self.to_date = to_date
        self.core_payroll = Core_Payroll (self.dbms)
        self.core_hr = "Core_Hr (self.dbms)"
        self.config = self.core_payroll.payroll_config ()
        self.payroll_processor = data
        self.failed_employees = []
        self.employee_query = """
            SELECT
                CAST(replace(employee.basic_pay, ',', '') AS numeric) AS basic_pay,
                employee.name,
                employee.id,
                employee.full_name,
                employee.first_name,
                employee.middle_name,
                employee.email,
                employee.last_name,
                employee.date_of_joining,
                employee.last_day_of_work,
                employee.working_days,
                employee.working_hours,
                employee.designation_id,
                employee.inable_probation,
                employee.is_separated,
                employee.is_separated_emp_paid,
                jsonb_path_query_array(employee.deductions, '$[*].deduction') AS deductions,
                jsonb_path_query_array(employee.earnings, '$[*].earning') AS earnings,
                dd.name AS designation,
                tb.name AS tax_band
            FROM employee
            LEFT JOIN designation dd ON employee.designation_id = dd.id
            LEFT JOIN income_tax_band tb ON employee.tax_band_id = tb.id
        """

        self.tax_band_query = """
            SELECT
                itb.name,
                itb.deduct_on,
                itb.tax_free_amount,
                tsb.amount_from,
                tsb.amount_to,
                tsb.deduction_percentage
            FROM income_tax_band itb
            LEFT JOIN income_tax_band_salary_bands itbsb ON itb.id = itbsb.income_tax_band_id
            LEFT JOIN taxable_salary_band tsb ON tsb.id = itbsb.taxable_salary_band_id
            WHERE itb.is_current::integer = 1;
        """
        tax_band = self.core_payroll.fetch_data_from_sql(self.tax_band_query)
        grouped = defaultdict(list)

        for entry in tax_band:
            key = (entry["name"], entry["deduct_on"], entry["tax_free_amount"])
            grouped[key].append({
                "amount_from": entry["amount_from"],
                "amount_to": entry["amount_to"],
                "deduction_percentage": entry["deduction_percentage"]
            })
        tax_band = []
        for (name, deduct_on, tax_free_amount), bands in grouped.items():
            tax_band.append({
                "name": name,
                "deduct_on": deduct_on,
                "tax_free_amount": tax_free_amount,
                "salary_bands": bands
            })
        if tax_band:
            self.tb = utils.from_dict_to_object(tax_band[0])
            self.tb.name = "PAYE"


        self.employees = self.core_payroll.fetch_data_from_sql (self.employee_query)
        self.employee_dict = utils.array_to_dict (self.employees or [], "name")
        self.deductions_data = self.core_payroll.get_deduction_components (fetch_linked_tables=True)
        self.earnings_data = self.core_payroll.get_earning_components (fetch_linked_tables=True)
        dedu = utils.to_data_frame (self.deductions_data)
        grouped_dedu = dedu.groupby('is_statutory_component')
        self.deductions = {
            'none_statutory' if key == 0.0 else 'statutory': group.to_dict(orient='records')
            for key, group in grouped_dedu
        }

        earn = utils.to_data_frame (self.earnings_data)
        grouped_earn = earn.groupby('exclude_on_statutory_deductions')
        self.earnings = {
            'taxable' if key == 0 else 'none_taxable': group.to_dict(orient='records')
            for key, group in grouped_earn
        }

        self.taxable_earnings = utils.array_to_dict(DataConversion.safe_get (self.earnings, "taxable", []), "name")
        self.none_taxable_earnings = utils.array_to_dict(DataConversion.safe_get (self.earnings, "none_taxable", []), "name")
        self.statutory_deductions = utils.array_to_dict(DataConversion.safe_get (self.deductions, "statutory", []), "name")
        self.none_statutory_deductions = utils.array_to_dict(DataConversion.safe_get (self.deductions, "none_statutory", []), "name")

        self.decimals = dbms.system_settings.currency_decimals
        hr_settings = self.core_hr.get_company_settings (self.core_hr.company)
        self.hr_settings_working_days = 22 if not hr_settings else hr_settings.working_days

    def calculate_pro_rated_basic_pay(self, payroll_from_date, payroll_to_date, employee, emp_basic_pay):
        try:
            payroll_from_date = DataConversion.parse_date (payroll_from_date)
            payroll_to_date = DataConversion.parse_date (payroll_to_date)

            if not (payroll_from_date and payroll_to_date):
                raise ValueError("Payroll dates are invalid or missing.")
            joining_date_raw = DataConversion.safe_get(employee, "date_of_joining")
            joining_date = DataConversion.parse_date (joining_date_raw)

            basic_pay = DataConversion.convert_to_float(emp_basic_pay)
            working_days = DataConversion.convert_to_float(DataConversion.safe_get(employee, "working_days", 22))

            if basic_pay == 0.0 or working_days == 0.0:
                print(f"Unprocessable Payroll: {DataConversion.safe_get(employee, 'name')}'s basic pay or working days is zero")
                return 0.0

            prorated_salary = 0.0
            dw = 0

            is_separated = DataConversion.safe_get(employee, "is_separated") == 1
            is_unsettled_flag = DataConversion.safe_get(employee, "is_separated_emp_paid")
            is_unsettled = is_unsettled_flag == "Unsettled" or isinstance(is_unsettled_flag, dict)

            if is_separated and is_unsettled:
                last_day_raw = DataConversion.safe_get(employee, "last_day_of_work")
                last_day = DataConversion.parse_date (last_day_raw)

                if last_day and joining_date:
                    if payroll_from_date <= last_day <= payroll_to_date and joining_date <= last_day:
                        dw = count_week_days(payroll_from_date, last_day)
                        prorated_salary = (basic_pay / working_days) * dw

            elif joining_date and payroll_from_date <= joining_date <= payroll_to_date:
                dw = count_week_days(joining_date, payroll_to_date)
                prorated_salary = (basic_pay / working_days) * dw

            else:
                prorated_salary = basic_pay

            return utils.fixed_decimals(prorated_salary, self.decimals)

        except Exception as e:
            print("Error in calculate_pro_rated_basic_pay:", str(e))
            return 0.0

    def _parse_date(self, date_str):
        try:
            if isinstance(date_str, datetime):
                return date_str.date()
            elif isinstance(date_str, str):
                return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return datetime.today().date()

    def checkEmployeeEligibility(self, payrollFromDate, payrollToDate, joining_date, lastDayOfWork, separation_status, payment_state):
        joining_date = DataConversion.convert_to_datetime(joining_date)
        lastDayOfWork = DataConversion.convert_to_datetime(lastDayOfWork)
        return_bool = False

        if separation_status == 0 or separation_status is None:
            return_bool = joining_date <= payrollToDate
        elif separation_status == 1 and (payment_state == "Unsettled" or payment_state is None):
            if lastDayOfWork is not None:
                if lastDayOfWork >= payrollToDate:
                    return_bool = True
                else:
                    return_bool = payrollFromDate <= lastDayOfWork <= payrollToDate
            else:
                return_bool = False

        return return_bool


    def calc_payroll (self):
        new_calc_processor = []
        deduction_calc = DeductionCalculator ()
        overall_totals = utils.from_dict_to_object ({
            "excluded_amount": 0,
            "total_employee": 0,
            "total_basic": 0,
            "total_net": 0,
            "total__earnings_with_excluded": 0,
            "total_earnings": 0,
            "total_deductions": 0,
            "total_income_tax": 0,
            "earnings_totals": {},
            "deductions_totals": {}
        })
        for payroll_emp in self.payroll_processor:
            total_earnings = 0
            total_deductions = 0
            employee = copy.deepcopy (payroll_emp)
            emp = DataConversion.safe_get (self.employee_dict, DataConversion.safe_get(payroll_emp, 'employee', ''), {})
            if emp:
                emp_status = self.checkEmployeeEligibility (self.from_date, self.to_date,emp.date_of_joining, emp.last_day_of_work, emp.is_separated, emp.is_separated_emp_paid)
                if emp_status:
                    basic_pay = self.calculate_pro_rated_basic_pay (self.from_date, self.to_date,emp, DataConversion.safe_get(emp, "basic_pay", 0.00))
                    total_earnings += basic_pay
                    total_basic = DataConversion.safe_get(overall_totals, "total_basic", 0) + basic_pay
                    DataConversion.safe_set (employee, "basic_pay", basic_pay)
                    DataConversion.safe_set (overall_totals, "total_basic", total_basic)
                    earnings = DataConversion.safe_get (emp, "earnings", [])
                    deductions = DataConversion.safe_get (emp, "deductions", [])
                    earnings = json.loads (earnings)
                    deductions = json.loads (deductions)
                    if len (earnings) > 0:
                        for earning_name in earnings:
                            val = 0.00
                            if earning_name:
                                earning = DataConversion.safe_get (self.taxable_earnings, earning_name, None)
                                if earning:
                                    val_type = DataConversion.safe_get (earning, "value_type", '')
                                    if str (val_type).lower () == "custom":
                                        val = DataConversion.safe_get (payroll_emp, earning_name, 0.00)
                                    else:
                                        val = EarningCalculator.calc_earning (emp, basic_pay, earning)
                                total_earnings += val
                                overall_earning = DataConversion.safe_get(overall_totals.earnings_totals, earning_name, 0) + val
                                DataConversion.safe_set (employee, earning_name, val)
                                DataConversion.safe_set (overall_totals.earnings_totals, earning_name, overall_earning)
                        total_earning = DataConversion.safe_get(overall_totals, "total_earnings", 0) + total_earnings
                        DataConversion.safe_set (overall_totals, "total_earnings", total_earning)
                        DataConversion.safe_set (employee, 'gross', total_earnings)
                    if len (deductions) > 0:
                        for deduction_name in deductions:
                            val = 0.00
                            if deduction_name:
                                deduction = DataConversion.safe_get (self.statutory_deductions, deduction_name, None)
                                if deduction:
                                    val_type = DataConversion.safe_get (deduction, "value_type", '')
                                    if str (val_type).lower () == "custom":
                                        val = DataConversion.safe_get (payroll_emp, deduction_name, 0.00)
                                    else:
                                        val = deduction_calc.calc_deduction (emp, employee, deduction)
                                    total_deductions += val
                                    overall_deductions = DataConversion.safe_get(overall_totals.deductions_totals, deduction_name, 0) + val
                                    DataConversion.safe_set (employee, deduction_name, val)
                                    DataConversion.safe_set (overall_totals.deductions_totals, deduction_name, overall_deductions)
                            total_deduction = DataConversion.safe_get(overall_totals, "total_deductions", 0) + total_deductions
                            DataConversion.safe_set (overall_totals, "total_deductions", total_deduction)
                    # income_tax_band = IncomeTaxCalculator.calculate_income_tax_band (emp, employee, self.tb)
                    # DataConversion.safe_set (employee, DataConversion.safe_get (self.tb, 'name', "PAYE"), income_tax_band)
                    # total_deduction = DataConversion.safe_get(overall_totals, "total_deductions", 0) + income_tax_band
                    # total_income_tax = DataConversion.safe_get(overall_totals, "total_income_tax", 0) + income_tax_band
                    # DataConversion.safe_set (overall_totals, "total_income_tax", total_income_tax)
                    # DataConversion.safe_set (overall_totals, "total_deductions", total_deduction)
                    # DataConversion.safe_set (employee, "net", (DataConversion.convert_to_float (DataConversion.safe_get (employee, "net", 0)) - DataConversion.convert_to_float (DataConversion.safe_get (employee, "net", 0))))

                else:
                    pp (DataConversion.safe_get(payroll_emp, 'employee', ''), emp_status)
        pp (overall_totals)
        # calculate Earnings
        # calculate Deductions
        # calculate income Tax Band
        # calculate none Taxable Earnings
        # calculate final Net
        pass