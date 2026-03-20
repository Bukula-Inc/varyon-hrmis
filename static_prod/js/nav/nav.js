import Utils from '../utils/utils.js'
import Searcher from './searcher.js'
import { color_codes } from '../constants/colors.js'
class Nav_Manager {
    // initialize navigation
    constructor() {
        this.color_codes = color_codes
        this.nav_btn = $('.nav-btn')
        this.nav_menu_dropdown = $('#nav-menu-dropdown')
        this.nav_menu_dropdown_close_btn = $('#nav-menu-dropdown-close-btn')
        this.nav_menu_content = $('#nav-menu-content')
        this.$module_content_wrapper = $('.module-menu')
        this.$module_menu_content_wrapper = $('.module-content-menu')
        this.$swap_menu_btn = $('.swap-module-menu')
        this.$module_menu = $('.module-menu-content')
        this.$nav_actions_wrapper = $(".nav-dropdown-actions-wrapper")
        this.current_module = ''
        this.utils = new Utils()
        this.routes = []
        this.init_nav_menu()
        this.init_nav_actions()
        new Searcher({ utils:this.utils, nav: this })
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
            $(cls.nav_btn).on('click', function (e) {
                cls.toggle_nav_menu_dropdown()
            })
            $(cls.nav_menu_dropdown_close_btn).on('click', function (e) {
                cls.toggle_nav_menu_dropdown()
            })
        }
        
    }

    // populate navigation menus  
    async populate_nav_menu() {
        const cls = this
        let html = ''
        cls.clear_nav_menu_content()
        const allowed_content = await this.utils.delay_until(()=>{
            if(lite.allowed_content){
                return lite.allowed_content
            }
        }, 50000)
        const module_menus = lite?.allowed_content[lite?.utils?.get_current_module()]
        if(!lite.utils.is_empty_object(module_menus)){
            cls.utils.object_has_data(module_menus.menu_cards) && lite.utils.ascend(lite.utils.get_object_values(module_menus.menu_cards), "idx").map(card => {
                if (!card?.name?.toLowerCase()?.includes('dashboard') && card.idx) {
                    html += cls.open_close_nav_menu_card(true, card.name)
                    const sorted = lite.utils.ascend(card.card_items,"idx")
                    !cls.utils.is_empty_array(sorted) && sorted.map(card_item => {
                        html += cls.add_nav_menu_url_component(card_item)
                    })
                    html += cls.open_close_nav_menu_card()
                }
            })
            this.add_nav_menu_content(html)
        }

        // handle sub-link togglers   
        $('.sub-link-toggler').change(function (e) {
            $(this).siblings('.sub-nav-toggler').toggleClass('expanded')
            $(this).parents('.navigation-wrapper').find('.sub-links').toggleClass('hidden expanded')
        })
        // handle click on the url
        $('.navigation-link').on('click', function (e) {
            e.preventDefault()
            $('#loader-overlay').removeClass('hidden')
            window.location.href = $(this).attr('href')
        })
    }



    // open and close the navigation menu card
    open_close_nav_menu_card(is_open = false, title = '') {
        return is_open ?
            `<div class="w-full nav-card-wrapper bg-default/5 text-white rounded-md"> 
                <div class="text-white mb-2 bg-default font-semibold text-18 w-full flex items-center justify-between cursor-pointer p-2 rounded-t-md">
                    ${title}
                <span class="material-symbols-outlined text-[16px] text-black mr-2"> expand_more </span>
            </div> 
            <div class="w-full mt-3 text-13 h-full">` :
            `</div> </div>`
    }

    add_nav_menu_url_component(item = {}) {
        let url = this.create_url(item.app, item.module, item.app, item.page_type, item.content_type)
        const child_items = this.create_child_routes(item)
        const id = this.utils.unique()
        const color = this.generate_color()
        return `
            <div class="navigation-wrapper w-full mb-1 flex items-center justify-start flex-col">
                <div class="w-[98%] mb-1 ml-1 flex items-center justify-between">
                    <a href="/app${url?.trim()}" class="navigation-link text-default text-13 w-full flex items-center justify-start transition duration-100 hover:translate-x-[-5px] h-[30px] hover:text-default">
                        ${item.icon ? `<span class="material-symbols-outlined text-[${color.inner}] mr-1 text-20 bg-[${color.base}] p-1 rounded-full">${item.icon}</span>` : ''}
                        ${item.title}
                    </a>
                    <input type="checkbox" id="${id}" class="sub-link-toggler hidden"/>
                    <label for="${id}" class="sub-nav-toggler border-none px-3 cursor-pointer">${child_items ? this.create_chevron('bottom') : ''}</button>
                </div>
                <div class="sub-links hidden w-[97%] bg-gray-100 p-1 rounded-md ${!child_items ? 'hidden' : `text-[${color.inner}]`}">
                    ${child_items}
                </div>
            </div>
        `
    }

    create_child_routes(item) {
        let child_routes = ''
        if (!this.utils.is_empty_array(item?.child_items||[])) {
            item?.child_items?.map(child => {
                const url = this.create_url(child.app, child.module, child.app, child.page_type, child.content_type)
                const color = this.generate_color()
                child_routes += `
                    <a href="/app${url?.trim()}" class="navigation-link text-default text-13 w-full ml-3 flex items-center justify-start mb-1 transition duration-100 hover:translate-x-[-5px] h-[30px] hover:text-default">
                        ${child.icon ? `<span class="material-symbols-outlined text-[${color.inner}] mr-1 text-20 bg-[${color.base}] p-1 rounded-full">${child.icon}</span>` : ''}
                        ${child.title}
                    </a>
                `
            })
        }
        return child_routes
    }



    // toggle navigation menu dropdown
    toggle_nav_menu_dropdown() {
        $(this.nav_btn).toggleClass('expanded')
        $(this.nav_menu_dropdown).toggleClass('expanded')
        if($(this.nav_btn).hasClass("expanded")){
            $("body").addClass("overflow-hidden")
        }
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

    goto_help(){
        lite.alerts.toast({
            toast_type:lite.status_codes.unprocessable_entity,
            title:"Coming Soon",
            message:"Component not ready yet!"
        })
    }
}

export default Nav_Manager