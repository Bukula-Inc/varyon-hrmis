from controllers.utils import Utils
from controllers.utils.dates import Dates
utils = Utils()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw

def export_customer(dbms, object, data):
    new_data = data
    return utils.respond(utils.ok, data)