from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates() 

pp = utils.pretty_print
throw = utils.throw


class Trial_Balance_Generator:
    def __init__(self) -> None:
        pass

    def generate_trial_balance_transactions(self,data):
        return utils.respond(utils.ok, data)