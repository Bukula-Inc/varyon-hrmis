export default class Expandable_Field{
    constructor(){
        this.expandable_field_configs = {}
        
    }
    init(){
       const fields = $('div.lite-field[type="expandable"]:not(.initialized)') 
       if(lite.utils.array_has_data(fields)){
        $.each(fields,(_,f)=>{
            const 
                id = lite.utils.get_attribute(f, "lite-id"), 
                fieldname = lite.utils.get_attribute(f, "fieldname"),
                value = lite.utils.get_attribute(f, "value")

            if(!this.expandable_field_configs[id]){
                this.expandable_field_configs[id] = { id:id, fieldname:fieldname, value:value, field:f }
            }
            else{
                this.expandable_field_configs[id].field = f
            }
            
            $(f)?.off("click")?.click(e=>{
                const id = lite.utils.get_attribute(e.currentTarget, "id")
                const config = this.expandable_field_configs[id], description = lite.utils.capitalize(lite.utils.replace_chars(config?.fieldname||"","_"," "))
                const field = lite.html_generator.build_form_field({
                    id:id,
                    liteid:id,
                    fieldtype:"rich",
                    fieldname:config?.fieldname,
                    omitlabels:true,
                    value:config?.value,
                    placeholder: description,
                    height: 350
                })
                $("body").append(`
                    <div id="${id}" class="expandable-modal fixed w-full h-full bg-default/50 top-0 left-0 overflow-hidden overflow-y-auto" style="z-index:1000">
                        <div class="fixed p-3 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vw] h-[70vh] bg-white border border-dotted border-default shadow-md rounded-md flex flex-col items-center justify-between">
                            <div class="w-full h-[5%] flex items-center justify-between border-b">
                                <strong>${description}</strong>
                                <button class="close-expandable text-red-500 text-[30px]">
                                    <span class="material-symbols-outlined">close</span>
                                </button>
                            </div>

                            <div class="w-full h-[85%] overflow-hidden overflow-y-auto">${field}</div>

                            <div class="w-full h-[5%] flex items-center justify-end">
                                <button class="close-expandable bg-gray-200 text-orange-600 border w-[120px] h-[30px] btn rounded-md ml-2">
                                    <span class="material-symbols-outlined">close</span>
                                    Cancel
                                    
                                </button>
                                <button for="${id}" class="update-expandable text-white bg-default w-[120px] h-[30px] btn rounded-md ml-2">
                                    Update
                                    <span class="material-symbols-outlined">save</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `)
                $(".close-expandable")?.off("click").click(e=>{
                    $(`.expandable-modal`)?.remove()
                    $(`.expandable-modal`)?.off()
                    $(`.expandable-modal`)?.empty()
                })
                lite.rich_editor.init_rich_editors()

                $(`.update-expandable[for="${id}"]`)?.off("click")?.click(e=>{
                    const field = $(".expandable-modal")?.find(`textarea[id="${id}"]`)
                    if(lite.utils.array_has_data(field)){
                        const value = lite.rich_editor.get_content(field[0])
                        this.update_field($(`.lite-field.expandable-field#${id}`), value)
                        $(`.expandable-modal`)?.remove()
                        $(`.expandable-modal`)?.off()
                        $(`.expandable-modal`)?.empty()
                    }
                })
            })
        })
       }
    }

    get_value(field){
        return this.expandable_field_configs[lite.utils.get_attribute(field, "id")]?.value || ""
    }

    update_field(field, value, update_child_table=true){
        if(value !== undefined){
            this.expandable_field_configs[lite.utils.get_attribute(field,"id")].value = value
            $(field)?.html(value)
            if(lite?.form_controller?.is_child_table_field(field) && update_child_table){
                lite?.form_controller?.set_form_table_value($(field)?.parents(".table")?.attr("fieldname"), $(field)?.parents(".table-row")?.attr("id"), $(field).attr("fieldname"), value)
            }
        }
    }
}