from controllers.utils import Utils
from controllers.utils.dates import Dates

from .trial_balance import Trial_Balance_Generator

utils = Utils()
dates = Dates() 

pp = utils.pretty_print
thtrow = utils.throw


tbg = Trial_Balance_Generator()


class Accounting_Analytics:
    def __init__(self) -> None:
        pass

    def generate_trial_balance_transactions(self,data):
        return tbg.generate_trial_balance_transactions(data)