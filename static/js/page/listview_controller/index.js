import HTML_Builder from "../html/html_builder.js"

import {
    open_document,
    submit_selected_rows,
    cancel_selected_rows,
    export_selected_rows_to_excel,
} from "../../listviews/functions/common.js"

export default class Listview_Controller {
    
    constructor(config) {
        this.has_loaded = false
        this.page_size = 20
        this.total_records = 0
        this.queried_records = 0
        this.total_pages = 0
        this.current_page = 1
        this.listview = {}
        this.config = config
        lite.utils = config.utils
        this.connect = config.connect
        this.page_controller = config.page_controller
        this.session = config.session
        this.lite_picker = config.lite_picker
        this.page_info = null
        this.document = null
        this.prev_document = null
        this.listview = null
        this.list_height = null
        this.listview_columns = null
        this.list_column_fields = []
        this.main_content_wraper_classname = '.main-content-wrapper'
        this.content_group_wrapper = '.content-group.active'
        this.filters_wrapper_classname = '.filters-wrapper'
        this.filter_fields_wrapper_classname = '.filter-fields'
        this.list_wrapper_class = '.listview-wrapper'
        this.list_actions_classname = '.list-actions'
        this.list_actions_btn_classname = '.list-actions-btn'
        this.list_body_classname = '.lbody'
        this.list_body_row_classname = '.list-row'
        this.list_row_cell_classname = '.list-cell'
        this.list_check_classname = '.list-check'
        this.action_option_classname = '.row-action-option'
        this.list_action_option_classname = '.action-option'
        this.list_row_class_name = '.list-row'
        this.pagination_wrapper_class = '.pagination_wrapper'
        this.$pagination_selector = '.paginate-select'
        this.$page_size_selector = '.page-size-select'
        this.page_jump = '.page-jump'
        this.$main_content_wrapper = null
        this.$content_groups = null
        this.$filters_wrapper = null
        this.$filter_fields_wrapper = null
        this.is_multicontent = false
        this.$active_content_group = null
        this.$listview_wrapper = null
        this.$list_wrapper = null
        this.$list_body = null
        this.list_actions = {}

        // html bulder
        this.html_builder = new HTML_Builder(this.config)

        // functions
        this.dropdown_toggler = null
        this.list_functions = {}
        this.row_functions = {}
        this.list_action_configs = []
        this.row_action_configs = []

        // data
        this.old_filters = {}
        this.filters = {}
        this.rows = []
        this.selected_rows = []

        // sorting
        this.sortable_heads = null
        this.sort_order_class_name = '.sort-order'
        this.sortable_list_head_class_name = '.list-head.sortable'
        this.sorting_fields = []
    }

    async init_listview() {
        // evaluate listview initialization
        lite.form_data = undefined
        lite.form_state = undefined
        lite.is_new_form = false
        const listview  = await lite.utils.import_list_content()
        if(listview){
            // clear forms first
            $(".form-fields").empty()
            $(".audit-trail-wrapper, .preview-wrapper")?.remove()
            this.listview = {...listview}
            this.page_info = this.session.get_type_session()
            this.document = this.page_info?.document?.toLowerCase()
            this.list_height = this?.listview?.setup.list_height || 400
            this.filters = {}
            this.default_filters = lite.utils.copy_object(this.listview?.default_filters) || null
            this.fixed_cols = []
            this.fixed_cols.push({
                column_title: `ID/Name`,
                column_name: "name",
                column_type: "link",
                model: this?.listview?.setup?.model,
                columns: 3,
                sortable: true,
                icon:"edit_note",
                icon_color:"teal"
            })
            if(this.listview?.setup?.include_creation_date_column !== false){
                this.fixed_cols.push({
                    column_title: `Created On`,
                    column_name: "created_on",
                    column_type: "date",
                    columns: 1,
                    sortable: true,
                    icon:"event_available",
                    icon_color:"orange"
                })
            }
            if (this.listview) {
                this.listview_columns = [
                    ...this.fixed_cols,
                    ...this.listview?.columns
                ]
            }
    
            if (this.#validate_configuration()) {
                this.#get_list_columns()
                if (!lite.utils.is_empty_object(this.listview)) {
                    this.$main_content_wrapper = $(this.main_content_wraper_classname)
                    this.$content_groups = this.$main_content_wrapper?.find(this.content_group_wrapper)
                    this.$active_content_group = this.$content_groups
                    if (!lite.utils.is_empty_array(this.$content_groups)) {
                        if (this.page_controller.is_multi_content_page())
                            this.$active_content_group = this.$content_groups?.find('.multi-content-group:not(.hidden)')
                    }
                    if (lite.utils.is_empty_array(this.$active_content_group)) {
                        console.error(`LISTVIEW GENERATION ERROR: The config for ${this.document} is not properly setup!`)
                    }
                    else {
                        this.#map_default_functions()
                        this.#init_listview_filters()
                        this.#init_list()
                        this.#init_scroll_manager()
                    }
                }
                else { console.error(`LISTVIEW GENERATION ERROR: The config for ${this.document} is not properly setup!`) }
            }
            else { console.error("Page List View Configuration faild!") }
        }
    }
    #validate_configuration() {
        return true
    }
    #get_list_columns() {
        this.list_column_fields = []
        $.each(this.listview_columns, (_, c) => {
            if (c.column_name)
                this.list_column_fields.push(c.column_name)
        })
    }

    #init_listview_filters() {
        const params = lite.utils.get_url_parameters()
        this.$filters_wrapper = this.$active_content_group?.find(this.filters_wrapper_classname)
        if (!lite.utils.is_empty_array(this.listview?.filters) && !lite.utils.is_empty_array(this.$filters_wrapper)) {
            this.$filter_fields_wrapper = this.$filters_wrapper.find(this.filter_fields_wrapper_classname)
            if (this.$filter_fields_wrapper) {
                this.$filter_fields_wrapper?.empty()
                let list_filters = ""
                $.each(this.listview?.filters, (_, f) => {
                    f.omitlabels = true
                    f.classnames = 'filter-field mr-2 max-w-[190px]'
                    f.value = params[f.fieldname] || ''
                    list_filters += this.html_builder.build_form_field(f, this.config.setup)
                })
                this.$filter_fields_wrapper.append(list_filters)
                lite.lite_selector.init_selectors(this.#handle_filters_change, this, null, "lstfiltevents")
                lite.lite_date_picker.init()
                this.#handle_date_picker_change()
            }
        }
    }

    // handling filtering event
    #handle_date_picker_change(){
        $(".lite-field.filter-field[is-date-field='true']")?.off("focusout")?.focusout(e=>{
            const v = e.currentTarget.value, fieldname = $(e.currentTarget).attr("fieldname")
            if(this.filters[fieldname] !== v){
                this.#handle_filters_change({value:v, field:e.currentTarget}, this)
            }
        })
        

    }
    #handle_filters_change(data, cls) {
        if (lite.utils.lower_case(lite.utils.get_url_parameters("type")) == "list") {
            cls.old_filters = cls.filters
            let filts = {}
            filts[data.fieldname] = data.value
            if (!data.value) {
                lite.utils.remove_url_parameters(data.fieldname)
                $(data.field).attr('value_id', "")
            }
            else {
                $(data.field).attr('value_id', data.fieldname == "name" ? data.value : data.value_id)
                lite.utils.update_url_parameters(filts)
            }
            // get old value first
            const old_value = cls.filters[data.fieldname]
            // then update filters to prevent reload
            cls.#update_list_filters()            
            if( old_value != data.value){
                cls.populate_list()
            }
        }
    }

    #init_list() {
        if (!lite.utils.is_empty_array(this.listview_columns)) {
            this.$listview_wrapper = this.$active_content_group.find(this.list_wrapper_class)
            if (!lite.utils.is_empty_array(this.$listview_wrapper)) {
                this.$list_wrapper = this.$listview_wrapper
                const list_structure = this.html_builder.create_list_structure(this.listview_columns, this.list_height)
                this.$list_wrapper.empty().html(list_structure)
                this.$list_body = this.$list_wrapper?.find(this.list_body_classname)
                this.#map_row_functions()
                this.populate_list(true)
                this.#init_sorting()
                this.has_loaded = true
            }
        }
    }
    populate_list(reload_pagination=false) {
        // console.log("xxxxxxxxxxxxxxxxxxxxxxxxxx hehehehehehehehehehehehehehehe xxxxxxxxxxxxxxxxxxxxxxxxxx")
        this.#add_or_remove_list_loader()
        this.#update_list_filters()
        this.#clear_list()
        lite.connect.get({
            model: this.listview.setup.model,
            sort: this.sorting_fields,
            filters: this.filters,
            columns: this.list_column_fields,
            page_size: this.page_size,
            current_page: this.current_page,
        }).then(resolve => {
            
            if (resolve) {
                this.#add_or_remove_list_loader(false)
                if (resolve.status === lite.status_codes.ok) {
                    const data = resolve.data
                    this.total_pages = data.total_pages
                    this.total_records = data.total_records
                    this.queried_total = data.queried_total
                    this.#generate_rows(data.rows, reload_pagination)
                }
                else{
                    this.#enable_list_action_btns()
                }
                this.#enable_list_action_btns()
            }
            else {
                console.error("FAILED TO FETCH DATA: Something went wrong!")
            }
        }).catch(error => {
            console.error(error)
        })
    }


    #add_or_remove_list_loader(add=true,is_empty_content=false){
        if(add){
            this.$list_body?.html(`
                <div class="listview-loader h-[${this.list_height}vh] w-full flex items-center justify-center flex-col">
                    ${lite.utils.generate_loader({text:"Fetching Content",loader_type:"spin", size:50})}
                    <div class="px-5 text-12 py-1 rounded-md border bg-default/20 border-dotted border-secondary_color/50 text-default text-center mt-5">Fetching ${lite.utils.replace_chars(this?.listview?.setup?.model, "_"," ")} Content</div>
                </div>
            `)
        }
        else{
            this.$listview_wrapper.find(".listview-loader").remove()
        }
    }

    #generate_rows(data,reload_pagination=false) {
        let list_rows = ''
        this.$list_body?.empty()
        let count_start = this.current_page
        if(this.current_page > 1){
            count_start = lite.utils.string_to_float((this.current_page-1) * this.page_size)
        }
        
        $.each(data, (_, r) => {
            list_rows += this.html_builder.create_list_row(count_start, r, this.listview_columns, this.row_action_configs, this.listview)
            count_start += 1
        })
        this.$list_body.html(list_rows)
        this.#init_list_checks()
        this.#init_row_actions()
        
        if(reload_pagination){
            // this.#init_pagination()
        }
        this.#init_pagination()
    }

    #clear_list() {
        this.$list_body?.empty()
    }

    #calculate_pagination_visible_numbers(){
        let range = []
        let start = Math.max(1, this.current_page - 3)
        let end = Math.min(this.total_pages, this.current_page + 3)
        
        for (let i = start; i <= end; i++) {
            range.push(i);
        }
        return range
    }

    #init_pagination() {
        const visible_page_range = this.#calculate_pagination_visible_numbers()
        this.$list_wrapper.find(this.pagination_wrapper_class).remove()
        this.$list_wrapper.append(this.html_builder.create_pagination({
            total_pages: this.total_pages,
            page_range: visible_page_range,
            current_page: this.current_page,
            page_size: this.page_size,
            total_records: this.total_records,
            queried_total: this.queried_total
        }))
        // pagination click
        this.$list_wrapper.find(this.pagination_wrapper_class).find(this.$pagination_selector)?.off("click").click(e => {
            e.preventDefault()
            const next_page = lite.utils.string_to_int(lite.utils.get_attribute(e.currentTarget, 'index'))
            if (parseInt(next_page) !== parseInt(this.current_page)) {
                this.current_page = next_page
                $(".pagination_wrapper").find(".active").removeClass("active bg-default").find("span").removeClass("text-white font-bold")
                $(e.currentTarget).addClass("active bg-default").find("span").addClass("text-white font-bold")
                this.populate_list()
            }
        })

        

        this.$list_wrapper.find(this.page_jump)?.off("change").change(e => {
            const next_page = lite.utils.string_to_int(lite.utils.get_field_value(e.currentTarget))
            if (parseInt(next_page) !== parseInt(this.current_page)) {
                this.current_page = next_page
                this.populate_list()
            }
        })

        // page size selector
        this.$list_wrapper.find(this.$page_size_selector)?.off("change").change(e => {
            const page_size = lite.utils.string_to_int(lite.utils.get_field_value(e.currentTarget))
            if (parseInt(page_size) !== parseInt(this.current_page)) {
                this.page_size = page_size
                this.populate_list()
            }
        })
    }


    #init_sorting() {
        this.$listview_wrapper.find(this.sortable_list_head_class_name).off('click').click(e => {
            const column_name = lite.utils.get_attribute(e.currentTarget, 'column_name')
            const order = lite.utils.get_attribute(e.currentTarget, 'order')
            let new_order = ''
            switch (order) {
                case 'desc':
                    new_order = column_name
                    lite.utils.set_attribute(e.currentTarget, 'order', 'asc')
                    break;
                case 'asc':
                    new_order = `-${column_name}`
                    lite.utils.set_attribute(e.currentTarget, 'order', 'desc')
                    break;
            }
            if (!lite.utils.is_empty_array(this.sorting_fields)) {
                const new_list = this.sorting_fields.filter(s => lite.utils.replace_chars(s, '-', '') !== lite.utils.replace_chars(new_order, '-', ''))
                // this.sorting_fields = [...new_list, new_order]
                this.sorting_fields = [new_order]
            }
            else {
                this.sorting_fields.push(new_order)
            }
            if (!lite.utils.is_empty_array(this.sorting_fields))
                this.populate_list()
        })

    }

    #init_list_checks() {
        this.$list_wrapper?.find(this.list_check_classname)?.off("change")?.change(e => {
            const row_type = lite.utils.get_attribute(e.currentTarget, 'row-type')
            if (row_type === 'head') {
                const check_status = $(e.currentTarget).prop('checked')
                this.$list_wrapper.find(this.list_body_classname)?.find(this.list_check_classname)?.prop('checked', check_status)
            }
            this.#update_selected_rows()
            if (lite.utils.array_has_data(this.selected_rows)) {
                lite.utils.show(this.$filters_wrapper.find('.check-controlled'))
            }
            else {
                lite.utils.hide(this.$filters_wrapper.find('.check-controlled:not(.refresh)'))
            }
        })
    }

    #init_row_actions() {
        $(this.$list_wrapper).find(this.action_option_classname).on('click', e => {
            e.preventDefault()
            const
                action = lite.utils.get_attribute(e.currentTarget, 'for'),
                row_id = lite.utils.get_attribute(e.currentTarget, 'for-row'),
                row_html = lite.utils.get_element_by_id(row_id),
                row_values = this.#get_row_values(row_html)
            this.row_functions[action]({ controller:this, config: this.config, setup: this.listview.setup, row_id: row_id, row_html: row_html, values: row_values })
        })
    }

    #get_row_values(row) {
        const cells = $(row).find(this.list_row_cell_classname)
        let values = { id: lite.utils.get_attribute(row, "lite-value") }
        if (!lite.utils.is_empty_array(cells)) {
            $.each(cells, (_, c) => values[lite.utils.get_attribute(c, 'data-field-name')] = lite.utils.get_attribute(c, 'data-value'))
        }
        return values
    }

    #enable_list_action_btns() {
        this.$list_actions = $(this.$filters_wrapper).find(this.list_actions_classname)
        if (lite.utils.is_empty_array(this.$list_actions.find(this.list_actions_btn_classname))) {
            this.#map_list_functions()
                this.$list_actions.append(this.html_builder.create_list_actions_btn(this.list_action_configs))

            this.$filters_wrapper.find(".dropdown-toggle").click(e => {
                this.current_options_btn = e.currentTarget
            })
            this.$filters_wrapper.find(this.list_action_option_classname)?.click(e => {
                const action = lite.utils.get_attribute(e.currentTarget, 'action')
                this.list_functions[action](this.#get_data_list(), this)
                $(this.current_options_btn).trigger("click")
                $(this.current_options_btn).attr("aria-expanded", false)
            })
        }
    }

    #map_default_functions() {
        const setup = this.listview.setup
        this.row_action_configs = []
        this.row_functions = {}
        this.list_functions = {}
        this.list_functions['Refresh List'] = this.refresh_list
        this.list_action_configs.push({ fun: this.populate_list, title: 'Refresh List', icon: 'published_with_changes', icon_color: 'orange', classnames:"refresh" })
        this.row_functions['Open'] = open_document
        this.row_action_configs.push({ fun: open_document, title: 'Open', icon: 'open_in_new', icon_color: 'indigo', show_on_list_check: true })
        if (setup?.allow_submit) {
            this.list_functions['Submit Selected Rows'] = submit_selected_rows
            // this.row_functions['Submit Row'] = submit_selected_rows
            this.list_action_configs.push({ fun: submit_selected_rows, title: 'Submit Selected Rows', icon: 'save', icon_color: 'indigo', show_on_list_check: true })
            // this.row_action_configs.push({ fun: submit_selected_rows, title: 'Submit Row', icon: 'save', icon_color: 'indigo', show_on_list_check: true })
        }
        if (setup?.allow_cancel) {
            this.list_functions['Cancel Selected Rows'] = cancel_selected_rows
            this.row_functions['Cancel Row'] = cancel_selected_rows
            this.list_action_configs.push({ fun: cancel_selected_rows, title: 'Cancel Selected Rows', icon: 'block', icon_color: 'yellow', show_on_list_check: true })
            this.row_action_configs.push({ fun: cancel_selected_rows, title: 'Cancel Row', icon: 'block', icon_color: 'yellow', show_on_list_check: true })
        }
        if (setup?.allow_delete) {
            this.list_functions['Delete Selected Rows'] = this.delete_selected_rows
            this.row_functions['Delete Row'] = this.delete_row
            this.list_action_configs.push({ fun: this.delete_selected_rows, title: 'Delete Selected Rows', icon: 'delete', icon_color: 'red', show_on_list_check: true })
            this.row_action_configs.push({ fun: this.delete_row, title: 'Delete Row', icon: 'delete', icon_color: 'red', show_on_list_check: true })
        }
        if (setup?.allow_export_csv) {
            this.list_functions['Export Selected Rows To CSV'] = this.export_selected_rows_to_csv
            this.list_action_configs.push({ fun: this.export_selected_rows_to_csv, title: 'Export Selected Rows To CSV', icon: 'csv', icon_color: 'emerald', show_on_list_check: true })
        }
        if (setup?.allow_export_excel) {
            this.list_functions['Export Selected Rows To EXCEL'] = this.export_selected_rows_to_excel
            this.list_action_configs.push({ fun: this.export_selected_rows_to_excel, title: 'Export Selected Rows To EXCEL', icon: 'table_chart', icon_color: 'blue', show_on_list_check: true })
        }
    }

    #map_list_functions() {
        const actions = this.listview?.actions
        if (actions && !lite.utils.is_empty_array(actions?.main)) {
            $.each(actions?.main, (_, f) => {
                this.list_action_configs.push(f)
                this.list_functions[f?.title] = f?.fun
            })
        }
    }

    #map_row_functions() {
        const actions = this.listview?.actions
        if (actions && !lite.utils.is_empty_array(actions?.row)) {
            $.each(actions?.row, (_, f) => {
                this.row_action_configs.push(f)
                this.row_functions[f?.title] = f?.fun
            })
        }
    }

    #get_data_list() {
        this.#update_list_filters()
        this.#update_selected_rows()
        return {controller:this, filters: this.filters, selected_rows: this.selected_rows, setup: this.listview.setup }
    }
    #update_list_filters() {
        const filter_fields = this.$filter_fields_wrapper.find('input')
        if (!lite.utils.is_empty_array(filter_fields)) {
            let filters = {}
            $.each(filter_fields, (_, f) => {
                const val = lite.utils.get_attribute(f, "value") || lite.utils.get_field_value(f)
                if(val){
                    filters[lite.utils.get_attribute(f, 'fieldname')] = val
                }
            })

            const url_filters = lite.utils.get_url_parameters()
            if(lite.utils.object_has_data(url_filters)){
                $.each(lite.utils.get_object_keys(url_filters),(_, k)=>{
                    if(!["type", "list","document","doc","loc"].includes(k) && url_filters[k]){
                        filters[k] = url_filters[k]
                    }
                })
            }
            
            let default_filters = {}
            if (lite.utils.is_object(this.default_filters) && lite.utils.object_has_data(this.default_filters)){
                default_filters = this.default_filters
            }
            this.filters = {...filters, ...default_filters}
            return this.filters
        }

    }
    #update_selected_rows() {
        const rows = this.$list_wrapper.find(this.list_body_row_classname)
        this.selected_rows = []
        $.each(rows, (_, r) => {
            if ($(r).find(this.list_check_classname)?.prop('checked'))
                this.selected_rows.push({ values: this.#get_row_values(r), element: r })
        })
    }

    #init_scroll_manager() {
        // console.log(this.$list_body)
    }



    // ============================================================= LIST DEFAULT ACTIONS==============================
    refresh_list(params){
        const {controller} = params
        controller.populate_list(true)
    }

    async delete_row(params){
        const {controller, values, setup} = params
        const {id} = values
        if(id){
            const deleted = await lite.connect.delete_docs({model:setup?.model, docs:[id]})
            if(deleted.status == lite.status_codes.ok){
                lite.alerts.toast({
                    toast_type:lite.status_codes.ok,
                    title:"Deleted Successfully",
                    message:"Row deleted successfully",
                })
                controller.populate_list(true)
            }
        }
    }

    async delete_selected_rows(params){
        const {controller, selected_rows, setup} = params
        if(lite.utils.array_has_data(selected_rows)){
            let ids = selected_rows?.map(row=>lite.utils.string_to_float(row.values.id))
            const deleted = await lite.connect.delete_docs({model:setup?.model, docs:ids})
            if(deleted.status == lite.status_codes.ok){
                lite.alerts.toast({
                    toast_type:lite.status_codes.ok,
                    title:"Deleted Successfully",
                    message:"Selected rows deleted successfully",
                })
                controller.populate_list(true)
            }
        }
    }


    async export_selected_rows_to_csv(params){
        const {controller, selected_rows, setup} = params
        controller.#update_list_filters()
        const filters = controller.filters
        if(lite.utils.array_has_data(selected_rows)){
            let ids = selected_rows?.map(row=>lite.utils.string_to_float(row.values.id))
            const {status, data, error} = await lite.connect.export_data(setup.model,ids,"csv", filters, false)
        }
    }

    async export_selected_rows_to_excel(params){
        const {controller, selected_rows, setup} = params
        if(lite.utils.array_has_data(selected_rows)){
            let ids = selected_rows?.map(row=>lite.utils.string_to_float(row.values.id))
            const {status, data, error} = await lite.connect.export_data(setup.model,ids, "excel",false)
        }
    }
}
