from cron.jobs.payroll.processor import Payroll_Background_Jobs
class Payroll_BJ:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object

    @classmethod
    def init_payroll_processor (cls, dbms, object):
        instance = cls (dbms, object)
        Payroll_Background_Jobs.payroll_processor (dbms, object)