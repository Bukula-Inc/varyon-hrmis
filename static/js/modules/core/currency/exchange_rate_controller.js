;
import Core_HTML_Generator from "../../../page/html/core_html_generator.js";
export default class Exchange_Rate_Controllr{
    constructor(){
        this.exchange_rates = {}
        this.rates = []
        this.generator = new Core_HTML_Generator()
        this.$forex_wrapper = $('.forex-wrapper')
        this.$forex_wrapper_header = $('.forex-wrapper-header')
        
    }
    init(){
        this.init_exchange_rates()
    }
    async init_exchange_rates(){
        const {status, data, error_message} = await lite.connect.x_fetch("get_forex_currencies")
        if(status == lite.status_codes.ok){
            const currencies = data
            const reporting_currency = currencies.reporting_currency
            const trade_currencies = currencies.trade_currencies
            const total_trade_currencies = trade_currencies?.length
            if(total_trade_currencies > 0){
                this.$forex_wrapper.addClass(`grid-rows-${total_trade_currencies + 2}`)
                this.$forex_wrapper.html(this.generator.generate_forex_table(reporting_currency,trade_currencies))
                const forex_cells = this.$forex_wrapper.find('.forex-cell:not(.is-own)')
                if(lite.utils.array_has_data(forex_cells)){
                    $.each(forex_cells,(_,fx_cell)=>{
                        const fx_rate = $(fx_cell).find("input.forex-rate"),
                              fx_inverse = $(fx_cell).find("span.inverse-value")
                        if(fx_rate){
                            const from_currency = fx_rate.attr("from-currency"),
                                  to_currency = fx_rate.attr("to-currency")
                            this.exchange_rates[`${from_currency} - ${to_currency}`] = {
                                name: `${from_currency} - ${to_currency}`,
                                cell:fx_cell,
                                rate_field: fx_rate,
                                fx_inverse_field:fx_inverse,
                                from_currency:from_currency,
                                to_currency:to_currency,
                                rate: 1,
                                inverse: 1
                            }
                            let rate = {
                                name: `${from_currency} - ${to_currency}`,
                                from_currency: from_currency,
                                to_currency: to_currency,
                            }                    
                            this.rates.push(rate) 
                        }
                    })
                    await this.get_exchange_rates()
                    
                    $(".forex-cell:not(.is-own)").find("input.forex-rate").off("focusout").focusout(e=>{
                        const from_currency = lite.utils.get_attribute(e.currentTarget,"from-currency")
                        const to_currency = lite.utils.get_attribute(e.currentTarget,"to-currency")
                        this.update_exchange_rate(this.exchange_rates[`${from_currency} - ${to_currency}`])
                    })

                }
            }
        }
    }

   async get_exchange_rates(){
        const {status, data, error_message} = await lite.connect.x_post("get_trade_rates",this.rates)
        if(status === lite.status_codes.ok){
            $.each(data,(_,rate)=>{
                this.set_rate(rate)
            })
        }
    }

    set_rate(xchange_rate){
        const x_rate = this.exchange_rates[xchange_rate.name]
        $(x_rate.cell).find(".dynamic-loader").remove()
        $(x_rate.cell).find(".forex-fields-wrapper").removeClass("hidden")
        $(x_rate.rate_field).val(lite.utils.fixed_decimals(xchange_rate.rate,5))
        $(x_rate.fx_inverse_field).text(lite.utils.fixed_decimals(xchange_rate.inverse,5))
        x_rate.rate = xchange_rate.rate
        x_rate.inverse = xchange_rate.inverse
    }

    async update_exchange_rate(rate){
        let current_rate = this.exchange_rates[rate.name]
        const new_rate = lite.utils.string_to_float($(current_rate.rate_field).val())
        if(new_rate && current_rate.rate !== new_rate){
            const inverse = lite.utils.fixed_decimals(1 / new_rate,5)
            $(current_rate.fx_inverse_field).text(lite.utils.fixed_decimals(inverse,5))
            current_rate.rate = new_rate
            current_rate.inverse = inverse
            const new_rates = {
                name:current_rate.name,
                rate:current_rate.rate,
                inverse:current_rate.inverse,
                from_currency:current_rate.from_currency,
                to_currency:current_rate.to_currency,
            }
            const update = await lite.connect.x_post("update_exchange_rate", new_rates)
            if(update.status === lite.status_codes.ok){
                lite.alerts.toast({
                    toast_type: lite.status_codes.ok,
                    title: "Exchange Rate Updated",
                    message: `${new_rates.name} Updated Successfully!`,
                    timer: 4000
                })
                const data = update.data?.inverse_update
                const inverse_fx = this.exchange_rates[data.name]
                $(inverse_fx.rate_field).val(data.rate)
                $(inverse_fx.fx_inverse_field).text(data.inverse)
            }
        }
    }
}