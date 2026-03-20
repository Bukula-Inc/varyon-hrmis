from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def job_advertisement_before_save(dbms, object):
    core_hr =Core_Hr(dbms, object)

    object.body =core_hr.validate_job_advertisement(object.body)
    
    # if not object.body.designation:
    #     throw(f"the field {object.body.designation}, is not having a valid value.") 
    # if not object.body.company:
    #     throw(f"the field {object.body.company}, is not having a valid value.") 
    # if not object.body.department:
    #     throw(f"the field {object.body.department}, is not having a valid value.") 
    # if not object.body.vacancies:
    #     throw(f"the field {object.body.vacancies}, is not having a valid value.") 
    # if not object.body.description:
    #     throw(f"the field {object.body.description}, is not having a valid value.") 
    # if not object.body.lower_range:
    #     throw(f"the field {object.body.lower_range}, is not having a valid value.") 
    # if not object.body.upper_range:
    #     throw(f"the field {object.body.upper_range}, is not having a valid value.") 

    # throw("........")



def job_advertisement_before_submit(dbms, object):
    
    # SEND DATA TO WEB
    body =object.body

    # throw("........")


