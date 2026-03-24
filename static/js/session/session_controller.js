import session_variables from "./session_variables.js"

class Session_Controller {
    constructor(utils) {
        this.utils = utils
        this.validate_session_variables()
    }
    validate_session_variables() {
        if (!this.utils.is_empty_object(session_variables)) {
            this.utils.get_object_keys(session_variables).forEach(key => {
                if (!this.get_session(key)) {
                    this.set_session(key, session_variables[key])
                }
            })
        }
    }

    get_session(key = String) {
        const d = sessionStorage.getItem(key)
        return d ? this.utils.string_to_object(d) : null
    }
    remove_session(key = String) {
        const d = sessionStorage.removeItem(key)
        return d
    }

    get_type_session() {
        return this.get_session("type")
    }

    get_page_session() {
        return this.get_type_session()
    }

    get_document_session() {
        return this.get_session("type")?.document || null
    }

    get_page_content_type() {
        return this.get_document_session()
    }

    get_auth_session() {
        return this.get_session("auth")
    }

    set_session(key = String, value = String) {
        const data = this.utils.is_object(value) ? this.utils.object_to_string(value) : value
        sessionStorage.setItem(key, data)
        return true
    }
    

    update_session(key, new_value) {
        const data = this.utils.is_object(new_value) ? this.utils.object_to_string(new_value) : new_value
        sessionStorage.setItem(key, data)
        return true
    }

    get_navigation_history() {
        return this.get_session('navigation_history')
    }


    // cookie controller
    set_cookie(name, value, minutes) {
        const now = new Date();
        
        const new_value = this.utils.is_object(value) ? this.utils.object_to_string(value) : value
        const expiration = new Date(now.getTime() + minutes * 60000);
        document.cookie = `${name}=${new_value}; expires=${expiration.toUTCString()}; path=/`;
    }

    get_cookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [cookie_name, cookie_value] = cookie.split('=').map(c => c.trim());
            if (cookie_name === name) {
                try{
                    return cookie_value ? this.utils.string_to_object(cookie_value) : null;
                }
                    
                catch(e){
                    return cookie_value
                }
            }
        }
        return null;
    }

    clear_cookies_for_domain () {
        document.cookie.split(';')?.forEach(function(cookie) {
            const cookie_parts = cookie.split('=');
            const cookie_name = cookie_parts[0].trim();
            document.cookie = cookie_name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        });
        // const cookies = document.cookie.split(';');
        // console.log(cookies)
        // for (const cookie of cookies) {
        //     const [name, value] = cookie.split('=');
        //     document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT;`;
        // }
    }
}

export default Session_Controller
