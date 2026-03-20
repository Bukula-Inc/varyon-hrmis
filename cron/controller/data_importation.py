from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.core import Core
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw
class Data_Importation:
    def __init__(self, dbms, tc):
        self.dbms = dbms
        pass

    @classmethod
    def initialize_data_importation(cls, dbms, tc):
        di = dbms.get_list("Data_Importation", filters={"status":"Pending Importation"}, privilege=True, order_by=["id"])
        if di.status == utils.ok:
            for doc in di.data.rows:
                core = Core(dbms)
                importantion = core.start_data_importation(doc)
