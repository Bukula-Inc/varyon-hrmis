from controllers.utils import Utils
utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def update_company_logo(dbms,object):
    data = object.body.data
    company = dbms.get_doc("Company",data.company,user=object.user)
    if company.status == utils.ok:
        cd = company.data
        cd.company_logo = data.url
        update = dbms.update("Company", cd, object.user)
        return update

