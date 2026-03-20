

export default class Lite_Switch{
    constructor(){
        this.on_switch_change = []
    }
    init_switch_fields(on_switch_change, cls){
        if(on_switch_change){
            this.on_switch_change.push({fun:on_switch_change, cls:cls})
        }
        const lite_switch = $('.lite-field[type="switch"]')
        if(lite.utils.array_has_data(lite_switch)){
            $.each(lite_switch,(_,s)=>{
                $(s).find(".switch-toggler").off("click").click(e=>{
                    const toggled = this.toggle_switch(e)
                    if(lite.utils.array_has_data(this.on_switch_change)){
                        $.each(this.on_switch_change,(_,sw)=>{
                            if(sw?.fun){
                                sw.fun(toggled ,sw?.cls || null)
                            }
                        })
                    }
                })
            })
        }
    }
    toggle_switch(toggler){
        let new_value = 0
        const
            lite_field = $(toggler.currentTarget).parents(".lite-field"),
            value = lite.utils.string_to_int(lite_field?.attr("value"))
        if(value == 0){
            new_value = 1
            lite_field?.attr("value", new_value)
            $(toggler.currentTarget).parent().removeClass("bg-gray-200").addClass("bg-default")
            $(toggler.currentTarget).removeClass("left-0 bg-gray-400").addClass("left-[70%] bg-default border")
        }
        else{
            new_value = 0
            lite_field?.attr("value", new_value)
            $(toggler.currentTarget).parent().addClass("bg-gray-200").removeClass("bg-default")
            $(toggler.currentTarget).addClass("left-0 bg-gray-400").removeClass("left-[70%] bg-default border")
        }
        return {
            value:new_value,
            field:lite_field
        }
    }
    set_switch_value(field,value){
        $(field)?.attr("value", value)
        const toggler = $(field).find(".switch-toggler")
        if(value == 0){
            $(toggler).parent().addClass("bg-gray-200").removeClass("bg-default")
            $(toggler).addClass("left-0 bg-gray-400").removeClass("left-[70%] bg-default border")
        }
        else{
            $(toggler).parent().removeClass("bg-gray-200").addClass("bg-default")
            $(toggler).removeClass("left-0 bg-gray-400").addClass("left-[70%] bg-default border")
        }
    }
}