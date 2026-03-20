from controllers.utils import Utils
utils = Utils()

pp = utils.pretty_print
throw = utils.throw

def get_role_cards(dbms, object):
    allowed_content = dbms.get_tenant_allowed_content(get_dashboards=False, get_roles=False, get_allowed_menu_cards=True)
    if allowed_content.status != utils.ok:
        throw(f"Failed to fetch tenant allowed content: {allowed_content.error_message}")
    content = allowed_content.data
    modules = dbms.get_modules(filters={"name__in": content.modules}, fetch_linked_fields=False, fetch_linked_tables=False)
    if modules.status != utils.ok:
        return modules
    module_data = utils.array_to_dict(modules.data.rows, "name")
    menu_cards = dbms.get_menu_cards(filters={"module__in":content.modules, "name__in": content.menu_cards}, fetch_linked_fields=False)
    card_items = dbms.get_card_items(filters={"module__in":content.modules, "parent__in": content.menu_cards}, fetch_linked_fields=False)
    if not menu_cards:
        return utils.respond(utils.internal_server_error, f"Failed to fetch menu card data:{menu_cards}")
    menu_card_data = utils.group(menu_cards,"module")
    for key in content.modules:
        try:
            module_data[key].menu_cards = menu_card_data.get(key) or []
        except Exception as e:
            pp(f"FAILED TO ASSIGN MENU CARDS TO MODULE {key}: {str(e)}")
    return utils.respond(utils.ok, {"menu_cards": module_data, "card_items": utils.array_to_dict(card_items,"id")})
