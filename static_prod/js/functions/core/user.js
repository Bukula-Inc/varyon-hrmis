
export default class User{
    constructor(){

    }
    async get_logged_user(){
        const token =  lite.session.get_cookie ("lite_user")
        if (token)
            return await lite.connect.x_post("get_logged_in_user",{token:token}, false)
        return lite.connect.respond(lite.status_codes?.not_found, "User Token Missing")
    }
    async get_user(user_id){
        return await lite.connect.get_doc("Lite_User",user_id)
    }
    async update_user_roles(user,roles){
        const body = {
            "uid": user,
            roles:roles
        }
        const updated = await lite.connect.x_post("update_user_roles", body)
        return updated
    }

    async update_user_permissions(user, permissions){
        const body = {
            "uid": user,
            permissions:permissions
        }
        const updated = await lite.connect.x_post("update_user_permissions", body)
        return updated
    }
}