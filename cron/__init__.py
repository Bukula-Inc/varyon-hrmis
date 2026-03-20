"""
    HERE IS WHERE YOU LINK ALL YOUR BACKGROUND JOBS IN ACCORDANCE WITH HOW OFTEN YOU WANT THEM RUNNING.

    NOTE: 
    Each job is a dict of the `method=function` and `service=service name`. if the service is not recognized, the job 
    will not run at all.
"""

# CLASS/FUNCTION IMPORTS
from cron.jobs.hr import Hr_Background_Jobs
from cron.jobs.payroll import Payroll_Background_Jobs

one_minute = []
five_minutes = [
    # put your 10 minutes functions here
]

ten_minutes = [
    # put your 10 minutes functions here
]

thirty_minutes = [
    # put your 30 minutes functions here
]


one_hour = [
    # put your every 1 hour functions here
    
    # CRM 

]

one_day = [
    # put your every 1 day functions here
    { "method": Hr_Background_Jobs.leave_accruals, "service": "Leave Allocation" },
    { "method": Hr_Background_Jobs.employee_birth_days, "service": "Birth Day" },
    { "method": Hr_Background_Jobs.employee_from_leave, "service": "Back From Leave" },
    
    # Payroll
    { "method": Payroll_Background_Jobs.payroll_processor, "service": "Generate Payslips" }
]

one_month = [
    # put your every 1 month functions here
]

one_year = [
    # put your every 1 year functions here
]