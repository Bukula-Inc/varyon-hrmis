import Listview_Actions from "./listview_init_actions.js"
import { Field_Formatter } from './field_formatter.js';
import Bank_Transaction_Actions from './bank_transaction.js';

export class Global_Action_Inits{
    constructor(){
        this.init_gloabal_actions()
    }
    init_gloabal_actions(){
        this.init_lite_selector_fields()
        this.init_linked_read_only_fields()
        this.init_file_picker()
        this.init_file_content_clearing()
        this.init_file_removal_btn()
        new Field_Formatter()
        // listview default actions
        // new Listview_Actions()
        new Bank_Transaction_Actions()
    }


    // if clinked on the the linked field
    init_linked_read_only_fields(){
        $(document).on("click", '.lite-field[is\-linked\-read\-only="true"]', async (e) => {
            const value = $(e.currentTarget)?.attr("value"), model = $(e.currentTarget)?.attr("for")
            if(value && model){
                const loader_id = lite.alerts.loading_toast({
                    title: `Redirecting...`, 
                    message:`Please wait while the system redirects you.`
                })
                const {status, data, error_message} = await lite.connect.core("get_model_path",{"model": model})
                lite.alerts.destroy_toast(loader_id)
                if(status === lite.status_codes.ok){
                    lite.utils.redirect(data.module, data.loc || data.app, "info", data.document || data.content_type, `doc=${value}`, true)
                }
            }
        });
    }


    init_file_picker(){
        // enable drag and drop file actions
        $(document).on({
            "dragover": function(e) {
              e.preventDefault();
              $(e.currentTarget).addClass('bg-default/40').removeClass('bg-default/10')
            },
            "dragleave": function(e) { $(this).removeClass('bg-default/40').addClass('bg-default/10') },
            "drop": function(e) {
              e.preventDefault();
              const files = e.originalEvent.dataTransfer.files;
              $(this).removeClass('bg-default/40').addClass('bg-default/10');
              if(lite.utils.array_has_data(files)){
                const field = $(e.currentTarget)?.find('input[type="file"]')
                if(field){
                    field?.prop("files", files)
                    lite.lite_file_picker.process_file_content(field)
                }
              }
            }
          }, 
          '.file-drop-zone'
        )
        // enable file picker input change
        $(document).on({ "change": e=>lite.lite_file_picker.process_file_content(e.currentTarget), }, '.lite-field.lite-file-picker')
    }


    init_file_content_clearing(){
        $(document).on({
            "click": e=>{ 
                const field = $(e.currentTarget)?.siblings("label")?.find("input[type='file']")
                if(field){
                    lite.lite_file_picker.clear_input_file_content(field[0])}
                }
        }, 'button.clear-file-input-content')
    }
  
    init_file_removal_btn(){
        $(document).on({
            "click": e=>{ 
                e.preventDefault()
                lite.lite_file_picker.remove_file_from_file_list(e)}
        }, 'button.remove-single-field-file')
    }
    



    // init lite selector
    init_lite_selector_fields(){
        return
        $(document).on("change", 'input.lite-selector.initialized.select-field', async (e) => {
            const field = $(e.currentTarget), value = field?.val(), model = field?.attr("for")
            if(value && model){
                await lite.lite_selector.handle_fetch_from(e, value)
                if (lite.utils.array_has_data(lite.lite_selector.on_select_change)) {
                    const attrs = field[0]?.attributes
                    let obj = {
                        value_id: lite.utils.string_to_int(field.attr("value-id")) || '',
                        value: value,
                        wrapper: field?.parents(".lite-selector"),
                        field: e.currentTarget
                    }
                    lite.utils.array_has_data(attrs) && $.each(attrs, (_, att) => obj[att.name] = att.value)
                    $.each(lite.lite_selector.on_select_change, (_, f) => {
                        console.log(f.fun.name)
                        // f?.fun(obj, f?.cls)
                    })
                }
            }
        });
        // init selection change
        this.init_lite_selector_option_action()
    }

    // when lite selector option is clicked
    init_lite_selector_option_action(){
        $(document).on("click", '.lite-selector .select-options-list li.option', async (e) => {
            const value = $(e?.currentTarget)?.attr("value") || "", value_id = $(e?.currentTarget)?.attr("id") || ""
            const field = $(e.currentTarget)?.parents(".lite-selector").find("input.select-field")
            if(lite.utils.array_has_data(field) && value && value !== field?.val()){
                field?.val(value)?.attr("value-id", value_id)?.trigger("change")
                lite.lite_selector.create_check(e.currentTarget)
            }
            
        });
    }
    
}
