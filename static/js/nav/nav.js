import Utils from '../utils/utils.js'
import Searcher from './searcher.js'
import { color_codes } from '../constants/colors.js'
import NavigationController from './nav_controller.js'
class Nav_Manager {
    // initialize navigation
    constructor() {
        this.color_codes = color_codes
        this.models = []
        this.apps = {}
        this.reports = {}
        this.nav_btn = $('.nav-btn')
        this.nav_menu_dropdown = $('#nav-menu-dropdown')
        this.nav_menu_dropdown_close_btn = $('#nav-menu-dropdown-close-btn')
        this.nav_menu_content = $('#nav-menu-content')
        this.$module_content_wrapper = $('.module-menu')
        this.$module_menu_content_wrapper = $('.module-content-menu')
        this.$swap_menu_btn = $('.swap-module-menu')
        this.$module_menu = $('.module-menu-content')
        this.$nav_actions_wrapper = $(".nav-dropdown-actions-wrapper")
        this.$spotlight = $ ('div[spotlight]')
        this.current_module = ''
        this.utils = new Utils()
        this.routes = []
        this.init_nav_menu()
        this.init_nav_actions()
        new Searcher({ utils:this.utils, nav: this })
        this.navController = new NavigationController ()
    }

    generate_color(){
        return this.color_codes[Math.floor(Math.random() * this.color_codes.length)]
    }

    // get the current module for the system
    get_current_module() {
        const url = window.location.pathname
        if (url) {
            this.current_module = url?.split('/')[1]?.toLowerCase()
        }
    }
    // remove all navigation content from the nav menu
    clear_nav_menu_content() {
        $(this.nav_menu_content).empty()
    }
    // add content to the nav menu
    add_nav_menu_content(html) {
        $(this.nav_menu_content).html(html)
    }
    // initialize navigation menu
    async init_nav_menu() {
        const cls = this
        const current_module = this.utils.get_current_module()
        if(current_module){
            this.get_current_module()
            this.populate_nav_menu()
        }
        
    }

    // populate navigation menus
    async load_module(lst) {
    
        const icons = {
            hr: "diversity_3",
            payroll: "credit_card",
            staff: "person",
            core: "blur_circular"
        }

        let $mdl = $('#mdl-lst')
        $mdl.empty ()

        lst.forEach(mdl => {
            const icon = icons[mdl] ?? 'apps'
            const id = this.utils.unique()
            $mdl.append(`
                <a href="/app/${mdl}" id="${id}" link href="${mdl}" class="h-[80px] w-[30%] text-blue-600 rounded-xl bg-white p-3
                    hover:bg-blue-600 hover:text-white transition-all
                    ease-in-out cursor-pointer duration-500">
                    <div class="h-full w-full flex flex-col justify-center items-center">
                        <span class="material-icons-outlined text-[40px] leading-none block">
                            ${icon}
                        </span>
                        <p class="font-extrabold truncate capitalize text-sm">
                            ${mdl}
                        </p>
                    </div>
                </a>
            `)
        })
        
    }

    async populate_nav_menu() {
        const cls = this
        let html = ''
        cls.clear_nav_menu_content()
        const allowed_content = await this.utils.delay_until(()=>{
            if(lite.allowed_content){
                return lite.allowed_content
            }
        }, 50000)
        
        cls.load_module (lite.utils.get_object_keys (allowed_content))
        const module_menus = lite?.allowed_content[lite?.utils?.get_current_module()]
        if(!lite.utils.is_empty_object(module_menus)){
            cls.load_anchors (module_menus)
        }
    }

    add_spotlight_url_component (item) {
        let links = ''
        if (lite.utils.array_has_data (item)) {
            item.forEach ((itm, idx) => {
                let url = this.create_url (itm.app, itm.module, itm.app, itm.page_type, itm.content_type)
                const id = this.utils.unique ()
                const color = this.generate_color ()
                
                links += `
                    <a id="${id}" href="/app${url?.trim()}"
                        class="
                            w-full flex items-center justify-between
                            bg-slate-50
                            rounded-lg p-4 hover:shadow
                            transition-all duration-150
                            focus:outline-none focus:ring-2 focus:ring-default
                            "
                        >
                        <div class="flex items-center gap-4">
                            <span class="material-symbols-outlined text-4xl text-[${color.inner}]">
                                ${itm.icon || 'apps'}
                            </span>

                            <div class="text-left">
                                <div class="text-sm font-semibold text-[${color.inner}]">${itm.title}</div>
                                <div class="text-xs text-slate-300 truncate max-w-[200px]">
                                    ${ itm?.content_type || ''}
                                </div>
                            </div>
                        </div>

                        <span class="material-symbols-outlined text-white">
                            arrow_forward_ios
                        </span>
                    </a>
                `
            })
        }

        return links
     }

    async load_anchors (mdl_links) {
        const $mdl_menu_cards_wrapper = $ ("#menu-cards-links")
        $ ("[module-dashboard]").on ('click', (e) => {
            const dashboard = $ (e.target)
            location.replace (`/app/${mdl_links?.module || 'core'}`)
        })

        $mdl_menu_cards_wrapper.empty ()
        this.$spotlight.empty ()
        let $mdl_cards = ''
        let mdl_for_spotlight = ''
        
        const mdl_cards = mdl_links?.menu_cards || []

        if (lite.utils.object_has_data (mdl_cards)) {
            this.getSortedHrList (mdl_cards).forEach ((card, idx) => {
                if (idx > 0) {
                    const sub_links = this.add_nav_menu_url_component (card?.card_items || [])
                    const add_spotlight = this.add_spotlight_url_component (card?.card_items || [])
                    const color = this.generate_color ()
                    $mdl_cards += `
                        <div class="nav-group w-full transition-all text-[${color.inner}] bg-[${color.base}]">
                            <button
                                class="nav-toggle w-full flex items-center justify-between p-2 transition-all"
                                data-accordion-toggle
                            >
                                <div class="flex items-center gap-3 w-[90%]">
                                    <span class="material-icons-outlined p-1 rounded-md">${card?.icon || 'folder'}</span>
                                    <span class="label">${card?.name}</span>
                                </div>

                                <span class="material-icons-outlined chevron transition-transform duration-300">
                                    expand_more
                                </span>
                            </button>

                            <div class="nav-sub hidden space-y-1 pl-4 mt-1">
                                ${sub_links}
                            </div>
                        </div>

                    `
                    mdl_for_spotlight += `
                        <div class="col-span-1 flex flex-col gap-y-2 bg-white rounded-md p-2">
                            <div class="h-[65px] w-full text-[${color.inner}] bg-[${color.base}] rounded-lg font-extrabold text-xl py-1 capitalize flex gap-3 items-center px-5 text-white">
                                <span class="material-symbols-outlined text-4xl">
                                    ${card?.icon || 'folder'}
                                </span>
                                <div class="flex flex-col">
                                    <p> ${card?.name || ''} </p>
                                    <p class="text-[11px] font-light">Explore</p>
                                </div>
                            </div>
                            ${add_spotlight}
                        </div>
                    `
                }
            })
            this.$spotlight.html (mdl_for_spotlight)
            this.get_spotlight ()
        }

        $mdl_menu_cards_wrapper.html ($mdl_cards)

        this.set_active_nav()
        this.bind_nav_events()
    }
    set_active_nav() {
        const currentUrl = window.location.pathname + window.location.search

        $(".nav-group").removeClass("bg-default/10 rounded-md")
        $(".nav-toggle").removeClass("font-semibold text-default")
        $(".nav-sub").addClass("hidden")
        $(".chevron").removeClass("rotate-180")
        $(".sub-link").removeClass(
            "font-semibold text-default translate-x-[-5px]"
        )

        $(".sub-link").each(function () {
            const href = $(this).attr("href")
            if (!href) return

            if (currentUrl.includes(href)) {
                $(this).addClass(
                    "font-semibold text-default translate-x-[-5px]"
                )

                const $group = $(this).closest(".nav-group")

                $group.addClass("bg-default/10 rounded-md")
                $group.find(".nav-toggle")
                    .addClass("font-semibold text-default")

                $group.find(".nav-sub")
                    .removeClass("hidden")

                $group.find(".chevron")
                    .addClass("rotate-180")
            }
        })
    }

    bind_nav_events() {
        const cls = this

        $(document).off("click", ".sub-link").on("click", ".sub-link", function () {
            cls.reset_nav_state()

            $(this).addClass(
                "font-semibold text-default translate-x-[-5px]"
            )

            const $group = $(this).closest(".nav-group")

            $group.addClass("bg-default/10 rounded-md")
            $group.find(".nav-toggle")
                .addClass("font-semibold text-default")

            $group.find(".nav-sub")
                .removeClass("hidden")

            $group.find(".chevron")
                .addClass("rotate-180")
        })

        $(document).off("click", "[data-accordion-toggle]")
            .on("click", "[data-accordion-toggle]", function () {
                const $group = $(this).closest(".nav-group")

                $(".nav-group").not($group).each(function () {
                    $(this)
                        .removeClass("bg-default/10 rounded-md")
                        .find(".nav-sub").addClass("hidden")
                        .end().find(".chevron").removeClass("rotate-180")
                        .end().find(".nav-toggle")
                        .removeClass("font-semibold text-default")
                })

                $group.toggleClass("bg-default/10 rounded-md")
                $group.find(".nav-sub").toggleClass("hidden")
                $group.find(".chevron").toggleClass("rotate-180")
                $group.find(".nav-toggle")
                    .toggleClass("font-semibold text-default")
            })
        this.navController.bind ()
    }

    reset_nav_state() {
        $(".nav-group").removeClass("bg-default/10 rounded-md")
        $(".nav-toggle").removeClass("font-semibold text-default")
        $(".nav-sub").addClass("hidden")
        $(".chevron").removeClass("rotate-180")
        $(".sub-link").removeClass(
            "font-semibold text-default translate-x-[-5px]"
        )
    }

    getSortedHrList (data) {
        return Object.values(data)
            .sort((a, b) => a.id - b.id)
            .map(section => ({
                ...section,
                card_items: Array.isArray(section.card_items)
                    ? [...section.card_items].sort((a, b) => a.id - b.id)
                    : []
            })
        )
    }

    add_nav_menu_url_component(item = []) {
        let links = ''
        if (lite.utils.array_has_data (item)) {
            item.forEach ((itm, idx) => {
                let url = this.create_url (itm.app, itm.module, itm.app, itm.page_type, itm.content_type)
                const id = this.utils.unique ()
                const color = this.generate_color ()

                links += `
                    <a id="${id}" href="/app${url?.trim()}"
                        class="sub-link block text-13 transition duration-100 hover:translate-x-[-5px]">
                        ${itm.title}
                    </a>
                `
            })
        }

        return links
    }

    update_nav_menus(settings){
        this.$module_menu.empty()
        if(settings?.allowed_content){
            const modules = settings.allowed_content
            const current_module = this.utils.get_current_module()
            const sorted = lite.utils.get_object_values(modules).sort((a, b) =>  a.id - b.id)

            $.each(sorted, (_, m) => {
                const color = this.generate_color()
                if(!m.is_default){
                    this.$module_menu.append(`
                        <a href="${ m?.url?.trim()}" class="flex h-[50px] ${m.module === current_module ? "bg-default text-theme_text_color font-bold text-22" : ""} items-center justify-start pl-2 rounded-md transition duration-1000 hover:translate-x-[3%] hover:bg-default/30">
                            <span class="material-symbols-outlined mr-2 text-13 text-[${this.color_codes[_]?.inner}] ${m.module === current_module ? "text-22" : "text-22"} ">${m?.icon}</span>
                            <span class="mobile-hidden truncate overflow-ellipsis">${m?.title}</span>
                            <span class="mobile-show hidden"> ${m?.title.substring(0,3)} </span>
                        </a>
                    `)
                }
            })
        }
    }
    
    create_url(url, module, app, page, content_type, doc) {
        return url ? `/${module}/${url}?app=${app}&page=${page}&content_type=${content_type} ${doc ? "&doc=" + doc : ''}` : ''
    }

    // create breadcrumb
    create_breadcrumb(title = String, url = String, add_slash = Boolean) {
        if(title?.toLowerCase().includes("crm") || title?.toLowerCase().includes("hr")){
            title = title?.toUpperCase()
        }
        return `
            <li class="breadcrumb-item active font-semibold flex items-center justify-start" aria-current="page">
                <div href="${url?.trim()}" >${this.utils.capitalize(this.utils.replace_chars(title, '_', ' '))}</div>
            </li>
        `
    }

    // add chevron to navigation
    create_chevron(direction = 'right', size = 18) {
        return direction !== 'bottom' ?
            ` <span class="material-symbols-outlined text-gray-600 text-[${size}px]"> chevron_${direction} </span>` :
            `<span class="material-symbols-outlined text-gray-600 text-[${size}px]"> expand_more </span>`
    }

    create_new_url({mod="", model="", page_type="list", content_type="", url_params=""}) {
        if(!mod){
            return false
        }
        const flat_mapped = routes[mod]?.flatMap(item => item);
        if(!this.utils.is_empty_array(flat_mapped)){
            $.each(flat_mapped,(_,n)=>{
                console.log(n.routes)
            })
        }
    }   
    
    init_nav_actions(){
        const actions = {
            profile: this.goto_profile,
            help: this.goto_help,
            change_password: this.change_password,
            switch_company: this.switch_company,
            logout: this.logout,
        }
        this.$nav_actions_wrapper?.find(".dropdown-item")?.off("click")?.click(e=>{
            const action = lite.utils.get_attribute(e.currentTarget, "action")
            if(actions[action]){
                actions[action]()
            }
        })
    }

    goto_profile(){
        window.location.href = "/app/staff/staff_dashboard?app=staff_dashboard&module=staff&page=dashboard&content_type=Dashboard"
    }

    logout(){
        lite.session.clear_cookies_for_domain()
        window.location.replace("/auth/login")
    }

    async change_password(){
        const quick_modal = await lite.modals.quick_form("core","change password",async (values,setup)=>{
            if(values?.new_password == values.rpt_password){
                const loader_id = lite.alerts.loading_toast({
                    title: "Updating", 
                    message:`Please wait while we update your password.`
                })
                // lite.modals.close_modal(quick_modal.modal_id)
                const save = await lite.connect.x_post("update_user_password", values)
                lite.alerts.destroy_toast(loader_id)
                if(save.status === lite.status_codes.ok){
                    lite.alerts.toast({
                        toast_type:lite.status_codes.ok,
                        title:"Updated Successfully",
                        message:"Your new password has been set successfully! \n Logging out now..."
                    })
                   setTimeout(() => {
                        lite.session.clear_cookies_for_domain()
                        window.location.replace("/auth/login")
                   }, 3000);
                }
            }
            else{
                lite.alerts.toast({
                    toast_type:lite.status_codes.unprocessable_entity,
                    title:"New Passwords Mismatch",
                    message:"New passwords do not match! Please ensure to provide the same password in both new password fields!"
                })
            }
        })
    }

    async switch_company(){
        const quick_modal = await lite.modals.quick_form("core", "switch company",{text:"Switch", fun: async (values,setup)=>{
            const loader_id = lite.alerts.loading_toast({
                title: "Switching", 
                message:`Please wait while we switch the company.`
            })
            const {status, data, error_message} = await lite.connect.core("switch_company", values)
            lite.alerts.destroy_toast(loader_id)
            if(status === lite.status_codes.ok){
                lite.modals.close_modal(quick_modal.modal_id)
                lite.session.clear_cookies_for_domain()
                lite.connect.set_user_cookie(data.token)
                lite.alerts.toast({
                    toast_type:lite.status_codes.ok,
                    title:"Process Concluded",
                    message:"Company Switched Successfully! \n Refreshing the page now"
                })
                setTimeout(() => { location.replace(data.url) }, 1000);
            }
        }})
    }

    get_spotlight () {
        this.models = lite.utils.get_object_keys (lite?.allowed_content)
        console.log(this.get_current_module (),'====================================');
        // console.log(this.getSortedHrList (lite?.allowed_content[this.get_current_module ()]));
        console.log('====================================');
    }

    goto_help(){
        lite.alerts.toast({
            toast_type:lite.status_codes.unprocessable_entity,
            title:"Coming Soon",
            message:"Component not ready yet!"
        })
    }
}

export default Nav_Manager