import HTML_Builder from '../html/html_builder.js'
import Validator from './validator.js'
let class_obj = undefined

export default class Form_Controller {
    constructor(config) {
        this.page_controller = config?.page_controller
        this.session = config?.session
        this.connect = config?.connect
        this.lite_picker = config?.lite_picker
        this.page_session = ''
        this.content_type = ''
        this.doc_name = ''
        this.doc_data = ''
        this.page_type = ''
        this.html_bulder = new HTML_Builder(config)
        this.validator = new Validator(lite.utils.copy_dict(config))
        this.form_setup = null
        this.overrides = null
        this.alerts = config?.alerts
        this.form_fields_extender = null
        this.on_load = null
        this.custom_validation = null
        this.on_field_change = null
        this.on_scan = null
        this.on_row_select = null
        this.before_save = null
        this.after_save = null
        this.before_update = null
        this.after_update = null
        this.before_submit = null
        this.after_submit = null
        this.before_cancel = null
        this.after_cancel = null
        this.on_row_remove = null
        this.model = null
        this.setup = null
        this.workflow_actions = {}
        this.dropdown_actions = {}
        this.dropdown_list = []
        this.form_actions = {}
        this.form_action_functions = {}
        this.is_new_form = true
        this.is_saved = false
        this.is_submittable = false
        this.is_submitted = false
        this.has_child_tables = false
        this.child_tables = {}
        this.selected_child_table_rows = {}
        this.$form = null
        this.form_id = null
        this.$form_fields = null
        this.$form_actions_wrapper = $(".page-actions-wrapper").find(".content-group.form-content-view")
        this.table_wrapper_class_name = '.table-wrapper'
        this.table_head_class_name = '.thead'
        this.table_body_class_name = '.tbody'
        this.table_row_class_name = '.tr'
        this.table_cell_class_name = '.tc'
        this.table_field_class_name = '.table-field, .select-field'
        this.form_field_class_name = '.form-field'
        this.row_check_box_class_name = '.row-check'
        this.head_row_check_box_class_name = '.row-check.head-check'
        this.child_table_add_remove_action_btn = '.add-remove-action-btn'
        this.$save_btn = null
        this.$submit_btn = null
        this.$update_btn = null
        this.on_save = null
        this.on_submit = null
        this.on_cancel = null
        this.on_validate = null
        this.form_data = {}
        this.form_action_options = {}
        this.workflow = {}
        this.common_field_types = ["text", "longtext", "int", "currency", "percentage", "float","password","color", "rate"]
        this.numeric_fields_types = ["int", "currency", "percentage", "float", "rate"]
        this.selected_items = []
        this.table_actions = {}
        this.prefetched_data = {}

        // child table pagination
        this.child_table_page_size = 8
        this.child_table_pagination = {}
        this.child_table_data = {}

    }
    async init_form(config, is_quick_form=false, on_quick_form_save=null, quick_form_modal_id=null, default_data=null) {
        this.is_quick_form = is_quick_form
        this.quick_form_data = default_data
        this.reset_form()
        let form_setup = config
        if(!form_setup){
            form_setup = await lite.utils.import_form_content()
            // handle if we are preloading from another form
            if (form_setup?.form_customizer){
                const old_setup = {...form_setup}
                const {data, model_path, extra_form_setup} = await form_setup?.form_customizer(form_setup)
                if(model_path && lite.utils.object_has_data(model_path)){
                    form_setup = await lite.utils.import_form_content(model_path?.module, model_path?.content_type)
                    form_setup.setup = {
                        ...form_setup?.setup,
                        ...old_setup?.setup,
                        ...extra_form_setup || {}
                    }
                    form_setup.setup.model = lite.utils.replace_chars(model_path?.content_type, " ","_")
                    lite.page_controller?.content_type_title?.html(lite.utils.capitalize(lite.utils.replace_chars(model_path?.content_type, "_"," ")))
                    if(form_setup?.form_actions){
                        delete form_setup.form_actions
                    }
                }
                lite.session.set_session("content_type", model_path?.content_type)
                if(lite.utils.object_has_data(data)){
                    this.prefetched_data  = {status:lite.status_codes.ok, data:data}
                }
            }
        }
        if(form_setup){
            if (form_setup.setup?.fetch_fields_from_backend){
                const {status, data, error_message} = await lite.connect.get_form_fields({model:form_setup.setup?.model, doc: lite.utils.get_url_parameters("doc") || ""})
                if(status == lite.status_codes.ok){
                    if(data.fields){
                        form_setup.fields = data.fields || {}
                        lite.default_form_data = data.data || {}
                    }
                }
            }
            this.form_setup = {...form_setup}
            this.form_data = {}
            this.form_buttons = []
            this.page_session = lite.session.get_page_session()
            this.content_type = this.page_session.content_type
            this.page_type = this.page_session.page
            this.on_quick_form_save = on_quick_form_save
            this.$quick_form_save_btn = $(".modal-action-btn[action='save']")
            if (this.page_type === 'info' || this.page_type === 'new-form' || is_quick_form) {
                this.doc_data = {}
                this.doc_name = this.page_session?.doc
                if (this.content_type) {
                    const
                        form_config = this.form_setup,
                        setup = lite.utils.copy_object(form_config?.setup),
                        fields = lite.utils.copy_object(form_config?.fields),
                        fid = this.page_type === 'info' && !is_quick_form ? setup?.info_form_id : setup?.new_form_id
                    this.fields = [...form_config?.fields]
                    if (fid) {
                        this.model = setup?.model
                        await this.#load_overrides()
                        this.form_id = !is_quick_form ? $(`#${fid}`) : `#${quick_form_modal_id} #${fid}`
                        if (setup?.model) {
                            this.setup = setup
                            this.form_buttons = form_config?.form_buttons
                            this.form_actions = form_config.form_actions
                            this.dropdown_actions = {}
                            this.dropdown_list = []
                            this.is_submittable = setup.is_submittable || false
                            this.on_save = setup?.on_save || null
                            this.on_submit = setup?.on_submit || null
                            this.on_cancel = setup?.on_cancel || null
                            this.on_validate = setup?.on_validate || null
                            this.has_child_tables = false
                            this.on_scan = form_config?.on_scan || null
                            this.child_tables = {}
                            this.$form =  $(this.form_id)
                            this.$form_fields = this.$form.find(".form-fields")
                            this.$form_header = this.$form?.find(".form-header")
                            this.$form_header?.addClass("border-b mb-5")?.find(".inner-form-actions")?.remove()
                            this.$active_content_group = $(".content-group.active:not(.info-actions)")
                            if(this.setup?.custom_render && typeof this.setup?.custom_render === "function"){
                                this.setup?.custom_render(this.doc_data, this)
                            }
                            else{
                                if (this.$form) {
                                    this.$form.find('.form-title').text(`${this.page_type === 'new-form' ? 'New' : ''} ${setup.title || setup.model}`)
                                    if (this.$form_fields) {
                                        this.$form.addClass("relative mih-h-[30vh]").find(".dynamic-loader").remove().append(lite.utils.generate_loader({size:20,title:"Preparing Form", loader_type:"dots"}))
                                        this.get_opened_document().then(async status => {
                                            if (status) {
                                                this.$form.removeClass("relative mih-h-[30vh]").find(".dynamic-loader").remove()
                                                this.$form_fields.empty()
                                                lite.utils.add_class(this.$form_fields, `grid-cols-${setup.layout_columns || 2}`)
                                                if (this.fields && !lite.utils.is_empty_array(this.fields)) {
                                                    await this.extend_columns()
                                                    this.fields.map(async (field, idx) => {
                                                        const f = {...field}
                                                        if (f.fieldtype === 'table') {
                                                            this.has_child_tables = true
                                                            this.child_tables[f.model] = f
                                                            // add table actions for the row
                                                            this.table_actions[f.fieldname] = {
                                                                // "Insert Above":{ "title": "Insert Above", "icon": "arrow_upward", "icon_color": "indigo", action: this.insert_above_table_row, "for_docstatus": [0], "at_index": 0 },
                                                                // "Insert Below":{ "title": "Insert Below", "icon": "arrow_downward", "icon_color": "pink", action: this.insert_below_table_row, "for_docstatus": [0], "at_index": 1 },
                                                                // "Duplicate Row":{ "title": "Duplicate Row", "icon": "content_copy", "icon_color": "teal", action: this.duplicate_table_row, "for_docstatus": [0], "at_index": 2 },
                                                                "Remove Row":{ "title": "Remove Row", "icon": "delete", "icon_color": "orange", action: this.remove_table_row, "for_docstatus": [0], "at_index": 3 },
                                                            }
                                                            if(f.table_actions && lite.utils.array_has_data(f.table_actions)){
                                                                $.each(f.table_actions,(_, act)=>{
                                                                    this.table_actions[f.fieldname][act.title] = act
                                                                })
                                                            }
                                                            f.table_actions = this.table_actions[f.fieldname]
                                                        }
                                                        f.idx = idx
                                                        await this.#append_field(lite.utils.copy_object(f))
                                                    })
                                                } else console.error(`FORM GENERATION ERROR: Form fields not included!`)
                                                this.#init_form_actions()
                                                this.init_field_change_event_listener()
                                            } else {
                                                console.error("An error occurred while fetching the data.")
                                            }
                                            // keep a copy of the current class object
                                            class_obj = this
                                            this.#disable_form_submission()
                                            this.update_actions()
                                            this.enable_table_row_actions()
                                            lite.lite_selector.init_selectors(this.handle_select_change, this)
                                            lite.lite_file_picker.init_file_picker(this.handle_file_change, this)
                                            lite.lite_date_picker.init(this.handle_date_picker_change, this)
                                            lite.lite_time_picker.init(this.handle_time_picker_change, this)
                                            lite.lite_year_picker.init(this)
                                            lite.lite_switch.init_switch_fields(this.handle_permission_change,this)
                                            lite.expandable_field.init()
                                            this.#init_on_load_events()
                                            lite.lite_commands.init_form_commands(this)
                                            lite.code_editor.init_code_editors()
                                            lite.rich_editor.init_rich_editors()
                                            lite.utils.init_password_fields()
                                            lite.form_controller = this
                                            return true
                                        })
                                    } else console.error(`FORM GENERATION ERROR: Form fields wrapper not found for ${setup.model} form!`)
                                } else console.error(`FORM GENERATION ERROR: No FORM by id '${setup.form_id}'  for ${setup.model} found!`)
                            }
                        } else console.error("FORM GENERATION ERROR: Model not defined in the form  setup!")
                    } else console.error("FORM GENERATION ERROR: Please give the form an ID")
                } else console.error("FORM GENERATION ERROR: Page content type not defined!")
            }
        }
        // handle scanner
        if(this.on_scan){
            lite.scanners.barcode.add_scanner_event(this.on_scan, this)
        }
        return true
    }

    #disable_form_submission(){
        this.$form?.submit(function(event){
            return false
        })
    }

    // LOAD FORM HOOK OVERRIDES
    async #load_overrides(){
        const overrides = await lite.utils.import_form_overrides()
        if(overrides){
            this.overrides = overrides
            this.form_fields_extender = this.overrides?.form_fields_extender
        }
        this.#load_events()
    }

    // extend fields if required
    async extend_columns(){
        this.form_fields_extender = this.overrides?.form_fields_extender
        if(this.form_fields_extender){
            const new_fields = await this.form_fields_extender(this, this.fields)
            if(new_fields && lite.utils.is_object(new_fields) && !lite.utils.is_empty_array(new_fields)){
                this.fields = new_fields
            }
        }
    }

    reset_form() {
        if(!this.is_quick_form){
            $(".form-fields").empty()
            $(".audit-trail-wrapper, .preview-wrapper").remove()
            this.form_setup = {}
            this.form_data = {}
            this.page_session = null
            this.content_type = null
            this.page_type = null
            this.doc_data = {}
            this.doc_name = null
            this.model = null
            this.setup = null
            this.form_actions = null
            this.dropdown_actions = {}
            this.dropdown_list = []
            this.is_submittable = false
            this.on_save = null
            this.on_submit = null
            this.on_cancel = null
            this.on_validate = null
            this.has_child_tables = false
            this.child_tables = {}
            this.$form = null
            this.$form_fields?.empty()
            // this.$form_fields = null
            this.has_child_tables = false
            this.child_tables = []
            this.on_load = null
            this.custom_validation = null
            this.on_field_change = null
            this.on_scan = null
            this.on_row_select = null
            this.before_save = null
            this.after_save = null
            this.before_update = null
            this.after_update = null
            this.before_submit = null
            this.after_submit = null
            this.before_cancel = null
            this.after_cancel = null
        }
    }

    async #append_field(field_info){
        field_info.docstatus = this.doc_data?.docstatus || 0
        field_info.editableonsubmit = field_info?.editableonsubmit || false
        field_info.placeholder = field_info.placeholder || field_info.fieldlabel
        field_info.hidden = this.validate_display_field(field_info)
        const fieldname = field_info.fieldname
        if(field_info.fieldtype === "table"){
            this.child_table_data[fieldname] = []
            this.child_table_pagination[fieldname] = {  total_pages: 1,  total_records: 0,  current_page: 1,  start: 0,  end:1 }
            this.validate_table_display_field(field_info)
        }
        if (lite.utils.object_has_data(this.doc_data)) {
            if(field_info.fieldtype !== "table"){
                const val = this.doc_data[field_info?.fieldname]
                field_info.value = val || val == 0 ? this.doc_data[field_info?.fieldname] : field_info.default || ''
            }
            else{
                if(lite.utils.array_has_data(this.doc_data[fieldname])){
                    this.child_table_data[fieldname] = []
                    $.each(this.doc_data[fieldname], (i, row) => {
                        row.row_id = lite.utils.unique()
                        this.child_table_data[fieldname].push(row)
                    })
                    // compute pagination data for child tables
                    const
                        total_records = this.child_table_data[fieldname].length,
                        total_pages = Math.ceil(total_records/this.child_table_page_size),
                        start = (1 - 1) * this.child_table_page_size,
                        end   = start + this.child_table_page_size
                    this.child_table_pagination[fieldname] = { 
                        total_pages: total_pages || 1, 
                        total_records:total_records, 
                        current_page: 1, 
                        start:start, 
                        end:end
                    }
                    const new_rows = this.child_table_data[fieldname]?.slice(start, end)
                    new_rows.forEach((row, i) => new_rows[i].current_page_index = start + i)
                    field_info.rows = new_rows
                    field_info.total_pages
                }
                else{
                    this.child_table_data[fieldname] = []
                    this.child_table_pagination[fieldname] = {  total_pages: 1,  total_records: 0,  current_page: 1,  start: 0,  end:1 }
                }
            }
        }
        else{
            field_info.value = field_info.value || field_info.default || ''
        }
        field_info.workflow = this.workflow
        if(field_info.fieldtype !== "table"){
            this.$form_fields.append(this.html_bulder.build_form_field(field_info, this.setup, this.form_data?.docstatus))
        }
        else{
            const {wrapper, rows_data} = this.html_bulder.create_child_table(field_info, this.setup?.layout_columns || 2)
            this.$form_fields.append(wrapper)
            if(rows_data && lite.utils.array_has_data(rows_data)){
                this.child_table_data[field_info.fieldname]?.push(...rows_data)
            }
        }
    }

    #load_events() {
        this.events = {}
        this.events[this.model] = {
            on_load : this.overrides?.on_load,
            custom_validation : this.overrides?.custom_validation,
            on_field_change : this.overrides?.on_field_change,
            on_row_select : this.overrides?.on_row_select,
            before_save : this.overrides?.before_save,
            after_save : this.overrides?.after_save,
            before_update : this.overrides?.before_update,
            after_update : this.overrides?.after_update,
            before_submit : this.overrides?.before_submit,
            after_submit : this.overrides?.after_submit,
            before_cancel : this.overrides?.before_cancel,
            after_cancel : this.overrides?.after_cancel,
            on_row_add : this.overrides?.on_row_add,
            on_row_remove : this.overrides?.on_row_remove,
        }
    }
    #init_on_load_events() {
        const onload = this.events[this.model]?.on_load
        if (onload && onload?.length > 0) {
            $.each(onload, (_, f) => {
                f({
                    utils: lite.utils,
                    connect: this.connect,
                    form: this.$form,
                    controller: this,
                    setup: this.setup,
                    data: this.get_form_data()?.values || {}
                })
            })
        }
    }
    #init_form_actions() {
        this.#init_row_check_actions()
        this.#init_add_remove_row_action()
    }
    #init_row_check_actions() {
        this.$form_fields.find(this.table_wrapper_class_name)?.map((_, wr) => {
            $(wr).find(this.row_check_box_class_name)?.unbind("change")?.change(e => {
                const for_row = lite.utils.get_attribute(e.target, 'for')
                if (for_row == 'head-row') {
                    if ($(e.target).prop('checked')) {
                        $(wr).find(this.row_check_box_class_name).prop('checked', true)
                    } else {
                        $(wr).find(this.row_check_box_class_name).prop('checked', false)
                    }
                }
                if (!$(e.target).prop('checked')) {
                    $(wr).find(this.head_row_check_box_class_name)?.prop('checked', false)
                }
                this.#get_selected_rows()
                if (!lite.utils.is_empty_array(this.events[this.model]?.on_row_select)) {
                    $.each(this.events[this.model]?.on_row_select, (_, fn) => fn({
                        setup: this.setup,
                        selected_rows: this.selected_child_table_rows
                    }))
                }
            })
        })
    }

    generate_row_from_table_fields(fields){

    }

    #init_add_remove_row_action() {
        this.table_row_controller_btns = {}
        this.$form_fields.find(this.table_wrapper_class_name)?.map((_, wr) => {
            const model_type = lite.utils.get_attribute(wr, 'for'), table_field_name = lite.utils.get_attribute(wr, 'fieldname')
            const btns = $(wr).find(this.child_table_add_remove_action_btn)
            this.table_row_controller_btns[this.child_tables[model_type]?.fieldname] = lite.utils.array_has_data(btns) ? {remove: $(btns[0]), add: $(btns[1])} : {}
            $(wr).find(this.child_table_add_remove_action_btn)?.off("click")?.click(e => {
                e.preventDefault()
                const 
                    action = lite.utils.get_attribute(e.currentTarget, 'action'),
                    table = $(e.currentTarget).parents('[fieldtype="table"]')
                let jump_to_last_page=false
                if (action === 'add') {
                    jump_to_last_page=true
                    table.hasClass('border-red-600') ? table.removeClass('border-red-600') : ''
                    const {row_element, row_data} = this.html_bulder.create_table_row(this.child_tables[model_type], true, true)
                    this.child_table_data[this.child_tables[model_type]?.fieldname]?.push(row_data)
                    if (this.events[this.model]?.on_row_add && !lite.utils.is_empty_array(this.events[this.model]?.on_row_add)) {
                        $.each(this.events[this.model]?.on_row_add, (_, f) => {
                            f({ form: this.$form, controller: this, connect: this.connect })
                        })
                    }
                    lite.lite_selector.init_selectors()
                    lite.lite_date_picker.init()
                    lite.lite_time_picker.init()
                    lite.lite_year_picker.init(this)
                    lite.lite_switch.init_switch_fields()
                    lite.expandable_field.init()
                    lite.utils.init_password_fields()
                    this.#init_row_check_actions()
                    this.init_field_change_event_listener()
                    this.enable_table_row_actions()

                    const table_dependents = this.$form.find(`div.th[display-on]`)
                    if(table_dependents && lite.utils.array_has_data(table_dependents)){
                        table_dependents.map((_,d)=>{
                            const display_on = lite.utils.get_attribute(d, "display-on")
                            const value = this.get_form_value(display_on)
                            this.display_or_hide_dependant_fields(display_on, value,true)
                        })
                    }

                } else {
                    this.#get_selected_rows()
                    let rows_to_be_removed = [], ids_to_be_removed = []
                    $.each(this.selected_child_table_rows[model_type], (_, r) => {
                        $(r.element).remove()
                        const row_to_be_deleted = this.child_table_data[table_field_name]?.find(ct=>ct?.row_id == $(r.element)?.attr("id"))
                        rows_to_be_removed.push(row_to_be_deleted)
                        ids_to_be_removed.push(row_to_be_deleted.row_id)
                    })
                    $(wr).find(this.head_row_check_box_class_name)?.prop('checked', false)
                    if (this.events[this.model]?.on_row_remove && !lite.utils.is_empty_array(this.events[this.model]?.on_row_remove)) {
                        $.each(this.events[this.model]?.on_row_remove, (_, f) => {
                            f({
                                form: this.$form,
                                controller: this,
                                connect: lite.connect,
                                rows: rows_to_be_removed
                            })
                        })
                    }
                    this.child_table_data[table_field_name] = this.child_table_data[table_field_name]?.filter(row=>!ids_to_be_removed?.includes(row?.row_id))
                }
                this.populate_child_table(table_field_name, this.child_table_data[table_field_name],false,true,true, jump_to_last_page)
            })
            // add pagination actions
            this.#add_table_pagination(table_field_name)
        })
        this.#init_pagination_actions()
    }

    #calculate_pagination_visible_numbers(current_page, total_pages){
        let range = []
        let start = Math.max(1, current_page - 3)
        let end = Math.min(total_pages, current_page + 3)
        for (let i = start; i <= end; i++) { range.push(i)}
        return range
    }

    #add_table_pagination(table_field_name){
        const 
            tr = this.$form_fields.find(`${this.table_wrapper_class_name}[fieldname="${table_field_name}"]`), 
            page_stats = this.child_table_pagination[table_field_name],
            page_range = this.#calculate_pagination_visible_numbers(page_stats.current_page, page_stats.total_pages)
        tr?.find(".child-table-pagination")?.html(lite.html_generator.create_pagination({
            total_pages: page_stats.total_pages,
            current_page: page_stats.current_page,
            page_size: this.child_table_page_size,
            total_records: page_stats.total_records,
            queried_total: page_stats.end,
            page_range: page_range,
            include_page_jump:false,
            include_page_size_changer:false,
            scale:0.9
        }))
    }

    #init_pagination_actions(){
        $(document).off("click", ".child-table-pagination .paginate-select")
        $(document).on("click", '.child-table-pagination .paginate-select', async (e) => {
            e.preventDefault()
            const 
                tr = $($(e?.currentTarget).parents(".lite-field.table-wrapper")[0]),
                table_field_name = lite.utils.get_attribute(tr, "fieldname")
            const next_page = lite.utils.string_to_int(lite.utils.get_attribute(e.currentTarget, 'index'))
            if (parseInt(next_page) !== this.child_table_pagination[table_field_name]?.current_page) {
                tr?.find(".pagination_wrapper").find(".active").removeClass("active bg-default").find("span").removeClass("text-white font-bold")
                $(e.currentTarget).addClass("active bg-default").find("span").addClass("text-white font-bold")

                // update pagination
                this.child_table_pagination[table_field_name].current_page = parseInt(next_page)
                this.child_table_pagination[table_field_name].start = (this.child_table_pagination[table_field_name].current_page - 1) * this.child_table_page_size
                this.child_table_pagination[table_field_name].end = this.child_table_pagination[table_field_name].start + this.child_table_page_size
                const 
                    page_stats = this.child_table_pagination[table_field_name],
                    page_range = this.#calculate_pagination_visible_numbers(page_stats.current_page, page_stats.total_pages)
                tr?.find(".child-table-pagination")?.html(lite.html_generator.create_pagination({
                    total_pages: page_stats.total_pages,
                    current_page: page_stats.current_page,
                    page_size: this.child_table_page_size,
                    total_records: page_stats.total_records,
                    queried_total: this.child_table_page_size,
                    page_range: page_range,
                    include_page_jump:false,
                    include_page_size_changer:false,
                    scale:0.9
                }))

                const new_rows = this.child_table_data[table_field_name]?.slice(page_stats.start,page_stats.end)
                new_rows.forEach((row, i) => new_rows[i].current_page_index = page_stats.start + i)
                this.populate_child_table(table_field_name, new_rows, false, false, true)
            }
        })
    }

    add_new_table_row(table_name,values,trigger_event_change=true){
        this.table_row_controller_btns[table_name]?.add?.trigger("click")
        let row_data = this.get_table_row(table_name,null,null,true)
        if(row_data && values && lite.utils.is_object(values)){
            $.each(lite.utils.get_object_keys(row_data),(_,k)=>{
                if(values[k]){
                    this.set_form_table_value(table_name,row_data[k].row_id,row_data[k].field, values[k],null,trigger_event_change)
                }
            })  
        }
        return this.get_table_row(table_name,null,null,true)
    }

    remove_table_row(row_id){
        console.log("yet to be implemented")
    }

    #get_selected_rows() {
        this.$form_fields.find(this.table_wrapper_class_name)?.map((_, wr) => {
            const table_type = lite.utils.get_attribute(wr, 'for')
            let new_values = []
            $(wr).find(this.table_body_class_name)?.find(this.table_row_class_name)?.map((_, tr) => {
                if ($(tr).find(this.row_check_box_class_name)?.prop('checked')) {
                    let row = {}
                    $(tr).find(this.table_field_class_name)?.map((_, f) => {
                        row[lite.utils.get_attribute(f, 'fieldname')] = lite.utils.get_field_value(f)
                    })
                    new_values.push({
                        element: tr,
                        values: row
                    })
                }
            })
            this.selected_child_table_rows[table_type] = new_values
        })

    }

    refresh_form(data) {
        data.form_controller?.init_form()
    }



    duplicate_form(data) {
        const cls = data.form_controller
        delete data.values?.id
        delete data.values?.name
        data.values.status = "Active"
        data.values.docstatus = 0
        lite.session.set_session("clone_doc", data.values)
        cls.page_controller.utils.update_url_parameters({page: "new-form"})
        cls.page_controller.init_page_url_changed()
    }

    new_form(data) {
        const cls = data.form_controller
        cls.page_controller.utils.update_url_parameters({page: "new-form"})
        cls.page_controller.init_page_url_changed()
    }

    paste_form(data, cls) {
        cls.duplicate_data = data
        cls.init_form()
    }

    amend_form(data) {
        const cls = data.form_controller
        cls.duplicate_form(data)
    }


    copy_clipboard(data) {
        const cls = data.form_controller
        const d = JSON.stringify(data.values)
        const area = document.createElement('textarea');
        area.value = d;
        area.style.display = 'none';
        // area.style.left = '-9999px'; // Move it off-screen
        document.body.appendChild(area);
        area.select();
        document.execCommand('copy');
        document.body.removeChild(area);
        cls.alerts.toast({
            toast_type: lite.status_codes.ok,
            title: `Copying JSON data`,
            message: `${data.values.name} Copied Successfully!`,
        })
    }








    // /////////////////////////////////////////////////        SAVING  ************** UPDATING ************** SUBMITTING ************** CANCELLING      \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    


    // to upload form data if form has any files
    async update_uploaded_files(data, validation){
        // process file content for the main form
        if(validation?.has_files){
            if(validation?.processed_files){
                $.each(lite.utils.get_object_keys(validation?.processed_files),(_,key)=>{
                    data[key] = lite.lite_file_picker.processed_form_files[validation.processed_files[key]]
                })
            }
        }
        // process file content for the tables
        if(validation?.has_table_files){
            $.each(lite.utils.get_object_keys(validation.table_files), (_,tbl_key)=>{
                $.each(data[tbl_key], (__,data_row)=>{
                    $.each(validation.table_files[tbl_key], (___, fieldname)=>{
                        data_row[fieldname] = lite.lite_file_picker?.processed_form_files[data_row[fieldname]] || ""
                    })
                })
            })
        }
    }
    
    // to save info
    async save_doc() {
        let validated = { setup: this.setup, ...this.validator.validate(this,false,true)}
        if (validated.validation_status) {
            await lite.lite_file_picker.upload_form_files(this)
            let has_validated = true
            let values = validated.data?.values
            const custom_validation = this?.events[this?.model]?.custom_validation
            if(custom_validation && !lite.utils.is_empty_array(custom_validation)){
                const cv = await Promise.all(custom_validation.map( async f=>{
                    if(typeof f === "function"){
                        let v = await f({controller:this, values: values})
                        if(v === false){
                            has_validated = false
                        }
                    }
                }))
            }
            
            if(has_validated){
                this.update_action_button('save-action-btn', "Saving", false)
                const uploads = await lite.lite_file_picker.upload_form_files(this)
                if(uploads){
                    let data = lite.utils.copy_object(validated.data.values)
                    this.update_uploaded_files(data, validated.data?.file_content)
                    return lite.connect.create({
                        model: validated?.setup?.model,
                        is_submittable: validated?.setup?.is_submittable,
                        setup: validated?.setup,
                        data: {
                            ...data,
                            status: this.setup?.allow_submit ? "Draft" : "Active"
                        }
                    }).then(resolve => {
                        const {status, data, error_message} = resolve
                        this.update_action_button('save-action-btn',"",true)
                        if (status === lite.status_codes.ok) {
                            lite.alerts.toast({
                                toast_type: status,
                                title: `Saved New ${lite.utils.replace_chars(this.setup.model, "_", " ")}`,
                                message: `${data?.data.name} Saved Successfully!`,
                            })
                            this.doc_data = data
                            lite.form_data = this.doc_data
                            lite.utils.update_url_parameters({page:"info", doc: data.data.id})
                            lite.page_controller.init_page_url_changed()
                        }
                        return resolve
                    })
                }
                return false
            }
        }
    }
    // update_doc
    async update_doc(show_alerts=true) {
        const validated = { setup: this.setup, ...lite.utils.copy_object(this.validator.validate(this, false, true))}
        if (validated.validation_status) {
            let has_validated = true
            let values = validated.data?.values
            const custom_validation = this?.events[this?.model]?.custom_validation
            if(custom_validation && !lite.utils.is_empty_array(custom_validation)){
                const cv = await Promise.all(custom_validation.map( async f=>{
                    if(typeof f === "function"){
                        let v = await f({controller:this, values: values})
                        if(v === false){
                            has_validated = false
                        }
                    }
                }))
            }
            if(has_validated){
                this.update_action_button('update-action-btn', "Updating",false)
                const uploads = await lite.lite_file_picker.upload_form_files(this)
                if(uploads){
                    let data = lite.utils.copy_object(validated.data.values)
                    this.update_uploaded_files(data, validated.data?.file_content)
                    return await this.connect.patch({
                        model: validated?.setup?.model,
                        is_submittable: validated?.setup?.is_submittable,
                        setup: validated?.setup,
                        data: {
                            status:this.doc_data.status,
                            id: this.doc_data.id,
                            name: this.doc_data?.name,
                            owner: this.doc_data?.owner,
                            idx: this.doc_data?.idx,
                            ...data
                        }
                    }).then(resolve => {
                        this.update_action_button('update-action-btn',"",true)
                        if (resolve.status === lite.status_codes.ok) {
                            if(show_alerts){
                                lite.alerts.toast({
                                    toast_type: resolve.status,
                                    title: `Updated ${lite.utils.replace_chars(this.setup.model, "_", " ")}`,
                                    message: `${resolve.data?.data.name} Updated Successfully!`,
                                })
                            }
                            this.doc_data = resolve.data?.data
                            this.update_doc_info()
                        }
                        return resolve
                    })

                }
            }
        }
    }


    // do submit document
    download_doc(params){
        const pf = lite.lite_selector.get_select_value($(".lite-selector[action-type='print-format-toggler']"))
        if (params?.values?.id && pf)
            lite.utils.print_doc(pf,params.setup.model,params?.values?.id, 1)
        else if(!pf){
            lite.alerts.toast({
                toast_type: lite.status_codes.not_found,
                title: "Print Format Not Selected",
                message: "Please select a print format before downloading this document!",
            })
        }
        else{
            lite.alerts.toast({
                toast_type: lite.status_codes.not_found,
                title: `Missing ID`,
                message: "ID Not found",
            })
        }
    }

    // do submit document
    export_csv_or_excel(params){
       console.log(params)
    }

    // send document via email
    async send_doc_via_email(params){
        let {values, form_controller, setup} = params
        const loader_id = lite.alerts.loading_toast({
            title: `Fetching document for preview!`,
            message:`Please wait while the system fetches the preview information.`
        })
        const {status, data} = await lite.connect.core("get_doc_print_format",{model: setup?.model, doc: values?.id})
        lite.alerts.destroy_toast(loader_id)
        const recipient_email = lite.utils.find_personal_email(lite?.form_controller?.doc_data || values) 
        if(status === lite.status_codes.ok){
            const context = `
                <div id="uniq-document-direct-mailing" class="w-full h-[full] min-h-[500px] max-h-[650px] grid grid-cols-5 gap-x-5">
                    <div class="w-full h-[600px] overflow-hidden overflow-y-auto border border-orange-300 rounded-sm border-dotted col-span-3 scale-85 p-3">${data}</div>
                    <div class="w-full h-full rounded-xl p-5 col-span-2">
                        <h1 class="text-22 font-bold mb-3"><span class="material-symbols-outlined mr-2 text-20 text-orange-500">data_info_alert</span>Send Document via Email</h1>
                        <p class="text-gray-600 mb-3">To send this document via email. Please fill in the details below</p>
                        ${lite.html_generator.build_form_field({ id:"subject", fieldlabel: "Subject", fieldtype: "text", fieldname: "subject", value: lite.utils.replace_chars(setup?.model,"_", " "), placeholder: "Enter Subject", required:true})}
                        ${lite.html_generator.build_form_field({ id:"recipient", fieldlabel: "Recipient Email", fieldtype: "text", fieldname: "recipient_email", value: recipient_email, placeholder: "Enter recipient email"})}
                        ${lite.html_generator.build_form_field({ id:"cc", fieldlabel: "CC:: (Separated by comma)", fieldtype: "text", fieldname: "cc", value: "", placeholder: "example1@mail.com, example2@mail.com"})}
                        ${lite.html_generator.build_form_field({ id:"message", fieldlabel: "Message", fieldtype: "rich", fieldname: "message", value: "", placeholder: "Enter your message here", required:true, height:100})}
                    </div>
                </div>
            `

            const {modal_id} = lite.modals.custom_modal(
                `<h1 class="font-bold text-22 flex items-center justify-start">
                    <span class="material-symbols-outlined text-20 mr-3">attach_email</span>
                    Sending <strong class="bg-secondary_color/20 px-2 py-1 rounded-md text-secondary_color mx-2">${values.name}</strong> Via Email
                </h1>`,
                context,
                {
                    text:"Send Email Now",
                    persist_modal:true,
                    fun: async ()=>{
                        const fields = $("#uniq-document-direct-mailing").find(".lite-field")
                        if(fields && lite.utils.array_has_data(fields)){
                            let mail_data = {}
                            fields.map((_, f) => {
                                const fieldname = lite.utils.get_attribute(f, "fieldname")
                                if (fieldname) {
                                    mail_data[fieldname] = lite.utils.get_field_value(f) || ""
                                }
                            })
                            if(!mail_data?.subject?.trim()){
                                lite.alerts.toast({
                                    toast_type: lite.status_codes.not_found,
                                    title: `Subject Mandatory`,
                                    message: `Please add subject to this email!`,
                                })
                            }
                            else if(!mail_data?.recipient_email?.trim()){
                                lite.alerts.toast({
                                    toast_type: lite.status_codes.not_found,
                                    title: `Recipient Mandatory`,
                                    message: `Please add recipient to this email!`,
                                })
                            }
                            mail_data.message = lite.rich_editor.get_content($("#uniq-document-direct-mailing").find(".lite-field[fieldname='message']")) || ""
                            mail_data.doc = values?.id
                            mail_data.model = setup?.model
                            const loader_id = lite.alerts.loading_toast({
                                title: `Queuing Email`,
                                message:`Please wait while the system queues the email for sending.`
                            })
                            const {status, data} = await form_controller.connect.core("send_doc_via_email", mail_data)
                            lite.alerts.destroy_toast(loader_id)
                            if(status === lite.status_codes.ok){
                                lite.alerts.toast({
                                    toast_type: status,
                                    title: `Email Queued Successfully`,
                                    message: `Email for ${values.name} has been queued successfully!`,
                                })
                                lite.modals.close_modal(modal_id)
                            }
                        }
                    }
                },
                null,
                " !max-w-[80%] !w-[80%] !max-h-[700px] !h-[100%]",
            )

            lite.rich_editor.init_rich_editors()
        }
    }

    async submit_doc(data) {
        const cls = data.form_controller
        const id = data.values.id
        if (!id) {
            cls.alerts.toast({
                toast_type: resolve.status,
                title: `Submision Failed!`,
                message: `Document ID missing!`,
            })
        } else {
            cls.connect.submit_doc({
                model: cls.setup.model,
                doc_id: id
            }).then(resolve => {
                if (resolve?.status === lite.status_codes.ok) {
                    cls.alerts.toast({
                        toast_type: resolve.status,
                        title: `Submitted ${lite.utils.replace_chars(cls.setup.model, "_", " ")}`,
                        message: `${data.values.name} Submitted Successfully!`,
                    })
                    cls.doc_data = resolve.data?.data
                    cls.init_form()
                }
            })
        }
    }

    async delete_doc(data) {
        await lite.lite_file_picker.delete_form_files()
        const cls = data.form_controller
        const id = data.values.id
        if (!id) {
            cls.alerts.toast({
                toast_type: resolve.status,
                title: `Deletion Failed!`,
                message: `Document ID missing!`,
            })
        } else {
            cls.connect.delete_docs({
                model: cls.setup.model,
                docs: id
            }).then(resolve => {
                if (resolve?.status === lite.status_codes.ok) {
                    cls.alerts.toast({
                        toast_type: resolve.status,
                        title: `Deleted ${lite.utils.replace_chars(cls.setup.model, "_", " ")}`,
                        message: `${data.values.name} Deleted Successfully!`,
                    })
                    cls.page_controller.go_back()
                }
            })
        }
    }

    async cancel_doc(data) {
        const cls = data.form_controller
        const id = data.values.id
        if (!id) {
            cls.alerts.toast({
                toast_type: resolve.status,
                title: `Cancellation Failed!`,
                message: `Document ID missing!`,
            })
        } else {
            cls.connect.cancel_docs({
                model: cls.setup.model,
                docs: id
            }).then(resolve => {
                if (resolve?.status === lite.status_codes.ok) {
                    cls.alerts.toast({
                        toast_type: resolve.status,
                        title: `Cancelled ${lite.utils.replace_chars(cls.setup.model, "_", " ")}`,
                        message: `${data.values.name} Cancelled Successfully!`,
                    })
                    cls.init_form()
                }
            })
        }
    }

    async disable_doc(data) {
        const cls = data.form_controller
        const id = data.values.id
        const doctype = lite.utils.replace_chars(cls.setup.model, "_", " ")
        if (!id) {
            cls.alerts.toast({
                toast_type: resolve.status,
                title: `Disabling Failed!`,
                message: `Document ID missing!`,
            })
        } else {
            const loader_id = lite.alerts.loading_toast({
                title: "Disabling document", 
                message:`Please wait while ${doctype} gets disabled.`
            })
            cls.connect.x_post("disable_doc", {"id": id, model: cls.setup?.model}).then(resolve => {
                lite.alerts.destroy_toast(loader_id)
                if (resolve?.status === lite.status_codes.ok) {
                    cls.alerts.toast({
                        toast_type: resolve.status,
                        title: `Disabled ${doctype}`,
                        message: `${data.values.name} Disabled Successfully!`,
                    })
                    cls.init_form()
                }
            })
        }
    }

    async enable_doc(data) {
        const cls = data.form_controller
        const id = data.values.id
        const doctype = lite.utils.replace_chars(cls.setup.model, "_", " ")
        if (!id) {
            cls.alerts.toast({
                toast_type: resolve.status,
                title: `Disabling Failed!`,
                message: `Document ID missing!`,
            })
        } else {
            const loader_id = lite.alerts.loading_toast({
                title: "Enabling document", 
                message:`Please wait while ${doctype} gets enabled.`
            })
            cls.connect.x_post("enable_doc", {"id": id, model:cls.setup?.model}).then(resolve => {
                lite.alerts.destroy_toast(loader_id)
                if (resolve?.status === lite.status_codes.ok) {
                    cls.alerts.toast({
                        toast_type: resolve.status,
                        title: `Enabled ${doctype}`,
                        message: `${data.values.name} Enabled Successfully!`,
                    })
                    cls.init_form()
                }
            })
        }
    }

    async workflow_action(data, action) {
        const quick_modal = await lite.modals.quick_form("core", "workflow comment",{text:"Proceed", fun: async (values, setup)=>{
            const cls = data.form_controller
            const id = data.values.id, stage_no = lite.utils.string_to_int(data.workflow_stage_no)
            if (!id || !stage_no) {
                cls.alerts.toast({
                    toast_type: lite.status_codes.unprocessable_entity,
                    title: `Update Failed!`,
                    message: `Document ID/Stage no missing!`,
                })
            } else {
                cls.connect.workflow_action({
                    model: cls.setup.model,
                    values: [id],
                    stage_no:stage_no,
                    comment: values.comment,
                    action: action
                }).then(resolve => {
                    if (resolve?.status === lite.status_codes.ok) {
                        lite.modals.close_modal(quick_modal.modal_id)
                        cls.alerts.toast({
                            toast_type: resolve.status,
                            title: `Updating ${lite.utils.replace_chars(cls.setup.model, "_", " ")}`,
                            message: `${data.values.name} Updated Successfully!`,
                        })
                        cls.doc_data = resolve.data?.data
                        cls.init_form()
                    }
                })            
            }
        }})
    }

    update_action_button(btn_class,btn_text, is_completed=false){
       const btn = $(`.${btn_class}`)
       
       if(!is_completed){
            this.action_btn_html = btn.html()
            btn.html(`${lite.utils.generate_loader({light_mode:true,loader_type:"dots"})} ${btn_text}`)
            btn.prop("disabled",true)
       }
       else{
            btn.prop("disabled",false)
            btn.html(this.action_btn_html)
       }
    }

    // /////////////////////////////////////////////////        SAVING  ************** UPDATING ************** SUBMITTING ************** CANCELLING   **************   \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\





    


    async handle_select_change(data, cls) {
        // only act if the fields are within the same form
        if($(data.field)?.parents("form")?.attr("id") === $(class_obj.$form)?.attr("id")){
            // update table value if the field is a table field
            if(data?.istablefield){
                if(data?.row_id){
                    if(cls.child_table_data[data.table_name]){
                        const itm = cls.child_table_data[data.table_name].find(p => p.row_id === data?.row_id);
                        if(itm){
                            itm[data?.fieldname] = data.value
                        }
                    }
                }
            }
            if (cls.events[cls.model]?.on_field_change && !lite.utils.is_empty_array(cls.events[cls.model]?.on_field_change[data?.fieldname])) {
                await Promise.all(cls.events[cls.model]?.on_field_change[data?.fieldname]?.map(async f=>{
                    await f({
                        value_id: data.value_id,
                        value: data.value,
                        field: data.field,
                        lite_field: $(data.field).parents(".lite-field"),
                        fieldname: data.fieldname,
                        fieldtype: data.type,
                        form: cls.$form,
                        controller: cls,
                        istablefield: data?.istablefield,
                        fieldrow: data?.fieldrow,
                        row_id:data?.row_id,
                        connect: cls.connect
                    })
                }))
            }
            cls.display_or_hide_dependant_fields(data?.id, data?.value)
        }
    }


    handle_date_picker_change(data,cls){
    }
    handle_time_picker_change(data,cls){
    }


    handle_file_change(data, cls) {
        // only act if the fields are within the same form
        if($(data.field)?.parents("form")?.attr("id") === $(cls.$form)?.attr("id")){
            data.fieldname = lite.utils.get_attribute(data.field, "fieldname")
            data.istablefield = lite.utils.is_empty_array($(data.field).parents(".table-row")) ? false : true
            data.fieldrow = data.istablefield ? $(data.field).parents(".table-row")[0] : null
            data.row_id= $(data.fieldrow)?.attr("id")
            data.id = lite.utils.get_attribute(data.field,'id'),
            data.controller = cls
            cls.display_or_hide_dependant_fields(data.id, data.files)
            if (cls.events[cls.model]?.on_field_change && !lite.utils.is_empty_array(cls.events[cls.model]?.on_field_change[data.fieldname])) {
                $.each(cls.events[cls.model]?.on_field_change[data.fieldname], (_, f) => f(data))
            }
        }
    }

    init_field_change_event_listener() {
        $.each(this.$form_fields.find('.lite-field'), (_, f) => {
            const field_type = lite.utils.get_attribute(f, 'type')
            if (this.common_field_types.includes(field_type)) {
                $(f).off("focusout").on("focusout", e => {
                    let
                        fieldname = lite.utils.get_attribute(e.target, "fieldname"),
                        field_type = lite.utils.get_attribute(e.target, "type"),
                        id = lite.utils.get_attribute(f,'id'),
                        value = lite.utils.get_field_value(e.target)
                    this.display_or_hide_dependant_fields(id, value)
                    if(field_type === "int"){
                        value = lite.utils.string_to_int(value)
                    }
                    else if(this.numeric_fields_types.includes(field_type)){
                        value = lite.utils.string_to_float(value)
                    }
                    // if its a child table
                    const
                        istablefield = lite.utils.is_empty_array($(e.target).parents(".table-row")) ? false : true,
                        fieldrow = istablefield ? $(e.target).parents(".table-row")[0] : null,
                        row_id= $(fieldrow)?.attr("id"),
                        table_name = $(e.target).parents(".table")?.attr("fieldname") || null
                    if(this.is_child_table_field(f)){
                        const itm = this.child_table_data[table_name].find(p => p.row_id === row_id)
                        if(itm){
                            itm[fieldname] = value
                        }
                    }
                    if (this.events[this.model]?.on_field_change && !lite.utils.is_empty_array(this.events[this.model]?.on_field_change[fieldname])) {
                        $.each(this.events[this.model]?.on_field_change[fieldname], (_, f) => {
                            f({
                                fieldname: fieldname,
                                value: value,
                                fieldtype: field_type,
                                form: this.$form,
                                field: e.target,
                                lite_field: $(e.target).parents(".lite-field"),
                                istablefield: istablefield,
                                fieldrow: fieldrow,
                                row_id:row_id,
                                table_name: table_name,
                                controller: this,
                                connect: lite.connect
                            })
                        })
                    }
                }).focus(e => {})

            } else if (field_type === 'checkbox') {
                $(f).off("change").on("change", e => {
                    const
                        fieldname = lite.utils.get_attribute(e.target, "fieldname"),
                        istablefield = lite.utils.is_empty_array($(e.target).parents(".table-row")) ? false : true,
                        fieldrow = istablefield ? $(e.target).parents(".table-row")[0] : null,
                        row_id = $(fieldrow)?.attr("id"),
                        id = lite.utils.get_attribute(f,'id'),
                        value = $(f).prop("checked") ? 1 : 0,
                        table_name = $(e.target).parents(".table")?.attr("fieldname") || null
                    if(this.is_child_table_field(f)){
                        const itm = this.child_table_data[table_name].find(p => p.row_id === row_id)
                        if(itm){
                            itm[fieldname] = value
                        }
                    }

                    this.display_or_hide_dependant_fields(id, value)
                    if (this.events[this.model]?.on_field_change && !lite.utils.is_empty_array(this.events[this.model]?.on_field_change[fieldname])) {
                        $.each(this.events[this.model]?.on_field_change[fieldname], (_, f) => {
                            f({
                                fieldname: lite.utils.get_attribute(e.target, "fieldname"),
                                value: $(e.target).prop("checked") ? 1 : 0,
                                fieldtype: "check",
                                form: this.$form,
                                field: e.target,
                                lite_field: $(e.target).parents(".lite-field"),
                                istablefield: istablefield,
                                fieldrow: fieldrow,
                                row_id:row_id,
                                controller: this,
                                connect: this.connect
                            })
                        })
                    }
                })
            }
            else if (field_type === 'button') {
                $(f).off("click").on("click", e => {
                    const
                        istablefield = lite.utils.is_empty_array($(e.target).parents(".table-row")) ? false : true,
                        fieldrow = istablefield ? $(e.target).parents(".table-row")[0] : null,
                        row_id = $(fieldrow)?.attr("id"),
                        id = lite.utils.get_attribute(f,'id'),
                        value = $(f).prop("checked") ? 1 : 0
                    const fieldname = lite.utils.get_attribute(e.target, "fieldname")
                    this.display_or_hide_dependant_fields(id, value)
                    if (this.events[this.model]?.on_field_change && !lite.utils.is_empty_array(this.events[this.model]?.on_field_change[fieldname])) {
                        $.each(this.events[this.model]?.on_field_change[fieldname], (_, f) => {
                            f({
                                fieldname: lite.utils.get_attribute(e.target, "fieldname"),
                                value: $(e.target).prop("checked") ? 1 : 0,
                                fieldtype: "check",
                                form: this.$form,
                                field: e.target,
                                lite_field: $(e.target).parents(".lite-field"),
                                istablefield: istablefield,
                                fieldrow: fieldrow,
                                row_id:row_id,
                                controller: this,
                                connect: this.connect
                            })
                        })
                    }
                })
            }

        })
    }

    display_or_hide_dependant_fields(field_id, current_value, process_for_table_only=false){
        if(!process_for_table_only){
            const dependants = this.$form.find(`.lite-field[display-on="${field_id}"]:not(.table-field)`)
            if(dependants && !lite.utils.is_empty_array(dependants)){
                $.each(dependants,(_,d)=>{
                    const ev = lite.utils.get_attribute(d,"display-eval")
                    if(ev){
                        const ex = lite.utils.string_to_object(ev)
                        if(ex.slice(1)?.includes(current_value)){
                            lite.utils.show($(d).parents(".field-wrapper"))
                            lite.utils.show($(d))
                        }
                        else{
                            lite.utils.hide($(d).parents(".field-wrapper"))
                            lite.utils.hide($(d))
                        }
                    }
                })
            }
        }
        // table display on
        const table_dependents = this.$form.find(`div.th[display-on="${field_id}"]`)
        if(table_dependents && !lite.utils.is_empty_array(table_dependents)){
            $.each(table_dependents,(_,d)=>{
                const table_wrapper = $(table_dependents)?.parents(".table")

                const head_row = $(d)?.parents(".tr")
                const head_row_cols = lite.utils.string_to_int($(head_row)?.attr("cols")), col_cols = lite.utils.string_to_int($(d)?.attr("cols"))
                const ev = lite.utils.get_attribute(d,"display-eval")
                let new_row_cols = head_row_cols
                if(ev){
                    const ex = lite.utils.string_to_object(ev)
                    if(ex.slice(1)?.includes(current_value)){
                        if($(d).parents(".field-wrapper")?.hasClass("hidden") || $(d)?.hasClass("hidden")){
                            lite.utils.show($(d).parents(".field-wrapper"))
                            lite.utils.show($(d))
                            new_row_cols += col_cols
                        }
                    }
                    else{
                        if(!$(d).parents(".field-wrapper")?.hasClass("hidden") && !$(d)?.hasClass("hidden")){
                            lite.utils.hide($(d).parents(".field-wrapper"))
                            lite.utils.hide($(d))
                            new_row_cols -= col_cols
                        }
                       
                    }
                }
                head_row.removeClass(`grid-cols-${head_row_cols}`).addClass(`grid-cols-${new_row_cols}`).attr("cols", new_row_cols)                
                
                // handle table hiding and showing
                const t_rows = $(table_wrapper)?.find(".tbody .table-row")
                if(t_rows && lite.utils.array_has_data(t_rows)){
                    $(t_rows).removeClass(`grid-cols-${head_row_cols}`).addClass(`grid-cols-${new_row_cols}`).attr("cols", new_row_cols)
                    const cells = $(t_rows)?.find(`div.tc[display-on="${field_id}"]`)
                    $.each(cells,(_, cell)=>{
                        const ev = lite.utils.get_attribute(cell, "display-eval")
                        if(ev){
                            const ex = lite.utils.string_to_object(ev)
                            if(ex.slice(1)?.includes(current_value)){
                                if($(cell)?.hasClass("hidden") || $(cell).find(".lite-field")?.hasClass("hidden")){
                                    lite.utils.show($(cell))
                                    lite.utils.show($(cell).find(".lite-field"))
                                }
                            }
                            else{
                                if(!$(cell)?.hasClass("hidden") || !$(cell).find(".lite-field")?.hasClass("hidden")){
                                    lite.utils.hide($(cell))
                                    lite.utils.hide($(cell).find(".lite-field"))
                                }
                            }
                        }
                    })

                }
            })
        }
    }

    validate_display_field(field){
        if(field.hidden){
            return true
        }
        else if(field?.displayon && lite.utils.is_object(field.displayon)){
            if(!lite.utils.is_empty_object(this.doc_data)){
                const 
                    v = this.doc_data[field.fieldname],
                    controller_field =  this.fields.filter(f => f.id  === field.displayon[0])[0]?.fieldname,
                    ev = field.displayon.slice(1)
                if(controller_field){
                    if(ev.includes(this.doc_data[controller_field])){
                        return false
                    }
                    return true
                }
                return true
            }
            else{
                const controller_field_value =  this.fields.filter(f => f.id  === field.displayon[0])[0]?.default || [0]?.value
                return field.displayon?.slice(1)?.includes(lite.utils.is_number_variable(controller_field_value) ?  lite.utils.string_to_float(controller_field_value) : controller_field_value || "") ? false : true
            }
        }
    }

    validate_table_display_field(field_info){
        $.each(field_info?.fields,(_,field)=>{
            if(field?.displayon && lite.utils.is_object(field.displayon)){
                if(!lite.utils.is_empty_object(this.doc_data)){
                    const 
                        v = this.doc_data[field.fieldname],
                        controller_field =  this.fields.filter(f => f.id  === field.displayon[0])[0]?.fieldname,
                        ev = field.displayon.slice(1)
                    if(controller_field){
                        if(ev.includes(this.doc_data[controller_field])){
                            field.hidden = false
                        }
                        else{
                            field.hidden = true
                        }
                    }
                }
            }
        })
        
    }

    async get_await_form_value(field, table_name=null, table_row_id=null){
       return await new Promise((resolve,reject) => {
            let timeOut = null
            let initial_value = this.get_form_value(field, table_name, table_row_id)
            const interval = setInterval(() => {
                let v = this.get_form_value(field, table_name, table_row_id)
                if(v && initial_value !== v){
                    clearInterval(interval)
                    clearTimeout(timeOut)
                    resolve(v)
                }
            }, 5);
            timeOut = setTimeout(() => {
                clearTimeout(timeOut);
                clearInterval(interval)
                resolve(initial_value)
            }, 250);
        })
    }

    get_form_value(field, table_name, table_row_id) {
        if(!table_name){
            if(typeof field === "string"){
                field = this.get_form_field(field)
            }
            const field_type = lite.utils.get_attribute(field, 'type')
            if (this.common_field_types.includes(field_type)) {
                return $(field).val()
            } 
            else if (field_type === 'checkbox') {
                return $(field).prop('checked') ? 1 : 0
            } else if (field_type === 'read-only' || field_type === "switch") {
                return $(field).attr('value')
            } else if (field_type === 'link' || field_type === 'select') {
                return lite.lite_selector.get_select_value(field)
            }
        }
        else if(table_row_id){
            const row = this.child_table_data[table_name]?.find(r=>r.row_id === table_row_id)
            if(row){
                return row[field]
            }
        }
    }

    is_child_table_field(field){
        return $(field)?.parents(".tr.table-row")?.length > 0
    }

    get_table_fields_row_index_number(field){
        const tr = $(field)?.parents(".tr.table-row")
        if(lite.utils.array_has_data(tr)){
            const index = $(tr[0])?.attr("table-row-index")
            if(index && index != undefined && index != "undefined"){
                return {table_index: parseInt(index), table_name: lite.utils.get_attribute($(tr).parents(".table"),"fieldname")}
            }
        }
        return {table_index: false}
    }

    set_form_value(field, value, read_only_display_figure = null, trigger_change_event=true) {
        const field_type = lite.utils.get_attribute(field, 'type')
        if (this.common_field_types.includes(field_type)) {
            $(field).val(this.numeric_fields_types.includes(field_type) ? lite.utils.thousand_separator(value, lite.currency_decimals) : value)
            if(trigger_change_event){
                $(field).trigger("focusout")
            }
        } 
        else if (field_type === 'checkbox'){
            $(field).prop('checked', value == 1)
            if(trigger_change_event){
                $(field).trigger("change")
            }
        } 
        else if (field_type === 'read-only') {
            $(field).attr('value', value).text(read_only_display_figure || ($(field).attr("is-figure") === "true" ? lite.utils.thousand_separator(value,2) : value));
        } else if (field_type === 'link' || field_type === 'select') {
            lite.lite_selector.set_selected_value(field, value, trigger_change_event)
        }
        else if(field_type === 'switch') {
            $(field).attr('value', value)
        }
    }
    #update_table_row_if_rendered(table_name, row, field_name, read_only_display_figure, trigger_change_event){
        const table_row = $(`.table[fieldname="${table_name}"] #${row.row_id}`)
        if(table_row){
            let field = table_row.find(`.lite-field[fieldname="${field_name}"]`), value = row[field_name]
            if(field){
                const field_type = lite.utils.get_attribute(field, 'type')
                if (this.common_field_types.includes(field_type)) {
                    $(field).val(lite.utils.is_number_variable(value) && field_type !== "rate" ? lite.utils.thousand_separator(value, lite.currency_decimals) : value)
                    if(trigger_change_event){
                        $(field).trigger("focusout")
                    }
                } else if (field_type === 'checkbox') {
                    $(field).prop('checked', value == 1)
                    if(trigger_change_event){
                        $(field).trigger("change")
                    }
                } else if (field_type === 'read-only') {
                    $(field).attr('value', value).text(read_only_display_figure || ($(field).attr("is-figure") === "true" && field_type !== "rate" ? lite.utils.thousand_separator(value,2) : value));
                } else if (field_type === 'switch') {
                    $(field).attr('value', value)
                }
                else if (field_type === 'link' || field_type === 'select') {
                    if($(field).is("input")){
                        field = $(field).parents(".lite-selector.lite-field")
                    }
                    lite.lite_selector.set_selected_value(field, value, trigger_change_event)
                }
                else if(field_type === "expandable"){
                    lite.expandable_field.update_field(field, value, false)
                }
            }
        }
    }
    set_form_table_value(table_name, row_id, field, value, read_only_display_figure = null, trigger_change_event=true) {
        const row = this.child_table_data[table_name]?.find(r=>r.row_id === row_id)
        if(row && lite.utils.object_has_data(row)){
            row[field] = value
            this.#update_table_row_if_rendered(table_name, row, field, read_only_display_figure, trigger_change_event)
        }
    }

    get_form_field(field_name) {
        const 
            select = !this?.is_quick_form ? 
                this.$active_content_group?.find(`.lite-field[fieldname="${field_name}"]:not(.table-field):not(input)`) 
                : 
                this.$form?.find(`.lite-field[fieldname="${field_name}"]:not(.table-field):not(input)`),
            input = !this?.is_quick_form ? this.$active_content_group?.find(`.lite-field[fieldname="${field_name}"]:not(.table-field)`)
                : this.$form?.find(`.lite-field[fieldname="${field_name}"]:not(.table-field)`),

            table_field = !this?.is_quick_form ?
                this.$active_content_group.find(`.lite-field[fieldname="${field_name}"]:not(.table-field):not(div)`) 
                :
                this.$form.find(`.lite-field[fieldname="${field_name}"]:not(.table-field):not(div)`) 
        if(select && !lite.utils.is_empty_array(select)){
            return select
        }
        else if(input && !lite.utils.is_empty_array(input)){
            return input
        }
        else if(table_field && !lite.utils.is_empty_array(table_field)){
            return table_field
        }
        return false
    }

    get_form_table_field(table_name, row_id, field_name) {
        const select = $(`#${row_id} div.lite-selector.lite-field.table-field[fieldname="${field_name}"]`),
            input = $(`#${row_id} .lite-field.table-field[fieldname="${field_name}"]:not(div.lite-selector)`)
        if(select && !lite.utils.is_empty_array(select)){
            return select
        }
        else if(input && !lite.utils.is_empty_array(input)){
            return input
        }
    }
    get_form_table_value(table_name, row_id, field_name) {
        const select = $(`#${row_id} div.lite-selector.lite-field.table-field[fieldname="${field_name}"]`),
            input = $(`#${row_id} .lite-field.table-field[fieldname="${field_name}"]:not(div.lite-selector)`)
        if(select && !lite.utils.is_empty_array(select)){
            return $(select)?.find("input")?.val()
        }
        else if(input && !lite.utils.is_empty_array(input)){
            if($(input)?.attr("type") === "expandable"){
                return lite?.expandable_field?.expandable_field_configs[$(input)?.attr("lite-id")]?.value || ""
            }
            return $(input)?.find("input")?.val() || $(input)?.attr("value")
        }
    }

    get_table_rows(table_name) {
        return this.child_table_data[table_name] || []
    }

    get_table_column_values(table_name, column_names=[], detailed=false) {
        let columns = {}
        if(this.child_table_data[table_name] && lite.utils.array_has_data(this.child_table_data[table_name])){
            this.child_table_data[table_name].map(row=>{
                column_names.map(nm=>{
                    if(!columns[nm]){
                        columns[nm] = [row[nm]]
                    }
                    else{
                        columns[nm].push(row[nm])
                    }
                })
            })
        }
        return columns
    }

    get_table_row(table_name,row_id, get_first=false, get_last=false) {
        let row = {}
        if(get_first && lite.utils.array_has_data(this.child_table_data[table_name])){
            row = this.child_table_data[table_name][0]
        }
        else if(get_last){
            row = this.child_table_data[table_name]?.at(-1) || {}
        }
        else{
            row = this.child_table_data[table_name]?.find(r=>r.row_id === row_id)
        }
        return row || {}
    }

    clear_table(table_name){
        this.$form_fields.find(`div[fieldname="${table_name}"]`)?.find(".table")?.find(".tbody")?.empty()
    }

    populate_child_table(table_name, data, clear_existing_rows_before_populate=true, reinitialize_pagination=true, clear_existing_table_row_elements=true, jump_to_last_page=1){
        if(!lite.utils.is_empty_object(this.child_tables)){
            if(clear_existing_table_row_elements){
                this.clear_table(table_name)
            }
            if (clear_existing_rows_before_populate){
                this.child_table_data[table_name] = []
            }
            let field =  {...lite.utils.get_object_values(this.child_tables)?.find(p => p.fieldname === table_name) || {}}
            if(field && lite.utils.object_has_data(field)){
                let to_be_populated = []
                $.each(data,(_,d)=>{
                    if(!d.row_id || clear_existing_rows_before_populate){
                        d.current_page_index = d?.current_page_index || _
                        d.row_id = lite.utils.unique()
                        this.child_table_data[table_name]?.push(d)
                    }
                    if(_ < this.child_table_page_size){
                        to_be_populated.push(d)
                    }
                })
                // // compute pagination data for child tables
                if(!reinitialize_pagination){
                    this.add_child_table_row(table_name, to_be_populated)
                }
                else{
                    const
                        total_records = this.child_table_data[table_name].length,
                        total_pages = Math.ceil(total_records/this.child_table_page_size),
                        current_page = jump_to_last_page ? total_pages: 1,
                        start = (current_page - 1) * this.child_table_page_size,
                        end   = start + this.child_table_page_size
                    this.child_table_pagination[table_name] = { 
                        total_pages: total_pages || 1, 
                        total_records:total_records, 
                        current_page: current_page, 
                        start:start, 
                        end:end
                    }
                    this.add_child_table_row(table_name, this.child_table_data[table_name]?.slice(start, end))
                    this.#add_table_pagination(table_name)
                }
            }
        }
    }

    add_child_table_row(table_name, data){
        if(lite.utils.array_has_data(data)){
            let rows = ''
            const table_config = lite.utils.get_object_values(this.child_tables)?.find(t=>t.fieldname === table_name)
            if(table_config && lite.utils.object_has_data(table_config)){
                $.each(data,(i,r)=>rows += this.html_bulder.create_table_row({...table_config, value:r},true)?.row_element)
                this.$form_fields.find(`${this.table_wrapper_class_name}[fieldname="${table_name}"]`).find(".tbody").empty().append(rows)
                lite.lite_selector.init_selectors()
                lite.lite_date_picker.init()
                lite.lite_time_picker.init()
                lite.lite_year_picker.init(this)
                lite.lite_switch.init_switch_fields()
                lite.expandable_field.init()
                lite.utils.init_password_fields()
                this.init_field_change_event_listener()
            }
            
        }
    }

    hide_child_table_columns(table, columns=[]){

    }

    get_form_data() {
        return {
            values: {
                id: this.doc_data?.id,
                name: this.doc_data?.name,
                ...lite.utils.copy_object(this.validator.validate(this, true)?.data?.values)
            },
            setup: this.setup,
            form_controller: this,
            form: this.$form
        }
    }     



    update_doc_info() {
        lite.page_controller.update_doc_title_content()
    }


    create_form_buttons(){
        if(this.form_buttons && lite.utils.array_has_data(this.form_buttons)){
            $.each(this.form_buttons,(_,btn)=>{
                this.form_action_functions[btn.title] = btn.action
                this.$form_actions_wrapper.prepend(this.html_bulder.create_form_button(btn))
            })
            this.$form_actions_wrapper.find(".form-action-btn")?.click(e=>{
                const action = lite.utils.get_attribute(e.currentTarget, "action")
                if (typeof this.form_action_functions[action] === "function"){
                    this.form_action_functions[action](this.get_form_data())
                }
            })
        }
    }

    // lets dynamically update actions when the form is initialized
    update_actions() {
        this.dropdown_actions = {
            refresh : {title: "Refresh Form", icon: "published_with_changes", icon_color: "purple", action: this.refresh_form, for_docstatus: [0, 1, 2,3]},
            download : { icon: 'download', icon_color: 'orange', title: `Download ${this.setup.title}`, action: this.download_doc, for_docstatus: [0, 1]},
            export_csv_or_excel : { icon: 'csv', icon_color: 'pink', title: `Export CSV/EXCEL`, action: this.export_csv_or_excel, for_docstatus: [0, 1]},
            send_mail: { icon: 'mail', icon_color: 'violet', title: "Send Mail", action: this.send_doc_via_email, for_docstatus: [0, 1]},
        }
        if(this?.setup?.allow_create || this?.setup?.allow_create === undefined){
            this.dropdown_actions.new_form = { title: `New ${lite.utils.replace_chars(this.setup?.model,"_"," ")}`, icon: "add_circle", icon_color: "purple", action: this.new_form, for_docstatus: [0, 1, 2, 3]}
        }
        if(this?.setup?.allow_duplicate || this?.setup?.allow_duplicate === undefined){
            this.dropdown_actions.duplicate = { title: "Duplicate", icon: "content_copy", icon_color: "emerald", action: this.duplicate_form, for_docstatus: [0, 1, 2, 3]}
        }
        if(lite.utils.is_empty_object(this.workflow) || this.workflow?.allow_edit === true){
            this.dropdown_actions = {
                ...this.dropdown_actions,
                amend: { title: "Amend Doc", icon: "edit_square", icon_color: "indigo", action: this.amend_form, for_docstatus: [2,3]},
            }
            if(this?.setup?.allow_disable || this?.setup?.allow_disable === undefined){
                this.dropdown_actions = {
                    ...this.dropdown_actions,
                    disable:{ icon: 'lock', icon_color: 'red', title: "Disable", action: this.disable_doc, for_docstatus: [0,1,3], evaluate:["disabled", [0]]},
                    enable:{ icon: 'lock_open', icon_color: 'purple', title: "Enable", action: this.enable_doc, for_docstatus: [0,1, 3], evaluate:["disabled", [1]]},
                }
            }
            if(!this.workflow?.has_workflow){
                this.dropdown_actions.submit = { icon: 'check_box', icon_color: 'indigo', title: "Submit", action: this.submit_doc, for_docstatus: [0], at_index:1}
                this.dropdown_actions.cancel =  { icon: 'cancel', icon_color: 'red', title: "Cancel", action: this.cancel_doc, for_docstatus: [1]}
                this.dropdown_actions.delete = { icon: 'delete', icon_color: 'red', title: "Delete", action: this.delete_doc, for_docstatus: [0,2]}
            }
        }
        
        // empty actions if it is not quick form
        if(!this.is_quick_form){
            this.$form_actions_wrapper?.empty()
        }
        // if the form is new
        if (this.page_type === 'new-form' && !this.is_quick_form) {
            this.$form_actions_wrapper.html(this.html_bulder.create_save_button())
            this.$form_actions_wrapper.find(".save-action-btn")?.off("click")?.on("click", e => {
                e.preventDefault()
                this.save_doc()
            })
            this.create_form_buttons()
        }
        if(this.is_quick_form){
            this.$quick_form_save_btn?.off("click").click(async e=>{
                e.preventDefault()
                const validated = {
                    setup: this.setup,
                    ...this.validator.validate(this)
                }
                if (validated.validation_status) {
                    let has_validated = true
                    let values = validated.data?.values
                    const doctype = lite.utils.replace_chars(this.setup.model, "_", " ")
                    if(this.custom_validation && !lite.utils.is_empty_array(this.custom_validation)){
                        const custom_validations = await Promise.all(this.custom_validation.map( async f=>{
                            if(typeof f === "function"){
                                let v = await f({controller:this, values:values})
                                if(v === false){
                                    has_validated = false
                                }
                            }
                        }))
                    }
                    if(has_validated){
                        if(this.on_quick_form_save && typeof this.on_quick_form_save == "function"){
                            this.on_quick_form_save(values, this.setup)
                        }
                        else if(typeof this.on_quick_form_save?.fun == "function"){
                            this.on_quick_form_save.fun(values, this.setup)
                        }
                        else{ 
                            const loader_id = lite.alerts.loading_toast({
                                title: "Saving", 
                                message:`Please wait while ${doctype} is saving.`
                            })
                            const save = await this.save_doc()
                            lite.alerts.destroy_toast(loader_id)
                            if (save?.status === lite.status_codes.ok) {
                                lite.alerts.toast({
                                    toast_type: resolve.status,
                                    title: `Saved ${doctype}`,
                                    message: `${data.values.name} Saved Successfully!`,
                                })
                            }
                        }
                    }
                }
            })
        }

        // if the form is on the info page
        else if (this.page_type === 'info') {
            this.#set_up_print_actions()
            this.dropdown_list.push(this.dropdown_actions.refresh)
            this.form_action_options["Refresh Form"] = this.dropdown_actions.refresh
            // console.log(this.dropdown_actions, this.form_action_options)
            if(this?.setup?.allow_download){
                this.dropdown_list.push(this.dropdown_actions.download)
                this.form_action_options[`Download ${this.setup.title}`] = this.dropdown_actions.download
            }
            if (this.setup?.allow_submit) {
                if (this.doc_data?.docstatus == 0) {
                    this.form_action_options["Submit"] = this.dropdown_actions.submit
                    this.form_action_options["Delete"] = this.dropdown_actions.delete
                    this.dropdown_list.push(this.dropdown_actions.submit)
                    this.dropdown_list.push(this.dropdown_actions.delete)
                    if (this.setup?.allow_update || this.setup?.allow_update === undefined && (this.workflow?.allow_edit === true || lite.utils.is_empty_object(this.workflow))){
                        this.$form_actions_wrapper.append(this.html_bulder.create_update_button(this.doc_data))
                    }
                }
                if (this.setup?.allow_cancel && this.doc_data?.docstatus == 1) {
                    this.form_action_options["Cancel"] = this.dropdown_actions.cancel
                    this.dropdown_list.push(this.dropdown_actions.cancel)
                }
            } else {
                if (this.setup?.allow_delete || this.setup?.allow_delete == undefined){
                    this.form_action_options["Delete"] = this.dropdown_actions.delete
                    this.dropdown_list.push(this.dropdown_actions.delete)
                }
                if (this.setup?.allow_update || this.setup?.allow_update === undefined && (this.workflow?.allow_edit === true || lite.utils.is_empty_object(this.workflow))){
                    this.$form_actions_wrapper.append(this.html_bulder.create_update_button())
                }
            }
            if (this.setup?.allow_sending_mail) {
                this.form_action_options["Send Mail"] = this.dropdown_actions.send_mail
                this.dropdown_list.push(this.dropdown_actions.send_mail)
            }

            if(this.page_type === "info"){
                const form_data = lite.form_data
                this.form_action_options["Disable"] = this.dropdown_actions.disable
                this.dropdown_list.push(this.dropdown_actions.disable)
                this.form_action_options["Enable"] = this.dropdown_actions.enable
                this.dropdown_list.push(this.dropdown_actions.enable)
            }
            this.dropdown_list.push(this.dropdown_actions.export_csv_or_excel)
            // console.log(this.dropdown_list, this.dropdown_actions)
            this.#create_form_option_actions()

            // enable update button
            this.$form_actions_wrapper.find(".update-action-btn")?.off("click")?.on("click", e => {
                e.preventDefault()
                this.update_doc()
            })
        }
    }

    // enable table row actions
    enable_table_row_actions(){
        this.$form?.find('.table-row-actions')?.find("button")?.off("click")?.click(e=>{
            this.current_table_action_btn = e.currentTarget
            // enable table row actions
            $(".table-row-action-list")?.find(".row-option-action")?.off("click")?.click(async e=>{
                const obj = e.currentTarget
                const 
                    action = lite.utils.get_attribute(obj, "for"), 
                    table = lite.utils.get_attribute(obj, "table"), 
                    model = lite.utils.get_attribute(obj, "model")
                if(action && table){
                    const fun = this.table_actions[table][action]?.action
                    if(typeof fun === "function"){
                        let data = this.get_form_data()
                        const tr = $(this.current_table_action_btn)?.parents(".tr.table-row")
                        // hide actions
                        $(this.current_table_action_btn)?.trigger("click")
                        $(this.current_table_action_btn).attr("aria-expanded", false)
                        if(tr){
                            data.table = table
                            data.action = action
                            data.model = model
                            data.row_id = $(tr)?.attr("id")
                            data.row_data = this.get_table_row(table,data.row_id)
                            data.row_object = tr[0]
                            this.#get_selected_rows()
                            data.selected_rows = this.selected_child_table_rows[model]

                            // execute the function finally
                            await fun(data, this)

                            this.enable_table_row_actions()
                            this.enable_table_row_actions()
                            lite.lite_selector.init_selectors(this.handle_select_change, this)
                            lite.lite_file_picker.init_file_picker(this.handle_file_change, this)
                            lite.lite_date_picker.init(this.handle_date_picker_change, this)
                            lite.lite_time_picker.init(this.handle_time_picker_change, this)
                            lite.lite_switch.init_switch_fields(this.handle_permission_change,this)
                            lite.expandable_field.init()
                            this.#init_on_load_events()
                            lite.lite_commands.init_form_commands(this)
                            lite.code_editor.init_code_editors()
                            lite.rich_editor.init_rich_editors()
                            lite.utils.init_password_fields()
                        }
                    }
                }
            })
        })
    }

    // define default table actions
    async insert_above_table_row(data, cls){
        $(`#${data.row_id}`)?.before(cls.html_bulder.create_table_row(cls.child_tables[data.model], true, true))

    }
    async insert_below_table_row(data, cls){
        $(`#${data.row_id}`)?.after(cls.html_bulder.create_table_row(cls.child_tables[data.model], true, true))

    }
    async duplicate_table_row(data, cls){
        $(`#${data.row_id}`)?.after($(`#${data.row_id}`)?.clone())

    }

    async remove_table_row(data, cls){
        $(data?.row_object)?.remove()
        $.each(cls.on_row_remove, (_, f) => {
            if(typeof f === "function")
                f({ form: cls.$form, controller: cls, connect: lite.connect })
        })
    }

    #set_up_print_actions() {
        if (this.setup?.allow_print) {
            this.$form_actions_wrapper.html(this.html_bulder.create_print_format_select_button(this.doc_data, this.setup,this.doc_data?.default_print_format))
            if ((this.setup?.allow_print || this.setup?.allow_print == undefined) && this.doc_data?.docstatus !== 2) {
                this.$form_actions_wrapper.append(this.html_bulder.create_print_button(this.doc_data))
                this.$form_actions_wrapper.find(".print-action-btn")?.off("click").click(e=>{
                    const pf = lite.lite_selector.get_select_value($(".lite-selector[action-type='print-format-toggler']"))
                    if (this.doc_data?.id && pf)
                        lite.utils.print_doc(pf,this.setup.model, this.doc_data.id,0)
                    else if(!pf){
                        lite.alerts.toast({
                            toast_type: lite.status_codes.not_found,
                            title: "Print Format Not Selected",
                            message: "Please select a print format befor downloading this document!",
                        })
                    }
                })
            }
        }
    }

    #create_form_option_actions() {
        this.current_options_btn = null
        if (this.setup?.allow_submit) {}

        // ADD WORKFLOW ACTIONS COMING FROM THE BACKEND
        if(lite.utils.array_has_data(this.workflow?.available_actions||[])){
            
            $.each(this.workflow?.available_actions,(_,stage)=>{
                const act = { icon: stage.icon || 'overview_key', icon_color: stage.color ||'orange', title: stage.action, action: this.workflow_action, for_docstatus: [0,1,2], at_index:_+3, is_workflow_action:true, stage_no:stage.stage_no }
                this.dropdown_list.push(act)
                this.form_action_options[stage.action] = act
            })
        }



        if(this.setup?.allow_duplicate === undefined || this.setup?.allow_duplicate){
            this.dropdown_list.push(this.dropdown_actions.duplicate)
            this.form_action_options["Duplicate"] = this.dropdown_actions.duplicate
        }
        if(this.setup?.allow_amend === undefined || this.setup?.allow_amend){
            this.dropdown_list.push(this.dropdown_actions.amend)
            this.form_action_options["Amend Doc"] = this.dropdown_actions.amend
        }
        
        this.dropdown_list.push(this.dropdown_actions.new_form)
        if(this?.setup?.allow_create || this?.setup?.allow_create === undefined){
            this.form_action_options[`New ${lite.utils.replace_chars(this.setup?.model,"_"," ")}`] = this.dropdown_actions.new_form
        }
        if(lite.utils.array_has_data(this.form_actions)){
            $.each(this.form_actions,(_,fa)=>{
                this.form_action_options[fa.title] = fa
                this.dropdown_list.push(fa)
            })
        }

        // drop down option for the form
        this.$form_actions_wrapper.append(this.html_bulder.create_drop_down_button(this.dropdown_list, this.doc_data))
        this.$form_actions_wrapper.find(".dropdown-toggle").click(e => {
            this.current_options_btn = e.currentTarget
        })

        // drop down item click
        this.$form_actions_wrapper.find(".form-option-item").click(e => {
            const action = lite.utils.get_attribute(e.currentTarget, "for"), stage_no = lite.utils.get_attribute(e.currentTarget, "stage-no")
            if (this.form_action_options[action] && this.form_action_options[action] !== null) {
                this.form_action_options[action]?.action({...this.get_form_data(),workflow_stage_no: stage_no}, action)
            }
            $(this.current_options_btn).trigger("click")
            $(this.current_options_btn).attr("arial-expanded", false)
        })

    }


    // get opened document
    async get_opened_document() {
        lite.form_state = "new"
        this.doc_data = {}
        this.setup.docstatus = 0
        lite.form_data = {}
        lite.is_new_form = true
        const clone_doc = lite.session.get_session("clone_doc")
        if (clone_doc && lite.utils.object_has_data(clone_doc)) {
            this.doc_data = { ...lite.utils.copy_object(clone_doc)}
            lite.form_data = this.doc_data
            lite.session.update_session("clone_doc",{})
        } else {
            if (this.page_type === 'info' && this.doc_name && !this.is_quick_form) {
                lite.form_state = "draft"
                lite.is_new_form = false
                let resolve = this.prefetched_data
                if(!lite.utils.object_has_data(this.prefetched_data)){
                    resolve = await lite.connect.get_doc(this.setup.model, this.doc_name)
                    this.doc_data = resolve.data
                }
                else{
                    this.doc_data = resolve?.data
                    this.prefetched_data = null
                }
                if (lite.utils.object_has_data(this.doc_data)) {
                    this.audit_trail = this.doc_data?.audit_trail || {}
                    this.setup.docstatus = this.doc_data?.dostatus
                    this.workflow = this.doc_data?.workflow
                    lite.form_data = this.doc_data
                    if (this.setup.docstatus ===1){
                        lite.form_state = "submitted"
                    }
                    else if (this.setup.docstatus === 2){
                        lite.form_state = "cancelled"
                    }
                    this.update_doc_info()

                    // add document information to the form
                    if(lite.utils.is_empty_array(this.$form_header.find(".doc-name"))){
                        $(".info-view-content form")?.addClass("relative")?.append(this.html_bulder.create_trail_content(this.doc_data))
                        $(".info-view-content form")?.append(this.html_bulder.create_preview_content(this.doc_data))
                        $(".info-view-content form")?.append(this.html_bulder.create_workflow_comment_content(this.doc_data))
                        this.$form_header.prepend(this.html_bulder.create_form_download_and_preview(this.doc_data,this.setup))
                        this.$audit_trail_wrapper = $(".audit-trail-wrapper")
                        this.$preview_wrapper = $(".preview-wrapper")
                        this.$comments_wrapper = $(".comments-wrapper")
                        this.$form_header?.find(".show-audit-trail")?.off("click")?.click(e=>{
                            e.preventDefault()
                            if(this.$audit_trail_wrapper?.hasClass("hidden")){
                                this.$audit_trail_wrapper?.removeClass("hidden")
                            }
                            else{
                                this.$audit_trail_wrapper?.addClass("hidden")
                            }
                            $(".close-trail-btn")?.off("click")?.click(e=>{
                                e.preventDefault()
                                this.$audit_trail_wrapper?.addClass("hidden")
                            })
                        })

                        // to preview a document
                        this.$form_header?.find(".preview-doc")?.off("click")?.click(async e=>{
                            e.preventDefault()
                            const loader_id = lite.alerts.loading_toast({
                                title: `Fetching preview data!`, 
                                message:`Please wait while the system fetches the information.`
                            })
                            const {status, data, error_message} = await lite.connect.core("get_doc_print_format",{model:this.doc_data?.doctype, doc:this.doc_data?.id})
                            lite.alerts.destroy_toast(loader_id)
                            if(status == lite.status_codes.ok){
                                if(this.$preview_wrapper?.hasClass("hidden")){
                                    this.$preview_wrapper?.removeClass("hidden")
                                    this.$preview_wrapper?.find(".doc-preview-content")?.html(data)
                                }
                                $(".close-preview-btn")?.off("click")?.click(e=>{
                                    e.preventDefault()
                                    this.$preview_wrapper?.addClass("hidden")
                                })
                            }
                        })
                        // to view workflow comments
                        this.$form_header?.find(".show-comments")?.off("click")?.click(async e=>{
                            e.preventDefault()
                            if(this.$comments_wrapper?.hasClass("hidden")){
                                this.$comments_wrapper?.removeClass("hidden")
                            }
                            else{
                                this.$comments_wrapper?.addClass("hidden")
                            }
                            $(".close-comments-btn")?.off("click")?.click(e=>{
                                e.preventDefault()
                                this.$comments_wrapper?.addClass("hidden")
                            })
                        })
                    }
                }
                else{
                    lite.alerts.toast({
                        toast_type: resolve.status,
                        title: "Failed to fetch Document!",
                        message: "Something went wrong while fetching the doc."
                    })
                }
                return resolve.status
            }
            else if(this.is_quick_form){
                if (this.quick_form_data){
                    this.doc_data = this.quick_form_data
                    this.setup.docstatus = 0
                }
            }
        }
        return true
    }
}