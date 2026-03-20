from controllers.utils import Utils

utils = Utils ()
pp = utils.pretty_print
def get_gratuity_setup (dbms, object):
    res = dbms.get_doc ("Gratuity_Configuration", object.body.data.name)
    utils.pretty_print(res)  
    return utils.respond (res.status, response=res.data)