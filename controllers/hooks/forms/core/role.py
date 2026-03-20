from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
throw = utils.throw
def before_role_save(dbms, object):
    body = object.body
    role_content = body.role_content
    modules = utils.get_object_keys(role_content)
    content = []
    role_module = []
    for module in modules:
        data = role_content[module]
        data.module = module
        content.append(data)
        role_module.append({
            "role_module": module,
            "default_dashboard": role_content[module].default_dashboard,
            "role_cards": [role_content[module].cards]
        })
    del object.body.role_content
    object.body.role_module = role_module

def before_role_update(dbms, object):
    body = object.body
    role_content = body.role_content or body.role_module
    modules = utils.get_object_keys(role_content)
    content = []
    role_module = []
    for module in modules:
        data = role_content[module]
        data.module = module
        content.append(data)
        role_module.append({
            "role_module": module,
            "default_dashboard": role_content[module].default_dashboard,
            "role_cards": [role_content[module].cards]
        })
    del object.body.role_content
    object.body.role_module = role_module



# listview controllers
def before_role_fetch(dbms, object):
    enabled_modules = dbms.get_tenant_allowed_content(get_dashboards=False)
    if enabled_modules.status == utils.ok:
        if object.is_list_fetch:
            object.filters.update({"module__in":enabled_modules.data.modules})


def after_role_fetch(dbms, object, result):
    pass
