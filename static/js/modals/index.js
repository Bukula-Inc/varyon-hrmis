import Modal_HTML_Generator from "../page/html/modal_html_generator.js";
import Form_Controller from "../page/form_controller/index.js";
export default class Modals{
    constructor(){
        this.generator = new Modal_HTML_Generator()
        this.controller = new Form_Controller()
    }


    close_modal(modal_id){ $(`#${modal_id}`)?.remove() }


    init_close_action(modal_id){
        $(`#${modal_id}`)?.find(".close-modal").off("click").click(e=>{
            e.preventDefault()
            this.close_modal(modal_id)
        })
    }

    get_modal_data(modal_id){
        let values = {}
        $.each($(`#${modal_id}`)?.find(".content-wrapper")?.find(".lite-field"),(_, field)=>{
            if($(field)?.attr("type") == "checkbox"){
                values[$(field)?.attr("fieldname")] = $(field)?.prop("checked") ? 1 : 0
            }
            else{
                values[$(field)?.attr("fieldname")] = $(field)?.val() || $(field)?.attr("value")
            }
        })
        return values
    }


    async init_form_action_btns(on_confirm, on_cancel, modal_id, data){
        let values = {}
        $(`#${modal_id}`)?.find(".modal-action-btn")?.off("click")?.click(async e=>{
            e.preventDefault()
            if(!data){
                values = this.get_modal_data(modal_id)
                if(values){
                    data = values
                }
            }
            const action = lite.utils.get_attribute(e.currentTarget, "action")
            if(action === "cancel"){
                if(typeof on_cancel?.fun === "function"){
                    await on_cancel?.fun(data)
                }
                this.close_modal(modal_id)
            }
            else{
                if(typeof on_confirm?.fun === "function"){
                    await on_confirm?.fun(data)
                    this.close_modal(modal_id)
                }
            }
        })
    }

    async quick_form(module_name, content_type, on_save={text:"Confirm", icon:"task_alt", fun: null}, on_cancel={text:"Cancel", icon:"close", fun:null}, default_data=null, before_save=null, after_save=null){
        try{
            const form = await import(`../forms/${module_name}/${lite.utils.replace_chars(lite.utils.lower_case(content_type)," ","_")}.js`)
            let config = form?.default
            config.setup.is_quick_form = true
            const modal_id = await this.generator.quick_form(config,null, 2, false, on_save, on_cancel)
            const controller = new Form_Controller(config)
            controller.init_form(config, true, on_save, modal_id,default_data)
            this.init_close_action(modal_id)
            $(`#${modal_id}`).find(".modal-action-btn")?.off("click")?.click(e=>{
                const action = lite.utils.get_attribute(e.currentTarget, "action")
                if(action === "cancel"){
                    this.close_modal(modal_id)
                }
                else{
                    let values = {}
                }
            })
            return { modal:$(`#${modal_id}`), modal_id: modal_id }
        }
        
        catch(e){
            console.log(e)
            lite.alerts.toast({
                toast_type:lite.status_codes.internal_server_error,
                title: "Importation Failed",
                message: `Failed to import form setup for ${lite.utils.capitalize(content_type)}`
            })
        }
    }


    confirm(title, message, on_confirm={text:"Confirm", icon:"task_alt", fun: null}, on_cancel={text:"Cancel",icon:"close", fun:null}){
        const modal_id = this.generator.confirm_modal(title,message,on_confirm, on_cancel)
        this.init_close_action(modal_id)
        this.init_form_action_btns(on_confirm, on_cancel, modal_id)
        return { modal:$(`#${modal_id}`), modal_id: modal_id }
    }


    custom_modal(title, html_content, on_confirm={text:"Confirm", icon:"task_alt", fun: null}, on_cancel={text:"Cancel",icon:"close", fun:null}){
        const modal_id = this.generator.custom_modal(title, html_content, on_confirm, on_cancel)
        this.init_close_action(modal_id)
        this.init_form_action_btns(on_confirm, on_cancel, modal_id)
        return { modal:$(`#${modal_id}`), modal_id: modal_id }
    }


    feedback(title, message, on_confirm={text:"Submit", icon:"task_alt", fun: null}, on_cancel={text:"Cancel",icon:"close", fun:null}){
        const modal_id = this.generator.feedback_modal(title,message,on_confirm, on_cancel)
        const modal = $(`#${modal_id}`)
        let data = {
            stars: 0,
            message: ""
        }
        modal.find(".modal-rate-btn").mouseover(e=>{
            const index = lite.utils.get_attribute(e.currentTarget, "index")
            $(`.modal-rate-btn`).addClass("border text-gray-400 border-gray-300 bg-gray-50").removeClass("text-white border-none bg-default")
            for (let i = index; i >= 1; i--){
                $(`.modal-rate-btn[index="${i}"]`).removeClass("border text-gray-400 border-gray-300 bg-gray-50").addClass("text-white border-none bg-default")
            }
            data.stars = index
        })

        modal.find("#feedback-message")?.off("keyup")?.keyup(e=>{
            data.message = lite.utils.get_field_value(e.currentTarget)
        })

        this.init_close_action(modal_id)
        this.init_form_action_btns(on_confirm, on_cancel, modal_id, data)
        return { modal:$(`#${modal_id}`), modal_id: modal_id }
    }
}