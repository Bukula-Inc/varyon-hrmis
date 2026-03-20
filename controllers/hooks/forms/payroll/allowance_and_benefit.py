from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def before_allowance_and_benefits_save(dbms, object):
    body =DataConversion.safe_get(object, "body")
    if DataConversion.safe_get(body, "create_salary_component"):
        sc =utils.from_dict_to_object({
            "name": DataConversion.safe_get(body, "name"),
            "component_type": "Earning",
            "value_type": "System Value",
            "percentage": 0.0,
            "fixed_amount": 0.0,
            "is_type": "",
            "accounts": [{
                "company": "ECZ",
                "account": ""
            }]
        })
        try:
            dbms.create("Salary_Component", sc)
        except Exception as e:
            throw(f""" Failed to create a salary component for {DataConversion.safe_get(body, "name")}""")

