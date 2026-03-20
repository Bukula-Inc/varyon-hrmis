from controllers.hooks.forms.payroll.payroll_processor import initiate_Payroll_processor
from controllers.utils import Utils

utils = Utils ()
pp = utils.pretty_print

class Payroll_Background_Jobs:
    def __init__(self, dbms, object) -> None:
        self.dbms = dbms
        self.object = object

    @classmethod
    def payroll_processor (cls, dbms, object):
        instance = cls (dbms, object)
        initiate_Payroll_processor (dbms, object)
