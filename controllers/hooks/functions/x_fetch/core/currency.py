from controllers.core_functions.core import Core
from controllers.utils import Utils
from controllers.utils.dates import Dates
utils = Utils()
pp = utils.pretty_print


def get_forex_currencies(dbms, object):
    pp("hehehehehehhehehehehehhehehe")
    currencies = []
    reporting = "ZMW"
    # settings = dbms.system_settings
    # reporting_currency = settings.linked_fields.default_currency
    # reporting = {
    #     "name": reporting_currency.name,
    #     "symbol": reporting_currency.symbol,
    #     "country": reporting_currency.country,
    #     "country_code": settings.linked_fields.default_country.code
    # }
    # forex_currencies = dbms.get_list("Currency", filters={"include_in_forex_table":1 }, fetch_linked_fields=True, page_size=12,user=object.user)
    # if forex_currencies.status != utils.ok:
    #     forex_currencies = dbms.get_list("Currency", page_size=12,user=object.user)
    #     if forex_currencies.status != utils.ok:
    #         return forex_currencies
    # for fx_c in forex_currencies.data.rows:
    #     country_code = ''
    #     country = dbms.get_doc("Country",fx_c.country,user=object.user)
    #     if country.status == utils.ok:
    #         country_code = country.data.code
    #     currencies.append({
    #         "name":fx_c.name,
    #         "symbol":fx_c.symbol,
    #         "country":fx_c.country,
    #         "country_code": country_code
    #     })
    return utils.respond(utils.ok, {"reporting_currency":reporting, "trade_currencies": currencies})
        
        
def get_trade_rates(dbms,object):
    pp("hehehehehehhehehehehehhehehe")
    rates = object.body
    xchange_rates = []
    if rates and len(rates.data) > 0:
        for rate in rates.data:
            name = rate.name
            from_currency = rate.from_currency
            to_currency = rate.to_currency
            x_rate = dbms.get_doc("Exchange_Rate", name,user=object.user)
            data = None
            if x_rate.status == utils.ok:
                data = x_rate.data
                xchange_rates.append({
                    "name": data.name,
                    "from_currency": data.from_currency,
                    "to_currency": data.to_currency,
                    "rate": data.rate,
                    "inverse": data.inverse
                })
            else:
                x_rate = dbms.get_list("Exchange_Rate",filters={"from_currency": to_currency,"to_currency": from_currency},page_size=1,user=object.user)
                if x_rate.status == utils.ok:
                    d = x_rate.data.rows[0]
                    new_exchange_rate = {
                        "name": rate.name,
                        "from_currency":rate.from_currency,
                        "to_currency":rate.to_currency,
                        "rate": d.inverse * 1,
                        "inverse": 1 / d.inverse,
                        "status":"Active"
                    }
                    new_rate = dbms.create("Exchange_Rate", utils.from_dict_to_object(new_exchange_rate),object.user)
                    xchange_rates.append(new_exchange_rate)
                else:
                    new_exchange_rate = {
                        "name": rate.name,
                        "from_currency": rate.from_currency,
                        "to_currency": rate.to_currency,
                        "rate": 1,
                        "inverse": 1,
                        "status": "Active"
                    }
                    new_rate = dbms.create("Exchange_Rate", utils.from_dict_to_object(new_exchange_rate),object.user)
                    xchange_rates.append(new_exchange_rate)
        return utils.respond(utils.ok, xchange_rates)


    
def update_exchange_rate(dbms,object):
    pass
    # core_accounting = Core_Accounting(dbms, object.user, object)
    # data = object.body.data
    # return core_accounting.update_exchange_rate()

def update_bulk_exchange_rates(dbms,object):
    pass
    # core_accounting = Core_Accounting(dbms, object.user, object)
    # data = object.body.data
    # return core_accounting.update_exchange_rate()


def get_exchange_rate(dbms,object):
    pass
    # core_accounting = Core_Accounting(dbms,object.user,object)
    # data = object.body.data
    # return core_accounting.get_exchange_rate(data.from_currency, data.to_currency)
    

def convert_currency(dbms,object):
    pass
    # core_accounting = Core_Accounting(dbms,object.user,object)
    # data = object.body.data
    # return core_accounting.convert_currency(data.from_currency, data.to_currency,data.amount)