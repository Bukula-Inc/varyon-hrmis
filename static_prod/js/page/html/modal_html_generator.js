
import HTML_Builder from "./html_builder.js";
export default class Modal_HTML_Generator{
    constructor(){
        this.html_generator = new HTML_Builder()
    }

    #create_wrapper(content){
        const modal_id = lite.utils.unique(50)
        const wrapper = `
            <div id="${modal_id}" class="modal-wrapper w-full h-screen fixed top-0 left-0 bg-default/40 z-[100]" style="z-index:1000 intro-y flex items-center justify-center">
                <div class="quick-form w-[max-content] mx-auto">${content}</div>
            </div>
        `
        $("body").append(wrapper)
        return modal_id
    }

    async quick_form(config, title, columns=2, include_all_fields=false,on_save={},on_cancel={}){
        let fields = ""
        $.each(config?.fields,(_,f)=>{
            if(f?.required || (!f.required && include_all_fields)){
                fields += this.html_generator.build_form_field(f, config?.setup)
            }
        })
        let content = `
            <div class="box px-5 py-3 mt-10 min-w-[500px] max-w-[800px] min-h-[300px] intro-y">
                <div class="text-slate-600 text-13 w-full border-b pb-2 flex items-center justify-between mb-5">
                    <span class="font-semibold">${title || "New " + lite.utils.replace_chars(config.setup.model, "_", " ")}</span>
                    <button class="close-modal text-orange-500"><span class="material-symbols-outlined font-19 font-bold"> close </span></button>
                </div>
                <div class="min-h-[270px] max-h-[500px] overflow-y-auto">
                <form id="${config?.setup?.new_form_id}" class="w-full">
                    
                    <div class="form-fields grid gap-3 gap-x-5"></div>
                </form>
                </div>
                <div class="flex items-center justify-end border-t pt-2 h-[50px]">
                    <button action="cancel" class="modal-action-btn text-13 btn text-orange-800 border-secondary_color bg-orange-50 mr-2 w-[100px] h-[30px]">
                        <span class="material-symbols-outlined text-12 mr-1"> ${on_cancel?.icon || "cancel"}  </span> 
                        ${on_cancel?.text || "Cancel"}
                    </button>
                    <button action="save" class="modal-action-btn save-action-btn text-13 btn bg-default text-theme_text_color w-[130px] h-[30px]">
                        <span class="material-symbols-outlined text-12 mr-1"> ${on_save?.icon || "task_alt"}  </span>
                        ${on_save?.text || "Save"}
                    </button>
                </div>
            </div>
        `
        return this.#create_wrapper(content)
    }


    confirm_modal(title, message, on_confirm={text:"Confirm", fun: null}, on_cancel={text:"Cancel"}){
        let content = `
            <div class="box px-5 py-3 mt-10 min-w-[500px] max-w-[800px] min-h-[200px] intro-y">
                <div class="text-slate-600 text-13 w-full border-b pb-2 flex items-center justify-between mb-5">
                    <span class="font-semibold">${title}</span>
                    <button class="close-modal text-orange-500"><span class="material-symbols-outlined font-19 font-bold"> close </span></button>
                </div>
                <div class="min-h-[120px] max-h-[500px] overflow-y-auto">
                    <div class="content-wrapper gap-4">${message}</div>
                </div>
                <div class="flex items-center justify-end border-t pt-2 h-[50px]">
                    <button action="cancel" class="modal-action-btn text-13 btn text-orange-800 border-secondary_color bg-orange-50 mr-2 w-[100px] h-[30px] intro-x">
                        <span class="material-symbols-outlined font-19 font-bold mr-1"> ${ on_cancel?.icon || "close" } </span> 
                        ${on_cancel?.text || "Cancel"}
                    </button>
                    <button action="confirm" class="modal-action-btn text-13 btn bg-default text-theme_text_color min-w-[100px] h-[30px] intro-x">
                        <span class="material-symbols-outlined font-19 font-bold mr-1"> ${ on_confirm?.icon || "task_alt" } </span> 
                        ${on_confirm?.text || "Confirm"}
                    </button>
                </div>
            </div>
        `
        return this.#create_wrapper(content)
    }

    feedback_modal(title, message, on_confirm={text:"Submit", fun: null}, on_cancel={text:"Cancel"}){
        let content = `
            <div class="box px-5 py-3 mt-10 min-w-[500px] max-w-[800px] min-h-[200px] intro-y">
                <div class="text-slate-600 text-13 w-full border-b pb-2 flex items-center justify-between mb-5">
                    <span class="font-semibold">${title}</span>
                    <button class="close-modal text-orange-500"><span class="material-symbols-outlined font-19 font-bold"> close </span></button>
                </div>
                <div class="min-h-[120px] max-h-[500px] overflow-y-auto">
                    <div class="content-wrapper gap-4">${message}</div>
                    <div class="content-wrapper w-[70%] mx-auto gap-4 my-4 flex items-center justify-between">

                        <div class="flex flex-col items-center justify-center">
                            <button index="1" class="modal-rate-btn transition hover:scale-[1.5] duration-500 text-13 shadow-md btn text-gray-400 border-gray-300 bg-gray-50 mr-2 w-[40px] h-[40px] intro-y">
                                <span class="material-symbols-outlined font-bold text-20"> star </span> 
                            </button>
                            <span class="mt-1 text-10">1</span>
                        </div>
                        <div class="flex flex-col items-center justify-center">
                            <button index="2" class="modal-rate-btn transition hover:scale-[1.5] duration-500 text-13 shadow-md btn text-gray-400 border-gray-300 bg-gray-50 mr-2 w-[40px] h-[40px] intro-y">
                                <span class="material-symbols-outlined font-bold text-20"> star </span> 
                            </button>
                            <span class="mt-1 text-10">2</span>
                        </div>
                        <div class="flex flex-col items-center justify-center">
                            <button index="3" class="modal-rate-btn transition hover:scale-[1.5] duration-500 text-13 shadow-md btn text-gray-400 border-gray-300 bg-gray-50 mr-2 w-[40px] h-[40px] intro-y">
                                <span class="material-symbols-outlined font-bold text-20"> star </span> 
                            </button>
                            <span class="mt-1 text-10">3</span>
                        </div>
                        <div class="flex flex-col items-center justify-center">
                            <button index="4" class="modal-rate-btn transition hover:scale-[1.5] duration-500 text-13 shadow-md btn text-gray-400 border-gray-300 bg-gray-50 mr-2 w-[40px] h-[40px] intro-y">
                                <span class="material-symbols-outlined font-bold text-25"> star </span> 
                            </button>
                            <span class="mt-1 text-10">4</span>
                        </div>
                        <div class="flex flex-col items-center justify-center">
                            <button index="5" class="modal-rate-btn transition hover:scale-[1.5] duration-500 text-13 shadow-md btn text-gray-400 border-gray-300 bg-gray-50 mr-2 w-[40px] h-[40px] intro-y">
                                <span class="material-symbols-outlined font-bold text-30"> hotel_class </span> 
                            </button>
                            <span class="mt-1 text-10">5</span>
                        </div>
                    </div>
                    <div class="content-wrapper mb-5 px-2">
                        ${
                            this.html_generator.build_form_field({
                                id:"feedback-message",
                                fieldname: "feedback_message",
                                fieldlabel: "Message",
                                fieldtype: "longtext",
                                classnames:"h-[100px] intro-y",
                                required: false,
                                placeholder: "Please provide your feedback message here"
                            })
                        }
                    </div>
                </div>
                <div class="flex items-center justify-end border-t pt-2 h-[50px]">
                    <button action="cancel" class="modal-action-btn text-13 btn text-orange-800 border-secondary_color bg-orange-50 mr-2 w-[100px] h-[30px] intro-x">
                        <span class="material-symbols-outlined font-bold mr-1 text-12"> ${ on_cancel?.icon || "close" } </span> 
                        ${on_cancel?.text || "Cancel"}
                    </button>
                    <button action="confirm" class="modal-action-btn text-13 btn bg-default text-theme_text_color min-w-[100px] h-[30px] intro-x">
                        <span class="material-symbols-outlined font-bold mr-1 text-12"> ${ on_confirm?.icon || "add_comment" } </span> 
                        ${on_confirm?.text || "Submit"}
                    </button>
                </div>
            </div>
        `
        return this.#create_wrapper(content)
    }


    custom_modal(title, content, on_confirm={text:"Confirm", fun: null}, on_cancel={text:"Cancel"}){
        let html = `
            <div class="box px-5 py-3 mt-10 min-w-[500px] max-w-[800px] min-h-[200px] intro-y">
                <div class="text-slate-600 text-13 w-full border-b pb-2 flex items-center justify-between mb-5">
                    <span class="font-semibold">${title}</span>
                    <button class="close-modal text-orange-500"><span class="material-symbols-outlined font-19 font-bold"> close </span></button>
                </div>
                <div class="min-h-[120px] max-h-[500px] overflow-y-auto">
                    <div class="content-wrapper gap-4">${content}</div>
                </div>
                <div class="flex items-center justify-end border-t pt-2 h-[50px]">
                    <button action="cancel" class="modal-action-btn text-13 btn text-orange-800 border-secondary_color bg-orange-50 mr-2 w-[100px] h-[30px] intro-x">
                        <span class="material-symbols-outlined text-12 font-bold mr-1"> ${ on_cancel?.icon || "close" } </span> 
                        ${on_cancel?.text || "Cancel"}
                    </button>
                    <button action="confirm" class="modal-action-btn text-13 btn bg-default text-theme_text_color min-w-[100px] h-[30px] intro-x">
                        <span class="material-symbols-outlined text-12 font-bold mr-1"> ${ on_confirm?.icon || "task_alt" } </span> 
                        ${on_confirm?.text || "Confirm"}
                    </button>
                </div>
            </div>
        `
        return this.#create_wrapper(html)
    }
}