from controllers.utils import Utils
from controllers.utils.dates import Dates

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def declaration_of_interest(dbms, object):
    response_data =object.body.data

    fetch_committee =dbms.get_doc("Disciplinary_Committee", response_data.committee)
    if fetch_committee.status != utils.ok:
        pp(f"Something went wrong: {fetch_committee}")
        return
    
    committee =fetch_committee.data

    for member in committee[response_data.member_type]:
        if member ==response_data.member:
            if response_data.response =="Yes":
                member.interest_declaration ="Has Interest"
            else:
                member.interest_declaration ="Has no Interest"
    
    update_committee =dbms.update("Disciplinary_Committee", committee)
    if update_committee.status ==utils.ok:
        return True

