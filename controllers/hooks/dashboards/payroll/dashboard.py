# from datetime import datetime, timedelta
# from controllers.core_functions.payroll import Core_Payroll
# from controllers.core_functions.hr import Core_Hr
# from controllers.utils import Utils
# from controllers.utils.dates import Dates
# from controllers.utils.dict_to_object import Dict_To_Object


# utils = Utils()
# dates = Dates()
# pp = utils.pretty_print
# throw = utils.throw


# # PAYROLL DASHBOARD
# class Payroll_Dashboard:
#     def __init__(self,dbms,object):
#         self.dbms = dbms
#         self.object = object
#         self.user = object.user
#         self.settings = {}
#         self.past_7_days = dates.add_days(dates.today(), -7)
#         self.settings = self.dbms.system_settings
#         self.defaults = self.settings.accounting_defaults
#         self.company = self.settings.default_company
#         self.core_payroll = Core_Payroll(dbms, object)
#         self.core_hr = Core_Hr(dbms, object)


#     @classmethod
#     def dashboard(cls, dbms, object):
#         cls = cls (dbms,object)
#         return utils.respond(utils.ok,{
#             "overall_accrued_overtime": cls.get_overall_accrued_overtime(cls).data,
#             # "employee_info": cls.get_employee_info(cls).data,
#             # "advance_info": cls.get_advance_info(cls).data,
#             # "payroll_cost_summary": cls.get_payroll_cost_summary(cls).data,
#             # # "regulatory_summary": cls.get_regulatory_summary(cls).data,
#             # "payroll_cost_by_designation": cls.get_payroll_cost_by_designation(cls).data,
#             # "recent_payments": cls.get_recent_payments(cls).data,
#             # "next_payroll_date":cls.next_payroll_date(cls),
#         })
    
#     def get_employee_info(self):
#         res = {
#             "total_employees":0,
#             "number_of_employes_on_payroll": 0,
#             "overtime_accrued": "-"
#         }
#         employees = self.dbms.get_list("Employee", privilege=True, only_count=True)
#         if employees.status == utils.ok:
#             res["total_employees"] = employees.data

#         payroll_processor = self.dbms.get_list("Payroll_Processor", privilege=True, limit=1, filters={"docstatus": 1}, order_by=["-id"])
#         if payroll_processor.status == utils.ok:
#             payroll_processor_data = payroll_processor.data.rows[0]
#             res["number_of_employes_on_payroll"] = payroll_processor_data.total_employees
#         return utils.respond(utils.ok,res)
   
  
#     def next_payroll_date(self):
#         last_payment = self.dbms.get_list("Payroll_Processor", privilege=True, limit=1, filters={"docstatus": 1}, order_by=["-id"])
        
#         if last_payment.status == utils.ok:
#             last_payment_data = last_payment.data.rows
            
#             if last_payment_data:
#                 for payment in last_payment_data:
#                     if payment.frequency == "Monthly":
#                         last_payment_date = payment['to_date']
#                         next_payment_date = last_payment_date + timedelta(days=30)
#                         next_payment_date_str = next_payment_date.strftime("%Y-%m-%d")
#                         next_word_payment_date = dates.get_human_word_date(next_payment_date_str)
#                         return next_word_payment_date
#                     elif payment.frequency == "weekly":
#                         last_payment_date = payment['to_date']
#                         next_payment_date = last_payment_date + timedelta(days=7)
#                         next_payment_date_str = next_payment_date.strftime("%Y-%m-%d")
#                         next_word_payment_date = dates.get_human_word_date(next_payment_date_str)
#                         return next_word_payment_date
#         else:
#               return None 

#         return None 

    
#     def get_recent_payments(self):
#         res = []
#         recent_payments_data = self.dbms.get_list("Payroll_Processor", privilege=True,limit=6,filters={"docstatus":1})
#         if recent_payments_data.status == utils.ok:
#             res = recent_payments_data.data.rows
#         return utils.respond(utils.ok,res)
    
#     def get_advance_info(self):
#         advance_stats = self.core_payroll.get_advance_stat()
#         if not advance_stats:
#             res = []
#         else:
#             res = [
#                 {"name": "Total Advance", "value": utils.fixed_decimals( advance_stats.total_advance_amount_disbursed, 2)},
#                 {"name": "Paid Amount", "value":  utils.fixed_decimals(advance_stats.total_paid_amount,2)},
#                 {"name": "Unpaid Amount", "value":  utils.fixed_decimals(advance_stats.total_unpaid_amount, 2)},
#                 {"name": "Total Owing Employees", "value":  utils.fixed_decimals(advance_stats.employees_still_owing,2)},
#             ]
#         return utils.respond(utils.ok, res)

    
#     def get_payroll_cost_summary(self):
#         res = []
#         last_payment = self.dbms.get_list("Payroll_Processor", privilege=True,limit=1,filters={"docstatus":1},order_by=["-id"])
#         if last_payment.status == utils.ok:
#             d = last_payment.data.get("rows")[0]
#             res.append({"name": "Total Earnings", "value":utils.fixed_decimals(d.total_earnings,2)})
#             res.append({"name": "Total Deductions", "value":utils.fixed_decimals(d.total_deductions,2)})
#             res.append({"name": "Net", "value":utils.fixed_decimals(d.total_net,2)})
#         else:
#             res = []
          
#         return utils.respond(utils.ok,res)
    
#     def get_payroll_cost_by_designation (self):
#         payroll_processor = self.dbms.get_list("Payroll_Processor", privilege=True, limit=1, filters={"docstatus": 1}, order_by=["-id"])
#         res = []
#         if payroll_processor.status == utils.ok:
#             payroll_processor_data = payroll_processor.data.rows[0]
#             employee_info = payroll_processor_data.employee_info
#             grouped = utils.group(employee_info, "designation")
#             summed = utils.from_dict_to_object({})
#             keys = utils.get_object_keys(grouped)
#             for key in keys:
#                 df = utils.to_data_frame(grouped.get(key))
#                 # Convert the net values to integers before summing
#                 df["net"] = df["net"].astype(float)
#                 summed[key] = df["net"].sum()

#             res = [{"name": name, "value": value, "currency": "ZMW", "perc": 0} for name, value in summed.items()]
#         return utils.respond(utils.ok, res)

#     def get_regulatory_summary(self):
#         payroll_processor = self.dbms.get_list("Payroll_Processor", privilege=True, limit=1, filters={"docstatus": 1}, order_by=["-id"])

#         if payroll_processor.status == utils.ok:
#             payroll_processor_data = payroll_processor.data.rows[0]
#             # earnings = self.core_payroll.get_earning_components()
#             # deductions = self.core_payroll.get_deduction_components()
#             # extended = earnings + deductions

#             extended = self.core_payroll.get_is_statutory_component ()
#             if extended:

#                 # grouped = utils.group(extended, "is_statutory_component")
#                 # grouped_list = utils.array_to_dict(grouped.get(1), 'name')
#                 # grouped_list = utils.array_to_dict(extended.get(1), 'name')

#                 # pp (grouped, grouped_list)

#                 grouped_list = utils.array_to_dict(extended, 'name')
#                 keys = utils.get_object_keys(grouped_list)

#                 tax_band = self.core_hr.get_employee_tax_band()
#                 if tax_band.status == utils.ok:
#                     keys.append(tax_band.data.name)
#                 employee_info = payroll_processor_data.employee_info
#                 df = utils.to_data_frame(employee_info)

#                 df[keys] = df[keys].astype(float)
#                 sums = df[keys].sum().to_dict()
#                 res = [{"name": name, "value": utils.fixed_decimals(value, 2), "currency": "ZMW"} for name, value in sums.items()]
#             else:
#                 res = []
#         else:
#             res = []

#         return utils.respond(utils.ok, res)

#     def get_overall_accrued_overtime(self):
#         accrued_overtime =  self.core_payroll.get_overall_accrued_overtime()
#         return accrued_overtime

from datetime import timedelta
from controllers.core_functions.payroll import Core_Payroll
from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
import pandas as pd



utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw


# PAYROLL DASHBOARD
class Payroll_Dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.settings = self.dbms.system_settings
        self.defaults = self.settings.accounting_defaults
        self.company = self.settings.default_company
        self.core_payroll = Core_Payroll(dbms, object)
        self.core_hr = Core_Hr(dbms, object)

    @classmethod
    def dashboard(cls, dbms, object):
        instance = cls (dbms,object)
        return utils.respond(utils.ok,{
            "overall_accrued_overtime": instance.get_overall_accrued_overtime(),
            "employee_info": instance.get_employee_info(),
            "advance_info": instance.get_advance_info(),
            "payroll_cost_summary": instance.get_payroll_cost_summary(),
            "regulatory_summary": instance.get_regulatory_summary(),
            "payroll_cost_by_designation": instance.get_payroll_cost_by_designation(),
            "recent_payments": instance.get_recent_payments(),
            "next_payroll_date":instance.next_payroll_date(),
        })

    def get_employee_info(self):
        try:
            res = {
                "total_employees":0,
                "number_of_employes_on_payroll": 0,
                "overtime_accrued": "-"
            }
            employees = self.dbms.get_list("Employee", privilege=True, only_count=True)
            if employees.status == utils.ok:
                DataConversion.safe_set (res, "total_employees", DataConversion.safe_get (employees, "data"))

            payroll_processor = self.core_payroll.get_list("Payroll_Processor", privilege=True, limit=1, filters={"docstatus": 1}, order_by=["-id"])
            if payroll_processor:
                payroll_processor_data = DataConversion.safe_list_get (payroll_processor, 0)
                DataConversion.safe_set (res, "number_of_employes_on_payroll", DataConversion.safe_get (payroll_processor_data, "total_employees"))
            return res
        except Exception as e:
            pp (f"ERROR IN get_employee_info: {e}")

    def next_payroll_date(self):
        try:
            last_payment_data = self.core_payroll.get_list("Payroll_Processor", privilege=True, limit=1, filters={"docstatus": 1}, order_by=["-id"])
            if last_payment_data:
                if last_payment_data:
                    for payment in last_payment_data:
                        if DataConversion.safe_e(DataConversion.safe_get (payment, "frequency"), "Monthly", str, True):
                            last_payment_date = DataConversion.safe_get (payment, 'to_date', dates.add_days (dates.today (), - 30))
                            next_payment_date = last_payment_date + timedelta(days=30)
                            next_payment_date_str = next_payment_date.strftime("%Y-%m-%d")
                            next_word_payment_date = dates.get_human_word_date(next_payment_date_str)
                            return next_word_payment_date
                        elif DataConversion.safe_e(DataConversion.safe_get (payment, "frequency"), "Weekly", str, True):
                            last_payment_date =  DataConversion.safe_get (payment, 'to_date', dates.add_days (dates.today (), - 7))
                            next_payment_date = last_payment_date + timedelta(days=7)
                            next_payment_date_str = next_payment_date.strftime("%Y-%m-%d")
                            next_word_payment_date = dates.get_human_word_date(next_payment_date_str)
                            return next_word_payment_date
                return None
            return None
        except Exception as e:
            pp (f"ERROR IN next_payroll_date: {e}")

    def get_recent_payments(self):
        try:
            res = []
            recent_payments_data = self.core_payroll.get_list("Payroll_Processor", privilege=True,limit=6,filters={"docstatus":1})
            if recent_payments_data:
                res = recent_payments_data
            return res
        except Exception as e:
            pp (f"ERROR IN get_recent_payments:{e}")

    def get_advance_info(self):
        try:
            advance_stats = self.core_payroll.get_advance_stat()
            if not advance_stats:
                res = []
            else:
                res = [
                    {"name": "Total Advance", "value": utils.fixed_decimals(DataConversion.convert_to_float (DataConversion.safe_get (advance_stats, "total_advance_amount_disbursed")), 2)},
                    {"name": "Paid Amount", "value":  utils.fixed_decimals(DataConversion.convert_to_float (DataConversion.safe_get (advance_stats, "total_paid_amount")),2)},
                    {"name": "Unpaid Amount", "value":  utils.fixed_decimals(DataConversion.convert_to_float (DataConversion.safe_get (advance_stats, "total_unpaid_amount")), 2)},
                    {"name": "Total Owing Employees", "value":  utils.fixed_decimals(DataConversion.convert_to_float (DataConversion.safe_get (advance_stats, "employees_still_owing")),2)},
                ]
            return res
        except Exception as e:
            pp (f"ERROR IN get_advance_info: {e}")

    def get_payroll_cost_summary(self):
        try:
            res = []
            last_payment = self.core_payroll.get_list("Payroll_Processor", privilege=True,limit=1,filters={"docstatus":1},order_by=["-id"])
            res = []
            if last_payment:
                d = DataConversion.safe_list_get(last_payment, 0)
                DataConversion.safe_list_append (res, {"name": "Total Earnings", "value": utils.fixed_decimals(DataConversion.convert_to_float (DataConversion.safe_get (d, "total_earnings")),2)})
                DataConversion.safe_list_append (res, {"name": "Total Deductions", "value": utils.fixed_decimals(DataConversion.convert_to_float (DataConversion.safe_get (d, "total_deductions")),2)})
                DataConversion.safe_list_append (res, {"name": "Net", "value": utils.fixed_decimals(DataConversion.convert_to_float (DataConversion.safe_get (d, "total_net")),2)})
            return res
        except Exception as e:
            pp (f"ERROR IN get_payroll_cost_summary: {e}")

    def get_payroll_cost_by_designation(self):
        try:
            payroll_processor = self.core_payroll.get_list("Payroll_Processor", privilege=True, limit=1, filters={"docstatus": 1}, order_by=["-id"])
            res = []
            if payroll_processor:
                payroll_processor_data = DataConversion.safe_list_get (payroll_processor, 0)
                employee_info = DataConversion.safe_get (payroll_processor_data, "employee_info")
                df1 = utils.to_data_frame (DataConversion.remove_NaN_and_None (employee_info))
                if "designation" in df1.columns:
                    # grouped = utils.group(employee_info, "designation")
                    grouped = {
                        key: group.to_dict(orient="records")
                        for key, group in df1.groupby("designation")
                    }
                    summed = utils.from_dict_to_object({})
                    keys = utils.get_object_keys(grouped)
                    for key in keys:
                        df = utils.to_data_frame(grouped.get(key))
                        if "net" in df.columns:
                            df["net"] = df["net"].astype(float)
                            summed[key] = df["net"].sum()

                    res = [{"name": name, "value": value, "currency": "ZMW", "perc": 0} for name, value in summed.items()]
            return res
        except Exception as e:
            pp (f"ERROR IN get_payroll_cost_by_designation: {e}")

    def get_regulatory_summary(self):
            try:
                payroll_processor = self.core_payroll.get_list("Payroll_Processor", privilege=True, limit=1, filters={"docstatus": 1}, order_by=["-id"])
                if payroll_processor:
                    payroll_processor_data = DataConversion.safe_list_get (payroll_processor, 0)
                    earnings = self.core_payroll.get_earning_components()
                    deductions = self.core_payroll.get_deduction_components()
                    extended = earnings + deductions
                    if extended:
                        df = utils.to_data_frame (extended)
                        df["is_statutory_component"] = df["is_statutory_component"].fillna (0).astype (int)
                        grouped_df = {
                            k: v.to_dict(orient='records')
                            for k, v in df.groupby('is_statutory_component')
                        }
                        grouped_list = DataConversion.safe_get (grouped_df, 1, [])
                        grouped_list = utils.array_to_dict (grouped_list, "name")

                        keys = utils.get_object_keys(grouped_list)
                        tax_band = self.core_hr.get_employee_tax_band ()

                        if tax_band.status == utils.ok:
                            keys.append("PAYE")
                        employee_info = payroll_processor_data.employee_info
                        df = utils.to_data_frame(employee_info)
                        df[keys] = df[keys].astype(float)
                        sums = df[keys].sum().to_dict()
                        res = [{"name": name, "value": utils.fixed_decimals(value, 2), "currency": "ZMW"} for name, value in sums.items()]
                    else:
                        res = []
                else:
                    res = []

                return res
            except Exception as e:
                pp (f"ERROR IN get_regulatory_summary: {e}")


    def get_overall_accrued_overtime(self):
        try:
            accrued_overtime =  self.core_payroll.get_overall_accrued_overtime()
            return accrued_overtime
        except Exception as e:
            pp (f"ERROR IN get_overall_accrued_overtime: {e}")