
export default class Year_Picker{
    constructor(){
        this.fields = []
        this.on_change = []
    }
    init(on_year_change=undefined, cls=undefined){
        if(on_year_change && typeof on_year_change === "function"){
            this.on_change.push({fun:on_year_change, cls:cls})
        }
        const fields = $('.lite-field[is-year-field="true"]:not(.is-initialized)')
        if(lite.utils.array_has_data(fields)){
            $.each(fields,(_,f)=>{
                $(f).addClass("is-initialized")
                $(f).yearpicker({
                    onChange : function(value){
                      $(f)?.focusout()
                    },
                    year: parseInt($(f)?.attr("value")) || null
                })
            })
        }
    }
}