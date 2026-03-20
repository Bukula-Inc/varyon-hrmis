import os
import datetime

from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-i_!$hv!=d8gn%cc9=y$*$dyjjmw9cq&g0!$!&b+$$(3=ygv+ja'
CLIENT_API_KEY_SECRET_KEY = 'q0fXn3Uw1Yh37M4U-IH6Brr_a9LGM8H5_E_CU3VMFT4='
TOKEN_EXPIRATION_TIME = datetime.timedelta(minutes=100)


DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'corsheaders',
    'management',
    'services',
    'cron',
    'client_app',
    'client_app.authentication',

    # Core Module Apps
    'client_app.core',
    'client_app.core.core_dashboard',
    'client_app.core.cost_center',
    'client_app.core.series',
    'client_app.core.company',
    'client_app.core.country',
    'client_app.core.currency',
    'client_app.core.industry',
    'client_app.core.sector',
    'client_app.core.province',
    'client_app.core.state',
    'client_app.core.district',
    'client_app.core.doc_status',
    'client_app.core.city',
    'client_app.core.branch',
    'client_app.core.gender',
    'client_app.core.location',
    'client_app.core.system_settings',
    'client_app.core.data_importation',
    'client_app.core.user',
    'client_app.core.working_hours',
    'client_app.core.calendar',
    'client_app.core.priority',
    'client_app.core.department',
    'client_app.core.role',
    'client_app.core.workflow',
    'client_app.core.advanced_access_control',
    'client_app.core.otp',
    'client_app.core.rating',
    'client_app.core.share_management',
    'client_app.core.default_dashboard',
    'client_app.core.audit_trail',
    'client_app.core.disabled_document',
    'client_app.core.deleted_document',
    'client_app.core.menu_card',
    'client_app.core.form_customization',
    'client_app.core.files',
    'client_app.core.core_reports',
    'client_app.core.core_reports.auth_trail',
    'client_app.core.core_reports.audit_trail_report',

    # controller module
    'client_app.controller',
    'client_app.controller.controller_dashboard',
    'client_app.controller.module',
    'client_app.controller.background_job',
    'client_app.controller.background_job_results',
    'client_app.controller.billing_config',
    'client_app.controller.module_group',
    'client_app.controller.module_pricing',
    'client_app.controller.tenant',
    'client_app.controller.license',
    'client_app.controller.subscription',
    'client_app.controller.domain_controller',
    'client_app.controller.user_pool',

    # Human Resource Module Apps
    'client_app.hr',
    'client_app.hr.hr_dashboard',
    'client_app.hr.exit_interview_questionnair',
    'client_app.hr.performance_dashboard',
    'client_app.hr.leave_type',
    'client_app.hr.leave_policy',
    'client_app.hr.leave_entry',
    'client_app.hr.leave_compensation',
    'client_app.hr.leave_application',
    'client_app.hr.leave_allocation',
    'client_app.hr.appraisal_setup',
    'client_app.hr.appraisal',
    'client_app.hr.appraisal_question',
    'client_app.hr.appraisal_quarter',
    'client_app.hr.self_appraisal',
    'client_app.hr.employee',
    'client_app.hr.employee_attendance',
    'client_app.hr.employee_checkin',
    'client_app.hr.employment_type',
    'client_app.hr.appraisal_type',
    'client_app.hr.employee_promotion',
    'client_app.hr.leave.leave',
    'client_app.hr.leave_plan',
    'client_app.hr.leave_schedule',
    'client_app.hr.designation',
    'client_app.hr.work_plan',
    'client_app.hr.staffing_plan',
    'client_app.hr.job_opening',
    'client_app.hr.job_application',
    'client_app.hr.job_offer',
    'client_app.hr.interview_type',
    'client_app.hr.interview_schedule',
    'client_app.hr.interview_feedback',
    'client_app.hr.interview',
    'client_app.hr.memo',
    'client_app.hr.query',
    'client_app.hr.appointment_letter',
    'client_app.hr.company_policies',
    'client_app.hr.announcement',
    'client_app.hr.employee_feedback',
    'client_app.hr.self_appraisal_setup',
    'client_app.hr.grievance_type',
    'client_app.hr.employee_grievance',
    'client_app.hr.training_program',
    'client_app.hr.training_event',
    'client_app.hr.training_feedback',
    'client_app.hr.training_result',
    'client_app.hr.employee_resignation',
    'client_app.hr.employee_separation',
    'client_app.hr.exit_interview',
    'client_app.hr.violation_type',
    'client_app.hr.employee_disciplinary',
    'client_app.hr.case_outcome',
    'client_app.hr.bulletin',
    'client_app.hr.suggestion_category',
    'client_app.hr.suggestion_box',
    'client_app.hr.final_statement',
    'client_app.hr.employee_files',
    'client_app.hr.employee_profile',
    'client_app.hr.skill_levy',
    'client_app.hr.training_program_application',
    'client_app.hr.training_program_type',
    'client_app.hr.bonus',    
    'client_app.hr.hr_settings',
    'client_app.hr.bonus_planing',
    'client_app.hr.bonus_weightage',
    'client_app.hr.bonus_threshold',
    'client_app.hr.bonus_types',
    'client_app.hr.disciplinary_committee',
    'client_app.hr.hr_contract',
    'client_app.hr.contract_type',
    'client_app.hr.graduate',
    'client_app.hr.gratuity_setup',
    'client_app.hr.leave_dashboard',
    'client_app.hr.recruitment_dashboard',
    'client_app.hr.industrial_relations_dashboard',
    'client_app.hr.probation',
    'client_app.hr.interview_panel',
    'client_app.hr.leave_commutation',
    'client_app.staff.staff_leave_commutation',
    'client_app.hr.employee_separation_dashboard',
    'client_app.hr.training_resources',
    'client_app.hr.employee_welfare_dashboard',
    'client_app.hr.welfare_type',
    'client_app.hr.welfare',
    'client_app.hr.employee_welfare_feedback',
    'client_app.hr.employee_skill_distribution_dashboard',
    'client_app.hr.skills',
    'client_app.hr.performance_agreement',
    'client_app.hr.skills_inventory_dashboard',
    'client_app.hr.interview_rating',
    'client_app.hr.long_term_sponsorship',
    'client_app.hr.short_listed_applicants',
    'client_app.hr.training_plan',
    'client_app.hr.disciplinary_statement_form',
    'client_app.hr.hr_text_templates',
    'client_app.hr.hr_budget',
    'client_app.hr.budget_line',
    'client_app.hr.clearance_form',
    'client_app.hr.charge_form',
    'client_app.hr.authority_to_council_car',
    'client_app.hr.sitting_allowance_claim',
    'client_app.hr.verbal_warning',
    'client_app.hr.graduate_development_enrollment',
    'client_app.hr.certificate_of_service',
    'client_app.hr.membership_subscription',
    'client_app.hr.transport_request',
    'client_app.hr.id_card',
    'client_app.hr.express_mail',
    'client_app.hr.oath_affirmation_of_secrecy',
    'client_app.hr.caveat_agreement',
    'client_app.hr.locations',
    'client_app.hr.personal_loan_agreement',
    'client_app.hr.personal_loan',
    'client_app.hr.tution_advance_of_salary',
    'client_app.hr.staff_requisition_form',
    'client_app.hr.job_advertisement',
    'client_app.hr.separation_type',
    'client_app.hr.offence',
    'client_app.hr.sanction_type',
    'client_app.hr.offence_category',
    'client_app.hr.sitting_summary',
    'client_app.hr.appeal',
    'client_app.hr.acting_appointment',
    'client_app.hr.employee_transfer_memo',
    
    # hr Reports\
    'client_app.hr.hr_reports',
    'client_app.hr.hr_reports.monthly_attendance_sheet',
    'client_app.hr.hr_reports.recruitment_analytics',
    'client_app.hr.hr_reports.employee_information',
    'client_app.hr.hr_reports.employee_birthday',
    'client_app.hr.hr_reports.employee_leave_balance',
    'client_app.hr.hr_reports.leave_balance',
    'client_app.hr.hr_reports.employee_on_leave',
    'client_app.hr.hr_reports.employee_exit',
    'client_app.hr.hr_reports.employee_contacts',
    'client_app.hr.hr_reports.employee_advance_summary',
    'client_app.hr.hr_reports.leave_summary',
    'client_app.hr.hr_reports.training_feedback_report',
    'client_app.hr.hr_reports.self_appraisal_report',
    'client_app.hr.hr_reports.appraisal_report',
    'client_app.hr.hr_reports.employee_seperation_report',
    'client_app.hr.hr_reports.employee_welfare_report',
    'client_app.hr.hr_reports.employee_grievance_report',
    'client_app.hr.hr_reports.training_program_report',
    'client_app.hr.hr_reports.training_effectiveness',
    'client_app.hr.hr_reports.short_listed_applicants_report',
    'client_app.hr.hr_reports.interview_score_sheet',
    # PAYROLL
    'client_app.payroll',
    'client_app.payroll.payroll_dashboard',
    'client_app.payroll.payroll_setup',
    'client_app.payroll.payroll_processor',
    'client_app.payroll.payslip',
    'client_app.payroll.income_tax_band',
    'client_app.payroll.salary_component',
    'client_app.payroll.employee_grade',
    'client_app.payroll.advance_application',
    'client_app.payroll.advance_setup',
    'client_app.payroll.overtime',
    'client_app.payroll.professional_membership',
    'client_app.payroll.advance_balance',
    'client_app.payroll.deduction_register',
    'client_app.payroll.overtime_setup',
    'client_app.payroll.commission_setup',
    'client_app.payroll.commission',
    'client_app.payroll.payroll_loans_dashboard',
    'client_app.payroll.overtime_claim',
    'client_app.payroll.house_loan_application',
    'client_app.payroll.house_loan_agreement',
    'client_app.payroll.petty_cash',
    'client_app.payroll.imprest_a',
    'client_app.payroll.imprest_b',
    'client_app.payroll.imprest_c',
    'client_app.payroll.staff_expense_retirement',
    'client_app.payroll.application_for_a_personal',
    'client_app.payroll.cash_repayment',
    'client_app.payroll.pre_payroll_payment',
    'client_app.payroll.recoveries',
    'client_app.payroll.refunds',
    'client_app.payroll.pay_temp',
    'client_app.payroll.banking',
    'client_app.payroll.with_hold_pay',
    'client_app.payroll.arrears',

    # PAYROLL REPORTS
    'client_app.payroll.payroll_reports',
    'client_app.payroll.payroll_reports.monthly_attendance',
    'client_app.payroll.payroll_reports.napsa_report',
    'client_app.payroll.payroll_reports.nhima_report',
    'client_app.payroll.payroll_reports.paye_report',
    'client_app.payroll.payroll_reports.payroll_summary',
    'client_app.payroll.payroll_reports.private_insurance_report',
    'client_app.payroll.payroll_reports.skills_levy_report',
    'client_app.payroll.payroll_reports.overtime_report',
    'client_app.payroll.payroll_reports.payroll_payable',
    'client_app.payroll.payroll_reports.advance_report',
    'client_app.payroll.payroll_reports.imprest_report',
    'client_app.payroll.payroll_reports.loan_report',
    'client_app.payroll.payroll_reports.medical_report',
    'client_app.payroll.payroll_reports.transfer_file',
    'client_app.payroll.payroll_reports.amendments_report',

    # STOCK MANAGEMENT MODULE APP
    'client_app.stock.items',
    'website',

    # PRINTINGING
    'client_app.core.print_format',
    'client_app.core.print_doc',
    'client_app.core.print_configuration',
    'client_app.core.template_content',

    # mailing
    'client_app.core.email_config',

    # onboarding
    'client_app.onboarding',
    'client_app.onboarding.welcome',

    # STAFF
    'client_app.staff.staff_dashboard',
    'client_app.staff.submit_registration',
    'client_app.staff.staff_advance',
    'client_app.staff.staff_appraisal',
    'client_app.staff.staff_360_deg_appraisal',
    'client_app.staff.staff_imprest',
    'client_app.staff.staff_leave',
    'client_app.staff.staff_payslip',
    'client_app.staff.staff_performance',
    'client_app.staff.staff_profile',
    'client_app.staff.staff_purchase_requisition',
    'client_app.staff.staff_workplan',
    'client_app.staff.staff_leave_history',
    'client_app.staff.staff_earnings_and_deductions',
    'client_app.staff.staff_advance_history',
    'client_app.staff.staff_memo',
    'client_app.staff.staff_query',
    'client_app.staff.staff_policy',
    'client_app.staff.staff_anouncement',
    'client_app.staff.resignation',
    'client_app.staff.training_program_feedback',
    'client_app.staff.staff_employee_grievance',
    'client_app.staff.staff_job_opening',
    'client_app.staff.staff_job_application',
    'client_app.staff.staff_employee_feedback',
    'client_app.staff.staff_bulletin',
    'client_app.staff.staff_suggestion_box',
    'client_app.staff.staff_training_event',
    'client_app.staff.staff_employee_files',
    'client_app.staff.employee_task',
    'client_app.staff.staff_performance_agreement',
    'client_app.staff.staff_bid',
    'client_app.staff.staff_bid_evaluation',
    'client_app.staff.staff_exit_interview_questionnair',
    'client_app.staff.staff_welfare',
    'client_app.staff.staff_employee_welfare_feedback',
    'client_app.staff.staff_interview_evaluator',
    # 'client_app.staff.transport_request',
    'client_app.staff.staff_house_loan_application',
    'client_app.staff.staff_statement_form',
    'client_app.staff.skills_gap',
    'client_app.staff.staff_clearance_form',
    'client_app.staff.staff_ecz_imprest_retirement',
    'client_app.staff.charge',
    'client_app.staff.staff_verbal_warning',
    'client_app.staff.staff_graduate_development_enrollment',
    'client_app.staff.staff_certificate_of_service',
    'client_app.staff.staff_membership_subscription',
    'client_app.staff.staff_transport_request',
    'client_app.staff.staff_id_card',
    'client_app.staff.witness',

    #'client_app.staff.staff_employee_seperation',
    'client_app.staff.training_program_application_form',
    'client_app.staff.staff_overtime',
    'client_app.staff.staff_commission',
    'client_app.staff.staff_reports.staff_work_plan_report',
    'client_app.staff.staff_reports',
    'client_app.staff.staff_skill_profile',
    #  'client_app.staff.staff_employee_seperation',
    'client_app.staff.staff_leave_plan',
    'client_app.staff.approval',
    'client_app.staff.staff_petty_cash',
    'client_app.staff.staff_training_resources',
    'client_app.staff.staff_authority_to_council_car',
    'client_app.staff.staff_sitting_allowance_claim',
    'client_app.staff.staff_express_mail',
    'client_app.staff.staff_caveat_agreement',
    'client_app.staff.staff_oath_affirmation_of_secrecy',
    'client_app.staff.slong_term_sponsorship',
    'client_app.hr.section',
    'client_app.payroll.allowance_and_benefit',
    'client_app.hr.exit_interview_question',
    'client_app.hr.salary_increment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.middleware.TenantMiddleware',
    'django.middleware.gzip.GZipMiddleware'
]

ROOT_URLCONF = 'multitenancy.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'multitenancy.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ecz_uat',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PASSWORD': 'erpteam@probase',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    },
}

ATOMIC_REQUESTS = True

DATABASE_ROUTERS = ['middleware.routers.TenantRouter']

# custom authentication model
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_prod')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
# Media files (user-uploaded content)

MEDIA_URL = '/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# celery configurations
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_QUEUE = 'multitenancy'
CELERY_ROUTES = { 'cron.tasks.*': {'queue': 'multitenancy'},}


# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://localhost:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient'
#         },
#         'KEY_PREFIX': 'startapp'
#     }
# }


TENANT_ADMIN = {
    'DB': 'ecz_uat',
    'DOMAIN': 'startappsolution.com'
}
