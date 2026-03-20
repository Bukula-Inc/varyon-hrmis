export default class Validator {
    constructor(config) {
        this.code_editor = config.code_editor
        this.form = null
        this.form_controller = null
        this.error_wrapper = '.field-error-wrapper'
        this.error_text = '.error-text'
        this.values = []
        this.child_table_values = []
        this.has_passed = false
    }
    validate(form_controller, return_if_validation_failed = false, is_saving_or_updating=false) {
        this.form_controller = form_controller
        return this.#get_fields(return_if_validation_failed, return_if_validation_failed, is_saving_or_updating)
    }

    #clean_value(val, field){
        if(lite.utils.is_figure_value(val) && ["float", "currency", "number"].includes($(field)?.attr("fieldtype")) || ($(field)?.attr("fieldtype")== "read-only" && $(field)?.find("div.lite-field")?.attr("is-figure") == "true")){
            return lite.utils.string_to_float(val)
        }
        else if(lite.utils.is_integer_value(val) && ["float","int", "currency", "number"].includes($(field)?.attr("fieldtype")) || ($(field)?.attr("fieldtype")== "read-only" && $(field)?.find("div.lite-field")?.attr("is-figure") == "true")){
            return lite.utils.string_to_int(val)
        }
        return val
    }

    #get_fields(return_if_validation_failed, ignore_validation = false, is_saving_or_updating) {
        this.file_content = { has_files:false, has_table_files:false, form_files:[], table_files:{}, processed_files: {}, }
        const fields = this.form_controller.$form_fields.find(`${this.form_controller.form_field_class_name}:not(.table-search-field)`)
        if (!lite.utils.is_empty_array(fields)) {
            this.values = {}
            this.child_table_values = []
            this.has_passed = true
            $.each(fields, (_, f) => {
                const d = this.#get_field_data(f, ignore_validation, is_saving_or_updating)
                if(d.field && $(d.field)?.attr("type") == "file"){
                    const file_value = lite.lite_file_picker.get_file_content(d.field)
                    if(lite.utils.object_has_data(file_value)){
                        d.value = file_value
                    }
                }
                if ((!d.value || (!`${d.value}`.trim() && d.value !== `${0}`)) && d.rqd && !ignore_validation && !d.is_hidden) {
                    this.has_passed = false
                    this.#show_hide_error(f, true)
                    lite.utils.set_element_text($(f).find(this.error_text), 'This Field Is Required!')
                    this.#enable_field_change_listener(f)
                }
                else {
                    this.values[d.fieldname] = this.#clean_value(d.value, f )
                }
            })
            lite.lite_file_picker.lite_form_files.table_files = this.file_content.table_files
            if (this.has_passed || return_if_validation_failed)
                if (!lite.utils.is_empty_array(this.values))
                    return {
                        validation_status: this.has_passed,
                        data: {
                            values: this.values,
                            file_content: this.file_content
                        }
                    }
            return {
                validation_status: this.has_passed,
                data: []
            }
        }
        else {
            return false
        }
    }

    #get_field_data(field, ignore_validation = false, is_saving_or_updating) {
        let value = ''
        const direct_fields = ['text', 'int', 'date', "time", "float", "rate", 'barcode', "hidden", "currency", "percentage","password","color", "image"]
        const field_type = lite.utils.get_attribute($(field), 'fieldtype')
        const is_hidden = $(field).hasClass('hidden')
        let fieldname = lite.utils.get_attribute($(field).find('input:not(.table-search-field)'), 'fieldname') || lite.utils.get_attribute($(field), 'fieldname') || lite.utils.get_attribute($(field).find('.lite-field:not(.table-search-field)'), 'fieldname')
        if (direct_fields.includes(field_type)) {
            value = this.#clean_value(lite.utils.get_field_value($(field).find('input')) || lite.utils.get_field_value($(field)) || lite.utils.get_attribute(field, "value"), field)
        }
        else if(field_type == "longtext"){
            value = lite.utils.get_field_value($(field).find('textarea'))
        }
        else if (['link', 'select'].includes(field_type)) {
            value = lite.utils.get_field_value($(field).find('input')) || lite.utils.get_attribute(field, "value") || null
        }
        else if (field_type === 'check') {
            value = ($(field).find('input').prop('checked') ? 1 : 0) || 0
        }
        else if (field_type === 'read-only') {
            value = lite.utils.get_attribute($(field).find('.lite-field'), 'value')
        }
        else if (field_type === 'switch') {
            value = lite.utils.get_attribute($(field).find('.lite-field'), 'value')
        }
        else if (field_type === 'switch') {
            value = lite.utils.get_attribute($(field).find('.lite-field'), 'value')
        }
        else if(field_type === "code"){
            const id = lite.utils.get_attribute($(field).find(".lite-code-editor"),"lite-id")
            if(id){
                value = lite.code_editor.get_editor_code(id) || ''
            }
        }
        else if(field_type === "rich"){
            value = lite.rich_editor.get_content($(field).find("textarea")[0])
        }
        else if(field_type === "expandable"){
            // value = lite.expandable_field
        }
        else if(field_type === "file"){
            this.file_content.has_files = true
            const file_field = $(field).find(".lite-file-picker")[0]
            let file_content = lite.lite_file_picker.get_file_content(file_field) || lite.utils.get_attribute(file_field, "value")?.trim()
            if(!file_content){
                console.log("THERE ARE NO FILES SELECTED!")
            }
            else if(is_saving_or_updating){
                this.file_content.processed_files[fieldname] = file_content.field_id
            }
            else{
                file_content.fieldname = fieldname
                this.file_content.form_files.push(fieldname)
                value = file_content
            }
        }

        else if (field_type === 'table') {
            const table_field_name = $(field)?.attr("fieldname"), rows = $(field).find('.tbody .table-row')
            const table_data = this.form_controller.child_table_data[table_field_name]
            if(lite.utils.array_has_data(table_data)){
                value = table_data
            }
            // if(lite.utils.is_empty_array(table_data)){
            //     console.warn(`Child table ${table_field_name} does not have any data`)
            // }
            // else{
            //     value = table_data
            // }
            // if (lite.utils.array_has_data(rows)) {
            //     let has_rows_passed = true
            //     let table_rows = []
            //     $.each(rows, (_, r) => {
            //         let row_obj = {row_id:$(r)?.attr("id"), row_idx:_}
            //         if (has_rows_passed) {
            //             const cells = $(r).find('.tc')
            //             if (!lite.utils.is_empty_array(cells)) {
            //                 $.each(cells, (_, c) => {
            //                     const
            //                         lite_field = $(c).find('.lite-field'),
            //                         is_required = lite.utils.get_attribute(lite_field, 'is_required'),
            //                         is_hidden = $(lite_field).hasClass('hidden'),
            //                         fieldname = lite.utils.get_attribute(lite_field, 'fieldname'),
            //                         fieldtype = lite.utils.get_attribute(lite_field, 'type')
            //                     if (direct_fields.includes(fieldtype)) {
            //                         row_obj[fieldname] = lite.utils.get_field_value(lite_field)
            //                     }
            //                     else if(fieldtype == "longtext"){
            //                         row_obj[fieldname] = lite.utils.get_field_value($(c).find('textarea'))
            //                     }
            //                     else if (fieldtype === 'checkbox') {
            //                         row_obj[fieldname] = ($(c).find('input').prop('checked') ? 1 : 0) || 0
            //                     }
            //                     else if (fieldtype === 'read-only') {
            //                         row_obj[fieldname] = lite.utils.get_attribute(lite_field, 'value') || lite.utils.get_attribute(field, "value")
            //                     }
            //                     else if (fieldtype === 'switch') {
            //                         row_obj[fieldname] = lite.utils.get_attribute(lite_field, 'value') || lite.utils.get_attribute(field, "value")
            //                     }
            //                     else if (['link', 'select'].includes(fieldtype)) {
            //                         row_obj[fieldname] = lite.utils.get_field_value(lite_field[1]) /*|| lite.utils.get_attribute(field, "value")*/  || null
            //                     }
            //                     else if(fieldtype === "expandable"){
            //                         const xvalue = lite.expandable_field.get_value($(c).find('.lite-field.expandable-field'))
            //                         row_obj[fieldname] = xvalue
            //                     }
            //                     else if(fieldtype === "file"){
            //                         this.file_content.has_table_files = true
            //                         let file_content = lite.lite_file_picker.get_file_content(lite_field)
            //                         const field_lite_id = $(lite_field)?.attr("lite-id")
            //                         const field_id = $(lite_field)?.attr("id")
            //                         if(!file_content){
            //                             this.#show_hide_error(field,true)
            //                         }
            //                         else{
            //                             // add field id to the variable fore reference
            //                             row_obj[fieldname] = field_lite_id
            //                         }
            //                         // list the field in table fields array
            //                         if(!this.file_content.table_files[table_field_name]){
            //                             this.file_content.table_files[table_field_name] = [fieldname]
            //                         }
            //                         else{
            //                             if(!this.file_content.table_files[table_field_name]?.includes(fieldname)){
            //                                 this.file_content.table_files[table_field_name].push(fieldname)
            //                             }
            //                         }
            //                     }
            //                     if (!row_obj[fieldname] && is_required === 'true' && !ignore_validation && !is_hidden) {
            //                         has_rows_passed = false
            //                         lite_field.parents('.tc').addClass('border-red-400 border-[1.5px] z-3')
            //                         lite.alerts.toast({
            //                             toast_type: 404,
            //                             title: `Value Missing`,
            //                             message: `${lite.utils.capitalize(lite.utils.replace_chars(fieldname, "_"))} value required!`,
            //                         })
            //                     }
            //                     else {
            //                         lite_field.parents('.tc').removeClass('border-red-400 border-[1.5px] z-3')
            //                     }
            //                     if(["float","percentage","figure", "currency"].includes(lite.utils.lower_case(fieldtype))){
            //                         const v = lite.utils.string_to_float(row_obj[fieldname]) || 0.00
            //                         row_obj[fieldname] = v
            //                     }
            //                     if(lite.utils.lower_case(fieldtype) === "int"){
            //                         const v = lite.utils.string_to_int(row_obj[fieldname]) || 0
            //                         row_obj[fieldname] = v
            //                     }
            //                 })
            //             }
            //         }
            //         const doc_id = lite.utils.get_attribute(r, "doc-id")
            //         row_obj.id = doc_id !== "null" ? doc_id : null
            //         table_rows.push(row_obj)
            //     })
            //     value = has_rows_passed ? table_rows : null
            // }
            // else if (lite.utils.get_attribute(field, 'is_required')) {
            //     lite.utils.add_class($(field).find('.table'), 'border-red-600')
            //     value = null
            // }
        }
        
        if(["float","percentage","figure", "currency"].includes(lite.utils.lower_case(field_type))){
            value = lite.utils.string_to_float(value) || 0.00
        }
        if(lite.utils.lower_case(field_type) === "int"){
            value = lite.utils.string_to_int(value) || 0
        }
        if(!fieldname){
            fieldname  = lite.utils.get_attribute($(field).find('input'), 'fieldname') || lite.utils.get_attribute($(field), 'fieldname') || lite.utils.get_attribute($(field).find('.lite-field'), 'fieldname')
        }
        return {
            field: $(field)?.find('input') || $(field)?.find('textarea'),
            fieldname: fieldname,
            field_type: field_type,
            is_hidden: is_hidden,
            value: value,
            rqd: (lite.utils.get_attribute($(field).find('input'), 'is_required') === 'true' || lite.utils.get_attribute($(field), 'is_required') === 'true') ? true : false,
        }
    }
    #enable_field_change_listener(field) {
        $(field).find('input').on('change', (e) => {
            this.#show_hide_error(field, lite.utils.get_field_value(e.target)?.trim() ? false : true)
        })
        $(field).find('input').on('keyup', (e) => {
            this.#show_hide_error(field, lite.utils.get_field_value(e.target)?.trim() ? false : true)
        })
    }
    #show_hide_error(field, show = false) {
        if (show) {
            lite.utils.show($(field).find(this.error_wrapper))
            $(field).focus()
        }
        else {
            lite.utils.hide($(field).find(this.error_wrapper))
        }
    }
}