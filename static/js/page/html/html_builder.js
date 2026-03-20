export default class HTML_Builder {
    constructor() {
        this.setup = null
    }
    build_form_field(params, setup) {
        const {workflow, fieldname} = params
        this.numeric_fields_types = ["int", "currency", "percentage", "float", "rate"]
        if (setup) {
            this.setup = setup
        }
        const {
            id = '',
            fieldlabel = '',
            placeholder = '',
            fieldtype = 'text',
            hidden = false,
            required = true,
            label_class = 'text-12',
            wrapper_class = 'mt-1',
            columns = 1,
            read_only = false
        } = params
        let field = ''
        this.#validate_params(params)
        switch (fieldtype) {
            case 'text':
                field = this.input_text_field(params)
                break;
            case 'password':
                field = this.input_password_field(params)
                break;
            case 'color':
                field = this.input_color_field(params)
                break;
            case 'longtext':
                field = this.input_longtext_field(params)
                break;
            case 'rich':
                field = this.input_rich_field(params)
                break;
            case 'expandable':
                field = this.expandable_field(params)
                break;
            case 'code':
                field = this.input_code_field(params)
                break;
            case 'int':
                field = this.input_int_field(params)
                break;
            case 'float':
                field = this.input_float_field(params)
                break;
            case 'rate':
                field = this.input_rate_field(params)
                break;
            case 'currency':
                field = this.input_currency_field(params)
                break;
            case 'percentage':
                field = this.input_percentage_field(params)
                break;
            case 'check':
                field = this.input_check_field(params)
                break;
            case 'pure-check':
                return this.input_pure_check_field(params)
            case 'date':
                field = this.input_date_field(params)
                break;
            case 'year':
                field = this.year_field(params)
                break;
            case 'time':
                field = this.input_time_field(params)
                break;
            case 'select':
                field = this.select_field(params)
                break;
            case 'link':
                field = this.link_field(params)
                break;
            case 'file':
                field = this.file_field(params)
                break;
            case 'read-only':
                field = this.read_only_field(params)
                break;
            case 'barcode':
                field = this.barcode(params)
                break;
            case 'button':
                field = this.button_field(params)
                break;
            case 'image':
                field = this.image(params)
                break;
            case 'table':
                return this.create_child_table(params)
                break;
            case 'section-break':
                return this.section_break(params)
                break;
            case 'column-break':
                return this.column_break(params)
            case 'status':
                return this.status_field(params)
            case 'switch':
                field = this.input_switch_field(params)
                break;
            default:
                field = this.input_text_field(params)
                break;
        }
        if (params?.omitlabels) {
            if (params?.read_only === true || workflow?.allow_edit === false)
                return this.read_only_field(params)
            if(params.fieldtype === "check" && params.istablefield)
                return this.input_pure_check_field(params)
            return field
        }
        return `
                <div 
                    for="${id}" 
                    fieldtype="${read_only || workflow?.allow_edit === false ? 'read-only' : fieldtype}" 
                    value="${(params?.fieldtype !== 'code' && params?.fieldtype !== 'rich') ? params?.value : ''}" 
                    prev-val="${(params?.fieldtype !== 'code' && params?.fieldtype !== 'rich') ? params?.value : ''}" 
                    class="form-field field-wrapper  intro-x ${wrapper_class || ""} col-span-${columns} ${hidden ? 'hidden' : ''}"
                    ${params.fieldtype === "date" ? 'style="z-index:100"' : ""}
                    ${params.fieldtype === "link" ? 'for="'+params?.model+'"' : ''}
                >
                    <label class="form-label ${label_class || ""} text-slate-500 flex items-center justify-start text-13 w-[max-content] rounded-md">
                        ${fieldlabel || placeholder}
                        ${required ? '<span class="text-danger ml-2">*</span>' : ''}
                    </label>
                    ${![1,2,3].includes(params?.docstatus) &&  workflow?.allow_edit !== false ? field : (params?.editableonsubmit === true ? field : this.read_only_field(params))}
                    <div class="field-error-wrapper flex items-center justify-start mt-1 hidden">
                        <span class="material-symbols-outlined mr-2 text-11 text-danger">warning</span>
                        <span class="text-11 error-text text-danger"></span>
                    </div>
                </div>
            `
    }
    #validate_params({ id, fieldlabel, fieldname }) {
        if (!id) throw new Error(`id not provided for the form field ${fieldname || fieldlabel}`)
        // if (!fieldname) throw new Error(`fieldname not provided for the form field ${fieldname || fieldlabel}`)
    }

    input_text_field(opts) {
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="text" 
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control' : 'table-field'} w-full" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    input_switch_field(opts) {
        const v = opts?.value || 0
        return `
            <div type="switch" id="${opts?.id || ''}" fieldname="${opts?.fieldname}" ${opts?.attributes || ""} class="lite-field w-full flex items-center  ${opts?.omitlabels ? "justify-center" : "justify-between"} ${opts?.classnames || ""}" value="${v}" >
                ${!opts?.omitlabels ? `<span class="text-11">${opts?.fieldlabel}</span>` : ""}
                <div class="permission ${v === 1 ? "bg-default" :"bg-gray-200"} flex items-center ${opts?.omitlabels ? "justify-center" : "justify-between"} relative rounded-full h-[5px]  w-[40px] switch-toggler-wrapper transition duration-1000">
                    <div class="switch-toggler absolute w-[${opts?.size||"17"}px] h-[${opts?.size||"17"}px] rounded-full shadow-md transition duration-1000 ${v ==1 ? "left-[70%] bg-default border" : "left-0 bg-gray-400"} cursor-pointer" style="transition:.6s"></div>
                </div>
            </div>
        `
    }
    input_password_field(opts) {
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="password"
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control' : 'table-field'} w-full" 
                placeholder="${opts?.placeholder}"
            >
            <button class="hide-show-pwd h-[34%] absolute z-2 right-2 top-[33px] bg-gray-100 text-gray-500 shadow-md px-3 rounded-md flex items-center justify-center transition duration-3 hover:translate-x-[-3%]">
                <span class="material-symbols-outlined text-18"> visibility</span>
            </button>
        `
    }
    input_color_field(opts) {
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="color" 
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control' : 'table-field'} w-full" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    input_longtext_field(opts) {
        return `
            <textarea 
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="longtext" 
                ${opts?.value && opts?.value != "null" ? 'value="' + opts.value || "" + '"' : ''}
                ${opts?.value && opts?.value != "null" ? 'prev-val="' + opts.value || "" + '"' : ''}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                rows="1"
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 focus:outline-none resize-none ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control border' : 'table-field'} w-ful px-3" 
                placeholder="${opts?.placeholder}"
            >${opts?.value  && opts?.value != "null" ? opts?.value : ""}</textarea>
        `
    }
    input_rich_field(opts) {
        const uniq = opts?.liteid || lite.utils.unique(60)
        if(opts?.value){
            lite.rich_editor_values[uniq] = {field:null, value:opts?.value}
        }
        return `
            <textarea 
                id="${uniq}"
                lite-id="${uniq}"
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="rich" 
                value=""
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                height="${opts?.height || 50}"
                rows="1"
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 focus:outline-none resize-none ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control border' : 'table-field'} w-ful px-3" 
                placeholder="${opts?.placeholder}"
            ></textarea>
        `
    }

    expandable_field(opts) {
        const uniq = opts?.liteid || lite.utils.unique(60)
        if(opts?.value){
            lite.rich_editor_values[uniq] = {field:null, value:opts?.value || ''}
            lite.expandable_field.expandable_field_configs[uniq] = {id:uniq, field:null, value:opts?.value || ''}
        }
        return `
            <div class="w-full h-full relative h-[35px] overflow-hidden overflow-y-auto bg-white">
                <div 
                    id="${uniq}"
                    lite-id="${uniq}"
                    always-fetch="${opts?.alwaysfetch || true}"
                    is_required="${opts?.required || false}" 
                    type="expandable"
                    fieldname="${opts?.fieldname}"
                    ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                    ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                    height="${opts?.height || 50}"
                    rows="1"
                    ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                    class="lite-field expandable-field text-13 ${opts?.classnames || ''} ${opts?.hidden ? 'hidden' : ''} cursor-pointer w-full h-[30px] relatives ${!opts.istablefield ? 'form-control border' : 'table-field'} w-ful px-3" 
                    placeholder="${opts?.placeholder}"
                >
                    ${opts?.value || opts?.default || ""}
                </div>
                <div class="absolute right-2 top-2"><span class="material-symbols-outlined">expand_content</span></div>
            </div>
        `
    }


    input_int_field(opts) {
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="int"
                format-figure="${opts?.format_figure}"
                ${opts?.value || opts?.value == 0 ? 'value="' + opts.value + '"' : 0}
                ${opts?.value || opts?.value == 0 ? 'prev-val="' + opts.value + '"' : 0}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 h-[37px] focus:outline-none ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control border' : 'table-field border-none outline-none'} w-full  px-3" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    
    input_float_field(opts) {
        let val = opts.value || "0.00"
        if(opts?.format_figure !== false){
            val = lite.utils.thousand_separator(opts.value,2)
        }
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="float"
                ${opts?.value ? 'value="' + val + '"' : ''}
                ${opts?.value ? 'prev-val="' + val + '"' : ''}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 h-[37px] focus:outline-none ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control border' : 'table-field border-none outline-none'} w-full  px-3" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    input_rate_field(opts) {
        let val = opts.value || 1
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="rate"
                ${opts?.value ? 'value="' + val + '"' : ''}
                ${opts?.value ? 'prev-val="' + val + '"' : ''}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 h-[37px] focus:outline-none ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control border' : 'table-field border-none outline-none'} w-full  px-3" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    input_currency_field(opts) {
        let val = opts.value || "0.00"
        if(opts?.format_figure !== false){
            val = lite.utils.thousand_separator(opts.value,2)
        }
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="currency"
                ${opts?.value ? 'value="' + val + '"' : ''}
                ${opts?.value ? 'prev-val="' + val + '"' : ''}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 h-[37px] focus:outline-none ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control border' : 'table-field border-none outline-none'}  px-3 font-semibold text-end" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    input_percentage_field(opts) {
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="percentage"
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 h-[37px] focus:outline-none ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control border' : 'table-field border-none outline-none'}  px-3 font-semibold text-end" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    input_check_field(opts) {
        return `
            <div class="w-full flex items-center justify-start mb-6">
                <input 
                    autocomplete="off"
                    id="${opts?.id}" 
                    always-fetch="${opts?.alwaysfetch || true}"
                    is_required="${opts?.required || false}" 
                    fieldname="${opts?.fieldname}"
                    ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                    ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                    ${opts?.value ? 'value="' + opts.value + '"' : 0}
                    ${opts?.value ? 'prev-val="' + opts.value + '"' : 0}
                    ${opts?.value && opts?.value == 1 ? 'checked' : 0}
                    ${opts?.disabled ? "disabled" : ""}
                    type="checkbox" 
                    ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                    class="lite-field text-13 shadow-none form-check-input list-check appearance-none border border-default checked:bg-default hover:bg-default active:bg-default checked:border-default focus:outline-default/50 w-[25px] h-[25px] accent-default mr-2"
                >
                <label for="${opts?.id}" class="cursor-pointer transition duration-500 hover:translate-x-[-3%]">${opts?.fieldlabel}</label>
            </div>
        `
    }

    input_pure_check_field(opts) {
        return `
            <div class="w-full flex items-center justify-center h-full">
                <input 
                    autocomplete="off"
                    id="${opts?.id}" 
                    always-fetch="${opts?.alwaysfetch || true}"
                    is_required="${opts?.required || false}" 
                    fieldname="${opts?.fieldname}"
                    ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                    ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                    ${opts?.value == 1 ? 'checked' : ''}
                    ${opts?.disabled ? "disabled" : ""}
                    type="checkbox" 
                    ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                    class="lite-field text-13 shadow-none form-check-input list-check appearance-none border border-default checked:bg-default hover:bg-default active:bg-default checked:border-default focus:outline-default/50 w-[24px] h-[24px] accent-default mr-2"
                >
            </div>
        `
    }
    input_date_field(opts) {
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="text" 
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                is-date-field="true"
                double-picker="${opts?.doublepicker || false}"
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control' : 'table-field'} w-full" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    year_field(opts) {
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="text" 
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                is-year-field="true"
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control' : 'table-field'} w-full" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    input_time_field(opts) {
        return `
            <input 
                autocomplete="off"
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                is_required="${opts?.required || false}" 
                type="text" 
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                is-time-field="true"
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full min-h-[45px] ${!opts.istablefield ? 'form-control' : 'table-field'} w-full" 
                placeholder="${opts?.placeholder}"
            >
        `
    }
    select_field(opts) {
        let options = ''
        if (!lite.utils.is_empty_array(opts?.options)) {
            $.each(opts?.options, (_, o) => {
                options += `<option ${o?.value && o.value === o ? 'selected' : ''} value="${o}">${o}</option>`
            })
        }
        return `
            <select 
                type="select" 
                id="${opts?.id}"
                always-fetch="${opts?.alwaysfetch || true}"
                fieldname="${opts?.fieldname}" 
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                is_required="${opts?.required || false}"
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                class="lite-selector lite-field text-13 min-h-[45px] ${opts?.classnames || ''} ${opts.istablefield ? 'table-field' : ''} ${opts?.hidden ? 'hidden' : ''} border rounded-md px-3 w-full" 
                placeholder="${opts?.placeholder}">
                ${options}
            </select>
        `
    }

    link_field(opts) {
        return `
            <select 
                type="link" 
                for="${opts?.model}" 
                linkfield="${opts?.linkfield || 'name'}"
                id="${opts?.id}"
                always-fetch="${opts?.alwaysfetch || true}"
                fieldname="${opts?.fieldname}" 
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                is_required="${opts?.required || false || false}"
                ${opts?.value ? 'value="' + opts.value + '"' : ''}
                ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                filters='${opts?.filters ? JSON.stringify(opts?.filters) : null}'
                descriptions='${opts?.descriptions ? JSON.stringify(opts?.descriptions) : JSON.stringify([])}'
                prefix='${opts?.prefix ? opts?.prefix : ""}'
                postfix='${opts?.postfix ? opts?.postfix : ""}'
                class="lite-selector lite-field text-13 ${opts?.classnames || ''} ${opts.istablefield ? 'table-field' : ''} ${opts?.hidden ? 'hidden' : ''} border rounded-md px-3 w-full" 
                placeholder="${opts?.placeholder}">
            </select>
        `
    }
    file_field(opts) {
        const uniq = lite.utils.unique(100)
        if(opts?.placeholder){
            opts.placeholder += '/Drop File Here'
        }
        let display_value = ""
        const vl = opts?.value || opts?.default || ''
        if(vl){
            let files = vl.split(" &== ")
            if(lite.utils.array_has_data(files)){
                $.each(files,(_,file)=>{
                    display_value += lite.lite_file_picker.create_file_attachment_option(file?.split("/").pop(),files?.length || 1,_,file,true,true, !opts?.is_submitted)
                })
            }
            if(!display_value)
                opts?.placeholder || 'Select File'
        }
        return `
            <div multiple="${opts?.multiple || false}" class="file-drop-zone relative flex items-center cursor-pointer min-h-[${opts?.omitlabels ? 37 : 100}px] max-h-[${opts?.omitlabels ? "37px" : "max-content"}] ${!opts?.omitlabels ? "bg-default/10 flex-col justify-center border border-dotted border-default/50" : "justify-between"} rounded-md px-3 py-1 w-full text-13 form-control transition duration-1000">
                <label for="${uniq}" class="flex items-center justify-center cursor-pointer  w-full h-full truncate overflow-ellipsis text-13">
                    <div class="flex items-center w-full  ${!opts?.omitlabels ? 'flex-col justify-around': 'justify-between'}">
                        ${
                            !opts?.is_submitted ? `
                                <input 
                                    autocomplete="off"
                                    oldid="${opts?.id}" 
                                    id="${uniq}" 
                                    always-fetch="${opts?.alwaysfetch || true}"
                                    is_required="${opts?.required || false}" 
                                    type="file" 
                                    ${opts?.value ? 'value="' + opts.value + '"' : ''}
                                    ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                                    fieldname="${opts?.fieldname}"
                                    ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                                    ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                                    ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                                    class="lite-field lite-file-picker hidden text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''} ${!opts.istablefield ? 'form-control' : 'table-field'} w-full " 
                                    placeholder="${opts?.placeholder}"
                                    max-length="${opts?.max || 5}"
                                    ${opts?.multiple ? "multiple": ''}
                                >
                            `: ''
                        }
                        ${opts?.omitlabels ? (!opts?.is_submitted ? '<span class="material-symbols-outlined mr-2 text-17">attachment</span>':'') : (!opts?.is_submitted ?'<span class="material-symbols-outlined mr-2 text-30 mb-3 text-gray-400">place_item</span>':'')}
                        <div class="w-full flex items-center justify-center"></div>
                        <div arial-title="${opts?.placeholder || ''}" class="file-title w-full text-center max-h-[260px] overflow-y-auto pt-2" placeholder="${opts?.placeholder}">
                            ${display_value || opts?.placeholder}
                        </div>
                    </div>
                </label>
                ${
                    !opts?.is_submitted ? `
                        <button for="${opts?.id}" class="clear-file-input-content text-red-600 cursor-pointer w-[30px] flex items-center justify-center ${!opts?.omitlabels ? 'absolute top-0 right-0 h-[30px]': 'h-full'}">
                            <span class="material-symbols-outlined text-18">remove_selection</span>
                        </button>
                    `:
                    ''
                }
            </div>
            
        `
    }
    read_only_field(opts) {
        const uniq = lite.utils.unique(70)
        let display_value = opts?.value || ''
        if(opts?.is_figure || (lite.utils.is_number_variable(opts?.value) && opts?.format_figure != false))
            display_value = (lite.utils.is_number_variable(opts?.value) && this.numeric_fields_types.includes(lite.utils.lower_case(opts?.fieldtype)) || opts?.is_figure) ? lite.utils.thousand_separator(opts?.value,lite.defaults?.currency_decimals) : opts.value?.toString()
        else if(opts?.fieldtype === "percentage")
            display_value = `${opts?.value}%`
        else if(opts?.fieldtype === "rich"){
            lite.rich_editor_values[uniq] = {value:opts?.value || ''}
            return `<div class="p-2 rounded-md border">${opts.value}</div>`
        }
        else if(opts?.fieldtype === "check"){
            opts.disabled=true
            return this.input_check_field(opts)
        }
        if (opts.fieldtype === "link" && (opts?.value || opts?.default)){
            display_value = `
                <div class="text-default w-full h-full hover:text-secondary_color transition duration-1000 hover:font-semibold cursor-pointer flex items-center justify-between">
                    <span>${opts?.value || opts?.default || ''}</span>
                    ${!opts?.omitlabels ? '<span class="material-symbols-outlined text-15 text-secondary_color"> open_in_new </span>':""}
                </div>
            `
        }
        if (opts?.fieldtype === "file" && (opts?.value || opts?.default)){
            const vl = opts?.value || opts?.default
            if(vl){
                opts.is_submitted = true
                return this.file_field(opts)
            }
        }

        const v = `${opts?.value ? opts?.value : (opts?.default ? opts.default : '') }`
        return  `
            <div 
                id="${uniq}" 
                lite-id ="${uniq}"
                always-fetch="${opts?.alwaysfetch !=undefined ? opts?.alwaysfetch : true}"
                is_required="${opts?.required || false}" 
                type="read-only"
                value='${v}'
                fieldname="${opts?.fieldname}"
                ${opts.fieldtype === "link" ? 'is-linked-read-only="true" for="'+opts.model+'"' : ""}
                ${opts?.is_figure ? 'is-figure="true"': ''}
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''}  w-full px-3 flex items-center overflow-hidden overflow-y-auto min-h-[47px] max-h-[50px] ${!opts.istablefield ? 'form-control border h-[37px]' : 'table-field'}" 
                placeholder="${opts?.placeholder}"
            >
                ${display_value}
            </div>
        `
    }

    input_code_field(opts) {
        const uniq = lite.utils.unique()
        if(opts?.value){
            lite.preloaded_code[uniq] = opts?.value
        }
        return `
            <div 
                id="${opts?.id}" 
                always-fetch="${opts?.alwaysfetch || true}"
                lite-id="${uniq}"
                is_required="${opts?.required || false}" 
                type="code" 
                language="${opts?.language || 'html'}"
                value=''
                fieldname="${opts?.fieldname}"
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                class="lite-field lite-code-editor text-13 ${opts?.classnames || ''}  ${opts?.hidden ? 'hidden' : ''} w-full px-3 flex items-center truncate overflow-ellipsis min-h-[30px] ${!opts.istablefield ? 'form-control border h-[37px]' : 'table-field'}" 
                placeholder="${opts?.placeholder}"
            ></div>
        `
    }
    barcode(opts) {
        return `
            <div class="mt-1 w-full">
                <div class="w-full grid grid-cols-3 gap-x-3">
                    <input 
                        autocomplete="off"
                        id="${opts?.id}"
                        always-fetch="${opts?.alwaysfetch || true}"
                        fieldname="${opts?.fieldname}" 
                        ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                        ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                        ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                        type="text" 
                        ${opts?.value ? 'value="' + opts.value + '"' : ''}
                        ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                        class="lite-field text-13 barcode-field form-control w-full col-span-2  ${opts?.classnames || ''} ${opts?.hidden ? 'hidden' : ''}" 
                        placeholder="${opts?.placeholder}"
                        is_required="${opts?.required || false}"
                    >
                    <button
                        class="barcode-scanner w-full h-[38px] btn flex items-center justify-center text-12">
                        Scan
                        <span class="material-symbols-outlined ml-3 text-red-900 text-[18px]">
                            barcode_scanner
                        </span>
                    </button>
                </div>
            </div>
        `
    }

    button_field(opts) {
        return `
            <div class="mt-1 w-full">
                <button
                    id="${opts?.id}"
                    always-fetch="${opts?.alwaysfetch || true}"
                    fieldname="${opts?.fieldname}" 
                    ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                    ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                    ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                    type="button" 
                    ${opts?.value ? 'value="' + opts.value + '"' : ''}
                    class="lite-field button-field form-control w-full h-[38px] btn flex items-center justify-center text-12 ${opts?.classnames || ''} ${opts?.hidden ? 'hidden' : ''}" 
                    placeholder="${opts?.placeholder}"
                    is_required="${opts?.required || false}"
                >
                    <span class="material-symbols-outlined text-[18px] mr-3">
                        ${opts?.icon || "adjust"}
                    </span>
                    ${opts.fieldlabel}
                </button>
            </div>
        `
    }

    image(opts) {
        const v = opts?.value || opts?.default
        return `
            <div class="mt-1 w-full relative border border-gray-300 border-dashed rounded-md min-h-[30px] p-1">
                <div class="w-full gap-x-3">
                    <input 
                        autocomplete="off"
                        id="${opts?.id}"
                        always-fetch="${opts?.alwaysfetch || true}"
                        fieldname="${opts?.fieldname}" 
                        ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                        ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                        ${opts.fetchfrom ? 'fetch-from="' + opts.fetchfrom + '" fetch-field="' + opts.fetchfield + '"' : ""}
                        type="text" 
                        ${opts?.value ? 'value="' + opts.value + '"' : ''}
                        ${opts?.value ? 'prev-val="' + opts.value + '"' : ''}
                        value="${v}"
                        class="lite-field text-13 barcode-field form-control w-full col-span-2 hidden" 
                        placeholder="${opts?.placeholder}"
                        is_required="${opts?.required || false}"
                    >
                    <img class="w-full min-w-[150px] max-h-[150px] object-contain ${opts?.classnames || ''}" src="${v}"/>
                </div>
                <a href="${v}" download="${v}">
                    <span class="material-symbols-outlined text-13 bg-default text-theme_text_color rounded-full p-1 bottom-1 right-1 absolute shadow-md"> download </span>
                </d>
            </div>
        `
    }
    section_break(opts) {
        return `
            <div class="w-full intro-x font-semibold col-span-${this.setup?.layout_columns} ${opts?.addborder ? 'border-t' : ''} my-2 pt-1 text-12 transition duration-500 hover:scale-[1.2] text-24 pt-3">
                ${opts?.fieldlabel}
            </div>
        `
    }
    column_break(opts) {
        return `<div classname="column-break col-span-${opts.columns}"></div>`
    }

    status_field(opts) {
        return `
            <div class="w-full h-full flex items-center col-span-2 th">
                <div class="lite-field flex items-center justify-center rounded-full min-w-[80px] bg-red-100 text-danger">
                    Unpaid
                </div>
            </div>
        `
    }


    // child table generation
    create_child_table(opts, cols = 2) {

        const {workflow} = opts
        let $rows = '', rows_data = []
        let editable = (opts?.docstatus === 0 || opts?.editableonsubmit === true) || false
        if (workflow?.allow_edit === false){
            editable = false
        }
        if (lite.utils.array_has_data(opts?.rows)) {
            let row_data = lite.utils.ascend(opts?.rows, "id")
            $.each(row_data, (_, r) => {
                let opt = {value:r, idx:_, ...lite.utils.copy_object(opts)}
                $rows += this.create_table_row(opt, editable)?.row_element
            })
        }
        else {
            opts.idx = 0
            opts.value = ''
            const {row_element, row_data} = this.create_table_row(opts)
            $rows = ''
            if(opts?.addemptyrow) {
                $rows = row_element
                rows_data.push(row_data)
            }
        }
        const
            $head = this.#create_child_table_head(opts),
            $body = this.#create_table_body($rows),
            $wrapper = this.#create_child_table_wrapper(opts, $head, $body, editable)
        return {wrapper:`${$wrapper}`, rows_data: rows_data}
    }

    #create_child_table_search_field(params){
        const field = this.build_form_field({
            id: "search_table_field",
            omitlabels:true, 
            fieldname:`search_table_field`,
            fieldtype:"text", 
            placeholder:`Search ${lite.utils.capitalize(lite.utils.replace_chars(params?.fieldname,"_"," ")) || ""}`, 
            classnames:"table-search-field border-none h-[23px] outline-none text-center text-12"
        })
        return ''
        return `
            <div class="flex items-center justify-end border rounded-md overflow-hidden w-[200px] mb-2 relative">
                ${field}
                <span class="material-symbols-outlined absolute right-[10px] text-21 text-gray-400"> search </span>
            </div>
        `
    }

    #create_child_table_wrapper(opts, head, body, editable = true) {
        return `
            <div 
                for="${opts.model}" 
                fieldtype="table" 
                fieldname="${opts?.fieldname}"
                is_required="${opts?.required || false}" 
                ${opts?.displayon ? "display-on='"+ opts.displayon[0] +"'" : ''}
                ${opts?.displayon ? "display-eval='"+lite.utils.object_to_string(opts.displayon)+"'" :''}
                class="lite-field form-field table-wrapper  intro-x w-full mt-3 col-span-${opts?.columns || this.setup.layout_columns} ${opts?.hidden ? 'hidden' : ''} ${opts?.searchable || opts?.searchable === undefined ?"mt-10":""}"
            >
                <div class="flex items-center justify-between">
                    <div>
                        <div class="text-slate-500 mb-1 font-semibold">${opts?.fieldlabel || 'Add Items'}</div>
                        <small class="text-slate-400 text-12">${opts?.description || ''}</small>
                    </div>
                    <div class="flex items-center justify-end w-max-content gap-x-3">
                        ${opts?.searchable || opts?.searchable === undefined ? this.#create_child_table_search_field(opts) : ""}
                        ${head?.cols && head?.cols > 40 ? this.create_listview_scrollers(): ""}
                    </div>
                </div>
                <div for="${opts.model}" fieldname="${opts.fieldname}" class="table w-full rounded-md border border-dashed">${head?.head}${body}</div>
                <div class="w-full flex items-center justify-between border-t mt-3 border-dotted border-secondary_color">
                    ${editable && !opts?.excludeactions ? this.#create_child_table_action() : ''}
                    <div class="child-table-pagination flex items-center justify-end px-2 rounded-md"></div>
                </div>
            </div>
        `
    }

    #create_child_table_head(opts) {
        let cols = 2
        $.each(opts?.fields, (_, f) => cols += f?.hidden ? 0 : parseInt(f.columns || 1))
        const scrollable= cols > 40 ? true : false
        let head = `
            <div class="thead w-full h-[30px] text-13 ${scrollable ? 'flex items-center justify-start flex-row': ''}" cols="${cols}">
                <div cols="${cols}" class="tr w-full h-full grid grid-cols-${cols}  bg-default text-theme_text_color font-normal rounded-t-md">
                    <div class="th head-check-wrapper w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center col-span-1 maxs-w-[70px]">
                        <input autocomplete="off"id="" for="head-row" class="row-check form-check-input  list-check appearance-none border border-default checked:bg-default hover:bg-default active:bg-default checked:border-default focus:outline-default/50 head-check" type="checkbox">
                    </div>
        `
        
        $.each(opts?.fields, (_, f) => {
            head += `
            <div 
                cols="${f.columns || 1}"
                fieldname="${f.fieldname}" 
                class="th w-full h-full flex items-center pl-2 border-r border-r-dashed justify-start col-span-${f.columns || 1} pl-2 ${f?.hidden ? 'hidden' : ''}"
                ${f?.displayon ? "display-on='"+ f.displayon[0] +"'" : ''}
                ${f?.displayon ? "display-eval='"+lite.utils.object_to_string(f.displayon)+"'" :''}
            >
                <div class="w-full truncate overflow-ellipsis">
                    <span class="material-symbols-outlined ${f?.icon? "mr-1":""} text-${f.icon_color||"#fff"}-600"> ${f?.icon || ""} </span>
                    ${f.fieldlabel} ${f.required ? '<span class="text-danger ml-2">*</span>' : ''}
                </div>
            </div>`
        })
        head += `
            <div class="th head-check-wrapper w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center col-span-1 maxs-w-[70px]" cols="1">
                <div class="table-row-actions w-full h-full flex items-center border-r border-r-dashed justify-center col-span-1 maxs-w-[70px]">
                    <div class="dropdown min-w-1/2 sm:w-auto bg-red-900" style="position: relative;">
                        <button class="dropdown-toggle border-none" aria-expanded="false" data-tw-toggle="dropdown">
                            <span class="material-symbols-outlined text-purple-300 text-18"> tune</span>
                        </button>
                        <div class="dropdown-menu w-[max-content]" id="_hjlc5luf1" data-popper-placement="bottom-end" style="position: absolute; inset: 0px 0px auto auto; margin: 0px; transform: translate3d(-0.5px, 38px, 0px);">
                            <ul class="dropdown-content table-row-action-list">
                                <li class="form-option-items min-w-full hover:bg-default/30 rounded-md intro-x" for="Refresh Form">
                                    <a href="javascript:;" class="dropdown-item w-full w-[max-content] max-w-[300px]"> 
                                        <span class="material-symbols-outlined text-purple-800 mr-1 text-16">published_with_changes</span> Refresh Form
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `
        head += `</div></div>`
        return {head:head, cols:cols}
    }
    #create_table_body(rows = '') {
        return `<div class="tbody w-full text-[13px]">${rows}</div>`
    }

    create_table_row(opts, editable = true, is_new = false) {
        let cols = 2, row_id = opts?.value?.row_id || opts?.row_id || lite.utils.unique(), is_added_to_table_data = opts?.value?.row_id || opts?.row_id || false
        $.each(opts?.fields, (_, f) => cols += f?.hidden ? 0 : parseInt(f.columns || 1))
        let row = `
            <div id="${row_id}" table-row-index="${opts?.value?.current_page_index != undefined ? opts?.value?.current_page_index : opts?.current_page_index}" doc-id="${opts?.value?.id || null}" cols="${cols}" class="tr table-row hover:bg-default/30 bg-slate-50 intro-x w-full h-full grid grid-cols-${cols} text-slate-700 border-b border-dashed min-h-[40px] ">
                <div class="th w-full h-full flex items-center pl-2 border-r border-r-dashed justify-center col-span-1  maxs-w-[70px]">
                    <input autocomplete="off"for="body-row" class="row-check  list-check appearance-none border border-default checked:bg-default hover:bg-default active:bg-default checked:border-default focus:outline-default/50 form-check-input" type="checkbox" value="">
                </div>
        `
        let row_data = {}
        $.each(lite.utils.deep_clone(opts?.fields), (_, f) => {
            f.omitlabels = true
            f.istablefield = true
            f.read_only = false
            f.read_only = (!editable && !f?.editableonsubmit)

            if(opts?.value && lite.utils.is_object(opts?.value) && (opts?.value[f?.fieldname] || opts?.value[f?.fieldname] == 0)){
                f.value = opts?.value[f?.fieldname]
            }
            else if(f.fieldtype === "checkbox" || f.fieldtype === "check"){
                f.value = f?.value || f?.default || f[f?.fieldname] == 1 ? 1 : 0
            }
            else{
                f.value = f.value || f?.default ||  ( ["float", "percentage","int","number"].includes(opts.fieldtype) ? "0" : '')
            }
            row_data[f.fieldname] = f.value
            const field = this.build_form_field(f)
            row += `
                <div 
                    class="tc w-full h-full flex items-center border-r border-r-dashbed justify-start col-span-${f.columns || 1}  ${f?.hidden ? 'hidden' : ''}"
                    cols="${f.columns || 1}"
                    ${f?.displayon ? "display-on='"+ f.displayon[0] +"'" : ''}
                    ${f?.displayon ? "display-eval='"+lite.utils.object_to_string(f.displayon)+"'" :''}
                >
                    ${field}
                </div >
            `
        })
        if(!is_added_to_table_data){
            row_data.row_id = row_id
            row_data.current_page_index = 0
        }

        // handle table actions if any
        let acts = ''
        if(opts.table_actions && lite.utils.object_has_data(opts.table_actions)){
            $.each(lite.utils.ascend(lite.utils.get_object_values(opts.table_actions),"at_index"),(_, act)=>{
                acts += `
                <li class="form-option-items min-w-full hover:bg-default/30 rounded-md intro-x" for="Refresh Form">
                    <a href="javascript:;" for="${act.title}" table="${opts.fieldname}" model="${opts.model}" class="dropdown-item row-option-action w-full w-[max-content] max-w-[300px]"> 
                        <span class="material-symbols-outlined text-${act.icon_color || "purple"}-700 mr-1 text-16">
                        ${act.icon || "fiber_manual_record"}</span> ${lite.utils.capitalize(act.title)}
                    </a>
                </li>
                `
            })
        }
        row += `
            <div class="table-row-actions w-full h-full flex items-center border-r border-r-dashed justify-center col-span-1 maxs-w-[70px]" cols=1>
                <div class="dropdown min-w-1/2 sm:w-auto" style="position: relative; ">
                    <button class="dropdown-toggle border-none" aria-expanded="false" data-tw-toggle="dropdown">
                        <span class="material-symbols-outlined text-25 text-default"> more_vert </span>
                    </button>
                    <div class="dropdown-menu w-[max-content]" id="_hjlc5luf1" data-popper-placement="bottom-end" style="position: absolute; inset: 0px 0px auto auto; margin: 0px; transform: translate3d(-0.5px, 38px, 0px);">
                        <ul class="dropdown-content table-row-action-list">
                            ${acts}
                        </ul>
                    </div>
                </div>
            </div>
        `
        row += `</div > `
        return {row_element:row, row_data:row_data}
    }

    #create_child_table_action() {
        return `
            <div class="w-[max-content] flex items-center justify-start h-[30px] rounded-b-md mt-2">
                <button action="remove" class="btn w-[70px] add-remove-action-btn text-[18px] font-normal h-[25px] border-secondary_color text-orange-700 rounded-md">
                    <span class="material-symbols-outlined">remove</span>
                </button>
                <button action="add" class="btn w-[70px] add-remove-action-btn bg-default border-default/40 text-[18px] text-white ml-2 h-[25px] rounded-md">
                    <span class="material-symbols-outlined">add_circle</span>
                </button>
            </div >
        `
    }


    // listviews controller
    create_list_structure(columns, list_height = 40) {
        let
            cols = 5,
            header_default = `${this.create_list_check_sn_column('S/N', 'head')}`
        $.each(columns, (_, c) => {
            cols += c?.columns + 1 || 2
            header_default += `
                <div order="desc" column_name="${c.column_name}" class="list-head ${c.sortable ? 'sortable hover:text-white/50' : ''} w-full h-full intro-x transition flex items-center col-span-${c?.columns + 1 || 2} th">
                    <div order="desc" column_name="${c.column_name}" class="w-full font-semibold truncate overflow-ellipsis relative cursor-pointer flex items-center h-full">
                        <span class="hidden tooltip absolute top-[-4px] bg-default text-theme_text_color px-5 py-1 rounded-md w-[max-content]">
                            ${lite.utils.replace_chars(c.column_title, "_", " ")}
                        </span>
                        <span class="material-symbols-outlined ${c?.icon? "mr-1":""} text-${c.icon_color||"white"}-600"> ${c?.icon || ""} </span>
                        ${lite.utils.replace_chars(c.column_title, "_", " ")}
                    </div>
                    ${c.sortable ? '<span class="sort-order material-symbols-outlined text-13 mr-3">expand_all</span>' : ''}
                </div>
            `
        })
        return `<div class="w-full listview h-full border border-dashed rounded-md">
            ${this.create_header_row(cols, header_default)}
            ${this.create_list_body(list_height)}
        </div>`
    }

    create_listview_scrollers(){
        return `
            <div class="child-table-x-scrollers intro-x flex items-center justify-center mb-2">
                <button class="w-[50px] h-[30px] btn flex items-center justify-center mr-2 bg-purple-100">
                    <span class="material-symbols-outlined text-13">arrow_back_ios</span>
                </button>
                <button class="w-[50px] h-[30px] btn flex items-center justify-center bg-purple-100">
                    <span class="material-symbols-outlined text-13 p-0 m-0">arrow_forward_ios</span>
                </button>
            </div>
        `
    }

    create_header_row(cols, html) {
        return `
            <div class="w-full lhead gap-x-3 bg-default h-[40px] rounded-t-md text-theme_text_color grid grid-cols-${cols} font-normal border intro-x text-11">
                ${html}
                <div class="w-full h-full flex items-center justify-center col-span-2 th font-semibold">
                    <span class="material-symbols-outlined mr-1 text-theme_text_color text-16 text-orange-600">verified</span>Action
                </div>
            </div>
        `
    }
    create_list_check_sn_column(sn, for_row) {
        return `
            <div class="w-full h-full flex items-center col-span-1 ${for_row == 'head' ? 'th' : 'td'}">
                <div class="form-check w-full flex items-center justify-center border-r border-r-${for_row === "head" ? "white" : "default/90"} border-r-[2px]">
                    <input autocomplete="off"for="${for_row}" row-type="${for_row == 'head' ? 'head' : 'body'}" class="form-check-input list-check appearance-none border border-default checked:bg-default hover:bg-default active:bg-default checked:border-default focus:outline-default/50" type="checkbox" value="">
                </div>
            </div>
            <div idx="${sn}" data-field-name="sn" data-value="${sn}" class="w-full h-full flex items-center justify-center col-span-1 ${for_row == 'head' ? 'th' : 'td'}">
                <div class="form-check w-full flex items-center justify-center">
                    <div class="${for_row == 'head' ? 'text-white' : 'font-normal'} mr-2">${sn}</div>
                </div>
            </div>
        `
    }

    create_list_body(height = 60) {
        return `<div class="lbody w-full h-[${height}vh] overflow-y-auto"></div>`
    }

    create_list_row(sn, row, columns, actions, settings) {
        const cols = columns.reduce((acc, c) => acc + (c?.columns + 1 || 2), 5);
        const row_id = `${lite.utils.unique()}-list-row-${sn}`;
        let row_content = this.create_list_check_sn_column(sn, 'row-check');
    
        for (const c of columns) {
            const value = row[c.column_name];
            let v = lite.utils.format_value({ value_type: c.column_type, value, status_color:row?.status_color,status_inner_color:row?.status_inner_color });
            if (c.column_type === "check") {
                v = this.input_pure_check_field({ value, fieldname: c.column_name, disabled: true });
            } else if (c.column_type === "image") {
                v = `<img src="${value || "/static/images/avata/default-avata.png"}" class="w-[80%] px-3 h-[35px] rounded-md shadow-md border object-contain object-center"/>`;
            } else if (c.column_type === "icon") {
                v = `<span class="material-symbols-outlined text-17"> ${value} </span>`;
            }
    
            if (c.formatter && typeof c.formatter === "function") {
                v = c.formatter(value, row);
            }
    
            row_content += `
                <div data-field-name="${c.column_name}" data-value="${row[c.column_name]}" lite-value="${row.id}" class="list-cell ${columns.indexOf(c) === 0 ? 'font-semibold cursor-pointer' : ''} w-full h-full flex items-center pl-2 col-span-${c?.columns + 1 || 2} td truncate overflow-ellipsis cursor-pointer">
                    <div for-row="${row_id}" for="Open" class="row-action-option list-cell-child w-[99%] truncate overflow-ellipsis custom-hover">
                        ${v}
                    </div>
                </div>
            `;
        }
    
        return `
            <div id="${row_id}" lite-value="${row.id}" idx="${sn}" for="open" class="list-row w-full gap-x-3 bg-white h-[40px] border-b border-dashed text-slate-600 grid grid-cols-${cols} my-[2px] text-12 text-gray-600 transition hover:bg-gray-50">
                ${row_content}
                ${this.create_row_action_button(row_id, actions)}
            </div>
        `;
    }

    create_list_status(status_info){
        return `
            <div class="doc-status-wrapper px-3 flex items-center justify-center min-w-[100px] h-[30px] rounded-md text-orange-800 text-14 active" style="background-color: ${status_info?.status_color}; filter: brightness(99%); border: 1px solid ${status_info?.status_color};">
                <div class="w-[8px] doc-status-pill h-[8px] rounded-full mr-1" style="background-color: ${status_info?.inner_color};"></div>
                <span class="doc-status-text text-[13px] truncate overflow-ellipsis" style="color: ${status_info?.inner_color};">${status_info?.name}</span>
            </div>
        `
    }

    create_list_actions_btn(actions) {
        let options = '', custom_buttons = ''
        if (!lite.utils.is_empty_array(actions)) {
            $.each(actions, (_, f) => {
                if (!f?.is_custom_button)
                    options += `
                        <li class="check-controlled ${f?.classnames || ""} intro-x ${f?.show_on_list_check ? 'hidden' : ''}"><a action="${f?.title}" class="dropdown-item action-option">
                            <span class="material-symbols-outlined text-15 mr-1 text-${f?.icon_color}-700">${f?.icon}</span>${f?.title}
                        </a></li>
                    `
                else custom_buttons += `
                <button class="btn check-controlled intro-x ${f?.show_on_list_check ? 'hidden' : ''} ${f?.classnames} w-[max-content] px-3 text-12 mr-2">
                    <span class="material-symbols-outlined text-15 mr-1 text-${f?.icon_color}-700">${f?.icon}</span> ${f?.title}
                </button>
                `
            })

            return `
                <div class="flex items-center justify-end">
                    <div class="flex items-center justify-end">
                        ${custom_buttons}
                    </div>
                    <div class="dropdown w-[50px] list-actions-btn" style="position: relative;">
                        <button class=" w-[50px] dropdown-toggle btn w-full h-[47px]" aria-expanded="false" data-tw-toggle="dropdown">
                            <span class="material-symbols-outlined text-20">more_vert</span>
                        </button>
                        <div class="dropdown-menu w-[max-content]" id="_hjlc5luf1" data-popper-placement="bottom-end"
                            style="position: absolute; inset: 0px 0px auto auto; margin: 0px; transform: translate3d(-0.5px, 38px, 0px);">
                            <ul class="dropdown-content">${options}</ul>
                        </div>
                    </div>
                </div>
            `
        }
        return ''
    }

    create_row_action_button(row_id, actions) {
        let options = '', custom_buttons = '', cols = 1
        if (!lite.utils.is_empty_array(actions)) {
            $.each(actions, (_, f) => {
                if (!f?.is_custom_button)
                    options += `
                    <li>
                        <a for="${f?.title}" for-row="${row_id}" class="dropdown-item row-action-option"> 
                        <span class="material-symbols-outlined mr-2 text-17 text-${f?.icon_color}-700">${f?.icon}</span> ${f?.title}</a>
                    </li>
                `
                else {
                    cols += 1
                    custom_buttons += `
                <button for="${f?.title}" for-row="${row_id}" class="border-r flex items-center justify-center ${f?.classnames} w-[max-content] px-3 text-12 mr-2 row-action-option">
                    <span class="material-symbols-outlined text-15 mr-1 text-${f?.icon_color}-700">${f?.icon}</span> ${f?.title}
                </button>
                `
                }
            })
        }
        return `
            <div class="w-full h-full ${cols > 1 ? 'grid gap-x-5 grid-cols-' + cols : 'flex items-center justify-center'}  col-span-3">
                ${custom_buttons}
                <div class="dropdown w-1/2 sm:w-auto w-full h-full flex items-center justify-center" style="position: relative;">
                    <button class="dropdown-toggle border-default/50 w-full btn sm:w-auto" aria-expanded="false" data-tw-toggle="dropdown">
                        <span class="material-symbols-outlined text-17">more_vert</span>
                    </button>
                    <div class="dropdown-menu w-[140px]" id="_hjlc5luf1" data-popper-placement="bottom-end" style="position: absolute; inset: 0px 0px auto auto; margin: 0px; transform: translate3d(-0.5px, 38px, 0px);">
                        <ul class="dropdown-content w-full">${options}</ul>
                    </div>
                </div>
            </div>
        `
    }

    create_pagination(params) {
        const { total_pages, current_page, page_size, total_records,queried_total, page_range,include_page_jump=true,include_page_size_changer=true,scale=1 } = params
        let page_list = ''
        let page_options = ''
        $.each(page_range, (_,page)=>{
            page_list += `
                <li class="page-item transition duration-1000 ${page !== parseInt(current_page) ?'intro-x': '' }"> 
                    <a class="page-link paginate-select text-12 ${page === parseInt(current_page) ? 'active bg-default text-theme_text_color' : ''}" index="${page}">
                        <span class="${page === parseInt(current_page) ? 'text-white text-15 font-bold' : ''}">${page}</span>
                    </a> 
                </li>
            `
        })
        for(let i = 1;i<= total_pages;i++){
            page_options += `<option value="${i}">Page ${i}</option>`
        }
        return `
            <div class="w-full pagination_wrapper scale-[${scale}] col-span-12 flex flex-wrap items-center bg-white h-[40px] p-3 mb-3">
                <nav class="w-full sm:w-auto sm:mr-auto">
                    <ul class="pagination">
                        <li class="page-item">
                            <a class="page-link paginate-select" index="1"> 
                                <span index="1" class="material-symbols-outlined text-gray-400 text-20">keyboard_double_arrow_left</span>
                            </a>
                        </li>
                        ${page_list}
                        <li class="page-item">
                            <a class="page-link paginate-select" index="${total_pages}">
                                <span index="${total_pages}" class="material-symbols-outlined text-gray-400 text-20">keyboard_double_arrow_right</span>
                            </a>
                        </li>
                    </ul>
                </nav>
                <div class="w-[max-content] flex items-center justify-end gap-x-5">
                ${
                    include_page_size_changer || include_page_size_changer == undefined ? `
                        <select class="w-[230px] page-size-select form-select box mt-3 sm:mt-0 text-11 shadow-none">
                            <option value="50">Page Size(50 Rows Default)</option>
                            <option value="5">5 Rows</option>
                            <option value="10">10 Rows</option>
                            <option value="50">50 Rows</option>
                            <option value="100">100 Rows</option>
                            <option value="300">300 Rows</option>
                        </select>
                    
                    ` : ''
                }
                ${
                    include_page_jump || include_page_jump == undefined ?
                    `
                        <select class="w-20 page-jump form-select box mt-3 sm:mt-0 text-11 shadow-none" value="${current_page}">${page_options}</select>
                    ` : ''
                }
                <span class=" font-bold text-12 ml-1 flex items-center justify-between">
                    Total Records : 
                    <span class="bg-gray-100 px-3 rounded-md ml-2">${lite.utils.thousand_separator(current_page < total_pages? (current_page * queried_total) : total_records, 0)}/${lite.utils.thousand_separator(total_records, 0)}</span>
                </span>
                    
                </div>
            </div>
        `
    }



    // reports controllers
    create_report_actions(actions) {
        let btns = '', options = '', btn_wrapper = '', options_wrapper = ''
        $.each(actions, (_, a) => {
            if (a?.is_action_button) {
                btns += `
                    <button for="${a?.title}" format="${a.format}" class="report-action-option btn mr-2 w-[170px] bg-${a?.background_color}${a?.background_color !== 'default' ? '-800' : ''}  text-${a.color} shadow-none text-12">
                        <span class="material-symbols-outlined mr-2 text-13">${a?.icon}</span> ${a?.title}
                    </button>
                `
            }
            else {
                options += `
                    <li class="intro-x">
                        <a for="${a?.title}" format="${a.format}" class="report-action-option dropdown-item">
                            <span class="material-symbols-outlined text-[14px] mr-2 text-${a.icon_color}-700">${a?.icon}</span>
                            ${a?.title}
                        </a>
                    </li>
                `
            }
        })
        if (btns !== '') {
            btn_wrapper = `<div class="action_buttons flex items-center justify-center">${btns}</div>`
        }
        if (options !== '') {
            options_wrapper = `
                <div class="dropdown w-1/2 sm:w-auto" style="position: relative;">
                    <button id="report-actions-btn" class="dropdown-toggle w-full h-[50px] text-18 btn bg-default text-theme_text_color sm:w-auto" aria-expanded="false" data-tw-toggle="dropdown">
                        <span class="material-symbols-outlined mr-1 text-24">download</span>
                        Download Report
                        <span class="material-symbols-outlined text-20">more_vert</span>
                    </button>
                    <div class="dropdown-menu w-[200px]" id="_hjlc5luf1" data-popper-placement="bottom-end"
                        style="position: absolute; inset: 0px 0px auto auto; margin: 0px; transform: translate3d(-0.5px, 38px, 0px);">
                        <ul class="dropdown-content">${options}</ul>
                    </div>
                </div>
            `
        }

        return `${btn_wrapper}${options_wrapper}`
    }

    create_table_controllers(title) {
        return `
            <div class="flex items-center justify-center">
                <span class="font-semibold intro-x text-gray-700 flex items-center justify-start border-r border-r-2 pr-5">
                    <span class="material-symbols-outlined mr-1 text-23">list</span>
                    <div class="report-title max-w-[300px] truncate overflow-ellipsis text-20">${title}</div>
                </span>
                <button class="expand-shrink-table intro-x flex items-center justify-center ml-5 py-2 hover:text-default bg-secondary_color rounded-md px-3">
                    <span class="material-symbols-outlined mr-1 text-theme_text_color">pan_zoom</span>
                    <span class="text text-theme_text_color font-semibold text-13">Show Filters</span>
                </button>
            </div>
            <div class="x-scrollers intro-x flex items-center justify-center">
                <button class="w-[60px] h-[27px] btn flex items-center justify-center mr-2">
                    <span class="material-symbols-outlined text-15">arrow_back_ios</span>
                </button>
                <small class="text-gray-600 mx-2 font-bold h-18">Horizontal Scrollers</small>
                <button class="w-[60px] h-[27px] btn flex items-center justify-center">
                    <span class="material-symbols-outlined text-15 p-0 m-0">arrow_forward_ios</span>
                </button>
            </div>
        `
    }

    create_table_refresh_btn(){
        return `
            <button class="refresh-report min-w-[130px] h-[35px] bg-default text-theme_text_color ml-3 btn flex items-center justify-center mr-2 text-15">
                <span class="material-symbols-outlined text-18 text-theme_text_color mr-1">refresh</span>
                Refresh Report
            </button>
        `
    }

    // creating the report table
    create_report_table(columns, setup) {
        const headers = this.#create_report_head(columns, setup)
        const body = this.#create_report_body(setup)
        return `${headers}${body}`
    }

    #create_report_head(columns, setup) {
        const grid = setup?.is_grid_layout || false
        let grid_cols = 1
        if (grid){
            $.each(columns,(_, col)=>{ grid_cols += col.columns || 2 })
        }
        let cols = `<div data-value="S/N" class="table-cell h-[40px] flex ${ grid ? "col-span-1 is-grid" : ""} text-15 header-cell items-center justify-center">S/N</div>`
        
        $.each(columns, (_, c) => {
            const width = `min-w-[${c?.width || '150'}px]  max-w-[${c.width || '150'}px]`
            const col_span = `col-span-${c?.columns} h-[40px]`
            cols += `
                <div 
                    lite-value="${c.column_title}" 
                    lite-label="${c.column_title}"
                    lite-fieldname="${c.column_name}" 
                    lite-fieldtype="${c.column_type}"
                    lite-model="${c.model}" 
                    class="table-cell header-cell resizable  intro-x ${ grid ? col_span : width} ${c.sortable ? 'sortable' : ''}">
                        <div class="w-full h-full flex items-center justify-center ">
                            <div class="w-full h-full flex items-center truncate overflow-ellipsis text-15">${c.column_title}</div>
                            ${c.sortable ? '<span class="material-symbols-outlined">unfold_more</span>' : ''}
                        </div>
                </div>
            `
        })
        return `
            <div class=" ${grid ? "w-full": "w-[max-content]"} h-[40px]">
                <div class="table-row ${ grid ? "grid grid-cols-"+grid_cols+"" : ""} header-row h-[40px] bg-default text-theme_text_color">${cols}</div>
            </div>
        `
    }
    #create_report_body(setup) {
        return `
            <div class="table-body min-h-[30vh]  ${setup?.is_grid_layout ? "w-full" : "w-[max-content]"} "></div>
        `
    }

    create_report_row(sn, data, columns, setup) {
        const grid = setup?.is_grid_layout || false
        let grid_cols = 1
        if (grid){
            $.each(columns,(_, col)=>{ grid_cols += col.columns || 2 })
        }
        let cols = `<div data-value="${sn}" class="table-cell flex ${grid ? "col-span-1  h-[30px] is-grid" :""} items-center justify-center font-bold text-11">${sn}</div>`
        $.each(columns, (_, c) => {
            const width = `min-w-[${c?.width || '150'}px]  max-w-[${c.width || '150'}px]  h-[30px]`
            const col_span = `col-span-${c?.columns} h-[30px]`
            let v = data[c.column_name] || data[lite.utils.lower_case(c.column_name)]
            if(v){
                if(c.formatter && c.apply_formatter_on_total && data?.total_fields?.includes(c.column_name)){
                    v = c.formatter(data[c.column_name] || data[lite.utils.lower_case(c.column_name)])
                }
                else if(c.formatter && !c.apply_formatter_on_total){
                    v = c.formatter(data[c.column_name] || data[lite.utils.lower_case(c.column_name)])
                }
                else{
                    if (c.is_figure && !data?.is_head) {
                        if (v)
                            if(lite.utils.is_number_variable(v))
                                v = lite.utils.thousand_separator(data[c.column_name] || data[lite.utils.lower_case(c.column_name)], lite.defaults?.currency_decimals)
                            else v = ""
                        else
                            v = lite.utils.thousand_separator(0, lite.defaults?.currency_decimals)
                    }
                    if(c.column_name === "status" && data.status_info){
                        v = this.create_list_status(data.status_info)
                    }
                    if(c.column_type == "report" && v?.trim()){
                        v = `
                        <div class="flex items-center justify-start my-1 text-secondary_color hover:font-bold">
                            <span class="material-symbols-outlined text-secondary_color bg-secondary_color/10 rounded-md p-[1.1px] text-20 mr-1">read_more</span>
                            <span class="border-b border-b-secondary_color"> ${v}</span>
                        </div>
                        `
                    }
                }
            }
            else v = c.is_figure ? "0.00" : "-"
            cols += `
                <div 
                    lite-label="${c.column_title}"  
                    lite-fieldname="${c.column_name}" 
                    lite-fieldtype="${c.column_type}"  
                    lite-model="${c.model}" 
                    class="table-cell ${data.is_empty_row ? "empty-row" : ""} text-13 ${grid ? col_span : width} ${c.is_figure ? 'figure text-end' : 'text-start'} ${data.is_final_total? "border-b-double":""} ${data.is_opening_or_closing ? 'bg-secondary_color/5 font-bold text-[20px] text-secondary_color' : ''} ${c.column_type == "link" ? "tbl-link-cell underline decoration-secondary_color pb-1 hover:font-semibold text-secondary_color transition duration-400" : (c.column_type == "report" ? "tbl-report-cell" :"")}">
                        ${c.column_type == "link" ? `<span class="link-cell" lvl="${data[c.column_name] || data[lite.utils.lower_case(c.column_name)]}" mdl='${lite.utils.is_object(c.model)? JSON.stringify(c.model) : c.model}' is-single-mdl='${lite.utils.is_object(c.model) ? 0: 1}'></span>`:""}
                        ${c.column_type == "report" ? `<span class="report-cell" fieldname="${c.column_name}" lvl="${data[c.column_name] || data[lite.utils.lower_case(c.column_name)]}" report='${c.report}'></span>`:""}
                        <div class="w-full h-full flex items-center ${c.is_figure ? "justify-end" :""}">
                            <div class="w-[max-content] truncate overflow-ellipsis ${data?.total_fields?.includes(c.column_name) ? "border-b-[2px] border-t-[2px] border-gray-500 text-16 font-bold" : ""} ${c.classname || ''} ">
                                ${v || '-'}
                            </div>
                        </div>
                </div>
            `
        })

        return `<div class="table-row w-full ${grid? "grid grid-cols-"+grid_cols +"" :""} h-[30px] transition hover:bg-default/30 duration-1000 hover:cursor-pointer">${cols}</div>`
    }

    create_empty_report_row() {
        return `<div class="table-row w-full border-none"><div data-value="" class="items-center border-none"></div></div>`
    }



    // dynamic form buttons
    create_save_button(attr) {
        return `
            <div class="group bg-white h-max w-max rounded-[4rem] p-1 transition-all ease-in-out flex justify-center shadow-md items-center cursor-pointer overflow-hidden hover:bg-default">
                <button class="save-action-btn ${attr?.classname} h-[47px] rounded-[4rem] px-5 text-14 w-max btn bg-default transition-all ease-in-out text-theme_text_color shadow-md group-hover:bg-white group-hover:text-default">
                    <span class="material-symbols-outlined mr-2 text-18"> task_alt</span> Create Record
                </button>
            </div>              
        `
    }

    create_form_button(attr) {
        return `
            <button action="${attr?.title}" class="form-action-btn ${attr?.classname} min-w-[140px] max-w-[max-content]  btn shadow-md mr-1">
                <span class="material-symbols-outlined mr-2 text-18 text-${attr?.icon_color}-600 mr-1"> ${attr?.icon}</span> 
                ${attr.title}
            </button>               
        `
    }

    create_update_button(data, attr) {
        if(data?.disabled === 1 || [2,3].includes(data?.docstatus)){
            return ""
        }
        return `
            <div class="group bg-white h-max w-max rounded-[4rem] p-1 transition-all ease-in-out flex justify-center shadow-md items-center cursor-pointer overflow-hidden hover:bg-secondary_color">
                <button class="update-action-btn ${attr?.classname} h-[47px] rounded-[4rem] px-5 text-14 w-max btn bg-secondary_color transition-all ease-in-out text-theme_text_color shadow-md group-hover:bg-white group-hover:text-secondary_color">
                    <span class="material-symbols-outlined mr-2 text-18"> frame_reload</span> Update Record
                </button>
            </div>             
        `
    }

    create_amend_button(attr) {
        return `
            <button class="amend-action-btn ${attr?.classname} w-[120px] max-w-[max-content]  btn border-orange-600 text-white shadow-md ">
                <span class="material-symbols-outlined mr-2 text-18"> save</span> Amend
            </button>               
        `
    }

    create_submit_button(attr) {
        return `
            <button class="submit-action-btn ${attr?.classname} w-[120px] max-w-[max-content]  btn bg-default text-theme_text_color shadow-md ">
                <span class="material-symbols-outlined mr-2 text-18"> done_all</span> Submit Doc
            </button>               
        `
    }

    create_print_button(data, attr) {
        if(data?.disabled === 1 || [2,3].includes(data?.docstatus)){
            return ""
        }
        return `
            <button class="print-action-btn ${attr?.classname} w-[120px] font-semibold text-16 h-[47px] max-w-[max-content]  btn border border-secondary_color border-secondary_color bg-white shadow-none">
                <span class="material-symbols-outlined mr-2 text-18 text-secondary_color"> print</span> Print
            </button>               
        `
    }

    create_print_format_select_button(data, setup, print_format='') {
        if(data?.disabled === 1 || [2,3].includes(data?.docstatus)){
            return ""
        }
        return `
            <select type="link" for="Print_Format" linkfield="name" filters='${JSON.stringify({app_model:setup.model})}' action-type="print-format-toggler" value="${print_format || ""}" class="lite-selector bg-white print-format-option border rounded-md px-3 min-w-[140px] mr-2 z-" placeholder="Select Print Format" style="z-index:300">
            </select>             
        `
    }

    create_form_download_and_preview(data, setup){
        const form_title = `
            <h5 class="doc-name my-2 font-bold flex items-center justify-start text-14 intro-x text-gray-500">
                ${data?.name}
            </h5>
        `
        const preview = `
            <button class="flex bg-default/10 rounded-md px-4 py-2 items-center justify-center border-l w-[110px] preview-doc text-gray-600 text-12 px-4 intro-x">
                <span class="material-symbols-outlined text-20 text-emerald-600"> preview </span>
                <span class="ml-1 font-semibold">Preview</span>
            </button>
        `
        const trail = `
            <button class="flex bg-default/10 rounded-md px-4 py-2 items-center justify-center border-l w-[120px] show-audit-trail text-gray-600 text-12 px-4 intro-x">
                <span class="material-symbols-outlined text-purple-700 text-20"> data_info_alert </span>
                <span class="ml-1 font-semibold">Audit Trail</span>
            </button>
        `
        
        const download = `
            <a href="/app/core/print_doc/${data?.default_print_format}/${setup?.model}/${data.id}/1/" target="_blank"
                class="flex items-center justify-center border-l w-[130px] text-14 px-4 py-2 intro-x bg-default text-theme_text_color rounded-md">
                <span class="material-symbols-outlined text-theme_text_color text-20 mr-1"> download </span>
                <span class="font-semibold">Download</span>
            </a>
        `

        const workflow_comments = `
            <button class="show-comments rounded-md py-1 mb-1 flex items-center bg-secondary_color text-theme_text_color justify-center border-l w-[170px] text-gray-600 text-12 px-4 intro-x">
                <span class="material-symbols-outlined text-theme_text_color text-20"> chat </span>
                <span class="ml-1 font-semibold text-theme_text_color">Workflow Comments</span>
            </button>
        `

        return `
            <div class="inner-form-actions flex items-center justify-between w-max-content gap-x-4 mb-3">
                ${form_title}
                ${setup?.allow_preview &&  ![2,3].includes(data?.docstatus) && data?.default_print_format ? preview : ""}
                ${setup?.allow_download &&  ![2,3].includes(data?.docstatus) && data?.default_print_format ? download : ""}
                ${trail}
                ${data?.workflow?.comments && lite.utils.array_has_data(data?.workflow?.comments) ? workflow_comments : ""}
            </div>
        `
    }

    create_preview_content(doc){
        $(".info-view-content form")?.append(`
            <div class="preview-wrapper hidden w-full h-full fixed right-0 top-0 bg-default/20 rounded-md overflow-hidden flex items-center justify-end" style="z-index:500">
                <div class="w-[75%] h-[99%] intro-x rounded-l-md p-3 bg-white overflow-hidden shadow-md">
                    <div class="w-full h-[40px] flex items-center justify-between border-b  intro-x">
                        <div class="w-full h-[40px] flex items-center justify-start">
                            <span class="material-symbols-outlined  text-[30px] text-orange-600 mr-2"> data_info_alert</span>
                            <span class="font-bold  text-[17px]">Document Preview</span>
                        </div>
                        <button class="border-none cursor-pointer close-preview-btn">
                            <span class="material-symbols-outlined text-30 text-red-800">close</span>
                        </button>
                    </div>
                    <div class="w-full doc-preview-content h-full pb-[40px] overflow-y-auto"></div>
                </div>
            </div>
        `)

    }

    create_trail_content(doc){

        let trails = ""
        if(doc?.audit_trail){
            if(lite.utils.array_has_data(doc?.audit_trail?.audit_items)){
                const grouped = lite.utils.group(doc?.audit_trail?.audit_items, "created_on")
                $.each(lite.utils.get_object_keys(grouped),(_, k)=>{
                    trails += `
                        <div class="pb-5 relative overflow-hidden before:content-[''] before:absolute before:w-px before:bg-slate-300 before:left-[65px] lg:before:right-0 before:ml-3 before:mt-6 before:h-full ">
                            <div class="relative z-10 py-2 my-5 text-center text-slate-500 w-[max-content] bg-white rounded-full px-1 text-12 font-bold">
                                ${lite.utils.convert_date(k)}
                            </div>
                            <div class=" ml-[80px] w-[77%] pl-7 before:content-[''] before:absolute before:w-20 before:h-px before:left-[70px] before:bg-slate-200 before:rounded-full before:inset-x-0 before:z-[-1] ">
                                <div class="w-full flex flex-col  items-start before:content-[''] before:absolute before:w-6 before:h-6 before:bg-primary/20 before:rounded-full before:inset-x-0 lg:before:ml-[65px] lg:before:animate-ping after:content-[''] after:absolute after:w-6 after:h-6 after:bg-primary after:rounded-full after:inset-x-0 lg:after:ml-[65px] after:border-4">
                                    <div class="w-full h-[max-content]">
                    `
                    $.each(grouped[k],(__,v)=>{
                        let msg = ""
                        const modifier = v.linked_fields?.modified_by, owner = doc.linked_fields?.owner
                        const user = `${modifier?.first_name || ""} ${modifier?.middle_name || ""} ${modifier?.last_name || ""}`
                        if(v.action === "Created"){
                            msg = `${owner?.first_name || ""} ${owner?.middle_name || ""} ${owner?.last_name || ""} Created <span class="font-semibold">${doc.name}</span>`
                        }
                        else if(v.action === "Updated"){
                            msg = `${user} Changed <span class="font-semibold">${v.field}</span> from <span class="font-semibold">${v.before_content}</span> to <span class="font-semibold">${v.after_content}</span>`
                        }
                        trails += `
                            <div class="w-full flex items-start justify-between my-4  intro-y">
                                <div class="flex items-start justify-center">
                                    <span class="material-symbols-outlined text-12 mr-1 text-default bg-indigo-100 w-[20px] h-[20px] flex items-center justify-center rounded-full">
                                        edit_note
                                    </span>
                                    <div class="text-13 flex flex-col">
                                        <div>${msg}</div>
                                        <small></small>
                                        <small>Time: ${v.time_created}</small>
                                    </div>
                                </div>
                            </div>
                        `
                    })
                    trails += `
                                    </div>
                                </div>
                            </div>
                        </div>
                    `
                })
            }
        }
        $(".info-view-content form")?.append(`
            <div class="audit-trail-wrapper hidden w-full h-full fixed right-0 top-0 bg-default/20 rounded-md overflow-hidden flex items-center justify-end" style="z-index:500">
                <div class="w-[70%] h-[99%] intro-x rounded-l-md p-3 bg-white overflow-hidden shadow-md">
                <div class="w-full h-[40px] flex items-center justify-between border-b  intro-x">
                    <div class="w-full h-[40px] flex items-center justify-start">
                        <span class="material-symbols-outlined  text-[30px] text-orange-600 mr-2"> data_info_alert</span>
                        <span class="font-bold  text-[17px]">Audit Trail</span>
                    </div>
                    <button class="border-none cursor-pointer close-trail-btn">
                        <span class="material-symbols-outlined text-30 text-red-800"> close</span>
                    </button>
                </div>
                <div class="w-full grid grid-cols-7 gap-4 my-5 text-12 font-semibold border-b pb-3  intro-x">
                    <h3 class="flex items-center justify-start text-gray-500 intro-x">
                        <span class="material-symbols-outlined mr-1 text-17"> account_circle </span>
                        Owner:
                    </h3>
                    <h3 class="col-span-2  intro-x">${doc.linked_fields?.owner?.first_name || ""} ${doc.linked_fields?.owner?.middle_name || ""} ${doc.linked_fields?.owner?.last_name || ""}</h3>
                    <h3 class="flex items-center justify-start text-gray-500 intro-x">
                        <span class="material-symbols-outlined mr-1 text-17"> calendar_month </span>
                        Date:
                    </h3>
                    <h3 class="col-span-3 intro-x">${doc.created_on}</h3>
                    <h3 class="flex items-center justify-start text-gray-500 intro-x">
                        <span class="material-symbols-outlined mr-1 text-17"> category </span>
                        Type:
                    </h3>
                    <h3 class="col-span-2 intro-x">${lite.utils?.capitalize(lite.utils?.replace_chars(doc?.doctype || "", "_"," "))}</h3>
                    <h3 class="flex items-center justify-start text-gray-500 intro-x">
                        <span class="material-symbols-outlined mr-1 text-17"> badge </span>
                        ID/Name:
                    </h3>
                    <h3 class="col-span-3 intro-x">${doc.name}</h3>
                </div>
                <div class="mt-2 w-full h-[70%] overflow-y-auto intro-x">${trails}</div>
            </div>
            </div>
        `)
    }

    create_workflow_comment_content(doc){
        let comments = ""
        $.each(doc.workflow?.comments,(_, comment)=>{
            comments += `
                <div class="p-3 rounded-md my-2 bg-default/10 min-h-[50px]">
                    <div class="flex items-center justify-between w-[max-content]">
                        <div class="mr-2 bg-secondary_color/20 text-secondary_color rounded-full px-3 w-[max-content] mb-1 flex items-center justify-center text-12">
                            <div class="w-[5px] h-[5px] bg-secondary_color rounded-full mr-1"></div>
                            ${comment?.from_status}
                        </div>
                        <span class="material-symbols-outlined text-25"> trending_flat </span>
                        <div class="ml-2 bg-default/20 text-default rounded-full px-3 py-0 w-[max-content] mb-1 flex items-center justify-center text-12">
                            <div class="w-[5px] h-[5px] bg-default rounded-full mr-1"></div>
                            ${comment?.to_status}
                        </div>
                    </div>
                    <div class="ml-3 my-2">
                        <h5 class="font-semibold text-13">${comment?.comment_owner_first_name} ${comment?.comment_owner_middle_name} ${comment?.comment_owner_last_name}</h5>
                        <small class="text-secondary_color">${comment?.comment_owner_role}</small>
                    </div>
                    <div class="text-12 ml-3">${comment?.comment}</div>
                    <div class="text-9 ml-3 bg-default text-theme_text_color rounded-md px-2 mt-4  w-[max-content]">Commented on ${lite.utils.convert_date(comment?.comment_date)}</div>
                </div>
            `
        })
        const comment_content = `
            <div class="comments-wrapper hidden w-full h-full fixed right-0 top-0 bg-default/20 rounded-md overflow-hidden flex items-center justify-end" style="z-index:500">
                <div class="w-[65%] h-[99%] intro-x rounded-l-md p-3 bg-white overflow-hidden shadow-md">
                    <div class="w-full h-[40px] flex items-center justify-between border-b  intro-x">
                        <div class="w-full h-[40px] flex items-center justify-start">
                            <span class="material-symbols-outlined  text-[30px] text-orange-600 mr-2"> chat</span>
                            <span class="font-bold  text-[17px]">Workflow Comments</span>
                        </div>
                        <button class="border-none cursor-pointer close-comments-btn">
                            <span class="material-symbols-outlined text-30 text-red-800">close</span>
                        </button>
                    </div>
                    <div class="w-full doc-preview-content h-full pb-[40px] overflow-y-auto">${comments}</div>
                </div>
            </div>
        `
        $(".info-view-content form")?.append(comment_content)
        return comment_content
    }

    create_drop_down_button(opts, doc) {
        const docstatus = doc.docstatus
        if (lite.utils.is_empty_object(opts))
            return ``
        let option_list = '', workflow_actions = ''
        let shuffled = [...opts], added = []
        
        // shuffle according to index
        $.each(opts,(_,opt)=>{
            if(opt?.at_index){
                shuffled.splice(opt?.at_index,0, opt)
                delete shuffled[_ +1]
            }
        })

        $.each(shuffled, (_, opt) => {
            let qualified = false
            if(opt?.for_docstatus?.includes(docstatus) && !added.includes(opt.title)){
                added.push(opt.title)
                if(opt?.for_status === undefined){
                    qualified = true
                }
                else{
                    if(opt?.for_status?.includes(doc.status)){
                        qualified = true
                    }
                }
            }
            
            if(opt?.evaluate && qualified){
                if(!opt?.evaluate[1]?.includes(doc[opt?.evaluate[0]])){
                    qualified = false
                }
            }
            if(doc?.disabled === 1 && !["enable", `new ${lite.utils.lower_case(doc?.doctype)}`, "refresh form"].includes(lite.utils.lower_case(opt?.title))){
                qualified = false
            }
            if (qualified){
                if(opt?.is_workflow_action){
                    workflow_actions += `
                        <li class="form-option-item mb-3 min-w-full hover:[${lite.utils.adjust_hex_color_intensity(opt?.icon_color,30) || "default"}] rounded-md intro-x bg-[${lite.utils.adjust_hex_color_intensity(opt?.icon_color,80) || "white"}] text-${opt?.icon_color ? `[${opt?.icon_color}]` : "white"}" for="${opt.title}" stage-no="${opt?.stage_no}">
                            <a  href="javascript:;" class="dropdown-item w-full w-[max-content] max-w-[500px] font-semibold"> 
                                ${opt?.icon ? '<span class="material-symbols-outlined text-' + opt?.icon_color + '-800 mr-1 text-20">' + opt?.icon + '</span>' : ''} 
                                <span class="text-12">${opt?.title}</span>
                            </a>
                        </li>
                    `
                }
                else{
                    option_list += `
                        <li class="form-option-item min-w-full hover:bg-default/30 rounded-md intro-x" for="${opt.title}">
                            <a  href="javascript:;" class="dropdown-item w-full w-[max-content] max-w-[400px]"> 
                                ${opt?.icon ? '<span class="material-symbols-outlined text-' + opt?.icon_color + '-800 mr-1 text-16">' + opt?.icon + '</span>' : ''} ${opt?.title}
                            </a>
                        </li>
                    `
                }
            }
                
        })
        return `
            ${
                workflow_actions !== "" ? `
                    <div class="dropdown min-w-1/2 sm:w-auto" style="position: relative; ">
                        <button class="dropdown-toggle !w-[180px] !h-[50px] bg-secondary_color shadow-2xl text-theme_text_color w-full btn sm:w-auto bg-white border ml-2" aria-expanded="false" data-tw-toggle="dropdown">
                            <span class="material-symbols-outlined text-20 mr-1"> flowsheet </span> Workflow Actions
                        </button>
                        <div class="dropdown-menu w-[max-content]" id="_hjlc5luf1" data-popper-placement="bottom-end"
                            style="position: absolute; inset: 0px 0px auto auto; margin: 0px; transform: translate3d(-0.5px, 38px, 0px);">
                            <ul class="dropdown-content">${workflow_actions}</ul>
                        </div>
                    </div>
                ` : ""
            }
            <div class="dropdown min-w-1/2 sm:w-auto" style="position: relative; ">
                <button class="dropdown-toggle w-full btn sm:w-auto bg-white border ml-2 h-[47px]" aria-expanded="false" data-tw-toggle="dropdown">
                    <span class="material-symbols-outlined text-25 text-default"> more_vert </span>
                </button>
                <div class="dropdown-menu w-[max-content]" id="_hjlc5luf1" data-popper-placement="bottom-end"
                    style="position: absolute; inset: 0px 0px auto auto; margin: 0px; transform: translate3d(-0.5px, 38px, 0px);">
                    <ul class="dropdown-content">${option_list}</ul>
                </div>
            </div>           
        `
    }
}
