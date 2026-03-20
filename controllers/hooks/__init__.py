from controllers.form_fields.payroll.payroll_processor import fetch_payroll_processor_fields
from controllers.framework.core.approver import Approver
from controllers.hooks.dashboards.hr import employee_separation_dashboard, leave_commutation
from controllers.hooks.dashboards.hr.employee_skill_distribution import Employee_skill_distribution_dashboard
from controllers.hooks.dashboards.hr.leave_allocation import Leave_Allocation_Dashboard
from controllers.hooks.dashboards.hr.probation import *
from controllers.hooks.dashboards.hr.recurement_dashboard import main_recrement_dashboard
from controllers.hooks.dashboards.hr.welfare_dashbiard import employee_welfare_dashboard
from controllers.hooks.dashboards.payroll.payroll_and_loan_dashboard import *
# from controllers.hooks.downloa_data_customizer.customer_statement import on_customer_statement_download
from controllers.hooks.dashboards.staff.staff_skill_profile import *
from controllers.hooks.forms.controller.background_job import idlelize_job
from controllers.hooks.forms.controller.module import *
from controllers.hooks.forms.controller.tenant import *
from controllers.hooks.forms.core.default_dashboard import *
from controllers.hooks.forms.core.menu_card import *
from controllers.hooks.forms.core.workflow import before_workflow_save, before_workflow_update
from controllers.hooks.forms.hr.employee_welfare_feedback import employee_welfare_questions
from controllers.hooks.forms.hr.industrial_relations import *
from controllers.hooks.forms.hr.job_advertisement import *
from controllers.hooks.forms.hr.recuitment import *
from controllers.hooks.forms.hr.salary_increment import *
from controllers.hooks.forms.hr.separartion import *
from controllers.hooks.forms.hr.separation import *
from controllers.hooks.forms.payroll.allowance_and_benefit import *
from controllers.hooks.forms.payroll.petty_cash_and_imprest import *
from controllers.hooks.forms.staff.imprest_and_petty_cash import *
from controllers.hooks.forms.staff.skills_gap import before_skills_gap_submit
from controllers.hooks.forms.web.module_pricing import after_module_pricing_fetch
from controllers.hooks.functions.x_fetch.hr.bj_calender import BJ_Calender
from controllers.hooks.functions.x_fetch.hr.bj_leave import BJ_Leave
from controllers.hooks.functions.x_fetch.hr.bj_reminders import BJ_Reminders
from controllers.hooks.functions.x_fetch.hr.employee import get_salary_components
from controllers.hooks.functions.x_fetch.hr.employee import *
from controllers.hooks.functions.x_fetch.hr.industrial_relations_bj import Industrial_Relations
from controllers.hooks.functions.x_fetch.hr.recruitment import *
from controllers.hooks.functions.x_fetch.hr.separation_background_jobs import Separation_BJ
from controllers.hooks.functions.x_fetch.hr.bj_back_from_leave import back_from_leave
from controllers.hooks.functions.x_post.hr.employee_disciplinary import *
from controllers.hooks.functions.x_post.hr.employee_profile import Employee_Profile
from controllers.hooks.functions.x_post.hr.fetch_bidget_line import fetch_budget_line
from controllers.hooks.functions.x_post.hr.fetch_employee_profile_data import fetch_employee_profile_data
from controllers.hooks.functions.x_post.hr.leave import *
from controllers.hooks.functions.x_post.hr.recruitement import *
from controllers.hooks.functions.x_post.hr.separartion import update_clearance_form
from controllers.hooks.functions.x_post.hr.staffing_plan import *
from controllers.hooks.functions.x_post.payroll.components_salary import link_component_to_all_employees
from controllers.hooks.functions.x_post.payroll.prepayroll_payments import create_pre_payment_doc
from controllers.hooks.functions.x_post.staff.employee_welfare import staff_survey_feedback
from controllers.hooks.functions.x_post.staff.staff_leave_summary import *
from controllers.hooks.import_script.hr.employee_welfare import welfare_importation
from controllers.hooks.import_script.hr.leave_allocation import import_script_for_leave_allocation
from controllers.hooks.import_script.hr.leave_policy import import_script_for_leave_policy
from controllers.hooks.import_script.hr.leave_type import import_script_for_leave_type
from controllers.hooks.import_script.payroll.employee_grade import import_script_for_employees_grade
from controllers.hooks.forms.core.company import before_company_update
from controllers.hooks.forms.hr.work_plan import *
from controllers.hooks.functions.x_fetch.core.role import get_role_cards
from controllers.hooks.functions.x_fetch.onboarding import Onboarding
from controllers.hooks.functions.x_post.framework import *
# ============================================================================================

from controllers.hooks.forms.core.role import *
from controllers.hooks.forms.hr.employee_separation import *
from controllers.hooks.forms.payroll.salary_advance import *

# WEB
from controllers.hooks.functions.x_fetch.web import *
from controllers.hooks.functions.x_post.web.web import *

# REPORT IMPORTS
from controllers.hooks.import_script.hr.employee import import_script_for_employees

# procurement
from controllers.hooks.reports.core.audit_trail import audit_trail
from controllers.hooks.reports.core.auth_trail import auth_trail_report
from controllers.hooks.reports.hr.interview_score_sheet import *
from controllers.hooks.reports.hr.employee_attendace import monthly_attendance
from controllers.hooks.reports.hr.short_listed_applicants import *
from controllers.hooks.reports.hr.short_listed_report import *
from controllers.hooks.reports.hr.training_effectiveness import *
from controllers.hooks.reports.hr.hr_reports import *

# HR IMPORTS
# hr forms
from controllers.hooks.forms.hr.leave_allocation import *
from controllers.hooks.forms.hr.leave_application import *
from controllers.hooks.forms.hr.employee import *
from controllers.hooks.forms.hr.employee_promotion import *
from controllers.hooks.forms.hr.appraisal_setup import *
from controllers.hooks.forms.hr.appraisal import *
from controllers.hooks.forms.hr.closed_ended_qns import *
from controllers.hooks.forms.hr.self_appraisal import *
from controllers.hooks.forms.hr.staffing_plan import *
from controllers.hooks.forms.hr.emails import *
from controllers.hooks.forms.hr.interview_schedule import *
from controllers.hooks.forms.hr.job_offer import *
from controllers.hooks.forms.hr.training_program import *
from controllers.hooks.forms.hr.employee_discipline import *
from controllers.hooks.forms.hr.out_come import *
from controllers.hooks.forms.hr.final_statement import *
from controllers.hooks.forms.hr.employee_grievance import *
from controllers.hooks.forms.hr.appointment_letter import *
from controllers.hooks.forms.hr.training_feedback import *
from controllers.hooks.forms.hr.employee_attendance import *
from controllers.hooks.forms.hr.contracts import *
from controllers.hooks.forms.hr.job_application import *
from controllers.hooks.forms.hr.leave_commutation import *
from controllers.hooks.forms.hr.gratuity import *
from controllers.hooks.forms.hr.interview_rating import *
from controllers.hooks.forms.hr.leave_policy import *

# hr dashboard
from controllers.hooks.dashboards.hr.performance_dashboard import *
from controllers.hooks.dashboards.hr.training_program import *
from controllers.hooks.dashboards.hr.industrial_relations_dashboard import *
from controllers.hooks.dashboards.hr.recruitment_dashboard_ import *
from controllers.hooks.dashboards.hr.leave_dashboard import *
from controllers.hooks.dashboards.hr.dashboard import *
from controllers.hooks.dashboards.hr.designation import *
from controllers.hooks.dashboards.hr.employee import *
from controllers.hooks.dashboards.hr.employee_attendance import *
from controllers.hooks.dashboards.hr.employee_checkin import *
from controllers.hooks.dashboards.hr.staffing_plan import *
from controllers.hooks.dashboards.hr.job_opening import *
from controllers.hooks.dashboards.hr.job_application import *
from controllers.hooks.dashboards.hr.interview import *
from controllers.hooks.dashboards.hr.leave_type_side_view import *
from controllers.hooks.dashboards.hr.self_appraisal import Self_Appraisal
from controllers.hooks.dashboards.hr.appraisal import Appraisal
from controllers.hooks.dashboards.hr.appraisal_setup import Appraisal_Setup
from controllers.hooks.dashboards.hr.employee_grievance import Employee_Grievance
from controllers.hooks.dashboards.hr.employee_promotion import Promotion
from controllers.hooks.dashboards.hr.leave import Leave
from controllers.hooks.dashboards.hr.memo import Memo
from controllers.hooks.dashboards.hr.work_plan import Work_Plan
from controllers.hooks.dashboards.hr.grievance import *
from controllers.hooks.dashboards.hr.case_outcome import *
from controllers.hooks.dashboards.hr.gratuity import *
from controllers.hooks.dashboards.hr.employee_separation import *

# hr reports
from controllers.hooks.reports.hr.employee_exit import *
from controllers.hooks.reports.hr.employee_on_leave import *
from controllers.hooks.reports.hr.recruitment_analytics import *
from controllers.hooks.reports.hr.employee_leave_balance import *
from controllers.hooks.reports.hr.leave_summary import *
from controllers.hooks.reports.hr.employee_separation import *
from controllers.hooks.reports.hr.training_feedback import *
from controllers.hooks.reports.hr.appraisal_report import *
from controllers.hooks.reports.hr.self_appraisal_report import *
from controllers.hooks.reports.hr import *
from controllers.hooks.reports.hr.employee_welfare_report import *
from controllers.hooks.reports.hr.employee_grievance_report import *


# hr x_post
from controllers.hooks.functions.x_post.hr.employee import *
from controllers.hooks.functions.x_post.hr.interviews import *
from controllers.hooks.functions.x_post.hr.scholarship import *
from controllers.hooks.functions.x_post.hr.work_plan import *
from controllers.hooks.functions.x_post.hr.skill_levy_employees import *
from controllers.hooks.functions.x_post.hr.attendance import *
from controllers.hooks.functions.x_post.hr.job_application import *
from controllers.hooks.functions.x_post.hr.bonus import *
from controllers.hooks.functions.x_post.hr.gratuity_setup import *
from controllers.hooks.functions.x_post.hr.leave_policy import get_policy_type
from controllers.hooks.functions.x_post.hr.loans import *


# hr xfetch
from controllers.hooks.functions.x_fetch.hr.employees_for_attendance import *

# PAYROLL IMPORTS
from controllers.hooks.forms.payroll.payroll_processor import *
from controllers.hooks.functions.x_post.payroll.overtime_setup import *

from controllers.hooks.functions.x_post.payroll.overtime import *
from controllers.hooks.forms.payroll.overtime import *
from controllers.hooks.forms.payroll.employee_grade import *
from controllers.hooks.dashboards.payroll.overtime import *
from controllers.hooks.dashboards.payroll.advance import *
from controllers.hooks.dashboards.payroll.payslip import *
from controllers.hooks.dashboards.payroll.employee_grade import *
from controllers.hooks.dashboards.payroll.salary_component import *
from controllers.hooks.forms.payroll.income_tax_band import *

#PAYROLL REPORTS
from controllers.hooks.reports.payroll.napsa_report import *
from controllers.hooks.reports.payroll.overtime_report import *
from controllers.hooks.reports.payroll.paye_report import *
from controllers.hooks.reports.payroll.nhima_report import *
from controllers.hooks.reports.payroll.private_insurance import *
from controllers.hooks.reports.payroll.payroll_summary import *
from controllers.hooks.reports.payroll.payroll_payable import *
from controllers.hooks.reports.payroll.advance_report import *
from controllers.hooks.reports.payroll.ecz_imprest import *

# CORE IMPORTS
from controllers.hooks.forms.core.data_importation import *
from controllers.hooks.forms.core.user import *
from controllers.hooks.functions.x_fetch.core.user import *
from controllers.hooks.functions.x_post.core.company import *
from controllers.hooks.functions.x_post.core.mailing import *
from controllers.hooks.functions.x_post.core.mailing import *

# X-FETCH IMPORTS
from controllers.hooks.functions.x_fetch.payroll.payroll import *
from controllers.hooks.functions.x_fetch.hr.appraisal import *
from controllers.hooks.functions.x_fetch.hr.employee import *
from controllers.hooks.functions.x_fetch.core.currency import *
from controllers.modules.payroll.core import *
from controllers.hooks.functions.x_post.hr.employee_resignation import *

# X-POST IMPORTS
from controllers.hooks.functions.x_post.core.data_importation import *
from controllers.hooks.functions.x_post.core.user import *
from controllers.hooks.functions.x_post.hr.final_statement import *
from controllers.hooks.dashboards.hr.skils_distribution import Skills_Distribution

# PRINT
from controllers.hooks.forms.print_configuration.print_controller import *

from controllers.hooks.dashboards.core.user import *
from controllers.hooks.dashboards.hr.dashboard import *
from controllers.hooks.dashboards.hr.designation import *
from controllers.hooks.dashboards.hr.employee import *

from controllers.hooks.dashboards.core.dashboard import *
from controllers.hooks.dashboards.core.currency import *
from controllers.hooks.dashboards.core.data_importation import *
from controllers.hooks.dashboards.payroll.dashboard import *
from controllers.hooks.dashboards.payroll.payroll_processor import *

# STAFF
from controllers.hooks.dashboards.staff.dashboard import *
from controllers.hooks.dashboards.staff.payslip_stats import *
from controllers.hooks.dashboards.staff.overtime_stats import *
from controllers.hooks.dashboards.staff.staff_imprest import *
from controllers.hooks.dashboards.staff.advance import *
from controllers.hooks.dashboards.staff.leave_summary import *
from controllers.hooks.dashboards.staff.project_task import *
from controllers.hooks.dashboards.staff.staff_profile import *
from controllers.hooks.forms.staff.staff_feedback import *
from controllers.hooks.forms.staff.witness import *
from controllers.hooks.listviews.staff.before_fetch import *


# X_POST
from controllers.hooks.functions.x_post.staff.witness import *
from controllers.hooks.functions.x_post.hr.test import *

#STAFF REPORTS
from controllers.hooks.reports.staff.work_plan import *
from controllers.hooks.reports.staff.leave_history import *

from controllers.mailing.formats.project_management import *
# CORE
from controllers.hooks.functions.x_fetch.core.calender import *

# PAYROLL
from controllers.hooks.functions.x_post.payroll.advance import *
from controllers.hooks.forms.payroll.salary_component import *
from controllers.hooks.functions.x_post.payroll.get_advance_config import *
from controllers.hooks.functions.x_post.payroll.employee_salary_component import *
from controllers.hooks.import_script.payroll.payroll_processor import *
from controllers.hooks.forms.payroll.settlements import *
from controllers.hooks.forms.payroll.recoveries import *
from controllers.hooks.forms.payroll.refunds import *

from controllers.hooks.functions.x_fetch.payroll.salary_component import *

# forms
from controllers.hooks.forms.payroll.loans import *
# from conrollers.hooks.dasboard.asset import *

from controllers.hooks.forms.hr.hr_budget import *

# IMPORT SCRIPTS
from controllers.hooks.dashboards.hr.fetch_employee_profile_data import *
from controllers.hooks.import_script.hr.leave_application import import_script_for_leave_application

from controllers.hooks.forms.hr.acting_appointment import *
from controllers.hooks.forms.payroll.pay import *
from controllers.hooks.functions.x_fetch.payroll.employees import *
from controllers.hooks.forms.hr.trasfer import *

# Staff
from controllers.hooks.forms.hr.bonus import *

from controllers.hooks.reports.payroll.transfer_file import *
from controllers.hooks.reports.payroll.amendments_report import *

from cron.jobs.hr import Hr_Background_Jobs

# ALL YOUR FORM HOOKS
form_hooks = {
    # HR HOOKS
    "Appraisal_Setup": {
        "before_submit": [before_appraisal_setup_submit],
        # "before_fetch": [applicant_ref],
    },
    "Employee_Transfer_Memo": {
        "before_save": [on_save_of_employee_memo],
        "before_update": [on_save_of_employee_memo],
        "before_submit": [on_submit_of_employee_memo],
    },
    "Closed_Ended_Question":{
        "before_save": [before_qns_save_and_update],
        "before_update": [before_qns_save_and_update],
        # "before_fetch": [applicant_ref],
    },
    "Open_Ended_Question":{
        "before_save": [before_qns_save_and_update],
        "before_update": [before_qns_save_and_update],
        # "before_fetch": [applicant_ref],
    },
    "Payroll_Recovery": {
        "before_save": [on_recovery_save],
        "before_update": [on_recovery_save],
        "before_submit": [on_recovery_submit],
    },
    "Payroll_Arrears": {
        "before_save": [on_arrears_save],
        "before_update": [on_arrears_save],
        "before_submit": [on_arrears_submit],
    },
    "Payroll_Refunds": {
        "before_save": [on_refund_save],
        "before_update": [on_refund_save],
        "before_submit": [on_refund_submit],
    },
    "Leave_Policy": {
        "before_submit": [on_submissions_of_Leave_policy],
    },

    "Leave_Allocation": {
        "before_save": [before_allocation_save],
        "before_submit": [create_leave_entry],
        "before_cancel": [leave_allocation_cancel],
    },
    
    "Leave_Application": {
        "before_save": [leave_application_save, doc_status_for_leave],
        "before_update": [leave_application_save],
        "before_submit": [leave_entry_updating],
        "before_cancel": [leave_application_cancel],
    },
    
    "Pay_For_Temps_Or_Seasonal_Employee": {
        "before_save": [on_serve_seasonal_and_temp_pay],
        "before_update": [on_serve_seasonal_and_temp_pay],
        "before_submit": [on_serve_seasonal_and_temp_pay_submit],
    },
    "Leave_Commutation": {
        "before_submit": [check_memo, commute_leave_days],
        "before_save": [commute_leave_days_save],
        "before_update": [commute_leave_days_save],
        # "before_fetch": [employee_ref],
    },
    "Leave_Commutation_Memo": {
        "before_submit": [commutation_memo],
        "before_save": [commute_leave_days_save],
        # "before_fetch": [employee_ref],
        "before_update": [commute_leave_days_save],
    },

    # "employee_separation":{
    # #   "before_save": [separation_submit],
    #     "before_submit": [accept_separation],
    #     "before_cancel": [cancel_separation],
    # },

    "Employee_Attendance": {
        "before_save": [employee_attendance_in],
        # "before_update": [employee_attendance_out]
    },

    "Employee":{
        "before_save": [before_employee_save],
        "after_save": [after_employee_save],
        # "before_submit": [before_employee_submit],
    },
    "Leave_Plan": {
        # "before_fetch": [planner_ref],
    },
    "Employee_Promotion": {
        "before_save": [employee_promotion_save],
        "before_submit": [employee_promotion],
        # "before_fetch": [user_ref],
    },
    "Final_Statement": {
        "before_submit": [on_final_statement_submission],
        "before_save": [on_final_statement_save],
        # "before_fetch": [user_ref],
    },

    
    "Salary_Component": {
        "before_save": [on_salary_component_save],
        "before_update": [on_salary_component_update],
    },

    "Appointment_Letter": {
        "before_save": [on_save_appointment_letter_offer],
        "before_submit": [on_submit_appointment_letter_offer],
        # "before_fetch": [user_ref],
    },

    "Interview_Schedule": {
        "before_save": [on_save_interview_schedule],
        "before_submit": [before_interview_schedule_submit],
        # "before_fetch": [user_ref],
    },

    "Staffing_Plan": {
        "before_submit": [after_submit_staffing_plan],
        # "before_fetch": [user_ref],
    },
    # Staff
     "Staff_Feedback": {
        "before_submit": [before_staff_feedback_submit],
        # "before_fetch": [employee_ref],
    },
     "Skill_Gap": {
        "before_submit": [before_skills_gap_submit],
        # "before_fetch": [user_ref],
    },

    "Job_Offer": {
        "before_save": [on_save_job_offer],
        "before_submit": [before_job_offer_submit],
        # "before_fetch": [user_ref],
    },

    "Job_Application": {
        "before_submit": [on_job_application_submit],
        "before_save": [on_job_application_save],
    },

    "Company_Policy": {
        "before_submit": [on_company_policy],
        # "before_fetch": [user_ref],
    },


    "Training_Program": {
        "before_save": [training_program_before_save],
        "before_submit": [on_training_program_submit],
        # "before_fetch": [user_ref],
    },
    "Training_Plan": {
        "before_save": [before_training_plan_save],
        # "before_fetch": [user_ref],
        # "before_submit": [on_training_program_submit]
    },
    "Training_Feedback": {
        "before_save": [on_training_feedback_save],
        # "before_fetch": [employee_ref],
    },
    "Work_Plan": {
        "before_save": [on_save_work_plan],
        "before_submit": [on_submit_work_plan],
        # "before_fetch": [employee_ref],
    },
    "Appraisal": {
        "before_save": [before_appraisal_save],
        "before_update":[before_appraisal_update],
        "before_submit":[before_appraisal_submit],
        "after_fetch":[after_appraisal_fetch],
        # "before_fetch": [appraisee_ref],
    },
    "Certificate_Of_Service": {
        "before_save": [before_certificate_of_service_save],
        "before_submit": [before_certificate_of_service_submit],
        # "before_fetch": [employee_id_ref],
    },
    "Self_Appraisal": {
        "before_save": [before_appraisal_save],
        "before_update":[],
        "before_submit":[before_appraisal_submit],
        # "before_fetch": [appraisee_ref],
    },
    "Case_Outcome": {
        "before_submit": [on_submit_outcome],
        # "before_fetch": [subject_ref],
    },

    "House_Loan_Application": {
        "before_save": [on_house_loan_save],
        "before_update": [on_house_loan_save],
        "before_submit": [on_house_loan_submit],
        # "before_fetch": [employee_ref],
    },
    "Long_Term_Sponsorship": {
        "before_save": [long_term_sponsorship],
        "before_update": [long_term_sponsorship_update],
        "before_submit": [long_term_sponsorship_submit],
        # "before_fetch": [employee_ref],
    },
    "Long_Term_Sponsorship_Fund_Request": {
        "before_save": [long_term_sponsorship_req_fund],
        "before_submit": [long_term_sponsorship_req_fund_submit],
        # "before_fetch": [employee_ref],
    },
    "Job_Advertisement": {
        "before_save": [job_advertisement_before_save, ],
        "before_submit": [job_advertisement_before_submit],
        # "before_fetch": [user_ref],
    },
    "Staff_Requisition": {
        "before_save":  [staff_requisition_before_save],
        "before_submit": [staff_requisition_before_submit],
        # "before_fetch": [user_ref],
    },
    "Graduate_Development_Enrollment":{
        "before_save": [graduate_development_enrollment_before_save],
        "before_submit": [graduate_development_enrollment_before_submit],
        # "before_fetch": [user_ref],
    },

    #  PAYROLL HOOKS
    "Payroll_Processor":{
        "before_save":[on_payroll_processor_save],
        "before_update":[on_payroll_processor_update],
        "before_submit":[on_payroll_processor_submit],
        "before_cancel": [on_payroll_processor_cancel],
    },
    "Income_Tax_Band": {
        "before_save": [before_income_tax_band_save]
    },
    "Advance_Application": {
        "before_save": [on_normal_advance_save],
        "before_update": [on_normal_advance_update],
        "before_submit": [on_normal_advance_submit],
        # "before_fetch": [employee_id_ref],
    },
    "Second_Salary_Advance_Application": {
        "before_save": [on_second_advance_save],
        "before_update": [on_second_advance_update],
        "before_submit": [on_second_advance_submit],
        # "before_fetch": [employee_id_ref],
    },

    "Advance_Memo": {
        "before_save": [on_advance_memo_save],
        "before_update": [on_advance_memo_update],
        "before_submit": [on_advance_memo_submit],
        # "before_fetch": [employee_id_ref],
    },

    "Employee_Grade": {
        "before_update": [notify_employees],
    },
    "Employee_Grievance": {
        "before_save": [on_save_grievance],
        "before_submit": [on_submit_of_grievance],
        # "before_fetch": [raised_by_ref],
    },
    "Employee_Disciplinary": {
        "before_submit": [on_submit_employee_discipline],
        # "before_fetch": [issue_raiser_ref],
    },

    "Petty_Cash":{
        "before_save": [before_petty_cash_save],
        "before_update": [before_petty_cash_save],
        "before_submit": [before_petty_cash_and_imprest_submit],
        # "before_fetch": [initiator_ref],
    },

    "Imprest_Form_20_A":{
        "before_save": [before_imprest_save],
        "before_update": [before_imprest_save],
        "before_submit": [before_petty_cash_and_imprest_submit],
        # "before_fetch": [initiator_ref],
    },

    "Imprest_Form_20_B":{
        "before_save": [before_imprest_save],
        "before_update": [before_imprest_save],
        "before_submit": [before_petty_cash_and_imprest_submit],
        # "before_fetch": [initiator_ref],
    },

    "Imprest_Form_20_C":{
        "before_save": [before_imprest_save],
        "before_update": [before_imprest_save],
        "before_submit": [before_petty_cash_and_imprest_submit],
        # "before_fetch": [initiator_ref],
    },

    "Expense_Retirement":{
        "before_save": [before_retirement_save],
        "before_update": [before_retirement_save],
        "before_submit": [before_retirement_submit],
        # "before_fetch": [employee_no_ref],
    },

    "Personal_Loan_Application":{
        "before_save": [before_personal_loan_save],
        "before_submit": [before_personal_loan_submit],
        # "before_fetch": [employee_no_ref],
    },

    "Cash_Repayment":{
        "before_save": [before_repayment_save],
        "before_update": [before_repayment_save],
        "before_submit": [before_repayment_submit],
        # "before_fetch": [employee_ref],
    },

    "Professional_Membership_Subscription":{
        "before_save": [professional_membership_before_save],
        "before_update": [professional_membership_before_save],
        "before_submit": [professional_membership_before_submit],
        # "before_fetch": [employee_ref],
    },
    "Charge_Form": {
        # "before_save": [before_offence_save],
        "before_submit": [before_charge_form_submit],
        # "before_fetch": [user_ref],
    },
    
    "Offence": {
        "before_save": [before_offence_save],
        # "before_fetch": [user_ref],
        # "before_submit": [before_charge_form_submit]
    },
    "Disciplinary_Committee": {
        "before_save": [before_committee_save],
        "before_submit": [before_committee_save],
        # "before_fetch": [user_ref],
    },


    # CORE IMPORTATIONS 
    "Company":{
        "before_update":[before_company_update]
    },
    "Print_Configuration":{
        "before_save":[on_print_config_save]
    },
    "Data_Importation":{
        "before_save":[on_data_importation_save],
        "before_update":[on_data_importation_update],
        "before_submit":[on_data_importation_submit],
    },
    "Lite_User":{
        "before_save":[on_user_save],
        "after_save":[after_user_save],
        "before_update":[on_user_update],
        "after_fetch":[on_user_fetch]
    },
    "User_Pool":{
        "before_save":[on_user_pool_save],
    },
    "Role":{
        "before_save":[before_role_save],
        "before_update":[before_role_update],
        "before_fetch":[before_role_fetch],
        "after_fetch":[after_role_fetch],
    },
    "Workflow":{
        "before_save":[before_workflow_save],
        "before_update":[before_workflow_update]
    },
    # "Workflow_Doc":{
    #     "before_fetch":[before_workflow_doc_fetch],
    # },
    "Menu_Card":{
        "before_delete":[before_menu_card_save],
    },
    "Default_Dashboard":{
        "before_fetch":[before_default_dashboard_fetch],
        "before_delete":[before_default_dashboard_save],
        "before_update":[before_default_dashboard_update],
    },
    # CONTROLLER
    "Tenant":{
        "before_save":[before_tenant_save],
        "before_update":[before_tenant_update],
        "before_delete":[before_tenant_delete],
    },
    # HR
    "Memo": {
        "before_save": [memos],
        # "before_fetch": [user_ref],
    },
    "Employee_Seperation": {
        "before_save": [before_separation_save],
        "before_submit": [before_separation_submit],
        "before_cancel": [cancel_separation],
        # "before_fetch": [employee_ref],
    },
    "Recovery_Of_Medical_Bills": {
        "before_save": [on_emp_welfare_save],
        "before_update": [on_emp_welfare_save],
        "before_submit": [on_emp_welfare_submit],
        # "before_fetch": [employee_ref],
    },
    "Employee_Welfare_Survey": {
        "before_submit": [employee_welfare_questions],
        # "before_fetch": [employee_ref],
    },

    "Gratuity": {
        "before_save": [on_gratuity_save],
        "before_update": [on_gratuity_save],
        "before_submit": [on_gratuity_submit],
        # "before_fetch": [employee_ref],
    },

    "Announcement": {
        "before_save": [announcement],
        # "before_fetch": [user_ref],
    },

    "Bulletin": {
        "before_save": [bulletin],
        # "before_fetch": [user_ref],
    },
    "Clearance_Form": {
        "before_submit": [before_clearance_submit],
        # "before_fetch": [employee_ref],
    },

    "Allowance_and_Benefit":{
        "before_save": [before_allowance_and_benefits_save]
    },

    "Interview": {
        "before_save": [pending],
        # "before_fetch": [user_ref],
    },
    "Training_Resources": {
        "before_submit": [before_training_resources],
        # "before_fetch": [user_ref],
    },
    "Hr_Contract": {
        "before_save": [on_contract_save],
        "before_update": [on_contract_save],
        "before_submit": [on_contract_submit],
        # "before_fetch": [employee_ref],
    },
    "Acting_Appointment_Memo": {
        "before_save": [before_acting_appointment_memo_save],
        "before_update": [before_acting_appointment_memo_save],
        "before_submit": [before_acting_memo_submit],
        # "before_fetch": [employee_ref],
    },
    "Acting_Appointment": {
        "before_save": [before_acting_appointment_save],
        # "before_update": [before_acting_appointment_save],
        "before_submit": [before_acting_appointment_submit],
        # "before_fetch": [employee_ref],
    },
    "Interview_Rating": {
        "before_submit": [interview_rate],
        # "before_fetch": [user_ref],
    },
    "Appraise_Your_Self": {
        "before_save": [calculate_score],
        "before_update": [calculate_score],
        "before_submit": [calculate_score, used_performance_agreement],
        # "before_fetch": [employee_id_ref],
    },
    "Performance_Agreement": {
        "before_save": [save__],
        "before_submit": [activate_performance_agreement],
        # "before_fetch": [employee_id_ref],
    },
    # project management
    "Project":{
        "before_submit": [Project_Management_Formats.project_submit],
    },

    "Project_Task": {
        "before_submit": [Project_Management_Formats.on_submitting_task]
    },

    "ECZ_Imprest_Retirement":{
        "before_submit": [update_ecz_imprest],
        # "before_fetch": [employee_no_ref],
    },

    "Exit_Interview_Questionnair":{
        "before_save": [before_exit_interview_questionnaire_save],
        # "before_fetch": [employee_ref],
    },

    "Separation_Type":{
        "before_save": [before_separation_type_save]
    },
    "Request_Task_Adjustment": {
        "before_save": [on_work_plan_issue],
        "before_submit": [submit_work_plan_issue],
    },

    # WEB
    "Module_Pricing":{
        "after_fetch":[after_module_pricing_fetch]
    },
    "Witnessing": {
        "before_save": [on_witness_save],
        "before_submit": [on_witness_submit],
        # "before_fetch": [employee_ref],
    },
    "Applicant_Short_List": {
        "before_submit": [before_short_list_submission],
        # "before_fetch": [user_ref],
    },
    "Tuition_Advance_For_Salary_Form": {
        "before_save": [on_tuition_advance_save],
        "before_update": [on_tuition_advance_save],
        "before_submit": [on_tuition_advance_submit],
        # "before_fetch": [employee_ref],
    },
    "Leave_Schedule": {
        "before_save": [on_save_leave_schedule],
        "before_update": [on_update_leave_schedule],
        "before_submit": [on_submit_leave_schedule],
        # "before_fetch": [planner_ref],
    },
    "HR_Budget": {
        "before_save": [before_hr_budget_save],
        "before_update": [before_hr_budget_update],
        "before_submit": [hr_budget_submit],
        # "before_fetch": [user_ref],
    },
    "Overtime": {
        "before_save": [before_overtime_save],
        "before_submit": [before_overtime_submit],
        # "before_fetch": [applicant_ref],
    },
    "Overtime_CLaim": {
        "before_save": [before_overtime_claim_save],
        "before_update": [before_overtime_claim_save],
        "before_submit": [before_overtime_claim_submit],
        # "before_fetch": [employee_ref],
    },
    "Transport_Request": {
        # "before_fetch": [applicant_ref],
    },
    "Form_Of_Agreement_For_A_Personal_Loan": {
        # "before_fetch": [employee_ref],
    },
    "Personal_Loan_Agreement": {
        # "before_fetch": [employee_no_ref],
    },
    "Salary_Increment": {
        "before_save": [before_salary_increment_save],
        "before_update": [before_salary_increment_save],
        "before_submit": [before_salary_increment_submit]
    },
    "Bonus": {
        "before_submit": [before_bonus_submit],
        "before_save": [before_bonus_save],
    },
}


# ALL YOUR LISTVIEW HOOKS
listview_hooks = {  }

# ALL YOUR REPORTS HOOKS
report_hooks = {}

# ALL YOUR SCRIPTED REPORTS
script_reports = {
    "Payroll_Processor": payroll_import_script,
    "Payroll": payroll_import_script,

    #HR Reports
    "Leave Application": employee_on_leave_report,
    # "Job Application": recruitment_analytics_report,
    "employee_separation" : employee_exit_report,
    "Employee Leave Balance" : employee_leave_balance_report,
    "Recruitment Analytics": recruitment_analytics_report,
    "Leave Summary": leave_summary_report,
    "Employee Seperation Report": employee_separations,
    "Training Feedback Report": training_feedback_report_with_scores,
    "Appraisal Report": hr_appraisal_report,
    "Self Appraisal Report": hr_self_appraisal_report,
    "Employee Grievance Report": employee_grievance_report,
    "Training Effectiveness": training_effectiveness_report,
    "Short Listed Applicants": short_list,
    "Industrial Relations Summary": industrial_relations_summary,
    "Short List Report": short_list_report,
    "Monthly_Attendance": monthly_attendance,
    "Employee Information": employee_info,
    "Interview Score Sheet": interview_score_sheet_report,

    #Payroll Reports
    "Overtime Report": overtime_report,
    "Napsa Report": napsa_report,
    "Paye Report": paye_report,
    "Nhima Report": nhima_report,
    "Payroll Summary": payroll_summary_report,
    "Advance Report": advance_report,
    "ECZ Imprest Report": Imprest_Report.imprest_reports,
    "ECZ Loan Report": ecz_loan_report,
    "Employee Welfare Report": medical_deductions_report,
    "Payroll Journal Listing": payroll_journal_listing,
    "Transfer_FIle": transfer_file_report,
    "Amendments Report": amendments_report,

    # Staff Reports
    "staff_work_plan_report": staff_work_plan_report,
    "staff leave summary": staff_leave_summary,

    # CORE
    "Audit_Trail_Report": audit_trail,
    "Authentication_Trail": auth_trail_report,
}

# print/download data customization
download_data_customizer = {
    # "Customer Statement": on_customer_statement_download,
}

# CUSTOM FETCH FUNCTIONS
x_fetch = {
    # ONBOARDING
    "get_onboarding_content": Onboarding.get_onboarding_content,

    # GETTING PAYROLL PROCESSOR CONTENT
    "get_payroll_processor_content": get_payroll_processor_content,

    # CORE
    "get_forex_currencies":get_forex_currencies,
    "get_module_apps":get_module_apps,
    "get_role_cards":get_role_cards,
    "get_holidays": get_holidays,
    "commission_calculations":commission_calculations,

    # WEB
    "web_content": get_web_content, 
    "get_job_openings": get_job_openings,

    #Hr
    "get_appraisal_content": get_appraisal_content,
    "create_users_on_a_mass": create_users_on_a_mass,
    "get_salary_components": get_salary_components,
    "get_staff_planning": get_recruitment_staff_planning,
    "get_staffing": get_recruitment_staffing,
    "alter_employee_pay": alter_employee_pay,
    # "get_job_openings": get_recruitment_job_openings,
    "get_job_applications": get_recruitment_job_applications,
    "get_interviews": get_recruitment_interviews,
    "get_interview_types": get_recruitment_interview_types,
    "get_interview_schedules": get_recruitment_interview_schedules,
    "get_job_offers": get_recruitment_job_offers,
    "get_appointment_letters": get_recruitment_appointment_letters,
    "get_training_program_summary": get_training_program_summary,
    "deactivate_separated_employees": deactivate_separated_employees,
    "employees_for_attendance": employees_for_attendance,
    "behavioral_imperative": behavioral_imperative,
    "eligible_for_bonus": eligible_for_bonus,
    "get_separated_employees": get_separated_employees,
    "normalize_emp_information": normalize_emp_information,
    "add_paye_to_all_employees": add_paye_to_all_employees,
    "leave_bj_test": Hr_Background_Jobs.employee_from_leave,

    # Payroll 
    "update_salary_components": update_salary_components,
    "load_temp_employees": load_temp_employees,
    
    # CRM
    # TEMPRAL BACKGROUND JOB HOOKS USING X FETCH
    "separation_update": Separation_BJ.update_emp_init,
    "employee_from_case_out_come": Industrial_Relations.employee_from_case_out_come,
    "bj_reminders": BJ_Reminders.init_reminders,
    "bj_leave":  BJ_Leave.leave,
    "new_calender": BJ_Calender.bj_calender,
    "back_from_leave": back_from_leave,
}

# CUSTOM POST FUNCTIONS
x_post = {
    # FRAMEWORK
    "disable_doc": disable_doc,
    "enable_doc": enable_doc,
    "certify_user": certify_user,

    # to update company logo
    "update_company_logo":update_company_logo,

    # CORE X-REQUEST
    "get_trade_rates":get_trade_rates,
    "update_exchange_rate":update_exchange_rate,
    "update_bulk_exchange_rates":update_bulk_exchange_rates,
    # to get exchange rate for the transaction
    "get_exchange_rate":get_exchange_rate,
    "convert_currency":convert_currency,
    "start_data_importation": start_data_importation,
    "test_email_config":test_email_config,

    "get_logged_in_user":get_logged_in_user,
    "update_user_password":update_user_password,

    # USER MANAGER
    "update_user_dp": update_user_dp,
    "update_user_roles": update_user_roles,
    "update_user_permissions": update_user_permissions,

    # PAYROLL
    "get_advance_config": get_advance_config_,
    "link_component_to_all_employees": link_component_to_all_employees,
    "allocate_employee_salary_component": allocate_employee_salary_component,
    "compare_payrolls": compare_payrolls,


    # HR
    "get_employee_analytics":get_employee_analytics,
    "leave_entry_updating": leave_entry_updating,
    "approve_application": approve_application,
    "create_user_form_employee": create_user_form_employee,
    "get_employee_assets": get_employee_assets,
    "final_statement_calculated_totals": final_statement_calculated_totals,
    "employee_profile": Employee_Profile.employee_profile,
    "get_leave_type": get_leave_type,
    "reject": reject,
    "questions": questions,
    "pull_question": pull_question,
    "work_plan_commence_work": work_plan_process_task_work,
    "request_adjustment": request_adjustment,
    "get_work_plan": get_work_plan,
    "activate_work_plan": activate_work_plan,
    "company_skill_levy": company_skill_levy,
    "interview_rating": interview_rating,
    "submit_job_application_": submit_job_application_,
    "create_short_": create_short_,
    "get_designation_description": get_designation_description,
    "take_attendance": take_attendance,
    "applicant_required_documents":get_applicant_submitted_documenst,
    #  "approve_application":approved_scholarship,
    "reinstate_employee": reinstate_employee,
    "separate_with_separated_employees": separate_with_separated_employees,
    "get_job_advertisement_application": get_job_advertisement_application,
    "get__job_application_details": get__job_application_details,
    "reverse_job_consideration": reverse_job_consideration,
    "get_job_application": get_job_application,
    "filter_emps_by_designation": filter_emps_by_designation,
    "get_gratuity_setup": get_gratuity_setup,
    "create_users_from_selected": create_users_from_selected,
    "leave_plan_to_applications": leave_plan_to_applications,
    "job_offer_confirmation" :job_offer_confirmation,
    "fetch_case_out_come_id": fetch_case_out_come_id,
    "applicants_job_offer": applicants_job_offer,
    "get_appraisal_for": get_appraisal_for,
    "appointment_letter_approval": appointment_letter_approval,
    "appointment_letter_confirmation": appointment_letter_confirmation,
    "get_applicant_data": get_applicant_data,
    "fetch_employee_profile_data" : fetch_employee_profile_data,
    "create_employee_from_applicant": creating_employee_from_applicant,
    "policy_type": get_policy_type,
    "filter_emps_by_policys_category": filter_emps_by_policys_category,
    "long_term_sponsorship_fund_request": long_term_sponsorship_fund_request,
    "update_job_advertisement": update_job_advertisement,
    "leave_schedule_employees": leave_schedule_employees,
    "update_clearance_form": update_clearance_form,
    "test": tests,
    
    # bonuses
    "get_bonus_type": get_bonus_type,
  

    # STAFF
    "staff_leave_summary": get_staff_leave_summary,
    "staff_survey_feedback": staff_survey_feedback,
    "witness": witness,
    # "interview_rating_by_staff": interview_rating_by_staff,

    # WEB
    "submit_enquiry_from_web":submit_enquiry_from_web,
    "validate_kyc":validate_kyc,
    "get_job_opening": get_job_opening,
   
    # PAYROLL
    "get_overtime_setup": get_overtime_setup,
    "staff_overtime": get_overtime_details,
    "advance_calc": advance_calc,
    "filled_sits_in_designation": filled_sits_in_designation,
    "get_ot_claim": get_ot_claim,
    "create_pre_payment_doc": create_pre_payment_doc,


    # CONTROLLER
    "idlelize_job": idlelize_job,

    "create_jobOpenning_from_staffPlan": create_job_openning_from_staffing_plan,
    "fetch_budget_line": fetch_budget_line,
    "fetch_applicant_data_as_employee_obj": fetch_applicant_data_as_employee_obj,
    "create_employee_from_job_offer": create_employee_from_job_offer,
    "job_offer_status_update": job_offer_status_update,
}
# DASHBOARDS

dashboards = {

    # CORE
    "core":Core_Dashboard.core,
    "currency":Currency_Dashboard.currency,
    "user":User_Dashboard.user,
    "data_importation":Data_Importation_Dashboard.dashboard,

    # PAYROLL
    "payroll":Payroll_Dashboard.dashboard,
    "payroll_processor":Payroll_Processor.payroll_history,
    "payslip": PaySlip.payslip,
    "employee_grade": Employee_Grade.employee_grade,
    "salary_component": Salary_Componet.salary_component,
    "advance_side_view": Advance.advance_side_view,
    "Overtime": Overtime.overtime_side_view,
    "payroll_loans_dashboard": payroll_loans_dashboard,

    # HR
    "hr": HR_Dashboard.dashboard,
    "performance_dashboard": Performance_Dashboard.performance_dashboard,
    "leave_dashboard": Leave_Dashboard.dashboard,
    "industrial_relations_dashboard": Industrial_Relations_Dashboard.dashboard,
    "recruitment_dashboard": Recruitment_Dashboard.dashboard,
    "skill_distribution": Skills_Distribution.dashboard,

    "staffing_plan":Staffing_Plan.get_departments,
    "job_opening":Job_Opening.get_job_openings,
    "Job_Application":Job_Application.get_Applcations,
    "Interview": Interview.interview_side_view,
    "designation": Designation.designation,
    "employee": Employee.employee_sv,
    "employee_checkin":Checkin.employee_checkin,
    "appraisal_setup":Appraisal_Setup.appraisal_setup,
    "employee_attendance":Attendance.employee_attendance,
    "employee_promotion":Promotion.employee_promotion,
    "leave_allocation":Leave.leave_allocation_side_view,
    "self_appraisal":Self_Appraisal.self_appraisal,
    "appraisal": Appraisal.appraisal,
    "work_plan": Work_Plan.work_plan,
    "leave_commutation": leave_commutation.Leave_commutation.recent_leave_commutation,
    "leave_application": Leave.leave_application_side_view,
    "memo": Memo.memo,
    "grievance": Employee_Grievance.grievance,
    "case_outcome": Employee_Grievance_outcome.discipline_outcome,
    "side_view_leave_type": side_view_leave_type,
    "gratuity_side_view": Gratuity.gratuity_side_view,
    "dashboard_stats": main_recrement_dashboard,
    "leave_plan_sv": Leave.leave_plan_sv,
    "employee_separation": Employee_seperation_dashboard.employee_separation,
    "employee_separation_dashboard": employee_separation_dashboard.employee_separation_dashboard,
    "employee_skills_dashboard": Employee_skill_distribution_dashboard.dashboard,
    "probation_sv": probation_sv,
    "welfare_dashboard": employee_welfare_dashboard.welfare_dashboard,
    # "get_staffing_plan": ,

    # STAFF
    "staff": Staff_Dashboard.dashboard,
    "staff_payslip_statistics": Staff_Payslip_Statistics.staff_payslip_statistics,
    "staff_overtime_statistics": Staff_Overtime_Statistics.staff_overtime_statistics,
    "staff_advance":Staff_Advance.staff_advance,
    "employee_skills_qualif": Staff_Skill_Profile.skils_docs,
    # "staff_leave_summary": staff_leave_summary,
    "training_program": training_program,
    # "separation_side_view": separation_side_view,
    "staff_imprest_side_view": Staff_Imprest.staff_imprest_side_view,
    "staff_project_tasks": Staff_Project_Task.staff_project_tasks,
    "staff_Profile": Staff_Profile.staff_profile,
}

# custom functions to handle data import
custom_imports = {
    "Employee": import_script_for_employees,
    "Employee_Grade": import_script_for_employees_grade,
    "Leave_Policy": import_script_for_leave_policy,
    "Leave_Allocation": import_script_for_leave_allocation,
    "Recovery_Of_Medical_Bills": welfare_importation,
    "Leave_Type": import_script_for_leave_type,
    "Leave_Application": import_script_for_leave_application,
    "Payroll": payroll_import_script,
    "Payroll_Processor": payroll_import_script,
}


external_models = {
    "Approver": Approver.get_approvals,
}


# FORM FIELDS
form_fields = {
    "Payroll_Processor": fetch_payroll_processor_fields,
}

