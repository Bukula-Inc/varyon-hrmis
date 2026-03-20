import Utils from "../utils/utils.js"
const utils = new Utils ()
export default {
    get_url: '/api/get-data',
    post_url: '/api/post-data',
}

// Default API Configurations
const vars = {
    local: '/api',
    server: '/api'
}
export let API_CONFIG = {
    request_type: 'GET',
    base_endpoint: vars.local,
    request_endpoint: '',
    headers: {
        "Authorization": 'Bearer login',
        model: null, //eg Account
        'page_size': 1000000**2,
        current_page: 1,
        xfunction: null, //eg test
        filters: null, //eg {"modified_by": 1}
        fields: null, //eg ["name","docstatus"]
        'get_single': null, //eg Probase Group
        'order-by': null, //eg ["creation_time","name","-owner"]
    },
    body: null,
    request_types: {
        get: 'GET',
        post: 'POST',
        patch: 'PATCH',
        put: 'PUT',
        delete: 'DELETE',
    },
    status_codes: {
        ok: 200,
        created: 201,
        no_content: 204,
        moved_permanently: 301,
        found: 302,
        not_modified: 304,
        bad_request: 400,
        unauthorized: 401,
        forbidden: 403,
        not_found: 404,
        method_not_allowed: 405,
        unprocessable_entity: 422,
        internal_server_error: 500,
        not_implemented: 501,
        bad_request: 502,
        service_unavailable: 503
    },
    endpoint_extensions: {
        authenticate: '/authenticate/',
        request_password_reset_validation: '/request-password-reset-validation/',
        request_password_reset: '/request-password-reset/',
        get: '/get-data/',
        get_doc_value: '/get-doc-value/',
        report: '/reports/',
        form_fields: '/get-form-fields/',
        download_report: '/download-report/',
        post: '/post-data/',
        upload: '/upload/',
        extract_doc_data: '/extract-doc-data/',
        patch: '/patch-data/',
        submit: '/submit-doc/',
        delete: '/delete-doc/',
        cancel: '/cancel-doc/',
        x_fetch: '/x-fetch/',
        dashboard: '/dashboard/',
        x_post: '/x-post/',
        core: '/core/',
        export_data: '/export-data/',
        workflow_action: '/workflow-action/',

        // portal
        portal_request_otp: '/portal/request-otp',
        portal_validate_otp: '/portal/validate-otp',
        portal_get: '/portal/get',
        portal_post: '/portal/post',


        // services
        new_tenant: '/services/new-tenant/',
    },
}

export const GetBaseEndpoint = () => {
    return API_CONFIG.base_endpoint.split('/api')[0]
}

// call this function to configure your API Request
export const API_SETUP = (params) => {
    const { request_type, headers, body, endpoint_extension } = params
    API_CONFIG.request_endpoint = endpoint_extension
    API_CONFIG.request_type = API_CONFIG.request_types[request_type.toLowerCase().trim()]
    API_CONFIG.headers = headers || ''
    API_CONFIG.body = body || ''
    return API_CONFIG
}