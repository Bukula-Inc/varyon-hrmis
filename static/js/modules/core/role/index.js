
import Core_HTML_Generator from '../../../page/html/core_html_generator.js'

export default class Role{
    constructor(){
        this.card_items = {}
        this.generator = new Core_HTML_Generator()
        this.$permission_list_wrapper = $(".role-module-permission-list")
        lite.page_controller.on_page_type_change(this.on_page_type_change, this)
        
    }

    async on_page_type_change(data,cls){
        if(data.type === 'new'){
            cls.init_permissions(null)
        }
        if(data.type === "info"){
            this.form_data = null
            const data = await lite.utils.delay_until(()=>{
                if(lite.utils.object_has_data(lite.form_data)){
                    return lite.form_data
                }
            },20000)
            cls.init_permissions(data)
        }
    }

    async get_available_menu_cards(doc){
        if(doc && lite.utils.object_has_data(doc)){
            this.available_cards = []
            this.default_dashboards = {}
            $.each(doc.role_module, (_,md)=>{
                this.default_dashboards[md.role_module] = {dashboard:md.default_dashboard, permit_all: md.permit_all}
                const values = lite.utils.get_object_values(md.role_cards)
                $.each(values,(__, card_content)=>{
                    const flat_list = lite.utils.get_object_values(card_content).flat()
                    this.available_cards.push(...flat_list)
                })
            })
        }
    }

    async init_permissions(doc){
        const {status, data, error_message} = await lite.connect.x_fetch("get_role_cards")
        this.$permission_list_wrapper?.empty()
        if(status == lite.status_codes.ok){
            const menu_cards = data?.menu_cards, card_items = data.card_items
            lite.card_items = card_items
            await this.get_available_menu_cards(doc)
            $.each(lite.utils.sort(lite.utils.get_object_keys(menu_cards)),(_,key)=>{
                const obj = menu_cards[key]
                const module_cards_wrapper = this.generator.create_module_permission_wrapper(obj, this.default_dashboards, this.available_cards || [])
                this.$permission_list_wrapper?.append(module_cards_wrapper)
            })
            lite.lite_selector.init_selectors(this.handle_select_change, this)
            lite.lite_switch.init_switch_fields(this.handle_permission_change,this)
        }
    }

    handle_permission_change(data, cls){
        if(data){
            const allow_all = $(data.field).parents(".content-group.active .module-permission-card-wrapper")?.find(".lite-field.allow-all[type='switch']")
            if($(data?.field).hasClass("allow-all")){
                const v = data.value
                const actions = $(data.field).parents(".content-group.active .module-permission-card-wrapper")?.find(".lite-field[type='switch']:not(.allow-all)")
                if(lite.utils.array_has_data(actions)){
                    $.each(actions,(_,act)=>{
                        lite.lite_switch.set_switch_value(act, v)
                    })
                }
            }

            if($(data?.field).hasClass("select-all")){
                const v = data.value
                const document = lite.utils.get_attribute(data?.field, "id")
                const actions = $(data.field).parents(".content-group.active .module-permission-card-wrapper")?.find(`.permission-card[app="${document}"]`).find(".lite-field[type='switch']:not(.allow-all)")
                if(lite.utils.array_has_data(actions)){
                    $.each(actions,(_,act)=>{
                        lite.lite_switch.set_switch_value(act, v)
                    })
                }
                if(v == 0){
                    lite.lite_switch.set_switch_value(allow_all, v)
                }
            }
        }
    }
}

export const before_role_save_ = (params)=>{
    const { controller } = params
    const allowed_modules = $(".content-group.active .module-permission-card-wrapper")
    let ext_data = {}
    if(lite.utils.array_has_data(allowed_modules)){
        $.each(allowed_modules,(_,md)=>{
            const module_name = lite.utils.get_attribute(md, "module")
            const default_dashboard = lite.lite_selector.get_select_value($(md).find(".lite-selector.lite-field"))
            const card_items = $(md).find(".lite-field[type='switch'][value='1']")
            if(lite.utils.array_has_data(card_items)){
                if(!default_dashboard){
                    lite.alerts.toast({
                        toast_type:lite.status_codes.not_found,
                        title:`Dashboard required!`,
                        message:`Please select the default dashboard for ${lite.utils.capitalize(lite.utils.replace_chars(module_name,"_ "," "))}!`
                    })
                    throw new Error("")
                }
                else{
                    ext_data[module_name] = {default_dashboard: default_dashboard, cards:{}}
                    $.each(card_items,(idx,item)=>{
                        if(!$(item).hasClass("allow-all")){
                            const id = lite.utils.string_to_int($(item).attr("id")), card = lite.card_items[id]?.parent
                            if(!ext_data[module_name].cards[card]){
                                ext_data[module_name].cards[card] = [id]
                            }
                            else{
                                ext_data[module_name].cards[card].push(id)
                            }
                        }
                    })
                }
            }
        })
        if(lite.utils.is_empty_array(ext_data)){
            lite.alerts.toast({
                toast_type:lite.status_codes.not_found,
                title:"Please Select at least one role or permission before saving",
                message:`Please select the default dashboard for ${lite.utils.capitalize(lite.utils.replace_chars(module_name,"_ "," "))}!`
            })
            throw new Error("")
        }        
        params.values.role_content = ext_data
    }
    return true
}
