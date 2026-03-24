import HTML_Builder from '../html/html_builder.js'
import Report_HTML_Generator from '../html/report_html_generator.js'
import Default_Actions from './default_actions.js'

export default class Reports {
    constructor(config) {
        
        this.utils = config.utils
        this.page_controller = config.page_controller
        this.charts = config.charts
        this.session = config.session
        this.nav_manager = config.nav_manager
        this.connect = config.connect
        this.alerts = config.alerts
        this.has_loaded = false
        this.page_length = 0
        this.current_page_length = 0
        this.page_chunks = 200
        this.report_setup = null
        this.has_dynamic_columns = false
        this.html_builder = new HTML_Builder(config)
        this.report_html_generator = new Report_HTML_Generator()
        this.default_actions = new Default_Actions(config)
        this.$report_wrapper = lite.utils.get_elements('report-wrapper')
        this.$table_controllers = lite.utils.get_elements('table-controllers')
        this.$table_container = lite.utils.get_elements('table-container')
        this.$report_actions_wrapper = lite.utils.get_elements('report-actions-wrapper')
        this.$report_action_option = lite.utils.get_elements('report-download-action')
        this.$expand_shrink_table = lite.utils.get_elements('expand-shrink-table')
        this.$filters_wrapper = lite.utils.get_elements('report-filters-wrapper')
        this.filters_height = 0
        this.$x_scrollers = lite.utils.get_elements('x-scrollers')?.find('button') || null
        this.$left_scroller = this?.$x_scrollers[0] || null
        this.$right_scroller = this?.$x_scrollers[1] || null
        this.$table = null
        this.$header_row = null
        this.$table_body = null
        this.table_body_initial_height = 0
        this.table_width = 0
        this.filters = {}
        this.filter_fields = []

        this.configuration = null
        this.document = null
        this.filters_setup = []
        this.columns_setup = []
        this.report_column_list = []

        this.actions = {}
        this.action_configs = []
        this.setup_report()
        this.data = []
    }


    async setup_report() {
        const report_content = await lite.utils.import_report_content()
        this.report_setup = {...report_content}
        if(report_content){
            this.has_dynamic_columns = this.report_setup?.setup?.has_dynamic_columns
            const current = lite.utils.get_url_parameters()
            this.document = lite.utils.lower_case(current?.document)
            if (this.#validate_setup()) {
                this.filters_setup = this.report_setup.filters
                this.columns_setup = this.report_setup.columns
                this.action_setup = this.report_setup.actions
                this.action_setup = this.report_setup.actions
                this.configuration = this.report_setup.setup
                this.selectors = this.report_setup.selectors
                
                this.#get_report_columns()
                
                this.#setup_filters()
                this.#setup_actions()
                this.$table_controllers.html(this.html_builder.create_table_controllers(this.configuration.title))
                this.$table_controllers.find(".x-scrollers")?.append(this.html_builder.create_table_refresh_btn())
                this.#init_table_structure().then(r => { this.init_report() })
            }
        }
    }

    #validate_setup() {
        let has_passed = true
        if (this.report_setup) {

            if (!lite.utils.has_key(this.report_setup, 'setup')) {
                has_passed = false
                console.error("Setup is missing from the config!")
            }
            if (!lite.utils.has_key(this.report_setup, 'filters')) {
                has_passed = false
                console.error("Filters is missing from the config!")
            }
            if (!lite.utils.has_key(this.report_setup, 'columns') && !this.has_dynamic_columns) {
                
                has_passed = false
                console.error("Columns is missing from the config!")
            }
        }
        else {
            has_passed = false
            this.alerts.toast({
                toast_type: lite.status_codes.not_found,
                title: "Not Found",
                message: `CONFIG NOT FOUND ERROR: ${lite.utils.capitalize(this.document)} config not found!`,
                timer: 4000
            })
        }
        return has_passed
    }

    #get_report_columns() {
        this.report_column_list = ["is_opening_or_closing"]
        $.each(this.columns_setup, (_, c) => {
            if (c.column_name)
                this.report_column_list.push(c.column_name)
        })
    }


    #add_or_remove_report_loader(add=true,is_empty_content=false,error_message){
        const wrapper = this?.$report_body || this.$table_container
        if(add){
            wrapper?.html(`
                <div class="report-loader h-[40vh] w-[90vw] flex items-center justify-center flex-col">
                    ${lite.utils.generate_loader({text:"Fetching Content",loader_type:"spin", size:50})}
                    <div class="px-5 py-1 text-12 rounded-md border bg-default/20 border-dotted border-secondary_color/50 text-default text-center mt-5">Fetching <strong>${this.report_setup?.setup?.title}</strong></div>
                </div>
            `)
        }
        else if(is_empty_content){
            wrapper?.html(`
                <div class="report-loader h-[40vh] w-[90vw] flex items-center justify-center flex-col">
                    <div class="w-[60px] h-[60px] rounded-full border border-default/30 flex items-center justify-center"><span class="material-symbols-outlined text-30 text-default/80"> check_box_outline_blank </span></div>
                    <div class="px-5 py-1 text-12 rounded-md border bg-default/20 border-dotted border-secondary_color/50 text-default text-center mt-5">
                        No Information Found
                    </div>
                    <small class="text-gray-700 mt-2 text-center">There is no info found for <strong class="">${this.report_setup?.setup?.title}</strong> at the moment.</small>
                </div>
            `)
        }
        else{
            this.$report_wrapper.find(".report-loader").remove()
            if(error_message){
                wrapper?.html(`
                    <div class="report-loader h-[40vh] w-[90vw] flex items-center justify-center flex-col">
                        <div class="w-[60px] h-[60px] rounded-full border border-red-300 flex items-center justify-center"><span class="material-symbols-outlined text-30 text-red-700"> warning </span></div>
                        <div class="px-5 py-1 text-12 rounded-md border bg-red-100 border-dotted border-red-400 text-red-700 text-center mt-5">
                            ${error_message} 
                        </div>
                        <small class="text-gray-700 mt-2 text-center">Please try refreshing the report. <br> If the error persists. Contact Support</small>
                    </div>
                `)
            }
        }
    }

    #setup_actions() {
        this.$report_actions_wrapper.empty()
        this.#setup_select_options()
        this.#map_default_functions()
        this.#map_custom_actions()
        if (!lite.utils.is_empty_array(this.action_configs)) {
            this.$report_actions_wrapper.append(this.html_builder.create_report_actions(this.action_configs))
        }
    }

    #setup_select_options() {
        if (this.selectors && !lite.utils.is_empty_array(this.selectors)) {
            $.each(this.selectors, (_, s) => {
                this.$report_actions_wrapper.append(this.#create_selector(s))
            })
        }
    }
    #create_selector(s) {
        if (s.type === 'select') {
            let select = `<select type="select" action-type="${s.ismulticontent ? 'multi-content-toggler' : ''}" class="lite-selector border rounded-md px-3 w-[240px] mr-3" placeholder="${s.placeholder}">`
            if (s.options && !lite.utils.is_empty_array(s.options)) {
                $.each(s.options, (_, opt) => {
                    select += ` <option value="${opt}">${opt}</option>`
                })
            }
            select += '</select>'
            return select
        }
    }

    #handle_action_selector_change(data, cls) {
        cls.get_filters()
        cls.#populate_report()
    }

    #map_default_functions() {
        this.actions = {}
        this.action_configs = []
        // if (this.configuration?.allow_print) {
        //     this.actions['Print Report'] = this.default_actions.print
        //     this.action_configs.push({ title: 'Print Report', icon: 'print', background_color: 'default', color: 'white', is_action_button: true })
        // }
        // if (this.configuration?.allow_download_csv) {
        //     this.actions['Print Report'] = this.download
        //     this.action_configs.push({ title: 'Print Report', icon: 'print', icon_color: 'purple', format:"print" })
        // }
        if (this.configuration?.allow_download_csv) {
            this.actions['Download CSV'] = this.download
            this.action_configs.push({ title: 'Download CSV', icon: 'csv', icon_color: 'emerald', format:"csv" })
        }
        if (this.configuration?.allow_download_excel) {
            this.actions['Download EXCEL'] = this.default_actions.download_excel
            this.action_configs.push({ title: 'Download EXCEL', icon: 'table_chart', icon_color: 'blue', format:"excel" })
        }
        if (this.configuration?.allow_download_pdf) {
            this.actions['Download PDF'] = this.default_actions.download_pdf
            this.action_configs.push({ title: 'Download PDF', icon: 'picture_as_pdf', icon_color: 'orange', format:"pdf" })
        }
    }

    #map_custom_actions() {
        if (!lite.utils.is_empty_array(this.action_setup)) {
            $.each(this.action_setup, (_, a) => {
                this.actions[a.title] = a.fun
                this.action_configs.push(a)
            })
        }
    }

    #setup_filters() {
        this.$filters_wrapper.addClass("hidden")
        this.$expand_shrink_table.addClass("expanded")
        this.$filters_wrapper.empty()
        this.fields = ''
        $.each(this.filters_setup, (_, f) => {
            f.required = false
            f.label_class = 'text-10'
            f.wrapper_class = 'intro-x'
            this.$filters_wrapper.append(this.html_builder.build_form_field(f))
        })
        // lite.lite_selector.init_selectors()
        lite.lite_selector.init_selectors(this.#handle_action_selector_change, this)
        lite.lite_date_picker.init()
        lite.lite_year_picker.init()
        $('.lite-field[is-date-field="true"], .lite-field[is-year-field="true"]')?.off("focusout")?.focusout(e=>{
            const v = e.currentTarget.value, fieldname = $(e.currentTarget).attr("fieldname")
            if(this.filters[fieldname] !== v){
                this.get_filters()
                if(v?.includes(" --> ")){
                    let split = v?.split(" --> ")
                    if(split?.length > 1){
                        this.filters.start_date = split[0]
                        this.filters.end_date = split[1]
                    }
                }
                this.#populate_report()
            }
        })
    }

    async #init_table_structure() {
        if(!this.has_dynamic_columns){
            this.$table_container.empty().html(this.html_builder.create_report_table(this.columns_setup,this.report_setup?.setup))
            this.$report_body = this.$table_container.find('.table-body')
        }
        return this.#populate_report().then(r => {
            setTimeout(() => { $('.table-row').removeClass('intro-x') }, 1500);
            return r
        })
    }



    async #populate_report() {
        const next_page = this.current_page_length + this.page_chunks
        this.#add_or_remove_report_loader()
        return this.connect.get_report({
            model: this.configuration.model,
            filters: this.filters,
            columns: this.report_column_list,
            page_from: this.current_page_length,
            page_to: next_page
        }).then(resolve => {
           
            if (resolve.status && resolve.status == lite.status_codes.ok) {
                // if the table has dynamic cols
                if(lite.utils.array_has_data(resolve.data?.rows)){
                    const {rows, columns} = resolve.data
                    if(this.has_dynamic_columns){
                        if(!columns){
                            this.alerts.toast({
                                toast_type: lite.status_codes.not_found,
                                title: "Report Columns Not Found",
                                message: `Report didn't return any columns to display!`,
                                timer: 4000
                            })
                            return false
                        }
                        else{
                            this.columns_setup = columns
                            this.$table_container.empty().html(this.html_builder.create_report_table(this.columns_setup,this.report_setup?.setup))
                            this.$report_body = this.$table_container.find('.table-body')
                        }
                    }
                    this.current_page_length = next_page
                    this.#generate_rows(rows)
                    return true
                }
                this.#add_or_remove_report_loader(false,true)
            }
            else {
                this.#add_or_remove_report_loader(false,false,resolve.error_message)
                return true
            }

        }).catch(error => {
            console.error(error)
            return false
        })
    }

    #generate_rows(data) {
        this.data = data
        let report_rows = ''
        this.$report_body?.empty()
        $.each(data, (_, r) => report_rows += this.html_builder.create_report_row(_ + 1, r, this.columns_setup,this.report_setup?.setup))
        this.$report_body.append(report_rows)
        this.$report_body.append(this.html_builder.create_empty_report_row(this.columns_setup))
    }

    #init_resizing() {
        let header_cells = document.querySelectorAll(".header-cell.resizable");
        let isResizing = false;
        let initialX;
        let initialWidth;
        $.each($('.header-cell.resizable'), (_, d) => {
            $(d).mousedown(e => {
                isResizing = true;
                initialX = e.clientX;
                initialWidth = parseFloat(
                    getComputedStyle(e, null).getPropertyValue("width")
                );
                document.addEventListener("mousemove", resize);
                document.addEventListener("mouseup", stopResize);
            })
        })

        function resize(e) {
            if (!isResizing) return;
            const newWidth = initialWidth + (e.clientX - initialX);
            header_cells.style.width = newWidth + "px";
        }

        function stopResize() {
            isResizing = false;
            document.removeEventListener("mousemove", resize);
            document.removeEventListener("mouseup", stopResize);
        }
    }


    init_report() {
        this.$expand_shrink_table = lite.utils.get_elements('expand-shrink-table')
        this.$x_scrollers = lite.utils.get_elements('x-scrollers')?.find('button') || null
        this.$left_scroller = this?.$x_scrollers[0] || null
        this.$right_scroller = this?.$x_scrollers[1] || null
        this.$report_refresh_btn = $(".refresh-report")
        this.#update_table_properties()
        this.#init_x_scrollers()
        this.#init_refresh_report()
        this.#init_expand_shrink_table()
        this.#init_filters()
        this.#init_download_actions_btn()
        this.#init_report_action_options()
        
    }

    #update_table_properties() {
        const table = lite.utils.get_elements('table-container')
        const table_header = lite.utils.get_elements('header-row')
        const table_body = lite.utils.get_elements('table-body')
        const header_width = lite.utils.get_element_width(table_header)
        this.filters_height = lite.utils.get_element_height(this.$filters_wrapper)
        this.$table = table
        this.$header_row = table_header
        this.$table_body = table_body
        this.table_width = header_width
    }

    #init_download_actions_btn(){
        $("#report-actions-btn")?.click(e=>{
            this.current_options_btn = e.currentTarget
            this.$report_action_option = $(".report-action-option")
            this.$report_action_option?.off("click")?.click(e => {
                this.download(lite.utils.get_attribute(e.currentTarget, "format"))
            })
        })
    }

    #init_report_action_options() {
        
        this.$report_action_option?.click(e => {
            const file_type = lite.utils.get_attribute(e.target, 'for')
            const current = this.session.get_type_session()
            if (data && !lite.utils.is_empty_array(data)) {
                const title = lite.utils.capitalize(current.document || current.type) + ` - ${lite.utils.today()}`
                switch (lite.utils.lower_case(file_type)) {
                    case 'csv':
                        lite.utils.export_csv(data, title)
                        break;
                    case 'excel':
                        lite.utils.export_excel(data, title)
                        break;
                    default:
                        break;
                }
            }
        })
    }

    #init_expand_shrink_table() {
        this.$expand_shrink_table?.click(e => {
            if (this.$filters_wrapper.hasClass('hidden')) {
                this.$expand_shrink_table.find('.text').text("Hide Filters")
                this.#expand_shrink_table(false)
            }
            else {
                this.$expand_shrink_table.find('.text').text("Show Filters")
                this.#expand_shrink_table(true)
            }
        })
    }
    #expand_shrink_table(expand) {
        const table_body_height = lite.utils.get_element_height(this.$table_body) || 0
        const new_height = !expand ? (table_body_height + this.filters_height) : (table_body_height - this.filters_height)
        expand ? lite.utils.hide(this.$filters_wrapper) : lite.utils.show(this.$filters_wrapper)
        lite.utils.set_element_height(this.$table_body, new_height)
    }
    #init_x_scrollers() {
        $(this.$left_scroller)?.click(e => this.#scroll('-=260'))
        $(this.$right_scroller)?.click(e => this.#scroll('+=260'))
    }
    #scroll(dir) {
        $(this.$table)?.animate({
            scrollLeft: dir
        }, 'slow')
    }
    #init_refresh_report(){
        this.$report_refresh_btn?.click(e=>{
            this.#init_table_structure()
        })
    }
    // initialize filters
    #init_filters(fun = undefined) {
        this.#update_filters()
        if (this.filter_fields?.length > 0) {
            $.each(this.filter_fields, (i, el) => {
                const input_type = lite.utils.get_element_tag_name(el)
                if (input_type === 'select') {
                    $(el).change(e => {
                        if (fun !== undefined) {
                            fun({ filter_fields: this.filter_fields, filters: this.filters })
                        }
                    })
                }
                else if (input_type === 'input') {
                    $(el).on('input', e => {
                        if (fun !== undefined) {
                            fun({ filter_fields: this.filter_fields, filters: this.filters })
                        }
                    })
                }

            })
        }
    }
    on_filter(fun) {
        if (fun) {
            this.#init_filters(fun)
        }
    }
    // get filter fields
    get_filter_fields() {
        const fields = this.$filters_wrapper?.find('input.lite-field')
        this.filter_fields = fields
        return fields
    }
    // get filter values
    get_filters() {
        this.#update_filters()
        return this.filters
    }
    #update_filters() {
        this.filter_fields = this.get_filter_fields()
        let filters = {}
        if (lite.utils.array_has_data(this.filter_fields)) {
            $.each(this.filter_fields, (_, f) => {
                const v = $(f).val()
                if(v)
                    filters[lite.utils.get_attribute(f, 'fieldname')] = v
            })
        }
        this.filters = filters
    }

    // download functions
    async download(format) {
        const cols_html = this.report_html_generator.create_select_columns_on_report_download_form(this.columns_setup)
        const modal = lite.modals.custom_modal("Select Columns",cols_html,{text:"Download Now", fun:async (data)=>{
            if(data){
                const fields = lite.utils.remove_zero_values(data)
                this.download_fields = []
                this.columns_setup?.map(col=>{
                    if(fields[col.column_name]){
                        this.download_fields.push(col.column_name)
                    }
                })
                let title = `${this.configuration.title} - ${lite.utils.today()}`
                await this.connect.download_report({
                    model: this.configuration.model,
                    filters: this.filters,
                    fields: this.download_fields,
                    title: title,
                    format: format
                })
            }
        }})
        $("#select-all-report-columns")?.change(e=>{
            $(modal.modal)?.find("input[type=checkbox].lite-field")?.prop("checked", $(e.currentTarget).prop("checked"))
        })
    }
}
