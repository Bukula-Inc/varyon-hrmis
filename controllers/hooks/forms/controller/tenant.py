from controllers.utils import Utils

utils = Utils()
throw = utils.throw
pp = utils.pretty_print


def before_tenant_save(dbms, object):
    body = object.body
    if body.modules:
        module_pricing = dbms.get_list("Module_Pricing",filters={"name__in":utils.get_list_of_dicts_column_field(body.modules,"module_price")}, privilege=True, fetch_linked_tables=True,as_dict=True, as_dict_key="name")
        if module_pricing.status == utils.ok:
            for idx, mp in enumerate(body.modules):
                mp_data = module_pricing.data.get(mp.module_price)
                if mp_data:
                    body.modules[idx].module = mp_data.module

def before_tenant_update(dbms,object):
    body = object.body
    tenant = dbms.get_doc("Tenant", object.body.name)
    if tenant.status != utils.ok:
        throw(f"Failed to fetch tenant info:{tenant.error_message}")
    data = tenant.data
    for key in utils.get_object_keys(tenant.data):
        if key != "modules":
            if body.get(key) != data.get(key) and body.get(key) != None and body.get(key) != "":
                try:
                    data[key] = body[key]
                except Exception as e:
                    pass
    if body.modules:
        data.modules = body.modules
    object.body = data

def before_tenant_delete(dbms,object):
    if object.body.license_no:
        license = dbms.get_doc("License", object.body.license_no)
        if license.status == utils.ok:
            delete_license = dbms.delete("License", object.body.license_no)
            if delete_license.status != utils.ok:
                throw(f"Failed to delete license for the tenant:{delete_license.error_message}")
        elif license.status != utils.no_content:
            throw(f"Failed to fetch license:{license.error_message}!")

    user_pools = dbms.get_list("User_Pool", complex_filters=dbms.query_builder(tenant__name=object.body.name) | dbms.query_builder(tenant_id=object.body.id))
    if user_pools.status == utils.ok:
        for up in user_pools.data.rows:
            delete_user = dbms.delete("User_Pool", up.name)
            if delete_user.status != utils.ok:
                throw(f"Failed to delete user:{delete_user.error_message}")