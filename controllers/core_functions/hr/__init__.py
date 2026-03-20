from controllers.mailing.templates.hr_email_template import Default_Templates
from controllers.utils import Utils
from controllers.utils.dates import Dates
from analytics.hr import HR_Analytics
from analytics.payroll import Payroll_Analytics
from datetime import datetime
from controllers.mailing import Mailing
from controllers.mailing.templates.default_template import Default_Template
from controllers.utils.data_conversions import DataConversion
import json
import pandas as pd

from controllers.core_functions.hr.witnessing_controller import Witnessing

from datetime import datetime

def get_month_and_year ():
    now = datetime.now()

    month_name = now.strftime('%B')
    year = now.strftime('%Y')
    return month_name, year


utils = Utils ()
dates = Dates ()
pp = utils.pretty_print
throw = utils.throw

class Core_Hr:
    def __init__ (self, dbms, user=None, obj=None, privilege=False) -> None:
        self.dbms = dbms
        self.user = user if user else dbms.current_user.name
        self.defaults = None
        self.object = obj
        self.privilege = privilege
        self.hr_analytics = HR_Analytics(dbms)
        self.payroll_analytics = Payroll_Analytics(dbms)
        self.mailing = Mailing(self.dbms, self.object)
        self.system_settings = dbms.system_settings.linked_fields
        self.reporting_currency = self.system_settings.default_country
        self.company = self.dbms.current_user.default_company if self.dbms.current_user.default_company else self.system_settings.default_company.name
        self.witnessing = Witnessing (self)
    
    def get_emp_last_pay (self, emp):
        payslip = DataConversion.safe_list_get (self.fetch_data_from_sql ("SELECT * FROM payslip WHERE employee_id=%s ORDER BY to_date DESC LIMIT 1", (DataConversion.safe_get (emp, "id"),)), 0)
        if payslip:
            DataConversion.safe_set (emp, "ytd_paye", DataConversion.safe_get (payslip, "ytd_tax", 0))
            DataConversion.safe_set (emp, "ytd_net", DataConversion.safe_get (payslip, "ytd_net", 0))
            DataConversion.safe_set (emp, "ytd_napsa", DataConversion.safe_get (payslip, "ytd_napsa", 0))
            DataConversion.safe_set (emp, "ytd_gross", DataConversion.safe_get (payslip, "ytd_gross", 0))
            DataConversion.safe_set (emp, "ytd_private_pension", DataConversion.safe_get (payslip, "ytd_private_pension", 0))
        return emp

    def send_mail_to_witnesses (self, doctype: str, doc_name: str, applicant, witness:str):
        data = utils.from_dict_to_object ()
        applicant_names = DataConversion.safe_get (applicant, "full_name", f"""{DataConversion.safe_get (applicant,'first_name')} {DataConversion.safe_get (applicant,'middle_name', '')} {DataConversion.safe_get (applicant,'last_name')}""")
        DataConversion.safe_set (data, "doc_url", f"""https://{self.dbms.host}/app/staff/witness?module=staff&app=witness&page=new-form&content_type=witness&doc={doc_name}""")
        DataConversion.safe_set (data, "document_type", doctype)
        DataConversion.safe_set (data, "document_name", doc_name)
        DataConversion.safe_set (data, "submission_date", dates.today ())
        DataConversion.safe_set (data, "applicant_dept", DataConversion.safe_get (applicant,'department'))
        DataConversion.safe_set (data, "applicant", applicant_names)
        
        hs = self.get_company_settings ()

        witnesses = DataConversion.safe_get (hs, "council_witnesses", [])
        pp (witnesses, witness, applicant)

        if len (witnesses) > 0 and witness and applicant:
            swd = self.get_doc ("Employee", witness)
            witnesses_list = []
            # if swd:
            #     return witnesses_list
            total_witnesses = 1
            DataConversion.safe_set (data, "witness_name", DataConversion.safe_get (swd, "full_name", f"""{DataConversion.safe_get (swd,'first_name')} {DataConversion.safe_get (swd,'middle_name', '')} {DataConversion.safe_get (swd,'last_name')}"""))
            r = self.mailing.send_mail (recipient=DataConversion.safe_get (swd, "email"), subject=f"Witness {doctype} for {applicant_names}", body=self.witnessing.send_mail_to_witnesses (data))
            pp("iiiiiiiiiuyt",r)
            if r.status != utils.ok:
                return False
            DataConversion.safe_list_append (witnesses_list, {
                "witness_full_name": DataConversion.safe_get (swd, "full_name", f"""{DataConversion.safe_get (swd,'first_name')} {DataConversion.safe_get (swd,'middle_name', '')} {DataConversion.safe_get (swd,'last_name')}"""),
                "witness_email": DataConversion.safe_get (swd, "email"),
            })
            for wit in witnesses:
                id = DataConversion.safe_get (wit, "witness")
                email = DataConversion.safe_get (wit, "witness_email")
                witness_full_name = DataConversion.safe_get (wit, "witness_full_name")
                if email and id != DataConversion.safe_get (applicant, "name"):
                    try:
                        DataConversion.safe_set (data, "witness_name", witness_full_name)
                        r = self.mailing.send_mail (recipient=email, subject=f"Witness {doctype} for {applicant_names}", body=self.witnessing.send_mail_to_witnesses (data))
                        pp("tttttttttthh", r)
                        if r.status == utils.ok:
                            DataConversion.safe_list_append (witnesses_list, {
                                "witness_full_name": witness_full_name,
                                "witness_email": email,
                            })
                            total_witnesses += 1
                        pp ("====================, Council witness", r)
                    except Exception as e:
                        pp(e)
                        pass
            witness_doc = utils.from_dict_to_object ({
                "name": doc_name,
                "applicant": DataConversion.safe_get (applicant, "name"),
                "total_witnesses": total_witnesses,
                "total_witnessed": 0,
                "document_type": str(doctype).replace (" ", "_"),
                "witnesses": witnesses_list,
            })
            wdc = self.dbms.create ("Witnesses_Doc", witness_doc)
            if wdc.status == utils.ok:
                return True
            pp (wdc)
        return False

    def emp_get_leave_value (self, employee_id, wds=22, num_days=0, basic=0.00):
        leave_val = {}
        leave_days = self.emp_leave_annual_days (employee_id=employee_id)
        used_days = DataConversion.safe_get (leave_days, "used_days", 0.00)
        remaining_days = DataConversion.safe_get (leave_days, "remaining_days", 0.00)
        last_payslip = self.fetch_data_from_sql ("SELECT gross, basic_pay, employee_names FROM payslip WHERE employee_id=%s ORDER BY to_date DESC LIMIT 1", params=(employee_id,))
        if len (leave_days) <= 0:
            return False

        gross = basic
        if len (last_payslip) > 0:
            gross = DataConversion.convert_to_float (DataConversion.safe_get (last_payslip[0], "basic_pay", 0))
        days_pay = gross / DataConversion.convert_to_float (wds)
        DataConversion.safe_set (leave_val, "custom_days_value", days_pay * DataConversion.convert_to_float (num_days))
        DataConversion.safe_set (leave_val, "custom_days", DataConversion.convert_to_float (num_days))
        DataConversion.safe_set (leave_val, "used_days_val", days_pay * used_days)
        DataConversion.safe_set (leave_val, "remaining_days_val", days_pay * remaining_days)
        DataConversion.safe_set (leave_val, "used_days", used_days)
        DataConversion.safe_set (leave_val, "remaining_days", remaining_days)
        return leave_val
    
    def get_company_settings (self, company:str = None):
        if not company:
            company = self.company
        return self.get_doc ("Hr_Setting", name=company)

    def get_doc (self, model: str, name,privilege=False, fetch_by_field=None):
        doc = self.dbms.get_doc (model, name=name, user=self.user, privilege=privilege, fetch_by_field=fetch_by_field)
        if doc.status == utils.ok:
            return doc.data
        return None
    def fetch_data_from_sql (self, query,params=None, fetch='all'):
        result = self.dbms.sql(query, params=params,fetch=fetch)
        return result.data if result.status == utils.ok else []

    def get_list (self, model: str, filters={}, fetch_linked_tables=False, complex_filters={}, fetch_linked_fields=False,privilege=False, order_by=[], limit=None, fields=[]):
        list = self.dbms.get_list (model, filters=filters, fetch_linked_tables=fetch_linked_tables, fetch_linked_fields=fetch_linked_fields, user=self.user, privilege=privilege, limit=limit, order_by=order_by, complex_filters=complex_filters,fields=fields)
        if list.status == utils.ok:
            return list.data.rows
        return []
    
    def emp_leave_annual_days (self, employee_id=None, all=False, leave_type = "Annual Leave", filters={},return_by_employee=False):
        leave = []
        DataConversion.safe_set (filters, "leave_type", leave_type)
        if not all:
            DataConversion.safe_set (filters, "employee", employee_id)
        leave_entry = self.get_list("Leave_Entry", filters=filters,  privilege=True)
        df = utils.to_data_frame (leave_entry)
        if leave_entry:
            df['used_leave_days'] = pd.to_numeric (df['used_leave_days'])
            df['remaining_leave_days'] = pd.to_numeric (df['remaining_leave_days'])
            df['total_days'] = pd.to_numeric (df['total_days'])
            if return_by_employee:
                return df.groupby ('employee').agg ({
                    "used_leave_days": 'sum',
                    "remaining_leave_days": 'sum',
                    "total_days": 'sum',
                    "leave_type": 'first',
                    "employee": 'first',
                    "employee_name": 'first'
                }).to_dict(orient="records")
            else:
                leave = df.groupby ("entry_type").agg({
                    "used_leave_days": 'sum',
                    "total_days": 'sum',
                    "remaining_leave_days": 'sum',
                }).to_dict (orient="index")

        allocations = DataConversion.safe_get (leave, "Allocation")
        applications = DataConversion.safe_get (leave, "Application")
        used_days = DataConversion.safe_get (applications, "used_leave_days", 0.0)
        remaining_days = DataConversion.safe_get (allocations, "remaining_leave_days", 0.0)
        ret = utils.from_dict_to_object ()
        DataConversion.safe_set (ret, "used_days", used_days)
        DataConversion.safe_set (ret, "remaining_days", remaining_days - used_days)
        DataConversion.safe_set (ret, "total_days", DataConversion.safe_get (allocations, "total_days", 0.0))
        return ret

    def get_user_as_employee (self, user_id = None):
        user = user_id if user_id else self.user
        employee = self.get_list("Employee", filters={"user": user}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if employee:
            return employee[0]
        return None
    def job_application (self):
        job_applications = self.get_list("Job_Application", filters={}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if job_applications:
            return job_applications
        return None
    def job_offer (self):
        job_offers = self.get_list("Job_Offer", filters={}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if job_offers:
            return job_offers
        return None
    def interviews (self):
        interview = self.get_list("Interview", filters={"status": "Submitted"}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if interview:
            return interview
        return None
    def interviews_schedule (self):
        interview_schedule = self.get_list("Interview_Schedule", privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if interview_schedule:
            return interview_schedule
        return None
    
    def work_plan (self):
        workplan = self.get_list("Work_Plan", privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if workplan:
            return workplan
        return None
    
    def job_opening (self):
        job_openings = self.get_list("Job_Advertisement", filters={"status": "Submitted"}, privilege=True)
        if job_openings:
            return job_openings
        return None
    def get_employee_list(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False, fields=None, order=['-id'], use_sql=True):
        list_of_employees = self.get_list ("Employee", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables, fields=fields, order_by=order)
        if list_of_employees:
            return list_of_employees
        return None
    def get_grievances(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        get_grievance = self.get_list ("Employee_Grievance", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if get_grievance:
            return get_grievance
        return None
    def get_case_outcome(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        get_actions = self.get_list ("Case_Outcome", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if get_actions:
            return get_actions
        return None
    def get_designation_list(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        list_of_designation = self.get_list ("Designation", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if list_of_designation:
            return list_of_designation
        return None
    def final_statement(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        list_of_designation = self.get_list ("Final_Statement", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if list_of_designation:
            return list_of_designation
        return None
    def get_exit_interview(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        list_of_designation = self.get_list ("Exit_Interview", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if list_of_designation:
            return list_of_designation
        return None
    def employee_separation(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        list_of_designation = self.get_list ("employee_separation", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if list_of_designation:
            return list_of_designation
        return None
    
    def get_department_list(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        list_of_departments = self.get_list ("Department", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if list_of_departments:
            return list_of_departments
        return None
    def get_desciplines(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        list_of_departments = self.get_list ("Department", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if list_of_departments:
            return list_of_departments
        return None
    def staff_feedback(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        staff_feedback = self.get_list ("Staff_Feedback", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if staff_feedback:
            return staff_feedback
        return None

    def get_employment_type_list(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        list_of_employment_types = self.get_list ("Employment_Type", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if list_of_employment_types:
            return list_of_employment_types
        return None
    def appointment_letter(self,filters={}, fetch_linked_fields=False, fetch_linked_tables=False):
        appointment_letter = self.get_list ("Appointment_Letter", privilege=True, filters=filters, fetch_linked_fields=fetch_linked_fields, fetch_linked_tables=fetch_linked_tables)
        if appointment_letter:
            return appointment_letter
        return None
    def get_overtime_data (self, employee):
        overtime = self.get_list ("Overtime", filters={"applicant": employee, "docstatus": 1, "is_paid": 0})
        total_overtime: float = 0.00
        if overtime:
            total_overtime = self.payroll_analytics.calculate_overtime (overtime)
        return {"overtime": total_overtime}
    
    def get_unsettled_overtime_data(self, employee):
        res = []
        overtime_data = self.get_list(
            "Overtime",
            filters={"applicant": employee, "docstatus": 1, "is_paid": 0}
        )
        if overtime_data:
            for data in overtime_data:
                res.append(data)
        return res
    
    def get_unsettled_advance_data(self, employee):
        res = []
        advance_data = self.get_list(
            "Advance_Application",
            filters={"applicant": employee, "docstatus": 1, "is_paid": 0,},
            fetch_linked_tables=True
        )
        if advance_data:
            return_obj = utils.from_dict_to_object ({})
            for data in advance_data:
                if data.pay_with_partial_payments == 1:
                    for payments in data.calculated_value:
                        return_obj.repayments = payments
                        return_obj.doc = data
                        res.append(return_obj)
                else:
                    return_obj.repayments = data
                    return_obj.doc = data
                    res.append (return_obj)
        return res


    def get_advance_data (self, employee, pay=False):
        if pay:
            return self.settle_Advance (employee=employee)
        return self.get_advance (employee=employee)
    def settle_Advance (self, employee):
        settlement: float = 0.00
        emp = self.get_doc ("Employee")
        advance = self.get_list ("Salary_Advance_Entries", filters={"applicant": employee, "paid": 0})
        if advance:
            for adv in advance:
                if adv.balance and adv.total_repaid < adv.amount:
                    settlement += adv.monthly_repayment
        return settlement

    def get_advance (self, employee: str):
        return self.get_list ("Salary_Advance_Entries", filters={"applicant": employee, "is_active": "yes"})

    def get_leave_info(self):
        data = {
            "total_days": 0,
            "available_days": 0,
            "pending_applications":0,
            "approved_applications":0
        }
        appls = 0
        leave_entries = self.get_list("Leave_Entry", privilege=True)
        applications = self.get_list("Leave_Application", privilege=True)

        if leave_entries:
            grouped = self.hr_analytics.group_leave_by_type(leave_entries)
            if grouped.get("status") == utils.ok:
                grouped_data = grouped.get("data").get("overall_totals")
                data["overall_totals"] = grouped_data.get("total_days")
                data["used_days"] = grouped_data.get("used_days")
                data["remaining_days"] = grouped_data.get("remaining_days")
        
        if applications:
            grouped = self.hr_analytics.group_leave_applications_by_status(applications, only_totals=True)
            if grouped.get("status") == utils.ok:
                grouped_data = grouped.get("data")
                data["pending_applications"] = grouped_data.get("Pending Approval")
                data["approved_applications"] = grouped_data.get("Approved")
                data["approved_applications"] = grouped_data.get("Approved")
        
        return data

    def get_employee_leave_days(self, employee_id, filters={}):
        filters["employee"] = employee_id
        leave_entry = self.get_list("Leave_Entry", filters=filters,  privilege=True)
        data = {
            "overall_totals": {
                "total_days": 0,
                "used_days": 0,
                "remaining_days": 0,
                "leave_days_in_working_hours": 0
            }
        }
        if leave_entry:
            group = self.hr_analytics.group_leave_by_type(leave_entry)
            if group.status== utils.ok:
                data = group.data
        return data

    def get_employee_payslips(self, employee_id):
        payslips = self.get_list("Payslip", filters={"employee": employee_id},  privilege=True, fetch_linked_tables=True, fetch_linked_fields=True)
        data = []
        if payslips:
            data = payslips
            return data
            
    def get_payslip_analytics(self, employee_id):
        payslips = self.get_list("Payslip", filters={"employee": employee_id, "created_on__gt":dates.get_first_date_of_current_year()},  privilege=True)
        data = {
            "overall_basic_pay": 0.00,
            "overall_gross": 0.0,
            "overall_earnings": 0.0,
            "overall_deductions": 0.0,
            "overall_advance_amount": 0.0,
            "overall_advance_repaid": 0.0,
            "overall_total_advance_repaid": 0.0,
            "overall_net": 0.0,
            "overall_working_days": 0.0,
            "overall_current_leave_days": 0.0,
            "overall_current_leave_value": 0.0,
            "overall_tax": 0.00,
            "overall_napsa": 0.00,
            "overall_ytd_pla": 0.00,
            "overall_private_pension": 0.00,
        }
        if payslips:
            data = payslips
            analyzed = self.payroll_analytics.calculate_payslips_ytd_stats(data)
            if analyzed.get("status")== utils.ok:
                data = analyzed.get("data")
        return data
 
    
    def get_staffing_plan(self, filters=None, limit=None, privilege=False):
        staffing_plans = self.dbms.get_list("Staffing", filters=filters, user=self.user, privilege=None)
        if  staffing_plans  is not None and  staffing_plans.get("status") == utils.ok and  staffing_plans.get("data"):
            return staffing_plans

    def get_employee_bonuses(self, name):
        bonuses = self.dbms.get_list("Bonus", filters={"employee": name}, privilege=True)
        
    def get_leave_allocated(self, name):
        leave_allocated = self.dbms.get_list("Leave_Allocation", name, privilege=True)
        if leave_allocated.get("status")== utils.ok:
            return leave_allocated.get("data").get("rows")
        else:
            return leave_allocated
    def leave_application (self):
        return self.get_list("Leave_Application", privilege=True)

    def get_leave_entries(self, filters={}, fetch_linked_fields=None):
            leaves =None
            leave_entry = self.dbms.get_list("Leave_Entry", filters=filters, fetch_linked_fields=fetch_linked_fields)
            if leave_entry.status == utils.ok:
                leaves = leave_entry.data.rows
            return leaves
    def get_leave_types(self, filters=None):
        leave_types = self.get_list("Leave_Type", privilege=True)
        if leave_types:
            return leave_types
        else:
            return None

    def get_leave_commutations_by_employee (self, emp):
        return_dict = utils.from_dict_to_object ({
            "balance": 0.00,
            "outstanding": 0.00
        })
        commutated_leave = self.get_list ("Leave_Commutation", filters={"employee": emp, "paid": "Unsettled", "approved": "Approved"})
        if commutated_leave:
            for cld in commutated_leave:
                return_dict.balance += cld.balance if cld.balance else return_dict.balance
                return_dict.outstanding += cld.amount if cld.amount else return_dict.outstanding
        return return_dict

    def get_employee_info (self, user_id=None, employee_id=None, get_leave_days=True, get_payslips=True, get_payslip_analytics=True, get_appraisals = True, get_expenses=False, get_advance=False, get_work_plan=False, get_overtime=False, get_employee_separation = True, get_promotion=True, get_commutation=True, privilege=False, get_welfare=True):
        employee = None
        if user_id:
            employee = self.get_list("Employee", filters={"user":user_id}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
            if employee:
                employee = employee[0]
        elif employee_id:
            employee = self.get_doc("Employee", employee_id, privilege=True)
            if employee:
                employee = employee
        self.employee = employee
        if get_leave_days:
            employee["leave_summary"] = self.get_employee_leave_days(self.employee.id)
        if get_payslips:
            employee["payslips"] = self.get_employee_payslips(self.employee.id)
        if get_payslip_analytics:
            employee["payslip_analytics"] = self.get_payslip_analytics(self.employee.id)
        if get_overtime:
            employee['overtime'] = self.get_overtime_data (self.employee.id)

        if get_commutation:
            employee['commutation'] = self.get_leave_commutations_by_employee (self.employee.id)
        if get_advance:
            advances = self.get_advance_data (self.employee.id)
            if not advances:
                employee['advance'] = 0.00
            else:
                for advance in advances:
                    employee[advance.source_type] = {
                        "amount": advance.monthly_repayment,
                        "repayment_period": advance.repayment_period
                    }
        # if get_advance:
        #     advances = self.get_advance_data (self.employee.id)
        #     if not advances:
        #         employee['advance'] = 0.00
        #     else:
        #         for advance in advances:
        #             employee[advance.source_type] = {
        #                 "amount": advance.monthly_repayment,
        #                 "repayment_period": advance.repayment_period
        #             }
        if get_employee_separation:
            employee['separation']  = self.get_employee_separation_details(self.employee.id)
        if get_appraisals:
            employee['employee_appraisals'] = self.get_employee_appraisals(self.employee.id)
        if get_promotion:
            employee['promotion'] = self.get_employee_promotion(self.employee.id)
        if get_welfare:
            welfare = self.get_welfare (self.employee.id)
            if welfare and len(welfare) > 0:
                for wf in welfare:
                    employee[wf.source_type] = {
                        "amount": wf.monthly_amount,
                        "units": wf.units
                    }
            else:
                employee['welfare'] = 0.00
        if get_work_plan:
            employee['work_plan'] = self.get_work_plan (self.employee.id)
        return utils.respond(utils.ok, employee)
    def get_welfare (self, employee):
        return self.get_list ("Welfare_Entries", filters= {"is_active": "yes", "employee": employee, "payment_method": "Payroll"})

    def get_work_plan (self, employee):
        work_plan = self.get_list ("Work_Plan_Task", filters={"is_current": 1, "planer_of_work_plan": employee})
        # work_plan = self.get_list ("Work_Plan_Task", filters={"progress_tracker__in": ["In Progress", "Pending", "Need Some More Time"], "is_current": 1, "status": "Active", "planer_of_work_plan": employee})
        if work_plan:
            work_plan = self.hr_analytics.group_work_plan (work_plan)
            if work_plan.status == utils.ok:
                return work_plan.data
            return []
        else:
            return []
    def get_employee(self,user_id=None, employee_id=None, get_leave_days=True, get_payslips=True, get_payslip_analytics=True, get_appraisals=True, get_expenses=False, get_advance=False, get_work_plan=False, get_overtime=False, get_all=False,get_employee_separation = True,order_by=[]):
        if get_all:
            employees_list = []
            employees = self.get_list ("Employee", order_by=order_by)
            if employees:
                for employee in employees:
                    emp =  self.get_employee_info (employee_id=employee.name, get_leave_days=get_leave_days, get_payslips=get_payslips, get_payslip_analytics=get_payslip_analytics,get_appraisals=get_appraisals,get_expenses=get_expenses, get_advance=get_advance, get_work_plan=get_work_plan, get_overtime=get_overtime, get_employee_separation = get_employee_separation)
                    if emp.status ==utils.ok:
                        employees_list.append (emp.data)
            return utils.respond(utils.ok, employees_list)
        else:
            return self.get_employee_info (user_id=user_id, employee_id=employee_id, get_leave_days=get_leave_days, get_payslips=get_payslips, get_payslip_analytics=get_payslip_analytics,get_appraisals=get_appraisals,get_expenses=get_expenses, get_advance=get_advance, get_work_plan=get_work_plan, get_overtime=get_overtime)



    def accept_separation (self, object):
        dbms =self.dbms
        # object =self.object
        core_hr = Core_Hr (dbms=dbms, obj=object,)
        mailing = Mailing(dbms=dbms)
        separation = object.body
        user =dbms.current_user
        email_body =None

        employee_info = core_hr.get_doc ("Employee", name=separation.employee)
        if employee_info:
            if separation.separation_type == "Termination":
                status = "Terminated"
                msg = f"""
                    We are writing to inform you that your employment with {employee_info.company} has been {status}, effective {separation.last_day_of_work}. 
                    This decision has been made after careful consideration and in accordance with our company's policies and procedures.
                    If you have any questions or concerns, please do not hesitate to reach out to our HR department.

                    
                """

                email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Sincerely")
            elif separation.separation_type == "Retirement":
                status = "Retired"
                msg = f"""
                    We are pleased to inform you that your retirement from {employee_info.company} has been officially processed, effective {separation.last_day_of_work}. 
                    We wish you a happy and fulfilling retirement!
                    Your dedication and contributions to our organization are greatly appreciated, and you will be missed. We hope you enjoy this new chapter in your life 
                    and pursue all the things that bring you joy.
                    If you have any questions or concerns, please don't hesitate to reach out to our HR department.
                    <br/>
                """

                email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Best regards")
            elif separation.separation_type == "Resignation":
                status = "Resigned"
                msg = f"""
                    This letter serves as formal confirmation that your resignation from {employee_info.company} has been accepted, effective {separation.resignation_date}. 
                    Your decision to leave the company has been processed, and your employment with us will officially end on {separation.last_day_of_work}.
                    We appreciate the contributions you made during your time with us and wish you the best in your future endeavors. 
                    <br/>
                    If you have any questions or concerns, please don't hesitate to reach out to our HR department.
                    <br/>
                """

                email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Best regards")
            elif separation.separation_type == "Redundancy":
                status = "Redundant"
                msg = f"""
                    We regret to inform you that your position at {employee_info.company} has been made redundant, effective {separation.last_day_of_work}.  
                    This decision has been made after careful consideration and in accordance with our company's policies and procedures.

                    We appreciate your contributions to the company and are grateful for your service.
                    If you have any questions or concerns, please don't hesitate to reach out to our HR department.
                    <br/>
                """

                email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Best regards")
            elif separation.separation_type == "End Of Contract":
                status = "Left"
                msg = f"""
                    We are writing to inform you that your contract with {employee_info.company} has come to an end, 
                    effective {separation.last_day_of_work}. We appreciate the work you have done during your time 
                    with us and are grateful for your contributions. 
                    <br/>
                    <br/>
                    <br/>
                    If you have any questions or concerns, please don't hesitate to reach out to us. We wish you the best in your future endeavors.
                    
                """
            else :
                status = "Separated"
                msg = f"""
                    We am writing to inform you that your employment with {employee_info.company}  has been {separation.separation_type}, effective {separation.resignation_date} to {separation.last_day_of_work}. 
                    This decision has been made after careful consideration and in accordance with our company's policies and procedures.
                    If you have any questions or concerns, please do not hesitate to reach out to me or our HR department.
                    <br/>
                """

                email_body =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=msg, final_greetings="Best regards")
            employee_info.status = status
            employee_info.doc_status = status
            employee_info.is_separated = 1
            employee_info.last_day_of_work = separation.last_day_of_work

            dbms.update ("Employee", employee_info, update_submitted=True)
            if separation.skip_exit_interview:
                dbms.create ("Exit_Interview", utils.from_object_to_dict ({
                    "employee": employee_info.name,
                    "employee_name": employee_info.full_name,
                    "department": employee_info.department,
                    "designation": employee_info.designation,
                    "date_of_joining": employee_info.date_of_joining,
                    "status": "Pending"
                }))

        if employee_info:
            confirmation_mail =Default_Templates().basic_template(sender=user.first_name+" "+user.last_name, receiver=employee_info.full_name, company=None, body=f"<h1> Separation of {employee_info.full_name} Has Been</h1><p> ")
            mailing.send_mail (recipient=user.email, subject="Separation Submission", body=confirmation_mail)
            if email_body !=None:
                mailing.send_mail (recipient=employee_info.email, subject="Separation Submission", body=email_body)

        separation.status = status
        dbms.update("Employee_Seperation", separation, update_submitted=True, privilege=True)

    def get_employee_separation (self, employee_id):

        core_assets = Core_Assets (dbms=self.dbms, object=self.object)
        employee = self.get_employee (employee_id=employee_id, get_advance=True, get_overtime=True, get_appraisals=True)

        employee_info = None
        if employee.status == utils.ok:
            employee_info = employee.data
            assets =utils.from_dict_to_object({})
            assets_as_emp =None
            assets_as_user =None


            assets_as_emp = core_assets.asset_custodian (custodian=employee_info.name, type="employee") or None
            assets_as_user = core_assets.asset_custodian (custodian=employee_info.user, type="user") if employee_info.user else None

            if assets_as_user !=None and assets_as_emp!=None:
                assets.total_assets =assets_as_emp.total_assets + assets_as_user.total_assets
                assets.asset_list =assets_as_emp.asset_list + assets_as_user.asset_list
                assets =assets_as_emp + assets_as_user
            elif assets_as_emp !=None:
                assets =assets_as_emp
            elif assets_as_user !=None:
                assets =assets_as_user


            get_leave = self.get_leave_entries (filters={"employee": employee_id, "remaining_leave_days__gt": 0})
            earnings = []
            deductions = []
            for deduction_ in employee_info.deductions:
                get_salary_deductions = self.get_doc ("Salary_Component", name=deduction_.deduction)
                if get_salary_deductions:
                   deductions.append(get_salary_deductions)
            for earning_ in employee_info.earnings:
                get_salary_earnings = self.get_doc ("Salary_Component", name=earning_.earning)
                if get_salary_earnings:
                   earnings.append(get_salary_earnings)

            employee_info.deductions = deductions
            employee_info.earnings = earnings
            paid_leave_type = []
            if get_leave:
                for leave in get_leave:
                    get_leave_type = self.get_doc ("Leave_Type", name=leave.leave_type)
                    if get_leave_type and get_leave_type.is_compensatory:
                        paid_leave_type.append (get_leave_type.name)
            if assets:
                employee_info.assets = assets
            employee_info.leave_summary.paid_leave = paid_leave_type
        if not employee_info:
            return utils.respond (utils.no_content, response={"status": utils.no_content, "error_message": "No Content Found"})
        return utils.respond (utils.ok, response=employee_info)
    
    def get_employee_separation_details(self, employee_id):
        result_object = {}
        emp_separation = self.dbms.get_list("Employee_Seperation", filters={'employee': employee_id }, privilege=True)
        if emp_separation.status == utils.ok:
            result = emp_separation.data.rows
            for data in result:
                result_object["employee"] = data.employee
                result_object["employee_name"] = data.employee_name
                result_object["separation_status"] = data.status
                result_object["separation_date"] = data.resignation_date
                result_object["notice_period"] = data.notice_period
                result_object["last_day_of_work"] = data.last_day_of_work
        return result_object
    
    def get_employee_work_plan_tasks(self, employee_id):
            result = {}
            emp_work_plan = self.dbms.get_list("Work_Plan", filters={'employee': employee_id },fetch_linked_tables=True, privilege=True)
            if emp_work_plan.status == utils.ok:
                data = emp_work_plan.data.rows
                for list in data:
                    task_data = list.work_plan_task
                    for task in task_data:
                        result["title"] = task.title
                        result["description"] = task.description
                        result["out_come"] = task.out_come
                        result["progress_tracker"] = task.progress_tracker
                        result["expected_start_date"] = task.expected_start_date
                        result["expected_end_date"] = task.expected_end_date
                        result["task_status"] = task.task_status
            return result
    
    def get_employee_imprest(self, user):
        data = []
        emp_imprest = self.dbms.get_list("Imprest", filters={'initiator': user },fetch_linked_tables=True, privilege=True)
        if emp_imprest.status == utils.ok:
            data = emp_imprest.data.rows
        return  data
    
    def get_employee_workflow(self):
        workflow = self.dbms.get_list("Workflow",fetch_linked_tables=True, privilege=True)
        if workflow.status == utils.ok:
            data = workflow.data.rows
        return  data
    
    
    def get_employee_tax_band(self):
        employees_tax_band = self.dbms.get_list("Income_Tax_Band", filters={"is_current":1}, privilege=True)
        if employees_tax_band.status == utils.ok:
            employees_tax_band_data = employees_tax_band.data.rows[0]
            return utils.respond(utils.ok, employees_tax_band_data)
        return utils.respond(utils.no_content,"No content found")
    
    def get_employee_promotion(self, employee_id="Gresham Sichoonda - 0003"):
        res = {}
        employee_promotion = self.dbms.get_list("Employee_Promotion", filters={"employee": employee_id}, privilege=True)

        if employee_promotion.status == utils.ok:
                employee_promotion_data = employee_promotion.data.rows
                for data in employee_promotion_data:
                    res["employee"] = data.employee
                    res["employee_name"] = data.employee_name
                    res["current_basic"] = data.current_basic
                    res["revised_basic"] = data.revised_basic
                    res["promotion_date"] = data.promotion_date
        return res

    # ===============================================APPRAISAL CONTROLLERS==========================================

    def get_employee_appraisals(self, employee, fetch_360=True, fetch_self=True):
        result = {
            "appraisals": [],
            "self_appraisals": []
        }

        if fetch_360:
            appraisal_info = self.dbms.get_list("Appraisal", filters={"appraisee": employee, "docstatus": 1}, privilege=True)
            if appraisal_info.status == utils.ok:
                result["appraisals"] = appraisal_info.data.rows

        if fetch_self:
            self_appraisal_info = self.dbms.get_list("Self_Appraisal", filters={"appraisee": employee, "docstatus": 1}, privilege=True)
            if self_appraisal_info.status == utils.ok:
                result["self_appraisals"] = self_appraisal_info.data.rows

        return result


    def get_appraisal_open_ended_questions(self):
        result = []
        open_ended = self.dbms.get_list("Open_Ended_Question", privilege=True)
        if open_ended.status == utils.ok:
            result = open_ended.data.rows
        return result
    

    def get_appraisal_closed_ended_questions(self, fetch_options=True):
        result = utils.from_dict_to_object({"questions": [], "options":[]})
        closed_ended = self.dbms.get_list("Closed_Ended_Question", privilege=True)
        if closed_ended.status == utils.ok:
            result.questions = closed_ended.data.rows
        if fetch_options:
            options = self.dbms.get_list("Appraisal_Question_Option", privilege=True)
            if options.status == utils.ok:
                result.options = options.data.rows
        return result
    

    def __generate_appraisal_email_content(self, doc):
        content = f"""
            <div style="width:100%"><h3>HELLO {doc.appraiser_name}</h3> <br>
                <p>
                    You have been invited to appraise {doc.appraisee_name}. Kindly note that you are required to submit the subjected 
                    appraisal form by {doc.appraisal_date}.
                </p>
                <hr>
                <p> To fill in the appraisal form, please open <a href="" style="margin-left:5px">{doc.name}</a> </p> <br>
                Or 
                <br>
                <a href="" style="background-color: #151030; width: 200px;height:40px;border-radius:10px;color:white;text-aligh:center">
                    CLICK HERE
                </a> 
                to be redirected to the appraisal form. 
                <br>

                <h4>Thank you for your cooperation.</h4>

                <h4>HUMAN RESOURCE MANAGEMENT DEPARTMENT.</h4>
            </div>
        """
        return Default_Template.template(content)

    def __generate_self_appraisal_email_content(self, doc):
        content = f"""
            <div style="width:100%"><h3>HELLO {doc.appraisee_name}</h3> <br>
                <p>
                    You have been invited to appraise {doc.appraisee_name}. Kindly note that you are required to submit the subjected 
                    appraisal form by {doc.appraisal_closure_date}.
                </p>
                <hr>
                <p> To fill in the appraisal form, please open <a href="" style="margin-left:5px">{doc.name}</a> </p> <br>
                Or 
                <br>
                <a href="" style="background-color: #151030; width: 200px;height:40px;border-radius:10px;color:white;text-aligh:center">
                    CLICK HERE
                </a> 
                to be redirected to the appraisal form. 
                <br>

                <h4>Thank you for your cooperation.</h4>

                <h4>HUMAN RESOURCE MANAGEMENT DEPARTMENT.</h4>
            </div>
        """
        return Default_Template.template(content)
    
    def generate_contract_creation_email_content(self, doc):
        content = f"""
            <div style="width:100%">
                <h3>Dear {doc.full_name},</h3>
                <p>
                    I am pleased to extend an offer of employment for the position of {doc.position_name} at {doc.company}. We are excited about the prospect of you joining our team and contributing to our ongoing success.
                </p>
                <p>Below are the details of your employment contract:</p>
                <p>{doc.contract_content}</p>
                <p>
                    To formally accept this offer, please sign and return the attached contract document by {doc.deadline_for_acceptance}. If you have any questions or need further clarification, feel free to reach out to me directly at {doc.contact_phone} or via email at {doc.contact_email}.
                </p>
                <p>We look forward to your positive response and are excited about the opportunity to work together.</p>
                <h4>Best regards,</h4>
                <p>
                    {doc.company}<br>
                   
                </p>
            </div>
        """
        return Default_Template.template(content)
    

    def generate_appraisal_360_form(self):
        results = utils.from_dict_to_object({"successful":[],"failed":[]})
        setup = self.object.body
        open_qs = []
        closed_qs = []
        total_questions = 0
        if setup.include_closed_ended_questions == 1:
            open_qs = self.get_appraisal_open_ended_questions()
            total_questions += len(open_qs)
        if setup.include_closed_ended_questions == 1:
            closed = self.get_appraisal_closed_ended_questions(fetch_options=False)
            closed_qs = closed.questions
            total_questions += len(closed_qs)

        for row in setup.appraisers:
            appraisee = row.linked_fields.appraisee
            appraiser = row.linked_fields.appraiser
            new_form = utils.from_dict_to_object({
                "appraisal_setup": setup.name,
                "appraisal_date": setup.appraisal_closure_date,
                "appraisee": appraisee.name,
                "appraisee_name": appraisee.full_name,
                "appraiser": appraiser.name,
                "appraiser_name": appraiser.full_name,
                "department": appraisee.department,
                "appraisal_quarter": setup.appraisal_quarter,
                "total_open_score" : 0,
                "total_closed_score": 0,
                "total_questions": total_questions,
                "total_open_ended_questions": len(open_qs),
                "total_closed_ended_questions": len(open_qs),
                "overall_score": setup.overall_score,
                "status": "Draft",
                "open_ended_questions": [],
                "closed_ended_questions":[] 
            })
            if open_qs:
                for open_q in open_qs:
                    new_form.open_ended_questions.append({open_q.name: ""})
            if closed_qs:
                for closed_q in closed_qs:
                    new_form.closed_ended_questions.append({closed_q.name: ""})
            
            created = self.dbms.create("Appraisal", new_form, self.object.user)
            if created.status == utils.ok:
                mail = self.mailing.send_mail(appraiser.email, "Appraisal Invitation", self.__generate_appraisal_email_content(created.data))
                
                results.successful.append(created.data)
            else:
                new_form.error_message = created.error_message
                results.failed.append(new_form)
        return utils.respond(utils.ok, results)



    def generate_self_appraisal_form(self):
        results = utils.from_dict_to_object({"successful":[],"failed":[]})
        setup = self.object.body
        open_qs = []
        closed_qs = []
        total_questions = 0
        if setup.include_closed_ended_questions == 1:
            open_qs = self.get_appraisal_open_ended_questions()
            total_questions += len(open_qs)
        if setup.include_closed_ended_questions == 1:
            closed = self.get_appraisal_closed_ended_questions(fetch_options=False)
            closed_qs = closed.questions
            total_questions += len(closed_qs)

        for row in setup.appraisees:
            appraisee = row.linked_fields.appraisee
            new_form = utils.from_dict_to_object({
                "appraisal_setup": setup.name,
                "appraisal_closure_date": setup.appraisal_closure_date,
                "appraisee": appraisee.name,
                "company": setup.setup,
                "appraisee_name": appraisee.full_name,
                "department": setup.department,
                "appraisal_quarter": setup.appraisal_quarter,
                "total_open_score" : 0,
                "total_closed_score": 0,
                "total_questions": total_questions,
                "total_open_ended_questions": len(open_qs),
                "total_closed_ended_questions": len(open_qs),
                "overall_score": setup.overall_score,
                "status": "Draft",
                "open_ended_questions": [],
                "closed_ended_questions":[]
            })
           
            if open_qs:
                for open_q in open_qs:
                    new_form.open_ended_questions.append({open_q.name: ""})
            if closed_qs:
                for closed_q in closed_qs:
                    new_form.closed_ended_questions.append({closed_q.name: ""})
            
            created = self.dbms.create("Self_Appraisal", new_form, self.object.user)
            if created.status == utils.ok:
                mail = self.mailing.send_mail(appraisee.email, "Appraisal Invitation", self.__generate_self_appraisal_email_content(created.data))
                
                results.successful.append(created.data)
            else:
                new_form.error_message = created.error_message
                results.failed.append(new_form)
        return utils.respond(utils.ok, results)
    
    def leave_application(self, filters={} ):
        leave_applications = self.dbms.get_list("Leave_Application", filters=filters, privilege=True)
        if leave_applications is not None and leave_applications.status == utils.ok and leave_applications.data:
            return leave_applications.data
        else:
            return None

    def to_and_from_hours_to_days (self, value: float | int, working_hours: float | int = None, return_type="hours"):
        if str (return_type).lower () == "hours":
            return working_hours * value
        elif str (return_type).lower () == "days":
            return value / working_hours
        return None
    def hours_to_milliseconds(self, hours):
        milliseconds = hours * 60 * 60 * 1000
        return milliseconds


    def get_payroll_employee_info (self, employee):
        pp (employee)

    def get_employee_payroll_content (self, employee, sc):
        try:
            components_vals = {}
            query = """
                SELECT * FROM payroll_activity_entries
                WHERE (cleared = 0 OR cleared IS NULL)
                AND employee_id = %s
                AND balance > %s
            """
            employee_payroll_content = self.fetch_data_from_sql (query, (DataConversion.safe_get(employee, "id"), 0,))
            if employee_payroll_content:
                df = utils.to_data_frame (employee_payroll_content)
                employee_payroll_content = {
                    key: group.to_dict('records')
                    for key, group in df.groupby('salary_component')
                }
            else:
                employee_payroll_content = utils.from_dict_to_object ()

            employee['deductions'] = json.loads (employee['deductions']) if isinstance (employee['deductions'], str) else []
            employee['earnings'] = json.loads (employee['earnings']) if isinstance (employee['earnings'], str) else []
            custom = DataConversion.safe_get (employee, 'unstandardized_components', [])
            customs = json.loads (custom) if custom else []
            if DataConversion.safe_gt (len (customs), 0, int):
                for c_sc in customs:
                    c_name = DataConversion.safe_get (c_sc, "component_name")
                    DataConversion.safe_set (employee, c_name, DataConversion.convert_to_float (DataConversion.safe_get (c_sc, "component_value", 0)))
                    DataConversion.safe_set (employee, f"main_value_{c_name}", DataConversion.convert_to_float (DataConversion.safe_get (c_sc, "main_value", 0)))
        
            if sc:
                for salary_component in sc.keys ():
                    salary_c_v = DataConversion.safe_get (employee_payroll_content, salary_component)
                    if salary_c_v:

                        sc_info = DataConversion.safe_list_get (salary_c_v, 0)
                        remaining_period = DataConversion.convert_to_int (DataConversion.safe_get (sc_info, "remaining_period", 0))
                        balance_amount = DataConversion.convert_to_float (DataConversion.safe_get (sc_info, "remaining_balance", 0))

                        if DataConversion.safe_e (salary_component, "Salary Advance", str, True):
                            sa_dues_data = utils.to_data_frame (salary_c_v)

                            if "salary_component" in sa_dues_data.columns:

                                sa_dues = {
                                    key: group.to_dict('records')
                                    for key, group in sa_dues_data.groupby('reference_type')
                                }

                                normal_advance = DataConversion.safe_get (sa_dues, "Advance_Application", [])
                                second_advance = DataConversion.safe_get (sa_dues, "Second_Salary_Advance_Application", [])
                                
                                if DataConversion.safe_gt(len (second_advance), 0, int):
                                    DataConversion.safe_set (employee, salary_component, DataConversion.convert_to_float (DataConversion.safe_get (DataConversion.safe_list_get (second_advance, 0), "balance", 0)))
                                else:
                                    DataConversion.safe_set (employee, salary_component, DataConversion.convert_to_float (DataConversion.safe_get (DataConversion.safe_list_get (normal_advance, 0), "balance", 0)))
                                
                                DataConversion.safe_set (components_vals, salary_component, {
                                    "balance": balance_amount,
                                    "remaining_period": remaining_period,
                                })
                        else:
                            DataConversion.safe_set (employee, salary_component, DataConversion.convert_to_float (DataConversion.safe_get (DataConversion.safe_list_get (salary_c_v, 0), "balance", 0)))
            DataConversion.safe_set (employee, "components_vals", components_vals)
            # if DataConversion.safe_get (employee, "name") == "911":
            # pp (employee)
            return employee
        except Exception as e:
            pp (f"ERROR: {e}")
    
    def validate_staff_requisition(self, body):
        # if not body.section:
        #     throw(f"The field 'section', has an invalid value.")
        if not DataConversion.safe_get (body, "source_of_recruitment", None):
            throw(f"The field 'source of recruitment', has an invalid value.")
        if not DataConversion.safe_get (body, "academic", None):
            throw(f"The field 'academic', has an invalid value.")
        if not DataConversion.safe_get (body, "professional", None):
            throw(f"The field 'professional', has an invalid value.")
        if not DataConversion.safe_get (body, "experience", None):
            throw(f"The field 'experience', has an invalid value.")
        if not DataConversion.safe_get (body, "requisitioned_by", None):
            throw(f"The field 'requisitioned by', has an invalid value.")
        if not DataConversion.safe_get (body, "requisitioners_job_title", None):
            throw(f"The field 'requisitioners job title', has an invalid value.")
        if not DataConversion.safe_get (body, "staffing_department", None):
            throw(f"The field 'staffing department', has an invalid value.")
        if not DataConversion.safe_get (body, "staffing_job_title", None):
            throw(f"The field 'staffing job title', has an invalid value.")
        if not DataConversion.safe_get (body, "employee_grade", None):
            throw(f"The field 'employee grade', has an invalid value.")
        if not DataConversion.safe_get (body, "contract_type", None):
            throw(f"The field 'contract type', has an invalid value.")        
        if not DataConversion.safe_get (body, "number_required", None):
            throw(f"The field 'number required', has an invalid value.")
        if not DataConversion.safe_get (body, "approved_establishment", None):
            throw(f"The field 'approved establishment', has an invalid value.")
        if not DataConversion.safe_get (body, "date_required", None):
            throw(f"The field 'date required', has an invalid value.")

    def validate_job_advertisement(self, body):
        if body:
            if not DataConversion.safe_get (body, "designation", None):
                utils.throw(f"the field 'designation', is not having a valid value.") 
            if not DataConversion.safe_get (body, "company", None):
                utils.throw(f"the field 'company', is not having a valid value.") 
            if not DataConversion.safe_get (body, "department", None):
                utils.throw(f"the field 'department', is not having a valid value.") 
            if not DataConversion.safe_get (body, "vacancies", 0):
                utils.throw(f"the field 'vacancies', is not having a valid value.")
            if not DataConversion.safe_get (body, "description", None):
                fetch_job_title =self.get_doc("Designation", DataConversion.safe_get (body, "designation", None))
                DataConversion.safe_set (body, "description", DataConversion.safe_get (fetch_job_title, 'description', ''))

            return body
        else:
            throw("No data was provided for the validation.")

    def validate_graduate_development_enrollment(self, body):
        if not DataConversion.safe_get (body, "requisitioned_by", None):
            throw(f"The field 'requisitioned by', has an invalid value") 
        if not DataConversion.safe_get (body, "department", None):
            throw(f"The field 'department', has an invalid value") 
        if not body.position:
            throw(f"The field 'position', has an invalid value") 
        if not DataConversion.safe_get (body, "number_required", None):
            throw(f"The field 'number required', has an invalid value") 
        if not DataConversion.safe_get (body, "employee_grade", None):
            throw(f"The field 'employee grade', has an invalid value")
        if not DataConversion.safe_get (body, "date_required", None):
            throw(f"The field 'date required', has an invalid value") 
        if not DataConversion.safe_get (body, "duration_of_programme", None):
            throw(f"The field 'duration of programme', has an invalid value") 
        # if not DataConversion.safe_get (body, "budget", None):
        #     throw(f"The field 'budget', has an invalid value") 
        # if not DataConversion.safe_get (body, "university_or_college", None):
        #     throw(f"The field 'university or college', has an invalid value") 
        # if not DataConversion.safe_get (body, "academic", None):
        #     throw(f"The field 'academic', has an invalid value")
        # if not DataConversion.safe_get (body, "professional", None):
        #     throw(f"The field 'professional', has an invalid value")

        return body





