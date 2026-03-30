from controllers.utils import Utils
import itertools
from itertools import chain
from collections import OrderedDict
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

class User_Controller:
    def __init__(self, dbms, user=None, obj=None) -> None:
        self.dbms = dbms
        self.user = user
        self.defaults = None
        self.current_user = self.dbms.current_user
        self.module = self.dbms.validation.module or ""
        self.app = ""
        self.content_type = ""
        self.url_params = utils.from_dict_to_object()
        if self.dbms.validation.extra_params:
            x_params = self.dbms.validation.extra_params
            self.app = x_params.app or ""
            self.content_type = x_params.content_type or ""

    def get_user_default_dashboard(self, fetch_actual=False):
        if not self.current_user.is_onboarded and not fetch_actual:
            if self.current_user:
                if not self.dbms.check_if_doc_exists("Onboarding", self.current_user.name):
                    create = self.dbms.create("Onboarding", {"name": self.current_user.name, "user": self.current_user.name, "current_stage":1}, privilege=True)
            return utils.respond(utils.ok, {
                "dashboard": "Onboarding", 
                "url": f"/app/onboarding/welcome",
                "module": "onboarding"
            })
        role = self.dbms.get_doc("Role", self.dbms.current_user.main_role, fetch_linked_fields=False, fetch_linked_tables=False, privilege=True)
        if role.status == utils.ok:
            if role.data.default_dashboard:
                dashboard = self.dbms.get_doc("Default_Dashboard", role.data.default_dashboard, fetch_linked_fields=False, fetch_linked_tables=False, privilege=True)
                if dashboard.status == utils.ok:
                    dash= dashboard.data
                    data = {
                        "dashboard": dash.name, 
                        "url": f"/app/{dash.module}/{dash.app_name}?loc={dash.app_name}&module={dash.module}&type={dash.page_type}&document={dash.content_type}",
                        "module": dash.module
                    }
                    return utils.respond( utils.ok, data)
                else:
                    return dashboard
        return role
    


    # get user allowed content
    def get_user_allowed_content(self):
        user_content = {}
        role_content = utils.from_dict_to_object({f"{self.module}":{}})
        allowed_content = self.dbms.get_tenant_allowed_content(get_dashboards=True, get_roles=True, get_allowed_menu_cards=True)
        if allowed_content.status != utils.ok:
            pp(f"FAILED TO FETCH USER ALLOWED CONTENT:{allowed_content.error_message}")
            return allowed_content
        content = allowed_content.data
        try:
            if not self.dbms.validation.module or (self.dbms.validation.module and self.dbms.validation.module.lower() in ["auth", "portal", "web",""]):
                return utils.respond(utils.no_content,"")
            user = self.dbms.current_user
            role_modules = self.dbms.get_list("Role_Module", filters={"parent":user.main_role, "role_module__in":content.modules}, complex_filters=self.dbms.query_builder(parent__isnull=False), privilege=True,as_dict=True, as_dict_key="role_module", fetch_linked_fields=True)
            if role_modules.status == utils.ok:
                active_modules = role_modules.data
                module_menu_cards = active_modules.get(self.module or [])
                mcs = utils.from_dict_to_object()
                if module_menu_cards and len(module_menu_cards) > 0:
                    ids = list(set(list(chain.from_iterable(module_menu_cards.role_cards[0].values()))))
                    # lets only get the menu cards allowed for the user but also only allowed for the tenant
                    allowed_menu_card_names = set(content.menu_cards).intersection(set(utils.get_object_keys(module_menu_cards.role_cards[0])))
                    menu_cards = self.dbms.get_list("Menu_Card", filters={"name__in": allowed_menu_card_names}, privilege=True)
                    menu_card_items_data = self.dbms.get_list("Menu_Card_Item", filters={"id__in":ids, "display": 1}, privilege=True)
                    if menu_cards.status == utils.ok:
                        mcs = utils.array_to_dict(utils.extract_dict_fields_from_list(menu_cards.data.rows,["id","idx","name","module"]),"name")
                        if menu_card_items_data.status == utils.ok:
                            mcs_items = utils.group(utils.extract_dict_fields_from_list(menu_card_items_data.data.rows,["id","idx","name","module","child_items","document","icon","type","title","loc", "parent"]),"parent")
                            for label, value in mcs.items():
                                mcs[label].card_items = mcs_items.get(label,[])
                            role_content[self.module].menu_cards = mcs

                for label, value in active_modules.items():
                    try:
                        dbd = value.linked_fields.default_dashboard
                        user_content[value.role_module] = {
                                "id":dbd.id,
                                "idx": dbd.idx,
                                "title":dbd.name,
                                "url": f"{value.linked_fields.role_module.url}/{dbd.app_name}?loc={dbd.app_name}&module={dbd.module}&type={dbd.page_type}&document={dbd.content_type}",
                                # "module": dbd.module,
                                "module": value.linked_fields.role_module.name,
                                "app": dbd.app_name,
                                "icon": value.linked_fields.role_module.icon,
                                "content_type": dbd.content_type,
                                "menu_cards": {} if value.role_module != self.module else mcs
                            }
                    except Exception as e:
                        pp(f"ERROR WHILE ASSIGNING DASHBOARD CONTENT:{str(e)}")
            return utils.respond(utils.ok, user_content)
        except Exception as e:
            pp(f"AN ERROR OCCURRED WHILE SETTING UP USER DEFAULTS:{str(e)}")
            return utils.respond(utils.no_content,"")
        

    def get_user_allowed_menu_items(self, group_by_module=True):
        data = utils.from_dict_to_object({"role":{}, "menus":[], "default_dashboard": self.get_user_default_dashboard(fetch_actual=True).data})
        role = self.dbms.get_doc("Role", self.dbms.current_user.main_role)
        if role.status == utils.ok:
            data.role = role.data
            if data.role.role_module:
                role_items = []
                for rm in data.role.role_module:
                    for cards in rm.role_cards:
                        role_items.extend(list(itertools.chain(*cards.values())))
                mcitm = self.dbms.get_list("Menu_Card_Item", filters={"id__in":role_items}, privilege=True)
                if mcitm.status == utils.ok:
                    menus = mcitm.data.rows
                    if group_by_module:
                        data.menus = utils.group(menus, "module")
                    else:
                        data.menus = menus
        return utils.respond(utils.ok, data)
    

    def evaluate_user_permission_on_doctype(self, doctype):
        doc = utils.replace_character(doctype, "_"," ")
        try:
            if doctype not in self.dbms.excluded_models:
                model_module = utils.get_model_module(doctype)
                if model_module.status != utils.ok:
                    return utils.respond(utils.internal_server_error, f"Failed to fetch configuration path for {utils}")
                wrapper = model_module.data
                filters = utils.from_dict_to_object({
                    "content_type__in": list(set([doctype, doctype.lower(), doc, doc.lower()])),
                    "module__in": list(set([wrapper.module, self.module, self.module.lower()])),
                    "app__in": list(set([wrapper.app, self.app])) 
                })
                items = self.dbms.get_list("Menu_Card_Item", filters=filters, privilege=True, fields=["id", "title", "parent"])
                if items.status != utils.ok:
                    return utils.respond(utils.bad_request, f"An error occurred while fetching menu item for doctype {doctype}: {items.error_message}")
                items = utils.get_list_of_dicts_column_field(items.data.rows, "id")
                role_module = self.dbms.get_doc("Role_Module", self.dbms.current_user.main_role, extra_filters={"role_module__name__in": [self.module, wrapper.module]}, fetch_by_field="parent", privilege=True)
                if role_module.status != utils.ok:
                    return utils.respond(utils.bad_request, f"An error occurred while fetching role module for doctype {doctype}: {role_module.error_message}")
                allowed_content = list(chain.from_iterable(utils.get_object_values(role_module.data.role_cards[0]))) 
                found = bool(set(items) & set(allowed_content))
                if not found:
                    return utils.respond(utils.forbidden, f"You are not allowed to access {utils.replace_character(doctype, '_', ' ')}! Please contact administrator!")
        except Exception as e:
            return utils.respond(utils.unprocessable_entity, f"An error occurred while evaluating user permissions: {str(e)}")
        return utils.respond(utils.ok, "Permitted")