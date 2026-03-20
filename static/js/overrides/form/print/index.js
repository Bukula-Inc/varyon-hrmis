import { 
    on_print_configuration_load
} from "./core.js";

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