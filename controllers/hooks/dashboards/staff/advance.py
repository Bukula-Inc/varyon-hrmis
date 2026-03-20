from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.object_generator import Generate_Object, Extract_Object
from controllers.core_functions.hr import Core_Hr
from datetime import datetime, timedelta,date
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()
# "created_on__gt": cls.past_30_days

class Staff_Advance:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_30_days = dates.add_days(dates.today(), -30)
        self.hr = Core_Hr(dbms,object.user,object)
        self.employee = None
        system_settings =  self.dbms.system_settings
        if system_settings:
            self.settings = utils.from_dict_to_object(system_settings)
            self.defaults =  self.settings.accounting_defaults
            comp = getattr(self.defaults, self.settings.default_company)
            cd = self.dbms.get_doc("Company",comp.name,fetch_linked_fields=True,privilege=True)
            cd.status == utils.ok or throw("Failed to fetch company info!")
            self.company = utils.from_dict_to_object(cd.data)
        

    @classmethod
    
    def staff_advance(cls, dbms, object):
        # Initialize the class instance correctly
        cls_instance = cls(dbms, object)
        
        result = {
            "total_applications": 0,
            "overall_advance_amount": 0.0,
            "overall_principal": 0.0,
            "overall_balance": 0.0,
            "overall_payment": 0.0,
            "overall_interest": 0.0,
            "unsettled_amount":0.0,
            "settled_amount":0.0,
            "advance_details": [],
            "partial_payments": []
        }
        
        advance = dbms.get_list("Advance_Application", filters={"applicant": dbms.current_user.name, "docstatus": 1},fetch_linked_tables=True, privilege=True)
        
        if advance.status == utils.ok:
            advance_data = advance.data.rows
            result["total_applications"] = len(advance_data)
            
            for data in advance_data:
                status = data.status
                name = data.name
                type_of_advance = data.type_of_advance
                purpose = data.purpose
                amount = utils.fixed_decimals(data.amount, 2)
                
                result["overall_advance_amount"] += amount
                
                result["advance_details"].append({
                    "status": status,
                    "name": name,
                    "type_of_advance": type_of_advance,
                    "purpose": purpose,
                    "total_advance_amount": amount,
                })
                for payment in data.calculated_value:
                    date_str = payment.month  # Assume this is a string in "YYYY-MM-DDTHH:MM:SS.SSSZ" format
                    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    payment_date = dt.date()
                    current_date = date.today()
                    
                    if payment.state == "Unsettled":
                        result["unsettled_amount"] += payment.payment
                    elif payment.state == "Settled":
                        result["settled_amount"] += payment.payment
                    
                    result["overall_principal"] += utils.fixed_decimals(payment.principal, 2)
                    result["overall_balance"] += utils.fixed_decimals(payment.balance, 2)
                    result["overall_payment"] += utils.fixed_decimals(payment.payment, 2)
                    result["overall_interest"] += utils.fixed_decimals(payment.interest, 2)
                    
                    if current_date.year == payment_date.year and current_date.month == payment_date.month:
                        result["current_month_payment"]= payment.payment
                    # result["partial_payments"].append({
                    #     "principal": payment.principal,
                    #     "balance": payment.balance,
                    #     "payment": payment.payment,
                    #     "interest": payment.interest,
                    #     "month": payment.month,
                    #     "state": payment.state,
                    # })
        return utils.respond(utils.ok, result)

