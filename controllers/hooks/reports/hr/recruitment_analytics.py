from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp =utils.pretty_print
throw =utils.throw

def recruitment_analytics(dbms, object):
    Job_Offer = dbms.get_list("Job_Offer", user=o)
    pp(Job_Offer)
    Job_Offer_data_result = []

    for offer in Job_Offer.get('data', {}).get('rows', []):
        if not isinstance(offer, dict):
            continue
        
        Job_Offer_row = {
            "job_application": offer.job_application,
            "applicant_name": offer.applicant_name,
            "applicant_email": offer.applicant_email,
            "offer_date": offer.offer_date,
            "designation": offer.designation,
            "company": offer.company
        }

        Job_Offer_data_result.append(Job_Offer_row)

    return utils.respond(utils.ok, {'rows': Job_Offer_data_result})
