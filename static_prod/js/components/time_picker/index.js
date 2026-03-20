
export default class Time_Picker{
    constructor(){
        this.fields = []
        this.on_change = []
    }
    init(on_time_change=undefined, cls=undefined){
        if(on_time_change && typeof on_time_change === "function"){
            this.on_change.push({fun:on_time_change, cls:cls})
        }
        const fields = $('.lite-field[is-time-field="true"]')
        if(lite.utils.array_has_data(fields)){
            $.each(fields,(_,f)=>{
                $(f).clockpicker({ autoclose: true })?.change(e=>$(e.currentTarget).focusout())
            })
        }
    }
}