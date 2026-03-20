from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def before_default_dashboard_fetch(dbms, object):
    enabled_modules = dbms.get_tenant_allowed_content(get_dashboards=False)
    if enabled_modules.status == utils.ok:
        if object.is_list_fetch:
            object.filters.update({"module__in":enabled_modules.data.modules})

def before_default_dashboard_save(dbms, object):
    body = object.body
    # pp(body)
    # allowed_menu = dbms.get_list("Allowed_Menu",filters={"menu_card": body.name}, privilege=True)
    # if allowed_menu.status == utils.ok:
    #     deleted = dbms.delete("Allowed_Menu",[allowed_menu.data.rows[0].id], privilege=True)


def before_default_dashboard_update(dbms, object):
    body = object.body
    # pp(body)
    # allowed_menu = dbms.get_list("Allowed_Menu",filters={"menu_card": body.name}, privilege=True)
    # if allowed_menu.status == utils.ok:
    #     deleted = dbms.delete("Allowed_Menu",[allowed_menu.data.rows[0].id], privilege=True)
