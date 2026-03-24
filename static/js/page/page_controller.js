
import Form_Controller from "./form_controller/index.js"
import Listview_Controller from "./listview_controller/index.js"

class Page_Controller {
    constructor({ utils, session, nav, connect, on_page_loaded, alerts, lite_commands,lite_date_picker,lite_selector, ...rest }) {
        // select all the elements
        this.overlay = $('#loader-overlay')
        this.breadcrumb = $('.breadcrumb')
        this.content_wrapper = $('.conetnt-wrapper')
        this.grid_content = $('.grid-content')
        this.page_content_type_selector = $('.page-content-content-type')
        // multi content wrapper
        this.multi_content_group = $('.multi-content-group')

        this.$main_grid = $(".main-grid")
        this.$side_grid = $(".side-grid")

        // 
        this.stats_view = $('.stats-view')
        this.content_group = $('.content-group')
        this.dashboard_view_content = $('.dashboard-view-content')
        this.list_view_content = $('.list-view-content')
        this.info_view_content = $('.info-view-content')
        this.new_form_view_content = $('.new-form-view-content')
        this.report_view_content = $('.report-view-content')
        // title elements
        this.title_content_wrapper = $('.title-content-wrapper')
        this.module_name_title = $('.module-name-title')
        this.app_name_title = $('.app-name-title')
        this.doc_name_title = $('.doc-name-title')
        this.doc_status_wrapper = $('.doc-status-wrapper')
        this.doc_status_pill = $('.doc-status-pill')
        this.doc_status_text = $('.doc-status-text')
        this.content_type_title = $('.content-type-title')
        this.back_forth_btns = $('.back-forth-btns')
        this.navigate_next_btn = $('.navigate-next-btn')
        this.navigate_prev_btn = $('.navigate-prev-btn')
        this.title_content = $('.title-content')
        this.page_description = $('.page-description')
        this.page_actions_wrapper = $('.page-actions-wrapper')
        this.actions_group = $('.actions-group')
        this.new_create_btn = $ (".list-view-content-create-new-btn")
        // buttons to initialize
        this.content_type_action = $('.content-type-action')
        this.content_type_action_select = $('select.lite-selector[action-type="multi-content-toggler"]')
        this.expand_table_btn = $('.expand-table-btn')
        this.new_action_btn = $('.new-action-btn')
        this.info_view_action_btn = $('.info-view-action-btn')
        this.main_content_wrapper = $('.main-content-wrapper')
        this.side_wrapper = $('.side-wrapper')
        this.side_list_view = $('.side-list-view')
        this.side_info_view = $('.side-info-view w-full')
        this.side_new_form_view = $('.side-new-form-view')
        // dropdown menus
        this.active_toggler = undefined
        this.dropdown_toggler = $('.dropdown-toggle')
        this.dropown_menu = $('.dropdown-menu')
        this.dropdown_item = $('.dropdown-item')

        // listview controller
        this.is_multicontent_page = false
        this.listview_controller = null
        // form controller
        this.form_controller = null

        // table management
        this.info_view_link = $('.info-view-link')
        this.connect = connect
        this.utils = utils
        this.session = session
        this.nav = nav
        this.alerts = alerts
        this.lite_commands = lite_commands
        this.lite_date_picker = lite_date_picker
        this.lite_selector = lite_selector
        this.is_page_loading = true
        this.page_loader_interval = null
        this.init_page_session()
        this.init_page_loader(on_page_loaded)

        this.on_page_type_change_actions = []


        // select controller
        this.on_select = null
        this.lite_selector.init_selectors(this.init_page_content_type_change_listener, this)
        this.lite_selector.init_selectors(this.handle_select_change_event, this)
    }

    init_page_session() {
        lite.session.set_session("listview_status", null)
        let session_data = this.session.get_type_session()
        const url_parameters = this.utils.get_url_parameters()
        session_data.module = this.utils.get_current_module()
        if (!this.utils.is_empty_object(url_parameters)) {
            this.utils.get_object_keys(url_parameters)?.forEach(key => {
                session_data[key] = url_parameters[key]
            });
        }
        this.session.set_session("type", session_data)
    }

    // handle page loading
    async init_page_loader() {
        this.page_loader_interval = setInterval(async () => {
            if (this.utils.get_page_state() === "loading") {
            } else if (this.utils.get_page_state() === "complete") {
                clearInterval(this.page_loader_interval)
                await this.init_controllers()
            }
        }, 200);
    }

    async init_controllers(){
        // lite.permission_controller?.init_permission_controller()
        this.listview_controller = new Listview_Controller({
            page_controller: this,
            session: this.session,
            utils: this.utils,
            connect: this.connect,
            alerts: this.alerts,
            lite_date_picker:this.lite_date_picker
        })
        // set listview controller state
        this.init_pop_state_listner()
        this.init_prev_next_navigation()
        this.init_page_url_changed()
        this.remove_skeleton()
        this.update_breadcrumb()
        this.update_title_content()
        this.init_page_actions()
        this.hide_overlay()
        this.init_page_menu_toggler()
        this.init_page_tables_manager()
        this.update_nav_user_actions()
    }

    

    init_pop_state_listner() {
        const cls = this
        window.addEventListener('popstate', function (event) {
            cls.init_page_url_changed()
        });
    }

    async on_page_loaded(func_to_execute) {
        const  after_load = await lite.utils.delay_until(()=>{
            if (this.utils.get_page_state() === "complete") {
                lite.utils.hide_display_icons()
                return true
            }
        })
        lite.nav.update_nav_menus(lite.system_settings)
        if (func_to_execute) {
            func_to_execute()
        }
    }

    // components skeleton from pag UI
    mark_skeleton() {
        $('.skeleton').addClass('skull')
    }
    enable_skeleton() {
        $('.skull').addClass('skeleton')
    }
    remove_skeleton() {
        this.mark_skeleton()
        lite.utils.init_dashboard()
        $('.skeleton').addClass('un-skeleton')
        $('.skeleton').removeClass('skeleton un-skeleton')
    }

    toggle_overlay() {
        this.overlay.toggleClass('hidden')
    }
    hide_overlay() {
        this.overlay.addClass('hidden')
    }

    // update breadcrumbs
    update_breadcrumb() {
        this.breadcrumb.empty()
        const current = this.session.get_type_session()
        if (current.module) {
            this.breadcrumb.append(this.nav.create_breadcrumb(this.utils.capitalize(current.module), '', true))
        }
        if (current.document) {
            this.breadcrumb.append(this.nav.create_breadcrumb(this.utils.capitalize(current.document), '', true))
        }
    }

    update_nav_user_actions(){
        if(!lite.utils.is_empty_object(lite.user)){
            if(lite.user?.dp){
                $(".nav-dp").attr("src",lite.user.dp)
            }
            $(".nav-full-names").text(`${lite.user?.first_name || ""} ${lite.user?.last_name || ""}`)
            $(".nav-designation").text(lite.user?.main_role || "")
            $(".nav-logo").attr("src", lite.user?.company?.company_logo || "/static/images/logo/logo.svg")
        }
    }

    init_prev_next_navigation() {
        const cls = this
        this.navigate_prev_btn.click(e => {
            window.history.back()
        })
        this.navigate_next_btn.click(e => {
            window.history.forward()
        })
        this.update_breadcrumb()
        this.content_type_title.click(function (e) {
            e.preventDefault()
            cls.utils.update_url_parameters({ type: 'list' })
            cls.init_page_url_changed()
        })
    }
    go_back() {
        window.history.back()
    }

    hide_content(el) {
        $(el)?.addClass('hidden').removeClass('active')
    }

    show_content(el) {
        $(el)?.removeClass('hidden').addClass('active')
    }
    go_to(url) {
        window.location.href = url
    }

    // handle when page type changes
    on_page_type_change(fun,cls){
        if(fun){
            this.on_page_type_change_actions.push({fun:fun,cls:cls})
        }
    }

    // initialize page url change listener
    init_page_url_changed() {
        let url_params = this.utils.get_url_parameters()
        if (this.utils.has_key(url_params, 'type') && this.utils.has_key(url_params, 'loc') && this.utils.has_key(url_params, 'document')) {
            url_params.module = this.utils.get_current_module()
            this.session.update_session('type', url_params)
        }
        else {
            const loc = this.utils.lower_case(this.utils.get_current_loc())
            if (loc?.includes('dashboard')) {
                const dashboard = this?.nav?.routes[0]
                if (dashboard && dashboard?.routes && !this.utils.is_empty_object(dashboard?.routes)) {
                    const db = dashboard?.routes[0]
                    const url = { loc: db.loc, type: db.type, document: db.document, module: db.module }
                    this.utils.update_url_parameters(url)
                    this.init_page_url_changed()
                }

            }
        }
        this.update_ui()
    }

    update_ui() {
        const current = this.session.get_type_session()
        this.hide_content(this.content_group)
        switch (current.type) {
            case 'list':
                this.show_content(this.list_view_content)
                // this.show_content (this.new_create_btn)
                break;
            case 'info':
                this.show_content(this.info_view_content)
                break;
            case 'new':
                this.show_content(this.new_form_view_content)
                break;
            case 'dashboard':
                this.show_content(this.dashboard_view_content)
                break;
            case 'report':
                this.show_content(this.report_view_content)
                this.utils.import_report_controller().then(resolve=>{
                    if(resolve){
                        try{
                            new resolve({
                                page_controller: this,
                                session: this.session,
                                utils: this.utils,
                                connect: this.connect,
                                alerts: this.alerts,
                                lite_date_picker:this.lite_date_picker
                            })
                        }
                        catch(error){
                            console.error(`Failed to initialize report:${error}`)
                        }
                    }
                })
                break;
            default:
                break;
        }
        this.update_breadcrumb()
        this.update_title_content()
        this.update_content_type_action()
        this.handle_multi_content_structures()
        if (current.type === 'info' || current.type === 'new') {
            this.form_controller = new Form_Controller({
                page_controller: this,
                session: this.session,
                utils: this.utils,
                connect: this.connect,
                alerts: this.alerts,
                lite_date_picker:this.lite_date_picker
            })
            this.form_controller?.init_form()
        }
        else if (current.type === 'list') {
            if(!lite.session.get_session("listview_status")){
                this.listview_controller?.init_listview()
                lite.session.set_session("listview_status", "loaded")
            }
        }
        // handle page type change event
        if(lite.utils.array_has_data(this.on_page_type_change_actions)){
            $.each(this.on_page_type_change_actions,(_,ev)=>{
                if(ev.fun){
                    ev.fun(lite.utils.get_url_parameters(), ev.cls)
                }
            })
        }
    }

    handle_multi_content_structures() {
        if (this.multi_content_group?.length) {
            const document = this.session.get_type_session()?.document?.toLowerCase()?.trim()
            this.hide_content(this.multi_content_group)
            const to_show = this.utils.get_elements_by_attribute(this.multi_content_group, 'for', document)
            this.show_content(to_show)
        }
    }



    // initialize page title content
    update_title_content() {
        const current = this.session.get_type_session()
        this.hide_content(this.doc_status_wrapper)
        switch (current.type) {
            case 'list':
                this.hide_content(this.module_name_title)
                this.hide_content(this.app_name_title)
                this.hide_content(this.doc_name_title)
                this.content_type_title.text(this.utils.capitalize(current.document || current.loc))
                break;
            case 'report':
                this.hide_content(this.module_name_title)
                this.hide_content(this.app_name_title)
                this.hide_content(this.doc_name_title)
                this.content_type_title.text(this.utils.capitalize(current.document || current.loc))
                break;
            case 'info':
                this.hide_content(this.module_name_title)
                this.show_content(this.content_type_title)
                this.content_type_title.html(this.utils.capitalize(current.document))
                break;
            case 'new':
                this.hide_content(this.module_name_title)
                this.show_content(this.content_type_title)
                // this.show_content(this.doc_name_title)
                this.content_type_title.html(this.utils.capitalize(current.document))
                // this.doc_name_title.html(`${this.nav.create_chevron()} New ${this.utils.capitalize(page.content_type || page.app)}`)
                // 
                break;
            case 'dashboard':
                this.show_content(this.content_type_title)
                this.content_type_title.html(current.document)
                break;
            default:
                break;
        }
    }

    update_doc_title_content() {
        const doc =  this.form_controller?.doc_data,
            status_info =doc?.status_info
        if(doc){
            // this.show_content(this.doc_name_title)
            this.show_content(this.doc_status_wrapper)
            // this.doc_name_title.html(`${this.nav.create_chevron()} ${doc?.name || ''}`)
            this.doc_status_wrapper.css({backgroundColor:status_info?.status_color,border:`1px ${status_info?.status_color} solid`})
            this.doc_status_pill.css({backgroundColor:status_info?.inner_color})
            this.doc_status_text.text(status_info?.name).css({color:status_info?.inner_color,fontWeight:700})
        }
    }

    update_content_type_action() {
        const document = this.utils.capitalize(this.session.get_type_session().document)
        if (document && document !== 0) {
            this.content_type_action_select.siblings('.plugin-dropdown_input.content-type-action').find('.item').text(document).attr('data-value', document)
        }
    }

    is_multi_content_page() {
        return $('input[action-type="multi-content-toggler"]')?.length > 0
    }


    // for multi-content pages
    init_page_content_type_change_listener(data, cls) {
        const action_type = lite.utils.has_key(data, 'action-type') ? data['action-type'] : null
        if (action_type && action_type === 'multi-content-toggler') {
            if (data.value && lite.utils.lower_case(data.value) !== lite.utils.lower_case(lite.utils.get_url_parameters("document"))) {
                lite.utils.update_url_parameters({ document: data.value })
                cls.init_page_url_changed()
            }
        }
    }
    on_content_type_change(fun, cls) {
        
        if (fun) {
            this.content_type_action_select?.change((e) => fun(e?.target?.value || null, cls))
        }
        else {
            console.error("ON CONTENT TYPE CHANGE ERROR:: Content type change function undefined.")
        }
    }
    // the dropdown menu toggler
    init_page_menu_toggler() {
        const cls = this
        this.dropdown_toggler.click(function (e) {
            cls.active_toggler = $(this)
        })
        this.dropdown_item.click(function (e) {
            e.preventDefault();
            $(this).parents('div').removeClass('show')
            cls.active_toggler.attr('aria-expanded', false)
        })
    }

    // initialize page actions
    init_page_actions() {
        const cls = this
        // on new creation.
        this.new_action_btn.click(function (e) {
            e.preventDefault()
            cls.utils.update_url_parameters({ type: "new" })
            // cls.utils.remove_url_parameters(["doc"])
            cls.init_page_url_changed()
        })

        // on new creation.
        this.info_view_action_btn.click(function (e) {
            e.preventDefault()
            cls.utils.update_url_parameters({ type: "info" })
            cls.init_page_url_changed()
        })
    }


    // manage page table actions
    init_page_tables_manager() {
        const cls = this
        this.info_view_link.click(function (e) {
            e.preventDefault()
            const doc = cls.utils.get_attribute(this, 'data-id')
            if (doc) {
                cls.utils.update_url_parameters({
                    type: 'info',
                    doc: doc
                })
                cls.init_page_url_changed()
            }
        })
    }

    // handle on select change
    on_select_chage(fun, cls) {
        if (this.utils.is_function(fun)) {
            this.on_select = fun
            this.lite_selector.init_selectors(this.on_select, cls)
        }
    }

    handle_select_change_event(data, cls) {
        // console.warn("Default Select change listener Uninitialized......")
    }


    // to open a document
    open_document(data) {
        // console.log("document opened!!!")
    }
    
}

export default Page_Controller
