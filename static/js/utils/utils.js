class Utils {
    constructor() {

    }
    
    async hide_display_icons(hidden=true){
        if(hidden){
            $(".material-symbols-outlined").addClass(".material-symbols-outlined-hidden")
        }
        else{
            const icons = await lite.utils.delay_until(()=>{
                if($(".material-symbols-outlined")?.length > 0)
                    return $(".material-symbols-outlined")
            })
            icons?.removeClass(".material-symbols-outlined-hidden")
        }
    }
    
    getDateDifference(from_date, to_date = undefined, unit_type, cd = false) {
        const fromDate = new Date(from_date);
        const toDate = to_date ? new Date(to_date) : new Date();
        const timeDifference = toDate - fromDate;
        let result;
    
        switch (unit_type.toLowerCase()) {
            case 'days':
                result = timeDifference / (1000 * 3600 * 24);
                break;
            case 'weeks':
                result = timeDifference / (1000 * 3600 * 24 * 7);
                break;
            case 'months':
                let monthsDifference = (toDate.getFullYear() - fromDate.getFullYear()) * 12;
                monthsDifference += toDate.getMonth() - fromDate.getMonth();
                if (cd && toDate.getDate() < fromDate.getDate()) {
                    monthsDifference -= 1;
                }
                result = monthsDifference;
                break;
            case 'years':
                result = toDate.getFullYear() - fromDate.getFullYear();
                break;
            default:
                result = 0;
                break;
        }
        return result;
    }
    

    is_function(param) {
        return typeof param === "function"
    }
    generate_loader(params = {light_mode:false,size:6, loader_type:"dots", classnames:"", text:"", text_classnames:""}){
        const color = params?.light_mode ? 'white' :'default'
        const size = params?.size || 6
        if(params?.loader_type && params.loader_type === 'dots'){
            return `
                <div class="${params?.classnames || 'flex items-center justify-center flex-col'} dynamic-loader">
                    <svg width="25" viewBox="0 0 120 30" xmlns="http://www.w3.org/2000/svg" fill="${color}" class="w-${size} h-${size} mr-2">
                        <circle cx="15" cy="15" r="15">
                            <animate attributeName="r" from="15" to="15" begin="0s" dur="0.8s" values="15;9;15" calcMode="linear" repeatCount="indefinite"></animate>
                            <animate attributeName="fill-opacity" from="1" to="1" begin="0s" dur="0.8s" values="1;.5;1" calcMode="linear" repeatCount="indefinite"></animate>
                        </circle>
                        <circle cx="60" cy="15" r="9" fill-opacity="0.3">
                            <animate attributeName="r" from="9" to="9" begin="0s" dur="0.8s" values="9;15;9" calcMode="linear" repeatCount="indefinite"></animate>
                            <animate attributeName="fill-opacity" from="0.5" to="0.5" begin="0s" dur="0.8s" values=".5;1;.5" calcMode="linear" repeatCount="indefinite"></animate>
                        </circle>
                        <circle cx="105" cy="15" r="15">
                            <animate attributeName="r" from="15" to="15" begin="0s" dur="0.8s" values="15;9;15" calcMode="linear" repeatCount="indefinite"></animate>
                            <animate attributeName="fill-opacity" from="1" to="1" begin="0s" dur="0.8s" values="1;.5;1" calcMode="linear" repeatCount="indefinite"></animate>
                        </circle>
                    </svg>
                    <span class="${params?.text_classnames || ''}"> ${params?.text || ''} </span>
                </div>
            `
        }
        return `
            <div class="${params?.classnames || 'flex items-center justify-center flex-col'} dynamic-loader">
                <div class="dark-spin border-${color} w-[${size}px] h-[${size}px] dynamic-loader"></div>
                <span class="${params?.text_classnames || ''}"> ${params?.text || ''} </span>
            </div>
        `
    }
    add_loader_component(params){
        $(params?.wrapper)?.html(`
            <div class="w-full ${params?.classnames} h-[90%] flex items-center justify-center font-semibold flex-col" >
                ${this.generate_loader(params)}
            </div>
        `)
    }
    add_empty_component({$wrapper,text,color="orange", classnames="",}){
        $($wrapper)?.html(`
            <div class="w-full h-[95%] flex items-center justify-center font-semibold flex-col ${classnames}" >
                <span class="material-symbols-outlined text-30 mb-5 text-${color}-400"> folder_copy </span>
                <span>${text || "No Content Found"}</span>
            </div>
        `)
    }

    create_status_wrapper(name, status_color, status_inner_color){
        return `
            <div class="doc-status-wrapper px-3 flex items-center justify-center min-w-[100px] h-[20px] rounded-md text-orange-800 text-14 active" style="background-color: ${status_color}; filter: brightness(99%); border: 1px solid ${status_color};">
                <div class="w-[8px] doc-status-pill h-[8px] rounded-full mr-1" style="background-color: ${status_inner_color};"></div>
                <span class="doc-status-text text-[13px] truncate overflow-ellipsis" style="color: ${status_inner_color};">${name}</span>
            </div>
        `
    }
    format_value({value_type,value,status_color, status_inner_color}){
        if(!value){
            if( ["figure","float"].includes(this.lower_case(value_type))){
                return "0.00"
            }
            else if(this.lower_case(value_type) === "int"){
                return "0"
            }
            else if(this.lower_case(value_type) === "percentage"){
                return "0%"
            }
            return '<div class="w-full flex items-center justify-center font-bold text-18 text-gray-400">-</div>'
        }
        if(["text","code","rich","long-text"].includes(this.lower_case(value_type))){
            return value
        }
        else if(this.lower_case(value_type) === "percentage"){
            return `${value}%`
        }
        else if( ["figure","float"].includes(this.lower_case(value_type))){
            return this.thousand_separator(value,2)
        }
        else if(this.lower_case(value_type) === "currency"){
            return this.thousand_separator(value,2)
        }
        else if(this.lower_case(value_type) === "int"){
            return this.thousand_separator(value,0)
        }
        else if(this.lower_case(value_type) === "status"){
            if(status_color && status_inner_color){
                return this.create_status_wrapper(value, status_color, status_inner_color)
            }
            else{
                return value
            }
        }
        else{
            return value
        }
    }
    copy_object(obj=[] | {}){
        return JSON.parse(JSON.stringify(obj))
        // return Object.assign({}, obj)
    }
    copy_dict(obj= {}){
        return Object.assign({}, obj)
    }
    deep_clone(obj) {
        if (typeof obj !== "object" || obj === null) return obj;

        if (Array.isArray(obj)) {
            return obj.map(item => this.deep_clone(item));
        }
        const copy = {};
        for (const key in obj) {
            const val = obj[key];
            if (typeof val === "function") {
            // Keep the same function reference
            copy[key] = val;
            } else if (typeof val === "object" && val !== null) {
            copy[key] = this.deep_clone(val);
            } else {
            copy[key] = val;
            }
        }
        return copy;
    }

    // check if the array is empty
    is_empty_array(obj = []) {
        return obj?.length === 0
    }
    array_has_data(obj = []) {
        return obj?.length > 0
    }
    is_empty_object(obj = {}) {
        if(obj)
            return Object.keys(obj).length === 0
        return true
    }
    object_has_data(obj = {}) {
        if(obj)
            return Object.keys(obj).length > 0
        return false
    }
    array_length(arr = []) {
        return arr?.length || 0
    }
    // get object keys
    get_object_keys(obj = {}) {
        return Object.keys(obj).length > 0 ? Object.keys(obj) : []
    }
    
    get_object_values(obj = {}) {
        return Object.keys(obj).length > 0 ? Object.values(obj) : []
    }

    object_has_key(obj, key){
        return obj.hasOwnProperty(key)
    }

    get_key_value_pairs(obj = {}, keys = []) {
        let o = {}
        $.each(keys, (_, k) => o[k] = obj[k])
        return o
    }
    filter_object(objs = [], key = '', value = '') {
        let res = objs?.filter(obj => obj[key] === value)
        if (!this.is_empty_array(res)) {
            return res[0]
        }
        return null
    }

    remove_undefined_values(obj = {}) {
        let new_obj = {}
        $.each(this.get_object_keys(obj), (_, k) => {
            if (obj[k] !== undefined && obj[k] !== null && obj[k] !== NaN) {
                new_obj[k] = obj[k]
            }
        })
        return new_obj
    }
    remove_undefined_keys(obj = {}) {
        let new_obj = {}
        $.each(this.get_object_keys(obj), (_, k) => {
            if (k !== "undefined") {
                new_obj[k] = obj[k]
            }
        })
        return new_obj
    }

    remove_zero_values(obj = {}) {
        let new_obj = {}
        $.each(this.get_object_keys(obj), (_, k) => {
            if (obj[k] !== undefined && obj[k] !== null && obj[k] !== NaN && obj[k] !== 0) {
                new_obj[k] = obj[k]
            }
        })
        return new_obj
    }

    keys_to_lower(obj = {}) {
        const new_obj = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                new_obj[key.toLowerCase()] = obj[key];
            }
        }
        return new_obj;
    }

    // check if object has a certain key
    has_key(obj, key) {
        return Array.isArray(obj) ? obj.includes(key) : obj.hasOwnProperty(key)
    }
    // check if the value is an array or object
    is_object(obj) {
        return typeof obj === ("object" || "array")
    }
    // convert a stringified object to an object
    string_to_object(str = null) {
        if (str) {
            try {
                return JSON.parse(str)
            } catch (error) {
                return str
            }
        }
        return null
    }
    // convert an object to a string
    object_to_string(obj = {} | []) {
        if (this.is_object(obj)) {
            return JSON.stringify(obj)
        }
        else {
            return obj
        }
    }
    // get location info
    get_location_info() {
        return window.location
    }

    // get web host name
    get_host() {
        return window.location.host
    }
    get_protocal(){
        return window.location.protocol
    }

    // get the current module for the system
    get_current_module() {
        const url = window.location.pathname
        if (url) {
            const comps = url?.split('/')
            const md = comps[1]?.toLowerCase()
            if(md === "app")
                return comps[2]?.toLowerCase()
            return md
        }
        return ''
    }
    get_current_loc() {
        const url = window.location.pathname
        if (url) {
            const comps = url?.split('/')
            const md = comps[1]?.toLowerCase()
            if(md === "app")
                return comps[3]?.toLowerCase() || ''
            return comps[2]?.toLowerCase() || ''
        }
        return ''
    }
    get_current_app() {
        return this.get_current_loc()
    }

    get_current_sub_loc() {
        const url = window.location.pathname
        if (url) {
            const comps = url?.split('/')
            const md = comps[1]?.toLowerCase()
            if(md === "app")
                return comps[4]?.toLowerCase() || 'dashboard'
            return comps[3]?.toLowerCase() || null
        }
        return ''
    }
    get_current_sub_app() {
        return this.get_current_sub_loc()
    }

    async import_nav_content(){
        const current_module  = this.get_current_module()
        if(current_module){
            try{
                const module_routes = await import(`../nav/module_routes/${current_module}.js`)
                if(module_routes){
                    return module_routes?.default || false
                }
                // console.error(`NAV MODULE ROUTES IMPORTATION ERROR: Failed to find /nav/module_routes/${current_module}.js file in nav_routes routes. ensure the file and module name matches!`)
                return false
            }
            catch{
                // console.error(`NAV MODULE ROUTES IMPORTATION ERROR: Failed to find /nav/module_routes/${current_module}.js file in nav_routes routes. ensure the file and module name matches!`)
                return false
            }
            
        }
    }

    async import_module_content(){
        const current_module  = this.get_current_module()
        const current_loc = this.get_current_loc()
        if(current_module){
            try{
                const module_loc = await import(`../modules/${current_module}/${current_loc}/index.js`)
                if(typeof module_loc?.default === 'function'){
                    return module_loc?.default || false
                }
                console.warn(`MODULE APP CLASS IMPORTATION ERROR: Failed to find /modules/${current_module}/${current_loc}/index.js file in modules. ensure the module directory and app directory matches both module and loc names!`)
                return false
            }
            catch{
                // console.warn(`MODULE APP CLASS IMPORTATION ERROR: Failed to find /modules/${current_module}/${current_loc}/index.js file in modules. ensure the module directory and loc directory matches both module and loc names!`)
                return false
            }
        }
    }

    async import_list_content(){
        const current_module  = this.get_current_module()
        if(current_module && current_module !== "portal"){
            const document = this.get_url_parameters("document")
            if(document){
                const file_name = this.lower_case(this.replace_chars(document," ","_"))
                try{
                    const lisview = await import(`../listviews/${current_module}/${file_name}.js`)
                    if(lisview.default){
                        return lisview.default || false
                    }
                    console.warn(`APP LISTVIEW CONFIGURATION IMPORTATION ERROR: Failed to find /listviews/${current_module}/${file_name}.js file in module listviews. ensure listview file for ${file_name} matches document!`)
                    return false
                }
                catch{
                    console.warn(`APP LISTVIEW CONFIGURATION IMPORTATION ERROR: Failed to find /listviews/${current_module}/${file_name}.js file in module listviews. ensure listview file for ${file_name} matches document!`)
                    return false
                }
            }
        }
    }

    async import_form_controller(){
        try{
            const form_controller = await import("../page/form_controller/index.js")
            if(form_controller.default){
                if(form_controller.default)
                    return form_controller.default || false
                else{
                    return false
                }
            }
            console.warn(`Failed to import form controller file!`)
            return false
        }
        catch(e){
            console.warn(`FORM CONROLLER IMPORTATION ERROR::${e}`)
            return false
        }
    }

    async import_form_content(module_name=undefined, document_name=undefined){
        const current_module  = module_name || this.get_current_module()
        if(current_module){
            const current_type = this.get_url_parameters("type")
            const document = document_name || this.get_url_parameters("document")
            if(document && current_type && ["new","info"].includes(current_type)){
                const file_name = this.lower_case(this.replace_chars(document," ","_"))
                try{
                    const form = await import(`../forms/${current_module}/${file_name}.js`)
                    if(form.default){
                        return form.default || false
                    }
                    console.warn(`APP FORM CONFIGURATION IMPORTATION ERROR: Failed to find /forms/${current_module}/${file_name}.js file in module forms. ensure form file for ${file_name} matches document!`)
                    return false
                }
                catch(e){
                    console.error(`APP FORM CONFIGURATION IMPORTATION ERROR::${e}`)
                    return false
                }
            }
        }
    }

    async import_form_overrides(){
        const current_module  = this.get_current_module()
        if(current_module){
            const document = this.get_url_parameters("document")
            if(document){
                const file_name = this.lower_case(this.replace_chars(document," ","_"))
                try{
                    const overrides = await import(`../overrides/form/${current_module}/index.js`)
                    if(overrides){
                        if(overrides[file_name])
                            return overrides[file_name] || false
                        else{
                            return false
                        }
                    }
                    console.warn(`APP FORM OVERRIDES IMPORTATION ERROR: Failed to find /overrides/form/${current_module}/index.js file in form overrides. ensure index.js file is created in ${current_module} directory!`)
                    return false
                }
                catch(e){
                    // console.error(`APP FORM OVERRIDES IMPORTATION ERROR::${e}`)
                    return false
                }
            }
        }
    }

    async import_report_controller(){
        try{
            const report_controller = await import("../page/report_controller/index.js")
            if(report_controller.default){
                if(report_controller.default)
                    return report_controller.default || false
                else{
                    return false
                }
            }
            console.warn(`Failed to import report controller file!`)
            return false
        }
        catch(e){
            console.error(`REPORT CONTROLLER IMPORTATION ERROR::${e}`)
            return false
        }
    }

    async import_report_content(){
        const current_module  = this.get_current_module()
        const sub_loc = this.get_current_sub_loc()
        const document = this.get_url_parameters("document")
        if(current_module && document){
            const file_name = this.lower_case(this.replace_chars(document," ","_"))
            try{
                
                const report = await import(`../reports/${current_module}/${file_name}.js`)
                if(report.default){
                    return report.default || false
                }
                console.warn(`APP REPORT CONFIGURATION IMPORTATION ERROR: Failed to find /reports/${current_module}/${file_name}.js file in module reports. ensure report file for ${file_name} matches document!`)
                return false
            }
            catch(e){
                console.error(`APP REPORT CONFIGURATION IMPORTATION ERROR::${e}`)
                return false
            }
        }
        console.warn(`APP REPORT CONFIGURATION IMPORTATION ERROR: Failed to find /reports/${current_module}/${file_name}.js file in module reports. ensure report file for ${file_name} matches document!`)
        return false
    }

    is_report_page(){
        return this.lower_case(this.get_current_loc())?.includes("report")
    }
    
    // get url parameters
    get_url_parameters(key) {
        const urlSearchParams = new URLSearchParams(window.location.search);
        const searchParameters = Object.fromEntries(urlSearchParams.entries());
        if (searchParameters.app && !searchParameters.loc) {
            searchParameters.loc = searchParameters.app
            delete searchParameters.app
        }
        if (searchParameters.page && !searchParameters.type) {
            searchParameters.type = searchParameters.page === "new-form" || searchParameters.page === "new" ? "new" : searchParameters.page
            delete searchParameters.page
        }
        if (searchParameters.content_type && !searchParameters.document) {
            searchParameters.document = searchParameters.content_type
            delete searchParameters.content_type
        }
        if(!this.is_empty_object(searchParameters)){
            if(!key){
                return searchParameters
            }
            else{
                return searchParameters[key] || ""
            }
        }
        return  {}
    }

    // replace url parameters
    set_url_parameters(params = String) {
        window.history.pushState(null, null, `?${params}`)
        return true
    }

    // update url parameters
    update_url_parameters(obj = {} | String) {
        let params = this.get_url_parameters()
        let new_params = '',
            parameter_string = ''
        if (!this.is_object(obj)) {
            new_params = obj
        }
        else {
            if (!this.is_empty_object(obj)) {
                this.get_object_keys(obj).forEach(key => {
                    let mapped_key = key
                    if (key === "app") mapped_key = "loc"
                    if (key === "page") mapped_key = "type"
                    if (key === "content_type") mapped_key = "document"
                    let value = obj[key]
                    if (mapped_key === "type" && value === "new-form") {
                        value = "new"
                    }
                    params[mapped_key] = value;
                })
            }
            params = this.remove_undefined_keys(params)
        }

        if (!this.is_empty_object(params)) {
            this.get_object_keys(params).forEach(key => {
                parameter_string += `${key}=${params[key]}&`;
            })
            if (!this.is_object(obj)) {
                parameter_string += `${new_params} `
            }
        }
        this.set_url_parameters(parameter_string.slice(0, -1))
    }

    remove_url_parameters(keys) {
        let params = this.get_url_parameters();
        let key_list = []
        if (this.is_object(keys)) {
            key_list.push(keys)
        }
        else {
            key_list = keys
        }

        if (!this.is_empty_array(keys)) {
            let parameter_string = ''
            const mapped_keys = keys.map(key => {
                if (key === "app") return "loc"
                if (key === "page") return "type"
                if (key === "content_type") return "document"
                return key
            })
            if (!this.is_empty_object(params)) {
                this.get_object_keys(params).forEach(key => {
                    if (!mapped_keys.includes(key))
                        parameter_string += `${key}=${params[key]}&`;
                })
            }
            this.set_url_parameters(parameter_string.slice(0, -1))
        }
    }
    redirect(module,loc,type,document,params,open_new_doc=false){
        if (type === "new-form") {
            type = "new"
        }
        if(!open_new_doc){
            window.location.href = `/app/${module}/${loc}/?loc=${loc}&type=${type}&document=${document}&${params || ''}`
        }
        else{
            const new_window = window.open(`/app/${module}/${loc}/?loc=${loc}&type=${type}&document=${document}&${params || ''}`)
        }
            
    }

    print_doc(print_format,model,doc,is_download_request=0){
        const new_window = window.open(`/app/core/print_doc/${print_format}/${model}/${doc}/${is_download_request}`, '_blank')
    }
    // get page state wether its still loading or not
    get_page_state() {
        return document.readyState
    }

    // capitalize words
    capitalize(inputString) {
        return inputString.replace(/\b\w/g, function (match) {
            return match.toUpperCase();
        });
    }

    upper_case(value) {
        return value?.toUpperCase()?.trim() || ''
    }
    lower_case(value) {
        return value?.toLowerCase()?.trim() || ''
    }

    replace_chars(text, key, replacement_key = " ") {
        const regex = new RegExp(key, "g");
        return text.replace(regex, replacement_key);
    }

    remove_special_chars(str,only_leave_numbers_and_letters){
        if(only_leave_numbers_and_letters)
            return str.replace(/[^a-zA-Z0-9]/g, '')
        return str.replace(/[^\w\s]/gi, '')
    }

    // get value from field
    get_field_value(field) {
        const field_type = $(field)?.attr("type")
        if(field_type === "expandable"){
            return lite?.expandable_field?.expandable_field_configs[$(field)?.attr("lite-id")]?.value
        }
        return field?.target?.value || $(field)?.val() || $(field)?.attr("value")
    }

    set_field_value(field, value) {
        $(field).val(value)
    }

    get_attribute(el, attribute_name) {
        return $(el).attr(attribute_name)?.trim() || ''
    }

    set_attribute(el, attribute_name, value) {
        return $(el).attr(attribute_name, value)
    }

    get_elements(class_or_id) {
        return $(`.${class_or_id}`) || $(`#${class_or_id}`) || $(`${class_or_id}`) || null
    }
    get_element_by_id(id) {
        if (id)
            return $(`#${id}`) || null
        return null
    }
    get_element_width(element) {
        return $(element)?.width() || 0
    }
    get_element_height(element) {
        return $(element)?.height() || 0
    }
    set_element_width(element, width = 0) {
        return $(element)?.width(width)
    }
    set_element_height(element, height) {
        return $(element)?.height(height)
    }
    get_elements_by_attribute(elements, attribute_key, attribute_value) {
        if (this.is_object(elements) && !this.is_empty_array(elements)) {
            let els = []
            elements.map((_, el) => {
                if ($(el)?.attr(attribute_key)?.toLowerCase()?.trim() === attribute_value?.toLowerCase()?.trim()) {
                    els.push(el)
                }
            })
            return els
        }
        return null
    }
    get_element_tag_name(element) {
        return $(element)?.prop('tagName')?.toLowerCase() || element?.prop('tagName')?.toLowerCase() || null
    }
    get_element_text(element) {
        return $(element)?.text()?.trim() || element.innerText || ''
    }
    set_element_text(element, text) {
        return $(element)?.html(text)
    }
    has_class(element, key) {
        return element?.hasClass(key) || false
    }
    add_class(element, key) {
        return element?.addClass(key)
    }
    has_class(element, key) {
        return element?.hasClass(key)
    }
    remove_class(element, key) {
        return element?.removeClass(key)
    }
    hide(element) {
        element?.addClass('hidden')
    }
    show(element) {
        element?.removeClass('hidden')
    }

    format_amount = (amount, decimals = 4, currency = 'ZMW') => {
        return new Intl.NumberFormat(currency, {
            style: 'currency',
            currency: currency,
            maximumFractionDigits: decimals
        }).format(amount)
    }

    currency = (amount, decimals = 4, currency = 'ZMW') => {
        if((!amount && amount !== 0) || !currency){
            return this.thousand_separator(amount,4)
        }
        return new Intl.NumberFormat(currency, {
            style: 'currency',
            currency: currency,
            maximumFractionDigits: decimals
        }).format(amount)
    }

    thousand_separator = (figure, decimals = 4) => {
        return new Intl.NumberFormat(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(figure);
    }
    string_to_int(str) {
        return parseInt(`${str}`?.replace(/\D/g, '') || 0)
    }

    string_to_float(str) {
        let figure = parseFloat(`${str || 0}`.replace(/[^0-9.]+/g, '') || 0.00)
        return figure
    }
    string_to_currency(str, currency, decimals = 2) {
        return this.format_amount(parseFloat(`${str}`?.replace(/[^\d.]/g, '')), decimals, currency)
    }
    
    fixed_decimals(figure, decimals = 4) {
        return this.string_to_float(parseFloat(`${figure}`).toFixed(decimals == undefined ?2 : decimals))
    }

    init_currency_field_constraints() {
        $('input[type="currency"]').on("keyup", e => {
            var inputValue = $(e).val();
            if (/[^0-9]/.test(inputValue)) {
                $(this).val(inputValue.replace(/[^0-9]/g, ''));
            }
        }).on("change", e => {
            var inputValue = $(e).val();
            if (/[^0-9]/.test(inputValue)) {
                $(this).val(inputValue.replace(/[^0-9]/g, ''));
            }
        })
    }
    get_current_year(){
        return new Date().getFullYear();
    }
    // dates
    convert_date = (date_string) => {
        var today = new Date(date_string).toLocaleDateString('en-GB', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        }).split(' ')
        return `${today[0]} ${today[1]}, ${today[2]}`
    }
    today(numeric = false) {
        if (numeric) {
            var today = new Date().toLocaleDateString('en-GB', {
                day: 'numeric',
                month: 'short',
                year: 'numeric'
            }).split(' ')
            return `${today[0]} ${today[1]}, ${today[2]}`
        }
        return new Date().toISOString().split('T')[0]
    }

    add_days(start_date, days) {
        const datePattern = /^\d{4}-\d{2}-\d{2}$/
        if (!datePattern.test(start_date))
            return false;
        const start = new Date(start_date)
        start.setDate(start.getDate() + days)
        const formated_date = start.toISOString().split('T')[0]
        return formated_date
    }

    first_date_of_current_month() {
        const current_date = new Date()
        const first_date = new Date(current_date.getFullYear(), current_date.getMonth(), 1);
        const res = first_date.toISOString().split('T')[0]
        return res
    }

    last_date_of_current_month() {
        const current_date = new Date()
        const year = current_date.getFullYear();
        const month = current_date.getMonth();
        const last_month = new Date(year, month + 1, 0);
        return last_month.toISOString().split('T')[0];
    }

    get_no_of_months(start_date, end_date) {
        const start = new Date(start_date);
        const end = new Date(end_date);
        const years = end.getFullYear() - start.getFullYear();
        const months = end.getMonth() - start.getMonth();
        if (months < 0) {
            years--;
            months += 12;
        }
        return years * 12 + months;
    }

    time() {
        var currentTime = new Date();
        var hh = currentTime.getHours();
        var mm = currentTime.getMinutes();
        var ss = currentTime.getSeconds();
        return `${hh}:${mm}:${ss}`
    }
    timestamp(){
        const current_date = new Date();
        const iso_string = current_date.toISOString();
        return iso_string
    }

    unique(length = 70) {
        var result = '';
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_';
        var charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }


    // exporting csv and excel data
    export_csv(json_rows, title) {
        if (!this.is_empty_array(json_rows)) {
            if (!this.is_object) {
                console.error("CSV EXPORT ERROR: This functions only accepts an array of objects as data!")
            }
            else {
                const keys = this.get_object_keys(json_rows[0])?.join(',')
                if (keys) {
                    let content = `${keys}\n`;
                    json_rows.map(row => {
                        let row_str = ''
                        this.get_object_keys(row)?.map(cell => {
                            row_str += `${row[cell]},`
                        })
                        content += `${row_str}\n`
                    })
                    // return
                    const blob = new Blob([content], { type: 'text/csv' });
                    const link = document.createElement("a");
                    link.href = window.URL.createObjectURL(blob);
                    link.download = `${title}.csv`;
                    document.body.appendChild(link);
                    link.click();
                }
                else {
                    console.error("CSV EXPORT ERROR: Data provided doess't appear be of an array of objects!")
                }

            }
        }
    }

    export_excel(json_rows, title) {
        const keys = this.get_object_keys(json_rows[0])
        if (keys) {
            let content = [keys];
            json_rows.map(row => {
                let row_arr = []
                this.get_object_keys(row)?.map(cell => {
                    row_arr.push(row[cell])
                })
                content.push(row_arr)
            })
            const ws = XLSX.utils.aoa_to_sheet(content);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, title);
            const blob = new Blob([XLSX.write(wb, { bookType: 'xlsx', type: 'array' })], {
                type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            });
            const link = $('<a>');
            link.attr('href', URL.createObjectURL(blob));
            link.attr('download', `${title}.xlsx`);
            $('body').append(link);
            link[0].click();
            URL.revokeObjectURL(link.attr('href'));
            link.remove();
        }


    }

    dateBackToIntegers (date) {
        var matches = date.split ("-")

        return matches || [];
    }

    parseFormattedDate(inputDate) {
        var regexPatterns = [
            /\b(\d{4})-(\d{2})-(\d{2})\b/,
            /\b(\d{2})-(\d{2})-(\d{4})\b/,
            /\b(\d{4})\/(\d{2})\/(\d{2})\b/,
            /\b(\d{2})\/(\d{2})\/(\d{4})\b/
        ]
        for (var i = 0; i < regexPatterns.length; i++) {
            var match = inputDate.match(regexPatterns[i]);
            if (match) {
                var year = parseInt(match[1], 10);
                var month = parseInt(match[2], 10);
                var day = parseInt(match[3], 10);

                return { year, month, day };
            }
        }
        return null
    }

    
    async count_figure(el, total, is_amount,decimals=0, currency=null) {
        let t = 0;
        const fraction = total / 25;
        let parts = Array.from({ length: 25 }, (_, i) => fraction);
        let interval = setInterval(() => {
            let am = parts.pop();
            t += am ? am : 0;
            let nf = is_amount ? `${this.currency(t,decimals,currency)}` : this.thousand_separator(t,0)
            $(el).html(`${nf}`);

            if (parts.length === 0) {
                if (t.toString().length >= 7 && is_amount) {
                    nf = this.currency(total,decimals,currency)
                    $(el).html(`${nf}`)
                }
                else{
                    this.thousand_separator(total,0)
                }
                clearInterval(interval);
                return true
            }
        }, 40);
    }

    init_password_fields(){
        const pwd_fields = $(".lite-field[type='password']")
        if(this.array_has_data(pwd_fields)){
            $.each(pwd_fields,(_,f)=>{
                $(f).siblings(".hide-show-pwd")?.off("click")?.click(e=>{
                    e.preventDefault()
                    if(this.get_attribute(f,"type") == "password"){
                        $(f).attr("type","text")
                        $(e.currentTarget).find("span").text("visibility_off")
                    }
                    else{
                        $(f).attr("type","password")
                        $(e.currentTarget).find("span").text("visibility")
                    }
                })
            })
        }
    }

    async delay_until(fun = null, timeout = null){
        return await new Promise((resolve, reject) => {
            let time_out = null
            let interval = null
            let result = null
            if(fun){
                interval = setInterval(() => {
                    result = fun()
                    if(result){
                        clearInterval(interval)
                        clearTimeout(time_out)
                        resolve(result)
                    }
                }, 5);
            }
            if (timeout){
                time_out = setTimeout(() => {
                    clearTimeout(time_out);
                    clearInterval(interval)
                    resolve(result)
                }, timeout);
            }
        })
    }

    init_dashboard(remove_loaders=false){
        if(!remove_loaders)
            $(".dashboard-content").addClass("overflow-hidden").append(`
                <div class="dashboard-content-loader absolute bg-white w-full h-full z-[10] bg-white rounded-md flex items-center justify-center top-0 left-0 flex-col">
                    ${ this.generate_loader({loader_type:"dots",size:10, color: "black"})}
                    <small>Loading data</small>
                </div>
            `)
        else{
            setTimeout(() => {
                $(".dashboard-content").find(".dashboard-content-loader").remove()
            }, 1000);
            
        }
    }

    date_format_with_th_or_nd_and_rd (date) {
        return moment(date).format('Do MMM, YYYY')
    }

    convertTimeTo24HourFormat(timeString) {
        const [time, meridiem] = timeString.split(' ')
        let [hours, minutes] = time.split(':')
      
        if (meridiem === 'PM') {
          hours = (parseInt(hours, 10) % 12) + 12
        } else {
          hours = (hours % 12)
        }
      
        hours = hours < 10 ? '0' + hours : hours
        minutes = minutes < 10 ? '0' + minutes : minutes
      
        return `${hours}:${minutes}`
    }

    abbreviate(str){
        let abbr = ""
        const split = str?.split(" ")
        $.each(split,(_,w)=>{
            abbr += w?.charAt(0)
        })
        return this.upper_case(abbr)
    }

    is_number_variable(variable){
        return  /^-?\d+(\.\d+)?$/.test(variable);
    }
    // for a value with comma separators
    is_figure_value(variable) {
        return /^-?(\d{1,3}(,\d{3})*|\d+)(\.\d+)?%?$/.test(variable);
    }
    is_integer_value(variable){
        return  /^-?\d+$/.test(variable);
    }
    sort(list){
        return list.sort()
    }
    ascend(arr, field){
        const sorted_bands = arr.slice().sort((a, b) => a[field] - b[field])
        return sorted_bands
    }

    group(lst, key){
        let grouped = {}
        $.each(lst,(_, v)=>{
            if(grouped[v[key]]){
                grouped[v[key]].push(v)
            }
            else{
                grouped[v[key]] = [v]
            }
        })
        return grouped
    }

    array_to_object(lst, key){
        let obj = {}
        if(lst && this.array_has_data(lst)){
            $.each(lst,(_,ob)=>{
                obj[ob[key]] = ob
            })
        }
        return obj
    }

    weeks_since = (date, weeks) => {
        const today = new Date()
        const delta = Math.floor((today - date) / (7 * 24 * 60 * 60 * 1000))
        return delta >= weeks
    }

    days_since = (date, days) => {
        const today = new Date()
        const delta = Math.floor((today - date) / (24 * 60 * 60 * 1000))
        return delta >= days
    }
    months_since = (date, months) => {
        const today = new Date();
        const todayMonth = today.getFullYear() * 12 + today.getMonth();
        const dateMonth = date.getFullYear() * 12 + date.getMonth();
        return todayMonth - dateMonth >= months;
    }
    years_since = (date, years) => {
        const today = new Date()
        const yearDelta = today.getFullYear() - date.getFullYear()
        const monthDelta = today.getMonth() - date.getMonth()
        return (yearDelta * 12 + monthDelta) >= years * 12
    }
    months_between(dt1, dt2) {
        const monthNames = []
        const [date1, date2] = [dt1, dt2].map(
            (date) => new Date(date)
        );
        const monthDiff = (
            (date2.getFullYear() - date1.getFullYear()) * 12 +
            date2.getMonth() -
            date1.getMonth() -
            (date2.getDate() < date1.getDate() ? 1 : 0)
        );
    
        while (date1 <= date2) {
            monthNames.push(date1.toLocaleString('en-US', { month: 'short' }))
            date1.setMonth(date1.getMonth() + 1);
        }
    
        return {months:monthNames, difference_between_months: monthDiff}
    }

    reverse_object(obj){
        const reversed_object = Object.keys(obj).reverse().reduce((result, key) => {
            result[key] = data[key];
            return result;
        }, {})
        return reversed_object
    }

    percentage_to_decimal(percentage){
        return percentage/100
    }

    remove_last_characters(str="", chars=1){
        return str.substring(0, str.length - chars)
    }
    slice_string(str="",from=0, chars=1){
        return str.slice(from, chars);
    }

    sum(arr){
        return arr.reduce((sum, num) => this.string_to_float(sum) + this.string_to_float(num), 0)
    }

     adjust_hex_color_intensity(hex, percent) {
        if (!/^#[0-9A-F]{6}$/i.test(hex)) {
            console.error("Invalid hex color");
            return hex;
        }
    
        // Remove "#" and convert to RGB
        const r = parseInt(hex.slice(1, 3), 16)
        const g = parseInt(hex.slice(3, 5), 16)
        const b = parseInt(hex.slice(5, 7), 16)
    
        // Adjust color by the percentage (darken or lighten)
        const adjust = (value, percent) => {
            return Math.round(value + (percent / 100) * 255)
        }
    
        // Apply adjustment and clamp between 0 and 255
        const new_r = Math.min(255, Math.max(0, adjust(r, percent)))
        const new_g = Math.min(255, Math.max(0, adjust(g, percent)))
        const new_b = Math.min(255, Math.max(0, adjust(b, percent)))
    
        // Convert back to HEX
        const new_hex = `#${new_r.toString(16).padStart(2, '0')}${new_g.toString(16).padStart(2, '0')}${new_b.toString(16).padStart(2, '0')}`
    
        return new_hex
    }

    group(lst, groupByKey) {
        lst.sort((a, b) => {
            if (a[groupByKey] < b[groupByKey]) return -1;
            if (a[groupByKey] > b[groupByKey]) return 1;
            return 0;
        });

        const grouped = {};
        for (const item of lst) {
            const key = item[groupByKey];
            if (!grouped[key]) {
                grouped[key] = [];
            }
            grouped[key].push(item);
        }

        return this.fromDictToObject ? this.fromDictToObject(grouped) : grouped;
    }

    is_email_value(value){
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    }

    find_personal_email(obj) {
        let found = null;
        const company_email = lite?.defaults?.company?.email || "", user_email = lite?.user?.email || ""
        const search = (node) => {
            if (!node || typeof node !== 'object') return;
            for (const [key, value] of Object.entries(node)) {
                if (!["owner", "modified_by"].includes(key) && typeof value === 'string' && this.is_email_value(value)) {
                    if (value !== company_email && value !== user_email) {
                        found = value;
                        return;
                    }
                }
                if (!["owner", "modified_by"].includes(key) && (key.toLowerCase() === 'email' || typeof value === 'string' && this.is_email_value(value))) {
                    if (value !== company_email && value !== user_email) {
                        found = value;
                        return;
                    }
                }
                if (typeof value === 'object') {
                search(value);
                    if (found) return;
                }
            }
        }
        search(obj);
        if (!found && user_email){
            found = user_email;
        }
        return found || "";
    }
}

export default Utils
