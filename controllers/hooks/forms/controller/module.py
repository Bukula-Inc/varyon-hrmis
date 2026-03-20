from controllers.utils import Utils

utils = Utils()
throw = utils.throw
pp = utils.pretty_print


def before_module_fetch(dbms,object):
    pp("heheheheheheheheheh")


def after_module_fetch(dbms,object):
    pp("hehehehehehehehehehiiiii")