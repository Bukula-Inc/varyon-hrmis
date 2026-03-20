export class Field_Formatter{
    constructor(){
        this.init()
        this.figure_fields = ["float","currency"]
    }

    init(){
        $(document).on("focusin", "input", e=> {
            let value = $(e?.currentTarget)?.val()
            if([...this.figure_fields,"percentage"].includes($(e?.currentTarget)?.attr("type"))){
                $(e?.currentTarget)?.val(lite.utils.string_to_float(value,lite.currency_decimals))
            }
            else if($(e?.currentTarget)?.attr("type") == "int"){
                $(e?.currentTarget)?.val(lite.utils.string_to_int(value,0))
            }
            $(e?.currentTarget).attr("prev-val", $(e?.currentTarget)?.val())
            $(e.currentTarget).select()
        })

        $(document).on("focusout", "input", e=> {
            let value = $(e?.currentTarget)?.val()
            if(this.figure_fields.includes($(e?.currentTarget)?.attr("type"))){
                $(e?.currentTarget)?.val(lite.utils.thousand_separator(value,lite.currency_decimals))
            }
            else if($(e?.currentTarget)?.attr("type") == "int"){
                $(e?.currentTarget)?.val(lite.utils.thousand_separator(value,0))
            }
            else if($(e?.currentTarget)?.attr("type") == "percentage"){
                $(e?.currentTarget)?.val(`${value}%`)
            }
            if($(e?.currentTarget)?.attr("prev-val") != value){
                $(e?.currentTarget).attr("prev-val", $(e?.currentTarget)?.val())
            }
        })
        $(document).on("change", "input", e=> {
            // let value = $(e?.currentTarget)?.val()
            // if(this.figure_fields.includes($(e?.currentTarget)?.attr("type"))){
            //     $(e?.currentTarget)?.val(lite.utils.thousand_separator(value,lite.currency_decimals))
            // }
            // else if($(e?.currentTarget)?.attr("type") == "int"){
            //     $(e?.currentTarget)?.val(lite.utils.thousand_separator(value,0))
            // }
            // else if($(e?.currentTarget)?.attr("type") == "percentage"){
            //     $(e?.currentTarget)?.val(`${value}%`)
            // }
            // if($(e?.currentTarget)?.attr("prev-val") != value){
            //     $(e?.currentTarget).attr("prev-val", $(e?.currentTarget)?.val())
            // }
        })
    }
}