from .core.series import series
from .core.sector import sector
from .core.industry import industry
from .core.city import city
from .core.country import country
from .core.currency import currency
from .core.province import province
from .core.district import district
from .controller.modules import module
from .core.gender import gender
from .core.branch import branch
from .core.priority import priority
from .core.questions import questions
from .core.working_hours import working_hours
from .core.print_format import print_format
from .core.email_config import email_config

from .hr.appraisal_type import appraisal_type
from .hr.appraisal_quarter import appraisal_quarter
from .hr.department import department
from .hr.designation import designation
from .hr.employment_type import employment_type
from .hr.leave_type import leave_type
from .hr.leave_policy import leave_policy_annual
from .hr.probation import employee_probation
from .hr.skills import skills
from .hr.interview_type import interview_type
from .hr.training_program_type import training_program_type
from .hr.grievance_type import grievance_type
from .hr.violation_type import violation_type
from .hr.welfare_type import welfare_type

from .controller.background_job import background_job
from .payroll.salary_component import salary_component

from management.defaults.hr.interview_type import interview_type
from management.defaults.hr.training_program_type import training_program_type
from management.defaults.hr.grievance_type import grievance_type
from management.defaults.hr.violation_type import violation_type
from management.defaults.hr.welfare_type import welfare_type
from .controller.module_group import module_group
from management.defaults.hr.separation_type import separation_type
from .hr.exit_interview_question import exit_interview_question

default_inserts = [
    module_group,
    # CORE DEFAULTS
    series,
    sector,
    industry,
    city,
    country,
    currency,
    province,
    district,
    gender,
    branch,
    module,
    priority,
    questions,
    working_hours,
    print_format,
    email_config,

    # MANAGEMENT DEFAULTS
    background_job,

    # HR DEFAULTS
    appraisal_type,
    department,
    designation,
    employment_type,
    leave_type,
    appraisal_quarter,
    interview_type,
    training_program_type,
    grievance_type,
    violation_type,
    welfare_type,
    leave_policy_annual,
    employee_probation,
    skills,

    # PAYROLL DEFAULTS
    salary_component,    
]