from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.utils.dates import Dates
from controllers.mailing import Mailing
from controllers.utils.data_conversions import DataConversion

dates = Dates ()
utils = Utils ()
throw =utils.throw
pp =utils.pretty_print

def on_contract_save (dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    if DataConversion.safe_get (object.body, "period", 0):
        if not DataConversion.safe_get (object.body, "effective_date"):
            throw ("Effective Date is <b class='text-rose-600'>Required!</b>")
        if not DataConversion.safe_get (object.body, "end_date"):
            throw ("End Date is <b class='text-rose-600'>Required!</b>")
    if not utils.get_text_from_html_string (DataConversion.safe_get (object.body, "contract_content")):
        throw ("Contract Content is <b class='text-rose-600'>Required!</b>")

    if not DataConversion.safe_get (object.body, "previous_processed"):
        DataConversion.safe_set (object.body, "previous_processed", 0)
    if not DataConversion.safe_get (object.body, "last_pp_date"):
        DataConversion.safe_set (object.body, "last_pp_date", DataConversion.safe_get (object.body, "effective_date"))

    
def on_contract_submit(dbms, object):
    core_hr = Core_Hr (dbms=dbms, obj=object, user=object.user)
    mailing = Mailing (dbms=dbms, object=object)
    contract = object.body
    emp_info = core_hr.get_doc ("Employee", name=contract.employee)
    if emp_info:
        contract['full_name'] = emp_info.full_name
        if object.body.period:
            emp_info.end_of_contract = object.body.end_date
            emp_info.contract = object.body.name
            r = dbms.update ("Employee", emp_info, update_submitted=True)
        mail = mailing.send_mail(emp_info.email, "Employment Contract", core_hr.generate_contract_creation_email_content(contract))