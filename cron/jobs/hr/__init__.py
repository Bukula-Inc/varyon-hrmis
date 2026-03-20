from cron.jobs.hr.leave_background_jobs import Leave_Controller
from cron.jobs.hr.employee import Employee_Controller

class Hr_Background_Jobs:
    def __init__(self, dbms, object):
        self.object = object
        self.dbms = dbms

    @classmethod
    def leave_accruals (cls, dbms, object):
        instance = cls (dbms, object)
        Leave_Controller.init_leave_accrual (dbms, object)
    
    @classmethod
    def employee_birth_days (cls, dbms, object):
        instance = cls (dbms, object)
        Employee_Controller.init_birth_day (dbms, object)

    @classmethod
    def employee_from_leave (cls, dbms, object):
        instance = cls (dbms, object)
        Leave_Controller.employee_from_leave (dbms, object)