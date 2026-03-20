from controllers.utils import Utils

utils =Utils()
pp =utils.pretty_print
throw =utils.throw


def short_list_report(dbms, object):
    fetch_short_list = dbms.get_list("")   
    
    return utils.respond(utils.ok, {'rows': ""})

