from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
throw = utils.throw
def before_menu_card_save(dbms, object):
    body = object.body
    allowed_menu = dbms.get_list("Allowed_Menu",filters={"menu_card": body.name}, privilege=True)
    if allowed_menu.status == utils.ok:
        deleted = dbms.delete("Allowed_Menu",[allowed_menu.data.rows[0].id], privilege=True)
