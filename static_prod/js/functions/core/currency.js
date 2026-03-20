
export default class Currency{
    constructor(){
        this.temp_exchange_rates = {}
    }

    async get_exchange_rate(from_currency,to_currency){
        if(from_currency === to_currency){
            return lite.connect.respond(lite.status_codes.ok, {
                from_currency: from_currency,
                to_currency: to_currency,
                rate: 1.00,
                exchange_rate: 1.00,
                inverse: 1.00,
            })
        }
        else{
            const data = {
                name: `${from_currency} - ${to_currency}`,
                from_currency: from_currency,
                to_currency: to_currency
            }
            if(this.temp_exchange_rates[data.name]){
                return {status:lite.status_codes.ok,data:this.temp_exchange_rates[data.name]}
            }
            const rate = await lite.connect.x_post("get_exchange_rate",data)
            if(rate.status === lite.status_codes.ok){
                this.temp_exchange_rates[data.name] = rate?.data
            }
            return rate
        }
    }
    async convert_currency(from_currency, to_currency, amount, convertion_rate,return_amount_only=false){
        if(!from_currency || !to_currency || !amount || amount == 0){
            if(return_amount_only){
                return amount
            }
            return lite.connect.respond(lite.status_codes.ok,{
                from_currency: from_currency,
                to_currency: to_currency,
                amount: amount,
                convertion_rate: convertion_rate
            })
        }
        if(from_currency === to_currency){
            if(return_amount_only){
                return amount
            }
            return lite.connect.respond(lite.status_codes.ok, {
                from_currency: from_currency,
                to_currency: to_currency,
                rate: 1.00,
                exchange_rate: 1.00,
                inverse: 1.00,
                converted_amount: amount
            })
        }
        else{
            const data = {
                name: `${from_currency} - ${to_currency}`,
                from_currency: from_currency,
                to_currency: to_currency,
                amount: amount,
                convertion_rate: convertion_rate
            }
            if(!this.temp_exchange_rates[data.name]){
                const rate = this.get_exchange_rate(from_currency,to_currency)
                if(rate.status === lite.status_codes.ok){
                    this.temp_exchange_rates[data.name] = rate.data
                }
                else{
                    const converted = await lite.connect.x_post("convert_currency",data)
                    if(return_amount_only){
                        return converted?.data?.converted_amount || false
                    }
                    return converted
                }
            }
            let converted = {...this.temp_exchange_rates[data.name]}
            converted.exchange_rate = converted.rate
            converted.amount = amount
            converted.converted_amount = lite.utils.fixed_decimals(converted.rate * amount, lite.defaults.currency_decimals)
            if(return_amount_only){
                return converted.converted_amount
            }
            return lite.connect.respond(lite.status_codes.ok,converted)
        }
    }

    async update_exchange_rate(from_currency,to_currency,rate){
        if(from_currency && to_currency && rate){
            const new_rates = {
                name:`${from_currency} - ${to_currency}`,
                rate:rate,
                exchange_rate:rate,
                inverse:lite.utils.fixed_decimals((1/rate),8),
                from_currency: from_currency,
                to_currency: to_currency,
            }
            const update = await lite.connect.x_post("update_exchange_rate", new_rates)
            if(update.status === lite.status_codes.ok){
                if(this.temp_exchange_rates[new_rates.name]){
                    this.temp_exchange_rates[new_rates.name].rate = rate
                }
                else{
                    this.temp_exchange_rates[update.data.name] = update.data
                }
            }
            return update
        }
    }
}