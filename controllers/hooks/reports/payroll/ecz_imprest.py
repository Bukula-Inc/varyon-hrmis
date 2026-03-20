from controllers.utils import Utils
from controllers.utils.dates import Dates

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

class Imprest_Report:
    def __init__(self, dbms, object):
        self.dbms =dbms
        self.object =object

    def imprest(self):
        imprest_lst =None
        requested_amount =0
        approved_amount = 0
        retired_amount = 0 
        balance =0
        imprest_report =[]

        fetch_ecz_imprest =self.dbms.get_list("ECZ_Imprest", filters={"docstatus": 1})
        if fetch_ecz_imprest.status ==utils.ok:
            imprest_lst =fetch_ecz_imprest.data.rows

        if imprest_lst !=None:
            for imprest in imprest_lst:
                imprest_report.append(utils.from_dict_to_object({
                    "imprest_id": imprest.name,
                    "initiator": imprest.initiator_first_name +" "+imprest.initiator_last_name,
                    "duration_from_date": imprest.duration_from_date,
                    "recommender": imprest.recommender,
                    "mode_of_travel": imprest.mode_of_travel,
                    "registration_number_of_vechile": imprest.registration_number_of_vechile,
                    "requested_amount": imprest.requested_amount,
                    "approved_amount": imprest.approved_amount,
                    "retired_amount": imprest.retired_amount, 
                    "balance":imprest.balance,
                }))      

                requested_amount +=float(imprest.requested_amount or 0)
                approved_amount +=float(imprest.approved_amount or 0)
                retired_amount +=float(imprest.retired_amount or 0)
                balance +=float(imprest.balance or 0)
                
                
            imprest_report.append(utils.from_dict_to_object({
                "imprest_id": "Totals",
                "initiator": "",
                "duration_from_date": "",
                "recommender": "",
                "mode_of_travel": "",
                "registration_number_of_vechile": "",
                "requested_amount": requested_amount,
                "approved_amount": approved_amount,
                "retired_amount": retired_amount, 
                "balance":balance,
                "is_opening_or_closing":True,
            }))

        return imprest_report

    @classmethod
    def imprest_reports(cls, dbms, object):
        instance =cls(dbms, object)

        return utils.respond(utils.ok, utils.from_dict_to_object({"rows":instance.imprest()}))