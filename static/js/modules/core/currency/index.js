
import Exchange_Rate_Controllr from './exchange_rate_controller.js'
import Core_HTML_Generator from '../../../page/html/core_html_generator.js'
export default class Currency{
    constructor(){
        this.generator = new Core_HTML_Generator()
        this.exchange_rate_controller = new Exchange_Rate_Controllr()
        this.$_top_xchange_rates = $(".top-xchange-rates")
        this.$exchange_rate_history = $(".exchange-rate-history")
        this.$_top_xchange_rates = $(".top-xchange-rates")
        this.$_top_xchange_rates = $(".top-xchange-rates")
        lite.page_controller.on_page_type_change(this.on_page_content_type_changed, this)
    }
    on_page_content_type_changed(data, cls){
        if(data.document === "Currency"){
            lite.page_controller.$main_grid.removeClass("col-span-4").addClass("col-span-3")
            lite.page_controller.$side_grid.removeClass("hidden")
            cls.init_currency_dashboard ()
        }
        else{
            lite.page_controller.$main_grid.removeClass("col-span-3").addClass("col-span-4")
            lite.page_controller.$side_grid.addClass("hidden")
            cls.exchange_rate_controller.init()
        }
    }
    async init_currency_dashboard(){
        const {status, data, error_message} = await lite.connect.dashboard("currency")
        lite.utils.init_dashboard(true)
        if(status === lite.status_codes.ok){
            this.data = data
            this.init_top_xchange_rates()
            this.init_exchange_rate_history()
            this.init_gain_or_loss_charts()
        } 
    }
    init_top_xchange_rates(){
        if(lite.utils.array_has_data(this.data?.xchange_rates)){
            $.each(this.data?.xchange_rates,(_,x)=>{
                this.$_top_xchange_rates.append(this.generator.create_top_xrate_row(x))
            })
        }
    }

    init_exchange_rate_history(){
        if(lite.utils.array_has_data(this.data?.exchange_rate_history)){
            $.each(this.data?.exchange_rate_history,(_,xh)=>{
                this.$exchange_rate_history.append(this.generator.create_xchange_rate_history_row(xh))
            })
        }
    }

    async init_gain_or_loss_charts(){
        const gain_or_loss = this.data.exchange_gain_or_loss
        if(!lite.utils.is_empty_object(gain_or_loss)){
            let data = {labels: [], values: []}
            $.each(lite.utils.get_object_keys(gain_or_loss),(_,gol)=>{
                data.labels.push(gain_or_loss[gol].date?.substring(0,8)?.trim())
                data.values.push(gain_or_loss[gol].value)
            })
            lite.charts.column_chart_with_negatives('exchange-gran-or-loss', data.labels, data.values,
            {
                title: 'Exchange gain/loss',
                y_axis_title: `Total Amount ${this.data?.currency}`,
                formatter_decimals: 2,
                height:200
            }
        )
        }
       
        
    }
}
