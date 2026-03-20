from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.default_templates import Default_Templates
from controllers.mailing.templates.default_template import Default_Template
from management.defaults.core.tenant_admin import tenant_admin
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def validate_pool_user(body, dbms, create=False, update=False, old_name=None):
    from controllers.dbms import DBMS
    admin_dbms = DBMS(init_admin=True, skip_user_validation=dbms.skip_user_validation)
    tenant = admin_dbms.get_doc("Tenant",dbms.tenant_db, privilege=True, fetch_by_field="db_name")
    if tenant.status != utils.ok:
        throw(f"Failed to fetch tenant configurations:{tenant.error_message}")
    if not dbms.tenant_db:
         throw("Tenant settings not properly configured!")
    if not create and not update:

        if admin_dbms.check_if_doc_exists("User_Pool", body.email.strip()):
            throw(f"User with email '{body.email}' already exists!")
    if create:
        create = admin_dbms.create("User_Pool", {"name": body.email,"tenant":tenant.data.name}, privilege=True, skip_workflows=True,skip_user_evaluation=True)
        if create.status != utils.ok:
             throw(f"Failed to create user account in pool:{create.error_message}")
    if update:
        up = admin_dbms.get_doc("User_Pool", old_name, privilege=True, fetch_linked_fields=False)
        new_name = admin_dbms.get_doc("User_Pool", body.name, privilege=True)
        if up.status == utils.ok:
            if up.data.tenant != tenant.data.id and up.data.tenant != tenant.data.name:
                throw(f"Email '{body.email}' already exists")
            else:
                if new_name.status == utils.ok:
                    if new_name.data.tenant != tenant.data.id  and new_name.data.tenant != tenant.data.name:
                        throw(f"Email '{body.email}' already exists")
        pool_user = admin_dbms.get_doc("User_Pool", old_name, privilege=True)
        if pool_user.status != utils.ok:
             throw(f"Failed to fetch user from pool:{pool_user.error_message}")
        pool_user.data.name = body.name
        pool_user.data.tenant = tenant.data.name
        update = admin_dbms.update("User_Pool", pool_user.data, privilege=True)
        if update.status != utils.ok:
             throw(f"Failed to update user pool:{update.error_message}")
         

def on_user_save(dbms, object):
    object.body.status = "Active"
    object.body.is_superuser = False
    object.body.is_staff = False
    object.body.user_permissions = []
    object.body.groups = []
    object.body.user_roles = []
    object.body.name = object.body.email
    if not object.body.password:
        pwd = utils.encrypt_password(generate=True)
    else:
         pwd = utils.encrypt_password(password=object.body.password)
    pwd.status == utils.ok or throw(pwd.error_message)
    pwd_data = pwd.data
    
    object.body.password = pwd_data.get("encrypted")
    object.body.pwd_data = pwd_data
    
    if object.body.first_name == "Administrator" and object.body.name != tenant_admin.get("name"):
        admin_usr =  dbms.get_doc("Lite_User",object.body.first_name, fetch_by_field="first_name", privilege=True)
        if admin_usr.status == utils.ok:
            throw("First Name can not be Administrator!")
    validate_pool_user(object.body, dbms)
    try:
        if object.body.permitted_companies:
            company_grouped = utils.array_to_dict(object.body.permitted_companies, "company")
            comp_keys = utils.get_object_keys(company_grouped)
            companies = dbms.get_list("Company", privilege=True, filters={"name__in":comp_keys},as_dict=True)
            if companies.status == utils.ok:
                company_data = companies.data
                for comp in comp_keys:
                    if company_data.get(comp):
                        company_grouped[comp].permitted_company_id = company_data.get(comp).id
                object.body.permitted_companies = utils.get_object_values(company_grouped)
    except Exception as e:
        pass
    

def after_user_save(dbms, object, result):
        body = object.body
        validate_pool_user(object.body, dbms,True)
        create = dbms.create("Onboarding", {"name": result.name, "user": result.name, "current_stage":1}, privilege=True)
        if body.first_name.lower() != "administrator":
            mailing = Mailing(dbms, object)
            dt      = Default_Templates()
            email   = body.email
            pwd     = body.pwd_data.password
            company = utils.from_dict_to_object()
            ss      = dbms.system_settings
            if ss:
                company = ss.linked_fields.default_company
            send_mail = mailing.send_mail(email,"User Creation",Default_Template.template(dt.new_user_template(company.name,dbms.host,email,pwd,body.first_name,company.company_logo),"New User Account Creation",company))
            pp ("==================RRRRRRRRRRRRRRRR", send_mail)


def on_user_fetch(dbms, object, result):
    if not object.is_list_fetch:
        try:
            if result.permitted_companies:
                ids = utils.array_to_dict(result.permitted_companies, "permitted_company_id")
                if ids:
                    for id in utils.get_object_keys(ids):
                        company = dbms.get_doc("Company", id, fetch_by_field="id", privilege=True)
                        if company.status == utils.ok:
                            ids[id].company = company.data.name
                result.permitted_companies = utils.get_object_values(ids)
        except Exception as e:
            pass





def on_user_update(dbms, object):
    body = object.body
    old_name = ""
    new_name = ""
    user = dbms.get_users(id=body.id, get_role=False, fetch_password=True, user_id= object.user)
    if user.status == utils.ok:
        usr = user.data
        old_name = usr.name
        if not body.first_name.lower().strip():
            throw("First name is mandatory for the user creation!")
        if usr.first_name.lower().strip() == "administrator" and body.first_name.lower().strip() != "administrator":
             throw("You are not allowed to changed any fields for Super Administrator account!")
        if body.first_name.lower().strip() == "administrator" and usr.first_name.lower().strip() != "administrator":
             throw("First Name can not be Administrator!")
        for label, value in body.items():
             if value or value == 0:
                  usr[label] = value
    try:
        if body.permitted_companies:
            company_grouped = utils.array_to_dict(body.permitted_companies, "company")
            comp_keys = utils.get_object_keys(company_grouped)
            companies = dbms.get_list("Company", privilege=True, filters={"name__in":comp_keys},as_dict=True)
            if companies.status == utils.ok:
                company_data = companies.data
                for comp in comp_keys:
                    if company_data.get(comp):
                        company_grouped[comp].permitted_company_id = company_data.get(comp).id
                usr.permitted_companies = utils.get_object_values(company_grouped)
    except Exception as e:
        pass
    object.body = usr

    

    validate_pool_user(usr, dbms,False, True, old_name)


# user pool
def on_user_pool_save(dbms, object):
    user = object.body
    pool = dbms.get_doc("User_Pool", user.name, privilege=True)
    if pool.status == utils.ok:
        throw(f"User with email '{user.name}' already used.")