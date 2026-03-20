import {  before_role_save_ } from "../../../modules/core/role/index.js";
import { 
    // for currency
    on_exchange_rate_change,
    on_print_configuration_load,
    extend_data_importation_fields,
    on_file_change,

    on_user_email_changed,
    on_user_loaded,
    calculate_shares,
    update_form_customization,
} from "./core.js";

export const data_importation = {
    form_fields_extender:extend_data_importation_fields,
    on_field_change: {
        file_url: [on_file_change],
    },
}

export const exchange_rate = {
    on_field_change: {
        rate: [on_exchange_rate_change],
    },
}



export const print_configuration = {
    on_load: [],
    on_field_change: {
        app_model: [on_print_configuration_load],
    },
    on_row_select: [],
    on_row_add: [],
    on_row_remove: [],
    before_save: [],
    after_save: [],
    before_update: [],
    after_update: [],
    before_submit: [],
    after_submit: [],
    before_cancel: [],
    after_cancel: [],
}


export const user = {
    on_load: [on_user_loaded],
    on_field_change: {
        email: [on_user_email_changed],
    }
}


// export const workflow = {
//     on_field_change: {
//         is_role_based_workflow: [on_is_role_based_change],
//     }
// }


export const role = {
    custom_validation: [before_role_save_],
    // on_field_change: {
    //     role_module: [on_role_module_change],
    //     permit_all_components: [on_role_module_change],
    // }
}


export const shares = {
    on_field_change: {
        total_shares: [calculate_shares],
        shareholder_total_shares: [calculate_shares],
    }
}




export const form_customization = {
    on_field_change: {
        name: [update_form_customization]
    }
}