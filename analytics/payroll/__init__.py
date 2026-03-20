import pandas as pd
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object

utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

class Payroll_Analytics:
    def __init__(self,dbms,object=None):
        self.dbms = dbms
        self.object = object

    def calculate_payslips_ytd_stats(self, data):
        df = utils.to_data_frame (data)
        df["basic_pay"] = pd.to_numeric(df["basic_pay"]).astype(float)
        df["gross"] = pd.to_numeric(df["gross"]).astype(float)
        df["total_earnings"] = pd.to_numeric(df["total_earnings"]).astype(float)
        df["total_tax_amount"] = pd.to_numeric(df["total_tax_amount"]).astype(float)
        df["total_deductions"] = pd.to_numeric(df["total_deductions"]).astype(float)
        df["advance_amount"] = pd.to_numeric(df["advance_amount"]).astype(float)
        df["advance_repaid"] = pd.to_numeric(df["advance_repaid"]).astype(float)
        df["total_advance_repaid"] = pd.to_numeric(df["total_advance_repaid"]).astype(float)
        df["net"] = pd.to_numeric(df["net"]).astype(float)
        df["working_days"] = pd.to_numeric(df["working_days"]).astype(float)
        df["current_leave_days"] = pd.to_numeric(df["current_leave_days"]).astype(float)
        df["current_leave_value"] = pd.to_numeric(df["current_leave_value"]).astype(float)
        df["napsa"] = pd.to_numeric(df["napsa"]).astype(float)
        df["ytd_pla"] = pd.to_numeric(df["ytd_pla"]).astype(float)
        df["private_pension"] = pd.to_numeric(df["private_pension"]).astype(float)
        overalls = {
            "overall_basic_pay": df["basic_pay"].sum(),
            "overall_gross": df["gross"].sum(),
            "overall_earnings": df["total_earnings"].sum(),
            "overall_deductions": df["total_deductions"].sum(),
            "overall_tax": df["total_tax_amount"].sum(),
            "overall_advance_amount": df["advance_amount"].sum(),
            "overall_advance_repaid": df["advance_repaid"].sum(),
            "overall_total_advance_repaid": df["total_advance_repaid"].sum(),
            "overall_net": df["net"].sum(),
            "overall_working_days": df["working_days"].sum(),
            "overall_current_leave_days": df["current_leave_days"].sum(),
            "overall_current_leave_value": df["current_leave_value"].sum(),
            "overall_private_pension": df["private_pension"].sum(),
            "overall_napsa": df["napsa"].sum(),
            "overall_ytd_pla": df["ytd_pla"].sum(),
        }

        return utils.respond(utils.ok, overalls)
    
    def calculate_overtime (self, overtime: list):
        df = utils.to_data_frame (overtime)
        total_ = 0
        df["total_earning"] = pd.to_numeric(df["total_earning"]).astype(float)
        total_ = df["total_earning"].sum ()
        return total_
    

    def calculate_totals(self, df: pd.DataFrame) -> dict:
        total_advance = df['amount'].sum()
        total_paid = df[df['status'] != 'Unsettled']['amount_paid'].sum()
        total_unpaid = total_advance - total_paid
        return {
            'total_advance_amount_disbursed': total_advance,
            'total_paid_amount': total_paid,
            'total_unpaid_amount': total_unpaid
        }

    def count_employees_still_owing(self, df: pd.DataFrame) -> int:
        return len(df[(df['cleared'] == 0) | (df['cleared'] == 1)])

    def analyze_advance_data(self, data: list) -> dict:
        df = utils.to_data_frame (data)
        totals = self.calculate_totals(df)

        employees_still_owing = self.count_employees_still_owing(df)

        pp (employees_still_owing)

        totals['employees_still_owing'] = employees_still_owing
        return Dict_To_Object(totals)