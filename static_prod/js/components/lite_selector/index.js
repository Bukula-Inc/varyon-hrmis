export default class Lite_Selector {
    constructor(config) {
        this.temp_select_values = {}
        this.utils = config.utils
        this.session = config.session
        this.connect = config.connect
        this.on_select_change = []
        this.selector_wrapper = '.select-field-wrapper'
        this.icon_class = '.material-symbols-outlined.active-option'
        this.option_class = 'li.option'
        this.selector_class_name = '.lite-selector'
        this.selector_element_class_name = 'select.lite-selector:not(.initialized)'
        this.inner_select_field_wrapper = '.inner-select-field-wrapper'
        this.select_field = 'input.select-field'
        this.options_wrapper = '.select-options-wrapper'
        this.options_list_ul = '.select-options-list'

        this.select_loader_class_name = '.select-loader'
        this.select_configs = {}
        // event actions
        this.on_focusin = []
        this.on_focusout = []

        this.options = []
    }
    
    init_selectors(on_select_change, cls, other_events, init_id) {
        if (this.utils.is_function(on_select_change)) {
            this.add_on_change_functions(on_select_change, cls, init_id)
        }
        if (!this.utils.is_empty_object(other_events)) {
            if (other_events?.on_focus_in) {
                this.on_focusin.push({ fun: other_events.on_focus_in, cls: cls })
            }
            if (other_events?.on_focus_out) {
                this.on_focusout.push({ fun: other_events.on_focus_out, cls: cls })
            }
        }
        
        const selectors = $(this.selector_element_class_name)
        
        if (!this.utils.is_empty_array(selectors)) {
            $.each(selectors, (_, s) => {
                $(s).addClass("initialized")
                const
                    selector_type = $(s).attr('type')?.trim() || null,
                    selector_for = $(s).attr('for')?.trim() || null,
                    fieldname = $(s).attr('linkfield')?.trim(),
                    filters = this.utils.string_to_object($(s).attr('filters')) || {},
                    value = $(s).attr('value')?.trim() || null,
                    descriptions = $(s).attr('descriptions')?.trim() || null,
                    prefix = $(s).attr('prefix')?.trim() || null,
                    postfix = $(s).attr('postfix')?.trim() || null,
                    id = $(s).attr('id')?.trim() || null,
                    select_id = `${selector_for || ""}__${fieldname || ""}_${this.utils.unique()}-${this.utils.unique()}`
                this.select_configs[select_id] = {
                    filters: {...filters, disabled: filters?.disabled || 0},
                    value: value,
                    descriptions: descriptions ? JSON.parse(descriptions) : [],
                    prefix:prefix,
                    postfix:postfix,
                    fieldname: fieldname,
                    model: selector_for,
                    select_type: selector_type,
                    id: select_id,
                    options: []
                }
                if (selector_type) {
                    if (selector_type === 'link') {
                        if (selector_for) {
                            let options = '', desc = [], prefix=""
                            // adding descriptions to the options
                            const lowered_model = lite.utils.lower_case(selector_for)
                            if(["lite_user", "employee"].includes(lowered_model)){
                                this.select_configs[select_id].descriptions = ["first_name","middle_name","last_name"]
                            }
                            else if(lowered_model === "currency"){
                                this.select_configs[select_id].descriptions = ["country"]
                            }
                            else if(["tax_invoice","credit_note","delivery_note", "quotation"].includes(lowered_model)){
                                this.select_configs[select_id].descriptions = ["customer", "issue_date"]
                                this.select_configs[select_id].prefix = "For"
                            }
                            else if(["purchase_invoice","debit_note","purchase_order"].includes(lowered_model)){
                                this.select_configs[select_id].descriptions = ["supplier", "issue_date"]
                                this.select_configs[select_id].prefix = "For"
                            }
                            else if(lowered_model === "account"){
                                this.select_configs[select_id].descriptions = ["root_type", "account_type", "currency"]
                                this.select_configs[select_id].separator = "|"
                            }
                            else if(lowered_model === "stock_item"){
                                this.select_configs[select_id].descriptions = ["item_code", "barcode"]
                                this.select_configs[select_id].separator = "|"
                            }

                            else if(lowered_model === "bank_account"){
                                this.select_configs[select_id].descriptions = ["parent", "currency"]
                            }

                            
                            if (value) {
                                options = this.create_selector_options([{ label: value, value: value, selected: true }], value,"","",prefix,desc)
                            }
                            if (options) {
                                this.recreate_selector(select_id, s, options)
                            }
                            else {
                                this.recreate_selector(select_id, s, this.create_empty_option(true))
                            }
                        }
                        else { console.error("SELECTOR INITIALIZATION ERROR: Please give the selector a for attribute (Model Name)") }
                    }
                    else {
                        
                        let options = [{ value: "", label: "" }]
                        const selector_options = $(s).find('option')
                        let selected = $(s).attr('value') || null
                        if ($(s)?.attr('action-type') === 'multi-content-toggler') {
                            selected = this.utils.get_url_parameters()?.content_type?.trim()
                        }
                        if (!this.utils.is_empty_array(selector_options)) {
                            $.each(selector_options, (_, o) => {
                                options.push({ value: $(o).val(), label: $(o).text(), selected: selected === $(o).val() })
                            })
                            this.select_configs[select_id].options = options
                        }
                        if (!this.utils.is_empty_array(options)) {
                            this.recreate_selector(select_id, s, this.create_selector_options(options, selected))
                        }
                        // this.init_create_quick_form()
                    }
                }
                else { console.error("SELECTOR INITIALIZATION ERROR: Please give the selector a type (select or link)") }
            })
        }
    }

    add_on_change_functions(fun, cls, init_id){
        let exists = false
        if(lite.utils.array_has_data(this.on_select_change)){
            $.each(this.on_select_change,(_,obj)=>{
                if(obj.init_id && obj.init_id === init_id) exists=true
            })
            if(!exists) this.on_select_change.push({ fun: fun, cls: cls, init_id: init_id })
        }
        
        else
            this.on_select_change.push({ fun: fun, cls: cls, init_id: init_id })
    }

    create_selector_options(data, selected = '', fieldname = '', labelfield = '', prefix="", descriptions=[], postfix="") {
        let options = ''
        $.each(data, (_, d) => {
            const id = d.id || d.value
            const value = d[fieldname] || d.value, label = d[labelfield] || d[fieldname] || d.label
            const is_selected = selected === value
            let desc = ""
            if(descriptions && lite.utils.array_has_data(descriptions)){
                $.each(descriptions,(_,dsc)=>{
                    desc += `${d[dsc]} `
                })
            }
            if (value)
                options += `
                    <li value="${value}" id="${id}" class="option intro-yy hover:bg-default hover:text-white border-b ${is_selected ? 'active' : ''}">
                        <div class="flex flex-col">
                            ${label}
                            ${
                                desc ? `
                                    <small class="font-semibold text-gray-500 pb-2 flex items-center justify-start">
                                        <span class="material-symbols-outlined text-secondary_color mr-[0.5px] text-sm" style="font-size:15px !important"> info</span>
                                        ${prefix || ""} ${desc || ""} ${postfix || ""}
                                    </small>
                                ` :""
                            }
                        </div>
                        ${
                            is_selected ? '<span class="material-symbols-outlined check text-default">check_circle</span>' : ''
                        }
                    </li>
                `
        })
        return options || this.create_empty_option()
    }

    create_empty_option(is_error = false) {
        return `
            <li value="" class="empty-option hover:bg-white w-full h-[150px] intro-y">
                <div class="flex items-center justify-center flex-col w-full text-gray-500">
                    ${!is_error ?
                '<span class="material-symbols-outlined text-[40px] mb-4 text-gray-500" style="font-size:50px !important">box</span>No Data Found'
                :
                '<span class="material-symbols-outlined text-[40px] mb-4 mt-15 text-red-500" style="font-size:30px !important">warning</span><span class="text-red-700">An error occurred</span>'
            }
                </div>
            </li>
            <!--${this.add_create_new_record_btn()} -->
        `
    }
    recreate_selector(lite_id, selector, options) {
        const attrs = $(selector)[0]?.attributes
        const new_selector = $('<div>'), select = $(`<input>`)
        new_selector.addClass(`${$(selector).attr('class') || ''} select-field-wrapper min-h-[46px]`)
        select.addClass(`lite-field select-field ${$(selector).attr('class')?.includes('table-field') ? ' table-field ' : ''}`)
        select.attr("lite-id", lite_id)
        select.attr('placeholder', $(selector).attr('placeholder') || `Select ${this.utils.capitalize(this.utils.replace_chars($(selector).attr('for'), '_', ' '))}`)
        new_selector.attr('data-arial-expand', false)
        !this.utils.is_empty_array(attrs) > 0 && $.each(attrs, (_, att) => {
            att.name !== 'class' && att.name !== 'id' && att.name !== 'value' && new_selector.attr(att.name, att.value)
            att.name !== 'class' && att.name !== 'value' && select.attr(att.name, att.value)
            if (att.name === 'class') {
                att.name === 'class' && new_selector.addClass(att.value)
                const class_list = att?.value?.replaceAll('  ', '')?.replace(
                    /\b(\w*border\w*|\w*px-\w*|\w*max-w\w*|\w*max-h\w*|\w*shadow\w*|\w*mr-\w*|\w*w-\w*|\w*h-\w*|\w*rounded-\w*)\b/g, ''
                )
                select.addClass(class_list)
            }
        })
        new_selector.html(`
            <div class="inner-select-field-wrapper"><span class="material-symbols-outlined expand-field-shrink">expand_more</span></div>
            <div class="select-options-wrapper shadow-md"><ul class="select-options-list px-2">${options}</ul></div>
        `)
        
        new_selector.find(this.inner_select_field_wrapper).prepend(select)
        $(selector).replaceWith(new_selector)
        this.init_select_action(new_selector)
        new_selector.find('li.option.active')?.trigger('click')
        new_selector?.find("input")?.attr("prev-val", new_selector.find('li.option.active')?.attr("id") || "")
    }

    update_select_options(select, additional_options) {
        $(select).parents(this.selector_class_name).find(this.options_list_ul).append(additional_options)
    }

    init_select_action(select) {
        let selector_height = $(select).height()
        let tr = select?.parents(".table-row")
        let height = 200
        const
            selector_options_wrapper = $(select).find(this.options_wrapper),
            select_field = select.find(this.select_field)
            
        let top = selector_height
        let direction = "focused-bottom"
        let expand = "expanded-bottom"

        select_field.off("focusin").focusin((e) => {
            const prev_value = $(e.currentTarget)?.val()
            if(prev_value){
                $(e.currentTarget)?.attr("prev-val", prev_value)
            }

            $(e.currentTarget).parents(this.selector_wrapper)?.attr('data-arial-expand', true).addClass('active')
            $(e.currentTarget).siblings(this.icon_class).addClass('rotate').text('close')

            const border_properties = this.get_border_properties($(e.currentTarget).parents(this.selector_class_name))

            let selector_rect = $(select)[0].getBoundingClientRect();
            let select_bottom = selector_rect.bottom + 300
            let select_top = selector_rect.top + 300

            const wrapper_bound = lite.page_controller.main_content_wrapper[0]?.getBoundingClientRect()
            const wrapper_bottom = wrapper_bound?.bottom || 0
            const wrapper_top = wrapper_bound?.top || 0

            if (select_bottom > wrapper_bottom) {
                top = -90
                height = 90
                direction = "focused-top"
                expand = "expanded-top"
            } else {
                top = selector_height
                direction = "focused-bottom"
                expand = "expanded-bottom"
            }
            select.parents(".field-wrapper").addClass("wrapper-expand-top")

            tr?.addClass("table-row-expanded")
            
            selector_options_wrapper.css({
                left: -1,
                top: top,
                borderWidth: border_properties.width,
                borderColor: border_properties.color,
                borderStyle: border_properties.style,
                height:height
            }).addClass(expand)
            $(e.currentTarget).parents(this.selector_class_name).addClass(direction)
            this.populate_select_data(e.currentTarget)
            
        }).off("focusout").focusout((e) => {
            // if(!this?.ignore_collapse){
                tr?.removeClass("table-row-expanded")
                $(e.currentTarget).siblings(this.icon_class).removeClass('rotate').text('expand_more')
                selector_options_wrapper.find('.empty-option').remove()
                setTimeout(() => {
                    $(e.currentTarget).parents(this.selector_class_name).removeClass("focused-top focused-bottom")
                    select.parents(".field-wrapper").removeClass("wrapper-expand-top")
                    selector_options_wrapper.css({
                        top: 0,
                        left: 0,
                        borderWidth: 0,
                        borderColor: 0,
                        borderStyle: 'none',
                        height:0
                    }).removeClass(expand)
                    $(e.currentTarget).parents(this.selector_wrapper)?.attr('data-arial-expand', false).removeClass('active')
                    $(e.currentTarget).parents(this.selector_wrapper).find(this.option_class).removeClass('hidden')
                }, 310);
            // }
        })?.off("keyup").keyup((e) => {
            const search_value = e.currentTarget.value?.toLowerCase()?.trim() || null
            let opt_val = '', has_matched = false
            const opts = $(e.currentTarget).parents(this.selector_wrapper).find(this.option_class)
            opts.removeClass('active').find(this.icon_class).remove()
            if (search_value) {
                $(opts).addClass('hidden')
                if (!this.utils.is_empty_array(opts) > 0) {
                    $.each(opts, (_, o) => {
                        opt_val = $(o).attr('value')?.toLowerCase()?.trim()
                        if (opt_val.includes(search_value)) {
                            has_matched = true
                            $(o).removeClass('hidden')
                        }
                    })
                    if (!has_matched) {
                        if (this.utils.is_empty_array(selector_options_wrapper.find('.empty-option'))) {
                            selector_options_wrapper.find(this.options_list_ul).append(this.create_empty_option())
                        }
                    }
                    else selector_options_wrapper.find('.empty-option').remove()
                }
            }
            else {
                selector_options_wrapper.find('.empty-option').remove()
                $(opts).removeClass('hidden')
            }
        })

        // to preserve scroller on the options
        $(this.selector_wrapper)?.off("mousedown").mousedown(e=>{
            if($(e.target)?.hasClass("select-options-wrapper")){
                this.ignore_collapse = true
            }
        })?.off("mouseup").mouseup(e=>{
            if($(e.target)?.hasClass("select-options-wrapper")){
                this.ignore_collapse = false
            }
        })
        

        $(this.inner_select_field_wrapper).find('.expand-field-shrink').off('click').click(e => {
            const parent = $(e.currentTarget).parents(this.selector_class_name)
            if (parent?.hasClass('focused')) {
                $(e.currentTarget).siblings('input')?.val('')?.trigger('change')
            }
            else {
                $(e.currentTarget).siblings('input').focus()
            }

        })

        this.init_option_selection_action(select, select_field)

        // if there is any change event listeners available 
        select_field?.off('change').on('change', async(e) => {
            const prev_val = await lite.utils.delay_until(()=>{ if($(e?.currentTarget)?.attr("prev-val")) return $(e?.currentTarget)?.attr("prev-val")?.trim()},1000)
            const value = $(e?.currentTarget)?.val()?.trim()
            let is_first_value = $(e?.currentTarget)?.attr("is-first-val")
            if(is_first_value === undefined){
                is_first_value = true
                $(e?.currentTarget)?.attr("is-first-val", 0)
            }
            
            if(prev_val != value || is_first_value === true){
                $(e?.currentTarget)?.attr("prev-val", value)
                if (!this.utils.is_empty_array(this.on_select_change)) {
                    if (this.utils.is_empty_array($(e.currentTarget).parents(this.selector_wrapper).find(`${this.option_class}[value="${value}"]`))) {
                        $(e.currentTarget)?.val('')
                    }
                    await this.handle_fetch_from(e.currentTarget, $(e.currentTarget)?.val())
                    const attrs = $(e.currentTarget)[0]?.attributes
                    let obj = {
                        value_id: $(e.currentTarget).parents(this.selector_wrapper).find(`${this.option_class}[value="${value}"]`)?.attr("id") || '',
                        prev_value:prev_val,
                        is_first_value:is_first_value,
                        value: e.currentTarget.value,
                        wrapper: select,
                        field: e.currentTarget
                    }
                    !this.utils.is_empty_array(attrs) && $.each(attrs, (_, att) => {
                        obj[att.name] = att.value
                    })
                    $.each(this.on_select_change, (_, f) => f?.fun(obj, f?.cls))
                }
            }
        })
    }

    get_select_properties(select_field) {
        if (select_field) {
            return {
                ...this.select_configs[$(select_field).attr("lite-id")],
                value: $(select_field).val(),
            }
        }
        return false
    }

    update_select_filters(selector, filters={}){
        console.log(selector, filters)
    }

    update_table_select_filters(table_name, field_name, filters={}){
        console.log(selector, filters)
    }

    populate_select_data(target) {
        const params = this.get_select_properties(target)
        if (params.select_type === 'link') {
            this.toggle_loader(target)
            this.get_selector_data(params.model, params.filters, [params.fieldname]).then(r => {
                this.toggle_loader(target, true)
                if (!r) {
                    this.update_select_options(target, this.create_empty_option(false))
                }
                else {
                    if (!this.utils.is_empty_array(r)) {
                        const options = this.create_selector_options(r, params?.value || '', params?.fieldname || 'name', "", "", params.descriptions)
                        if (options) {
                            this.update_select_options(target, options)
                            this.init_select_action(this.get_select_wrapper(target))
                        }
                    }
                    else {
                        this.update_select_options(target, this.create_empty_option())
                    }
                }
            })
        }
    }

    init_option_selection_action(select, select_field) {
        select.find(this.option_class).off("click")?.click((e) => {
            $(e.currentTarget).parents(this.selector_wrapper)?.find(this.select_field).val($(e.currentTarget).attr('value'))
            this.create_check(e.currentTarget)
            select_field.trigger('change')
        })

        // if there is a default page content type in place
        const active = select.find('li.option.active')
        if (!this.utils.is_empty_array(active)) {
            const action_type = this.utils.get_attribute(select, 'action-type')
            if (action_type) {
                select_field.trigger('change')
            }
        }
    }

    create_check(option) {
        $(option).siblings().removeClass('active').find(this.icon_class).remove()
        $(option).addClass('active').find(this.icon_class).remove()
        $(option).append(`<span class="material-symbols-outlined check active-option text-default">check_circle</span>`)
    }

    toggle_loader(target, remove) {
        $(target).parents(this.selector_class_name).find(this.options_list_ul).empty()
        if (!remove) {
            $(target).parents(this.selector_class_name).find(this.options_list_ul).append(`
                <div class="select-loader intro-y flex items-center justify-center h-[140px]">
                    ${this.utils.generate_loader({ loader_type: "dots" })} Fetching..
                </div>
            `)
        }

    }

    get_select_wrapper(select){
        return $(select).parents(this.selector_class_name)
    }

    get_select_value(selector) {
        if (typeof selector !== "string") {
            return $(selector).find("input").val() || $(selector).val()
        }
        else{
            return $(this.get_select_field(selector))?.find("input")?.val()
        }
            
    }
    get_select_field(fieldname) {
        const field = $(`div[fieldname="${fieldname}"]`)
        if(lite.utils.array_has_data(field)){
            return field[0]
        }
        return false
    }


    set_selected_value(selector, value, trigger_change_event=true) {
        const  select_field = $(selector).find("input"), select_property = this.get_select_properties(select_field)
        if(select_property && value){
            const option = this.create_selector_options([{label:value,value:value,is_selected:true}],value)
            this.update_select_options(select_field, option)
            select_field.val(value)
            if(trigger_change_event){
                select_field.trigger('change')
            }
        }
    }

    async get_selector_data(link, filters, columns = ['name']) {
        return lite.connect.get({ model: link, is_select: true, filters: filters, columns: columns, "fetch-lite":true }).then(resolve => {
            if (resolve.status === lite.status_codes.ok) {
                return resolve.data?.rows || []
            }
            return false
        })
    }
    get_border_properties(el) {
        return {
            width: el.css('border-width'),
            color: el.css('border-color'),
            style: el.css('border-style')
        }
    }


    add_create_new_record_btn(model){
        return `
            <button class="lite-selector-quick-form-btn w-full my-2 pt-2 border-t text-default mx-auto flex items-center justify-center"> 
            <span class="material-symbols-outlined mr-1"> add_circle </span>
                Create New 
            </button>
        `
    }

    init_create_quick_form(){
        $(".lite-selector-quick-form-btn")?.off("click")?.click(e=>{
            alert()
        })
    }

    async handle_fetch_from(field, value) {
        const doc_data = {}
        let doc = {}
        let data = {}
        let new_data = {}
        if (value) {
            const id = this.utils.get_attribute(field, 'id'), model = this.utils.get_attribute(field, 'for')
            let fetch_from_fields = ''
            if (this.utils.is_empty_array($(field).parents("form"))) {
                fetch_from_fields = $(field).parents(".main-content-wrapper").find(`.lite-field[fetch-from="${id}"]:not(.table-field)`)
            }
            else if (!$(field).hasClass('table-field')) {
                fetch_from_fields = $(field).parents("form").find(`.lite-field[fetch-from="${id}"]:not(.table-field)`)
            }
            else {
                fetch_from_fields = $(field).parents(".table-row").find(`.lite-field[fetch-from="${id}"]`)
            }
            if (!this.utils.is_empty_array(fetch_from_fields) && model) {
                if (doc_data && !lite.utils.is_empty_object(doc_data)) {
                    data = doc_data
                }
                else {
                    if(this.temp_select_values[model] && this.temp_select_values[model][value]){
                        doc = this.temp_select_values[model][value]
                    }
                    else{
                        let result = await this.connect.get_doc(model, value)
                        if (result.status === lite.status_codes.ok) {
                            doc = result.data
                            if(!this.temp_select_values[model]){
                                this.temp_select_values[model] = {}
                            }
                            this.temp_select_values[model][value] = doc
                        }
                        else {
                            console.error(`Failed to fetch dynamic data ${result}`)
                        }
                    }
                }
                if (!lite.utils.is_empty_object(doc)) {
                    $.each(fetch_from_fields, (_, f) => {
                        const
                            fetch_field = this.utils.get_attribute(f, 'fetch-field'),
                            field_type = this.utils.get_attribute(f, 'type'),
                            always_fetch = this.utils.get_attribute(f, 'always-fetch')
                        if (fetch_field) {
                            const v = doc[fetch_field]
                            if (field_type && field_type?.trim() === 'link' || field_type && field_type?.trim() === "select") {
                                this.set_selected_value($(f).parents(this.selector_class_name), v)
                            }
                            else if (field_type?.trim() === 'read-only') {
                                $(f).attr('value', v).text(v)
                            }
                            else {
                                $(f).val(v).trigger('change').trigger('focusout')
                            }
                        }
                    })
                }
                else {
                    $.each(fetch_from_fields, async (_, f) => {
                        const
                            fetch_field = this.utils.get_attribute(f, 'fetch-field'),
                            field_type = this.utils.get_attribute(f, 'type'),
                            always_fetch = this.utils.get_attribute(f, 'always-fetch')
                        if (fetch_field) {
                            let v = data[fetch_field]
                            if(!v){
                                const fn = lite.utils.get_attribute(field,"fieldname")
                                if (data && !lite.utils.is_empty_object(data.linked_fields)){
                                    const link_obj = data.linked_fields[fn]
                                    if( link_obj && !lite.utils.is_empty_object(link_obj)){
                                        v = link_obj[fetch_field]
                                    }
                                    else{
                                        // console.log(new_data)
                                        if(!lite.utils.is_empty_object(new_data)){
                                            let t_value = new_data[fetch_field] || false
                                            if(t_value){
                                                console.log("hi dadada")
                                            }
                                        }
                                        else{
                                            let result = await this.connect.get_doc(model, value)
                                            console.log(result)
                                            if (result.status === lite.status_codes.ok) {
                                                new_data = result.data
                                                v = new_data[fetch_field]
                                            }
                                            else {
                                                console.error(`Failed to fetch dynamic data ${result}`)
                                            }
                                        }
                                    }
                                }
                            }
                            if (field_type && field_type?.trim() === 'link' || field_type && field_type?.trim() === "select") {
                                this.set_selected_value($(f).parents(this.selector_class_name), v)
                            }
                            else if (field_type?.trim() === 'read-only') {
                                if(lite.form_state !== 1)
                                    $(f).attr('value', v).text(v)
                            }
                            else {
                                if (!$(f).val()) {
                                    $(f).val(v).trigger('change').trigger('focusout')
                                }
                            }
                        }
                    })
                }

            }
        }
    }
}

