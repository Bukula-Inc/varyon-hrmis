
export default class Date_Picker{
    constructor(){
        this.fields = []
        this.on_change = []
    }
    init(on_date_change=undefined, cls=undefined){
        if(on_date_change && typeof on_date_change === "function"){
            this.on_change.push({fun:on_date_change, cls:cls})
        }
        const fields = $('.lite-field[is-date-field="true"]:not(.initialized)')
        if(lite.utils.array_has_data(fields)){
            $.each(fields,(_,f)=>{
                $(f).addClass("initialized")
                if($(f)?.attr("double-picker") === "true")
                    new Lightpick({
                        field: f,
                        format: 'YYYY-MM-DD',
                        singleDate: false,
                        minDate: moment().subtract(60, 'years'),
                        maxDate: moment().add(10, 'years'),
                        startDate: new Date(),
                        onSelectEnd: (start, end) => $(f).focusout()
                    })
                else{
                    new Lightpick({
                        field: f,
                        format: 'YYYY-MM-DD',
                        singleDate: true,
                        minDate: moment().subtract(60, 'years'),
                        maxDate: moment().add(10, 'years'),
                        startDate: new Date(),
                        onSelect: (data) => $(f).focusout()
                    })
                }
            })
        }
    }
}