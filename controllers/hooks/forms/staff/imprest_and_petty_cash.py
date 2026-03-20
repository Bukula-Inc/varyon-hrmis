from controllers.utils import Utils

utils =Utils()
pp =utils.pretty_print
throw =utils.throw

def update_ecz_imprest(dbms, object):

    imp_ret =object.body
    imprest =None
    if imp_ret.imprest:
        imprest =imp_ret.linked_fields.imprest
    else: 
        throw("The referrence imprest is missing!")
    imprest.balance =imp_ret.balance_left
    imprest.retired_amount =float(imprest.retired_amount) +float(imp_ret.retired_amount)
    if float(imprest.retired_amount) ==float(imprest.requested_amount) and float(imp_ret.balance_left)<0:
        imprest.status ="Retired"
    else:
        imprest.status ="Partially Retired"
    imprest.docstatus =1

    try:
        dbms.update("ECZ_Imprest", imprest, update_submitted=True)
    except Exception as e:
        throw("An Error Occured, ",e)

    