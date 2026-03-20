from controllers.utils import Utils
utils = Utils()

pp = utils.pretty_print
throw = utils.throw

def get_module_apps(dbms, object):
    pass
    # modules = dbms.get_modules()
    # if modules.get("status") == utils.ok:
    #     module_objects = {}
    #     apps = utils.get_module___apps(group_by_module=True)
    #     if apps.get("status") == utils.ok:
    #         module_apps = apps.get("data")
    #         for md in modules.get("data").get("rows"):
    #             m = utils.replace_character(md.get("url"),"/app","")
    #             m = utils.replace_character(m,"/","")
    #             module_objects[m] = md
    #             module_objects[m]["apps"] = module_apps.get(m)
    #     return utils.respond(utils.ok, module_objects)
