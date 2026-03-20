from controllers.utils import Utils

utils = Utils ()
pp = utils.pretty_print
def get_advance_config_ (dbms, object):
    ret = dbms.get_doc ("Salary_Advance_Configuration", object.body.data.name, user=object.user)
    
    return utils.respond (ret.status, response=ret.data)