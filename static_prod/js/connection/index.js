import { API_CONFIG, API_SETUP } from "./config.js"


export default class Execute {
    constructor(config) {
        this.utils = config.utils
        this.alerts = config.alerts
    }
    validate_params(params, validation_type = "GET") {
        delete API_CONFIG.headers['xfun']
        if (!params.model)
            return this.respond(API_CONFIG.status_codes.not_found, "Model not found! Please include model in your parameters!")
        if (validation_type === "GET") {
            if (params.page_size)
                params['page-size'] = params.page_size
            else{
                params['page-size'] = 1000000**2
            }
            if (params.current_page)
                params['current-page'] = params.current_page
            if (params.sort)
                params['sort'] = JSON.stringify(params.sort)
            if (params.get_single || delete API_CONFIG.headers['get-single'])
                delete API_CONFIG.headers['get-single']
            if (!params.filters) {
                params.filters = undefined
            }
            else if (params?.filters !== null && !this.utils.is_object(params.filters)) {
                params.filters = undefined
                return this.respond(API_CONFIG.status_codes.not_found, "Filters only accept object-like items eg { name : 'example'}")
            }
            else {
                params.filters = this.utils.remove_undefined_values(params.filters)
            }
            params.filters = JSON.stringify(params.filters)
        }
        else if (validation_type === "POST") {
            if (!params.data || !this.utils.is_object(params.data) || this.utils.is_empty_array(params.data)) {
                return this.respond(API_CONFIG.status_codes.not_found, "Data missing in your parameters")
            }
        }
        return this.respond(API_CONFIG.status_codes.ok, params)
    }
    redirect_to (status, __to) {
        console.log(`${lite.utils.get_host()}${__to}`)
        window.open(`${lite.utils.get_host()}${__to}`, '_blank');
    }

    respond(status, response = '') {
        let res = { 'status': status }
        
        if (status !== API_CONFIG.status_codes.ok && status !== API_CONFIG.status_codes.created)
            res.error_message = response
        res.data = response
        return res
    }

    configure(props) {
        const { request_type = 'GET', headers = {}, body = {}, endpoint_extension } = props
        const authCookie = lite.session.get_cookie ("lite_user")
        if (authCookie || authCookie != "") {
            API_CONFIG.headers.Authorization = `Bearer ${authCookie}`
        }
        API_SETUP({
            request_type: request_type,
            endpoint_extension: endpoint_extension,
            headers: { ...API_CONFIG.headers, ...headers },
            body: body
        })
    }
   
    async request_password_reset (data) {
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.request_password_reset,
            body: JSON.stringify(data)
        })
        return await this.request ().then (resolve => {
            const response = resolve?.data
            if (response?.status === API_CONFIG.status_codes.ok) {
                return response
            }else {

                return resolve?.response?.data
            }
            
        })
    }

    async validate_password_reset(data) {
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.request_password_reset_validation,
            body: JSON.stringify(data)
        })
        return await this.request().then (resolve => {
            const response = resolve?.data
            if (response?.status === API_CONFIG.status_codes.ok) {
                return resolve
            }else {
                return resolve?.response?.data
            }
            
        })
    }

    set_user_cookie(cookie){
        const expiryTime = 60 * 60
        lite.session.set_cookie ("lite_user", cookie, expiryTime)
    }

    async authentication (data) {
       
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.authenticate,
            body: data
        })

        return await this.request("json").then(resolve => {
            if(resolve?.status === lite.status_codes.ok){
                const data = resolve.data?.data
                this.set_user_cookie(data.token)
                return this.respond(lite.status_codes.ok, data)
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }

    async request(responseType="json", params={}) {
        const mod = lite.utils.get_current_module()
        API_CONFIG.headers.api_key = lite.session.get_cookie("api_key") || lite.session.get_cookie("temp_auth_key") || null 
        API_CONFIG.headers.params = JSON.stringify({...params || {}, ...lite.utils.get_url_parameters() || {}})
        if(!responseType){
            responseType = "json"
        }
        if (mod){
            API_CONFIG.headers.module = mod
        }
        let url = `${API_CONFIG.base_endpoint}${API_CONFIG.request_endpoint}`
        if (API_CONFIG.request_endpoint?.includes("services/")){
            url = `${API_CONFIG.request_endpoint}`
        }
        if (API_CONFIG.request_endpoint?.includes("portal/")){
            url = `${API_CONFIG.request_endpoint}`
        }
        switch (API_CONFIG.request_type) {
            case API_CONFIG.request_types.get:
                return axios.get(url, { headers: API_CONFIG.headers, timeout: 120000, responseType: responseType }).then(r => {
                    return r
                }).catch(err => {
                    return err
                })
            case API_CONFIG.request_types.post:
                return axios.post(url, API_CONFIG.body, { headers: API_CONFIG.headers, timeout: 120000, responseType:responseType }).then(r => {
                    return r
                }).catch(err => {
                    return err
                })
            case API_CONFIG.request_types.patch:
                return axios.patch(url, API_CONFIG.body, { headers: API_CONFIG.headers, timeout: 120000, responseType: responseType }).then(r => {
                    return r
                }).catch(err => {
                    return err
                })

            case API_CONFIG.request_types.put:
                return axios.put(url, API_CONFIG.body, { headers: API_CONFIG.headers, timeout: 120000, responseType:responseType }).then(r => {
                    return r
                }).catch(err => {
                    return err
                })
            case API_CONFIG.request_types.delete:
                return axios.delete(url, { headers: API_CONFIG.headers, body: JSON.stringify(API_CONFIG.body) }).then(r => {
                    return r
                }).catch(err => {
                    return err
                })
            default:
                console.error("Unknown request type")
                break;
        }
    }

    clean_data(resolve){
        if(typeof resolve?.data === "string"){
            try{
                const res = resolve?.data
                const clean = res.replace(/NaN/g, 'null')
                return this.respond(resolve.status, JSON.parse(clean).data)
            }
            catch(e){
                return this.respond(resolve.status, resolve?.data?.data)
            }
        }
        return this.respond(resolve.status, resolve?.data?.data)
    }


    async get(params) {
        const validation = this.validate_params(params, "GET")
        if (validation.status === API_CONFIG.status_codes.ok) {
            let header_content = validation.data
            if(header_content?.columns && header_content?.columns.length > 0){
                header_content.fields = lite.utils.object_to_string(header_content.columns)
            }
            delete header_content.columns
            this.configure({
                params: params,
                headers: header_content,
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.get,
            })
            return await this.request().then(resolve => {
                if (resolve.status === API_CONFIG.status_codes.ok) {
                    if(typeof resolve?.data === "string"){
                        try{
                            const res = resolve?.data
                            const clean = res.replace(/NaN/g, 'null')
                            return this.respond(resolve.status, JSON.parse(clean).data)
                        }
                        catch(e){
                            return this.respond(resolve.status, resolve?.data?.data)
                        }
                    }
                    return this.respond(resolve.status, resolve?.data?.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {

                    if(resolve.request.status !== API_CONFIG.status_codes.no_content){
                        this.alerts.toast({
                            toast_type: resolve.request.status,
                            title: resolve.request.statusText,
                            message: resolve?.response?.data?.error_message,
                            timer: 6000
                        })
                    }
                    return this.respond(resolve.status, [])
                }
            })
        }
        else { console.error(validation) }
    }

    async get_report(params) {
        const validation = this.validate_params(params, "GET")
        if (validation.status === API_CONFIG.status_codes.ok) {
            this.configure({
                params: params,
                headers: validation.data,
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.report,
            })
            return await this.request().then(resolve => {
                if (resolve.status === API_CONFIG.status_codes.ok) {
                    return this.respond(resolve.status, resolve?.data?.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    return this.respond(resolve.request.status, resolve?.response?.data?.error_message)
                }
            })
        }
        else { console.error(validation) }
    }

    async get_form_fields(params) {
        const validation = this.validate_params(params, "GET")
        if (validation.status === API_CONFIG.status_codes.ok) {
            this.configure({
                params: params,
                headers: validation.data,
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.form_fields,
            })
            return await this.request().then(resolve => {
                if (resolve.status === API_CONFIG.status_codes.ok) {
                    return this.respond(resolve.status, this.clean_data(resolve)?.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    return this.respond(resolve.request.status, resolve?.response?.data?.error_message)
                }
            })
        }
        else { console.error(validation) }
    }
    async download_report(params) {
        const validation = this.validate_params(params, "GET")
        if (params.fields){
            params.fields = lite.utils.object_to_string(params.fields)
        }
        if (validation.status === API_CONFIG.status_codes.ok) {
            this.configure({
                params: params,
                headers: validation.data,
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.download_report,
            })
            const loader_id = lite.alerts.loading_toast({
                title: `Preparing ${params.title}.`, 
                message:`Please wait while the system prepares the report for download.`
            })
            return await this.request("blob").then(async resolve => {
                lite.alerts.destroy_toast(loader_id)
                if(resolve.status === API_CONFIG.status_codes.ok){
                    
                    let format = "csv"
                    if(params.format === "excel")
                        format = "xlsx"
                    else if(params.format === "pdf")
                        format = "pdf"
                    if(resolve.status == lite.status_codes.ok){
                        const data = resolve.data
                        const blob = new Blob([data], {type: 'application/csv'});
                        const url = window.URL.createObjectURL(blob);
                        const a = $('<a/>', { href: url, text: 'Download CSV', download: `${params.title}.${format}`})
                        $('body').append(a);
                        a[0].click();
                        window.URL.revokeObjectURL(url);
                    }
                }
                else{
                    const text = await resolve.request.response.text()
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.response.statusText,
                        message: text?.trim()?.replace(/^"|"$/g, '') || "An error occurred while downloading report!",
                        timer: 6000
                    })
                }
            })
        }
        else { console.error(validation) }
    }

    async x_fetch(x_fun) {
        if (!x_fun) {
            console.error("xfun required!")
        }
        else {
            this.configure({
                params: {},
                headers: { xfun: x_fun },
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.x_fetch,
            })
            return await this.request().then(resolve => {
                if (resolve.status === API_CONFIG.status_codes.ok) {
                    if(typeof resolve?.data === "string"){
                        try{
                            const res = resolve?.data
                            const clean = res.replace(/NaN/g, 'null')
                            return this.respond(resolve.status, JSON.parse(clean).data)
                        }
                        catch(e){
                            return this.respond(resolve.status, resolve?.data?.data)
                        }
                    }
                    return this.respond(resolve.status, resolve?.data?.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    return resolve
                }
            })

        }
    }
    async dashboard(dashboard_name, params) {
        if (!dashboard_name) {
            console.error("xfun required!")
        }
        else {
            this.configure({
                params: {},
                headers: { xfun: dashboard_name, xtra:lite.utils.object_to_string(params) || {} },
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.dashboard,
            })
            return await this.request(null, params).then(resolve => {
                if (resolve.status === API_CONFIG.status_codes.ok) {
                    if(typeof resolve?.data === "string"){
                        try{
                            const res = resolve?.data
                            const clean = res.replace(/NaN/g, 'null')
                            return this.respond(resolve.status, JSON.parse(clean).data)
                        }
                        catch(e){
                            return this.respond(resolve.status, resolve?.data?.data)
                        }
                    }
                    return this.respond(resolve.status, resolve?.data?.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    return resolve
                }
            })
        }
    }
    async get_doc(model, doc_name, other_params) {
        if (!model) {
            console.error("FAILED TO OPEN DC: Model missing!")
        }
        else if (!doc_name) {
            console.error("FAILED TO OPEN DOC: doc_name missing!")
        }
        else {
            const params = { model: model, 'get-single': doc_name }
            this.configure({
                params: params,
                headers: {...params, params: other_params ? lite.utils.object_to_string(other_params) : ""},
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.get,
            })
            
            return await this.request().then(resolve => {
                if (resolve.status === API_CONFIG.status_codes.ok) {
                    if(typeof resolve?.data === "string"){
                        try{
                            const res = resolve?.data
                            const clean = res.replace(/NaN/g, 'null')
                            return this.respond(resolve.status, JSON.parse(clean).data)
                        }
                        catch(e){
                            return this.respond(resolve.status, resolve?.data?.data)
                        }
                    }
                    return this.respond(resolve.status, resolve?.data?.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.request.statusText,
                        message: resolve?.response?.data?.error_message || "No content found for the requested document",
                        timer: 6000
                    })
                    return this.respond(resolve.request.status, resolve?.response?.data?.error_message)
                }
            })

        }
    }
    async get_doc_value(model, doc_name, field_name) {
        if (!model) {
            console.error("FAILED TO OPEN DC: Model missing!")
        }
        else if (!doc_name) {
            console.error("FAILED TO OPEN DOC: doc_name missing!")
        }
        else if (!field_name) {
            console.error("FAILED TO OPEN DOC: field_name missing!")
        }
        else {
            const params = { model: model, 'doc_name': doc_name, fields: field_name}
            this.configure({
                params: params,
                headers: params,
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.get_doc_value,
            })
            return await this.request().then(resolve => {
                if (resolve.status === API_CONFIG.status_codes.ok) {
                    return this.respond(resolve.status, resolve?.data?.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    throw new Error('Request failed')
                }
            })

        }
    }

    async get_system_settings() {
        if(["portal", "auth"].includes(lite.utils.lower_case(lite.utils.get_current_module())) && ["login","client_auth"].includes(lite.utils.lower_case(lite.utils.get_current_app()))){
            
            lite.session.clear_cookies_for_domain()
        }
        const system_settings = await this.core("get_system_settings")
        return system_settings
    }

    async get_single(model) {
        if (!model) {
            console.error("FAILED TO OPEN DC: Model missing!")
        }
        const params = { model: model, 'get-single': this.utils.replace_chars(model, "_", " ") }
        this.configure({
            params: params,
            headers: params,
            request_type: API_CONFIG.request_types.get,
            endpoint_extension: API_CONFIG.endpoint_extensions.get,
        })
        return await this.request().then(resolve => {
            if (resolve.status === API_CONFIG.status_codes.ok) {
                return this.respond(resolve.status, resolve?.data?.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                throw new Error('Request failed')
            }
        })
    }

    async create(params) {
        const validation = this.validate_params(params, 'POST')
        if (validation.status !== API_CONFIG.status_codes.ok) {
            return validation
        }
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.post,
            headers: validation.data,
            body: params.data
        })
        return await this.request().then(resolve => {
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: resolve.request.statusText,
                    message: resolve?.response?.data?.error_message,
                    timer: 6000
                })
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }

    async upload(params) {
        const fd = new FormData()
        $.each(lite.utils.get_object_keys(params.files),(_, key)=>{
            if(params.files[key] && lite.utils.array_has_data(params.files[key])){
                $.each(params.files[key],(_,fl)=>{
                    fd.append(key, fl)
                })
            }
        })
        
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.upload,
            headers: {'Content-Type': 'multipart/form-data'},
            body: fd
        })
        return await this.request().then(resolve => {
            API_CONFIG.headers['Content-Type']  = "application/json"
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: resolve.request.statusText,
                    message: resolve?.response?.data?.error_message,
                    timer: 6000
                })
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }


    async extract_doc_data(file) {
        const fd = new FormData()
        fd.append("doc", file)
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.extract_doc_data,
            headers: {'Content-Type': 'multipart/form-data'},
            body: fd
        })
        return await this.request().then(resolve => {
            API_CONFIG.headers['Content-Type']  = "application/json"
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: resolve.request.statusText ,
                    message: resolve?.response?.data?.error_message || resolve.request?.responseText,
                    timer: 6000
                })
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }
    

    async x_post(x_fun, body = {}, throw_exception=true) {
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.x_post,
            headers: { xfun: x_fun },
            body: {data:body}
        })
        return await this.request().then(resolve => {
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                if(typeof resolve?.data === "string"){
                    try{
                        const res = resolve?.data
                        const clean = res.replace(/NaN/g, 'null')
                        return this.respond(resolve.status, JSON.parse(clean).data)
                    }
                    catch(e){
                        return this.respond(resolve.status, resolve?.data?.data)
                    }
                }
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                if(throw_exception){
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.request.statusText,
                        message: resolve?.response?.data?.error_message,
                        timer: 6000
                    })
                }
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }


    async core(x_fun, body = {}, throw_exception=true) {
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.core,
            headers: { xfun: x_fun },
            body: {data:body}
        })
        return await this.request().then(resolve => {
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                if(throw_exception){
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.request.statusText,
                        message: resolve?.response?.data?.error_message,
                        timer: 6000
                    })
                }
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }



    async export_data(model, docs = [], file_type, filters={}, throw_exception=true) {
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.export_data,
            headers: {model: model, docs: lite.utils.object_to_string(docs), "file-type": file_type, filters: lite.utils.object_to_string(lite.utils.remove_undefined_values(filters))},
            body: {data:""}
        })
        const model_name = lite.utils.capitalize(lite.utils.replace_chars(model,"_"," "))
        const loader_id = lite.alerts.loading_toast({
            title: `Exporting ${model_name} Data.`, 
            message:`Please wait while the system exports ${model_name} information.`
        })
        return await this.request().then(resolve => {
            lite.alerts.destroy_toast(loader_id)
            if (resolve.request.status === API_CONFIG.status_codes.ok){
                const url = window.URL.createObjectURL(new Blob([resolve.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', file_type === "csv" ? 'data.csv': "data.xlsx");
                document.body.appendChild(link);
                link.click();
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: "Exported Successfully",
                    message: "Data Exported Successfully",
                    timer: 6000
                })
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                if(throw_exception){
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.request.statusText,
                        message: resolve?.response?.data?.error_message,
                        timer: 6000
                    })
                }
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }



    async workflow_action(data, throw_exception=true) {
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.workflow_action,
            headers: { model: data?.model, action: data?.action, doc: lite.utils.object_to_string(data.values), "stage-no":data.stage_no},
            body: {"comment":data?.comment||""}
        })
        const loader_id = lite.alerts.loading_toast({
            title: `Applying Workflow on ${lite.utils.capitalize(lite.utils.replace_chars(data?.model,"_"," "))}`, 
            message:"Please wait while applying workflow on the selected document."
        })
        return await this.request().then(resolve => {
            lite.alerts.destroy_toast(loader_id)
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                if(throw_exception){
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.request.statusText,
                        message: resolve?.response?.data?.error_message,
                        timer: 6000
                    })
                }
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }

    async new_tenant(body = {}) {
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.new_tenant,
            body: {data:body}
        })
        return await this.request().then(resolve => {
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else {
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: resolve.request.statusText,
                    message: resolve?.response?.data?.error_message,
                    timer: 6000
                })
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }

    async patch(params) {
        const validation = this.validate_params(params, 'POST')
        if (validation.status !== API_CONFIG.status_codes.ok) {
            return validation
        }
        this.configure({
            request_type: API_CONFIG.request_types.patch,
            endpoint_extension: API_CONFIG.endpoint_extensions.patch,
            headers: validation.data,
            body: params.data
        })

        return await this.request().then(resolve => {
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: resolve.request.statusText,
                    message: resolve?.response?.data?.error_message,
                    timer: 6000
                })
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }

    async submit_doc({ model, doc_id }) {
        if (!model) {
            console.error("Failed to Submit Doc: model missing in the parameters!");
        }
        else if (!doc_id) {
            console.error("Failed to Submit Doc: doc_id missing in the parameters!");
        }
        else {
            this.configure({
                request_type: API_CONFIG.request_types.put,
                endpoint_extension: API_CONFIG.endpoint_extensions.submit,
                headers: { model: model, doc: doc_id },
                body: {}
            })
            
            const loader_id = lite.alerts.loading_toast({
                title: `Submitting ${lite.utils.capitalize(lite.utils.replace_chars(model,"_"," "))}`, 
                message:"Please wait while doc submission is underway."
            })
            return await this.request().then(resolve => {
                lite.alerts.destroy_toast(loader_id)
                if (resolve.request.status === API_CONFIG.status_codes.ok) {
                    return this.respond(API_CONFIG.status_codes.ok, resolve.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.request.statusText,
                        message: resolve?.response?.data?.error_message,
                        timer: 6000
                    })
                }
                return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
            })
        }
        return this.respond(API_CONFIG.status_codes.internal_server_error, "Document Subm")
    }

    async cancel_docs({ model, docs = [] }) {
        if (!model) {
            console.error("Failed to Submit Doc: model missing in the parameters!");
        }
        else if (!docs) {
            console.error("Failed to Submit Doc: doc_id missing in the parameters!");
        }
        else {
            this.configure({
                request_type: API_CONFIG.request_types.put,
                endpoint_extension: API_CONFIG.endpoint_extensions.cancel,
                headers: { model: model, doc: docs },
                body: {}
            })
            const loader_id = lite.alerts.loading_toast({
                title: `Cancelling ${lite.utils.capitalize(lite.utils.replace_chars(model,"_"," "))}`, 
                message:"Please wait while we cancel the document."
            })
            return await this.request().then(resolve => {
                lite.alerts.destroy_toast(loader_id)
                if (resolve.request.status === API_CONFIG.status_codes.ok) {
                    return this.respond(API_CONFIG.status_codes.ok, resolve.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.request.statusText,
                        message: resolve?.response?.data?.error_message,
                        timer: 6000
                    })
                }
                return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
            })
        }
        return this.respond(API_CONFIG.status_codes.internal_server_error, "Document Subm")
    }

    async delete_docs({ model, docs = [] }) {
        if (!model) {
            console.error("Failed to Submit Doc: model missing in the parameters!");
        }
        else if (!docs) {
            console.error("Failed to Submit Doc: doc_id missing in the parameters!");
        }
        else {
            this.configure({
                request_type: API_CONFIG.request_types.delete,
                endpoint_extension: API_CONFIG.endpoint_extensions.delete,
                headers: { model: model, doc: JSON.stringify(docs)},
                body: {}
            })
            const loader_id = lite.alerts.loading_toast({
                title: `Deleting ${lite.utils.capitalize(lite.utils.replace_chars(model,"_"," "))}`, 
                message:"Please wait while we delete the document."
            })
            return await this.request().then(resolve => {
                lite.alerts.destroy_toast(loader_id)
                
                if (resolve.request.status === API_CONFIG.status_codes.ok) {
                    return this.respond(API_CONFIG.status_codes.ok, resolve.data)
                }
                else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                    this.redirect_to (resolve.response.status, "/auth/login")
                }
                else {
                    this.alerts.toast({
                        toast_type: resolve.request.status,
                        title: resolve.request.statusText,
                        message: resolve?.response?.data?.error_message,
                        timer: 6000
                    })
                }
                return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
            })
        }

        return this.respond(API_CONFIG.status_codes.internal_server_error, "Document Subm")
    }









    // PORTAL

    async portal_request_otp(data){
        if(!data){
            throw new Error("OTP data required")
        }
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.portal_request_otp,
            body: data
        })
        return await this.request().then(resolve => {
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else {
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: resolve.request.statusText,
                    message: resolve?.response?.data?.error_message,
                    timer: 6000
                })
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }

    async portal_validate_opt(otp, email) {
        if(!email?.trim() || !otp?.trim()){
            throw new Error("Email and OTP required")
        }
        if (!lite.session.get_cookie("temp_auth_key")){
            this.alerts.toast({
                toast_type: lite.status_codes.unprocessable_entity,
                title: "Missing Temp Auth Key",
                message: "Temp auth key is missing. Please reload the page to start afresh.",
                timer: 6000
            })
            return
        }

        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.portal_validate_otp,
            body: {otp:otp?.trim(), email: email}
        })
        return await this.request().then(resolve => {
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else {
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: resolve.request.statusText,
                    message: resolve?.response?.data?.error_message,
                    timer: 6000
                })
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }

    async portal_get(xfun, filters, model) {
        if (!xfun) {
            console.error("Model required!")
        }
        else {
            this.configure({
                params: {},
                headers: { xfun: xfun, filters: lite.utils.object_to_string(filters || {}), model: model || undefined },
                request_type: API_CONFIG.request_types.get,
                endpoint_extension: API_CONFIG.endpoint_extensions.portal_get,
            })
            return await this.request().then(resolve => {
                if (resolve.status === API_CONFIG.status_codes.ok) {
                    if(typeof resolve?.data === "string"){
                        try{
                            const res = resolve?.data
                            const clean = res.replace(/NaN/g, 'null')
                            return this.respond(resolve.status, JSON.parse(clean).data)
                        }
                        catch(e){
                            return this.respond(resolve.status, resolve?.data?.data)
                        }
                    }
                    return this.respond(resolve.status, resolve?.data?.data)
                }
                else {
                    return resolve
                }
            })

        }
    }

    async portal_post(model, body = {}) {
        this.configure({
            request_type: API_CONFIG.request_types.post,
            endpoint_extension: API_CONFIG.endpoint_extensions.portal_post,
            headers: { model: model },
            body: {data: body}
        })
        return await this.request().then(resolve => {
            if (resolve.request.status === API_CONFIG.status_codes.ok) {
                return this.respond(API_CONFIG.status_codes.ok, resolve.data?.data)
            }
            else if (resolve?.response?.status === API_CONFIG.status_codes.unauthorized) {
                this.redirect_to (resolve.response.status, "/auth/login")
            }
            else {
                this.alerts.toast({
                    toast_type: resolve.request.status,
                    title: resolve.request.statusText,
                    message: resolve?.response?.data?.error_message,
                    timer: 6000
                })
            }
            return this.respond(resolve?.response?.data?.status, resolve?.response?.data?.error_message)
        })
    }
}