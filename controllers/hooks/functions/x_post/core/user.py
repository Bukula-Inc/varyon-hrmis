from controllers.authentication import Authentication
from controllers.utils import Utils
from django.contrib.auth.hashers import check_password, make_password
from controllers.utils.jwt import JWT
utils = Utils()
throw = utils.throw
pp = utils.pretty_print

jwt = JWT()

def update_user_dp(dbms,object):
    data = object.body.data
    user = dbms.get_users(id=data.uid, get_role=True, fetch_password=True, user_id= object.user)
    if user.get("status") == utils.ok:
        usr = user.get("data")
        usr["dp"] = data.url
        return dbms.update("Lite_User", usr, privilege=True)


def create_user_role(dbms, object, uid,role_id):
    nr = {
        "docstatus": 0,
        "idx": 0,
        "disabled": 0,
        "status": "Active",
        "parent_type": "Lite_User",
        "parent": uid,
        "role": role_id
    }
    check = dbms.get_list("Lite_User_Role", user=object.user, filters={ "role":role_id, "parent": uid})
    if check.status != utils.ok:
        create = dbms.create("Lite_User_Role", utils.from_dict_to_object(nr), object.user)
        return create
    check["data"] = check.data.rows[0]
    return check

def create_user_permission(dbms, object, uid, perm_model, action):
    np = {
        "docstatus": 0,
        "idx": 0,
        "disabled": 0,
        "status": "Active",
        "parent_type": "Lite_User",
        "parent": uid,
        "permission_model": perm_model,
        "permitted_action": action
    }
    check = dbms.get_list("Lite_User_Permission", user=object.user, filters={ "permitted_action": action, "parent": uid, "permission_model": perm_model})
    if check.get("status") != utils.ok:
        create = dbms.create("Lite_User_Permission", utils.from_dict_to_object(np), object.user)
        return create
    check["data"] = check.data.rows[0]
    return check



def update_user_roles(dbms,object):
    data = object.body.data
    try:
        uid = data.uid
        roles = data.roles
        user = dbms.get_users(id=uid, jsonfy=True, get_role=True)
        new_roles = []
        user_data = None
        if user.get("status") == utils.ok:
            user_data = user.get("data")
            available_roles = dbms.get_list("Lite_User_Role", user=object.user, filters={"parent": uid})

            # IF THE USER DOES NOT HAVE ANY ROLES
            if available_roles.status == utils.no_content:
                for role in data.roles:
                    if role.add:
                        create = create_user_role(dbms, object, uid, role.role)
                        if create.status == utils.ok:
                            new_roles.append(create.data.id)

            # IF THE USER HAS SOME ROLES
            else:
                exsiting_roles = available_roles.data.rows
                existing_role_objects = {}
                for x_role in exsiting_roles:
                    existing_role_objects[x_role.role] = x_role
                for rw in roles:
                    if rw.add:
                        rid = existing_role_objects.get(rw.role)
                        if not rid:
                            create = create_user_role(dbms, object, uid, rw.role)
                            if create.get("status") == utils.ok:
                                new_roles.append(create.get("data").get("id"))
                        else:
                            new_roles.append(rid.get("id"))
                    else:
                        rid = existing_role_objects.get(rw.role)
                        if rid:
                            delete = dbms.delete("Lite_User_Role",[rid.get("id")],object.user)
                            delete.get("status") == utils.ok or throw(f"Failed to update user roles: {delete.get('error_message')}")

            
            return utils.respond(utils.ok,{"data":"Roles Updated Successfully"})
        return utils.respond(utils.not_found,{"data":"User Not Found"})
    except Exception as e:
        return utils.respond(utils.internal_server_error, {"error_message":e})



def update_user_permissions(dbms,object):
    data = object.body.data
    try:
        uid = data.uid
        permissions = data.permissions.values()
        user = dbms.get_users(id=uid, jsonfy=True, get_role=True)
        new_permissions = []
        user_data = None
        if user.get("status") == utils.ok:
            user_data = user.get("data")
            available_permissions = dbms.get_list("Lite_User_Permission", user=object.user, filters={"parent": uid})

            # IF THE USER DOES NOT HAVE ANY PERMISSIONS
            if available_permissions.get("status") == utils.no_content:
                for perm in permissions:
                    for p in perm:
                        actions = p.get("permissions")
                        for label, value in actions.items():
                            if value:
                                create = create_user_permission(dbms, object, uid, p.get("model"), label)
                                if create.get("status") == utils.ok:
                                    new_permissions.append(create.get("data").get("id"))

            # IF THE USER HAS SOME ROLES
            else:
                existing_permissions = available_permissions.get("data").get("rows")
                existing_perm_objects = {}
                for x_perm in existing_permissions:
                    existing_perm_objects[f"{x_perm.get('permission_model')}_{utils.replace_character(x_perm.get('permitted_action'),' ','_')}"] = x_perm
                for perm in permissions:
                    for p in perm:
                        actions = p.get("permissions")
                        for label, value in actions.items():
                            key = f"{p.get('model')}_{utils.replace_character(label,' ','_')}"
                            if value:
                                check = existing_perm_objects.get(key)
                                if check:
                                    new_permissions.append(existing_perm_objects.get(key).get("id"))
                                else:
                                    create = create_user_permission(dbms, object, uid, p.get("model"), label)
                                    if create.get("status") == utils.ok:
                                        new_permissions.append(create.get("data").get("id"))
                            else:
                                if existing_perm_objects.get(key):
                                    delete = dbms.delete("Lite_User_Permission",[existing_perm_objects.get(key).get("id")], object.user)
            return utils.respond(utils.ok,{"data":"Permissions Updated Successfully"})
        return utils.respond(utils.not_found,{"data":"User Not Found"})
    except Exception as e:
        return utils.respond(utils.internal_server_error, {"error_message":str(e)})


def get_logged_in_user(dbms, object):
    token = object.body.data.token
    decoded = jwt.decode_token(token)
    if decoded.get("status") == utils.ok:
        data = decoded.get("data")
        if data.get("user_id"):
            return dbms.get_doc("Lite_User",data.get("user_id"), privilege=True)
        

def update_user_password(dbms, object):
    body = object.body.data
    user = dbms.current_user
    if not check_password(body.old_password.strip(), user.password):
        throw("Incorrect old password!")
    if body.new_password != body.rpt_password:
        throw("New passwords do not match!")
    if not Authentication.validate_password(body.new_password):
        throw("Password not valid. It must contain at least \n one uppercase letter and one number")
    user.password = make_password(body.new_password)
    user.has_changed_default_password = 1
    update = dbms.update("Lite_User", user, dbms.current_user_id, skip_hooks=True, skip_audit_trail=True)
    return update


def certify_user(dbms, object):
    if dbms.current_user:
        if not dbms.check_if_doc_exists("User_Certificate", dbms.current_user.name):
            create = dbms.create("User_Certificate", {"name": dbms.current_user.name, "user": dbms.current_user.name}, privilege=True)
            return create
        user = dbms.current_user
        user.is_onboarded = 1
        update = dbms.update("Lite_User", user, privilege=True)
        pp(update)
        return dbms.get_doc("User_Certificate", dbms.current_user.name, privilege=True)

    return utils.respond(utils.unauthorized, "User not found in the headers!")