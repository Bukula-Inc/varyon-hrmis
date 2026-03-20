from controllers.utils import Utils
from controllers.utils.dates import Dates
# from controllers.dbms import DBMS
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

# TAX INVOICE DASHBOARD
class Currency_Dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        self.past_30_days = dates.add_days(dates.today(), -30)
        # self.core = Core_Accounting(dbms, self.user, self.object)
        self.settings = self.dbms.system_settings
        self.defaults = self.settings.accounting_defaults
        self.default_company = self.settings.linked_fields.default_company

    @classmethod
    def currency(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        return utils.respond(utils.ok,{
            "currency":cls.settings.default_currency,
            "xchange_rates": cls.get_xchange_rates(cls).get("data"),
            "currency_wise_transaction_trends": cls.get_currency_wise_transaction_trends(cls).get("data"),
            "exchange_rate_history": cls.get_exchange_rate_history(cls).get("data"),
            "exchange_gain_or_loss": cls.get_exchange_gain_or_loss(cls).get("data"),
        })
    

    def get_xchange_rates(self):
        res = []
        # reporting = self.settings.default_currency
        # in_forex_table = self.dbms.get_list("Currency", filters={"include_in_quick_rates":1},user=self.user, limit=4,order_by="id")
        # if in_forex_table.get("status") == utils.ok:
        #     for fx in in_forex_table.get("data").get("rows"):
        #         name = fx.get("name")
        #         if name != reporting:
        #             xrate = self.core.get_exchange_rate(reporting,name)
        #             if xrate.get("status") == utils.ok:
        #                 d = xrate.get("data")
        #                 data = {
        #                     "from":reporting,
        #                     "to": name,
        #                     "rate": d.get("rate"),
        #                     "inverse": d.get("inverse")
                            
        #                 }
        #                 hist = self.core.get_exchange_rate_history(reporting,name, 1)
        #                 if hist.get("status") == utils.ok:
        #                     d = Generate_Object(hist.get("data").get("rows")[0])
        #                     data["history"] = { "date": dates.date_to_numeric(d.created_on), "rate": d.rate, "inverse":d.inverse, "diff": utils.fixed_decimals((data.get("rate") - d.rate), 4) }
        #                 else:
        #                     data["history"] = { "date": dates.date_to_numeric(dates.add_days(dates.today(), -1)), "rate": "-", "inverse": "-", "diff": "-" }
        #                 res.append(data)
        return utils.respond(utils.ok,res)
    
    def get_currency_wise_transaction_trends(self):
        res = []
        # gls = self.dbms.get_list_by_group("GL_Entry", "transaction_currency", "reporting_debit_amount", user = self.user,limit=1000)
        # if gls.get("status") == utils.ok:
        #     d = gls.get("data")
        #     res = d
        return utils.respond(utils.ok,res)




    def get_exchange_rate_history(self):
        res = []
        # reporting = self.settings.default_currency
        # in_forex_table = self.dbms.get_list("Currency", filters={"include_in_quick_rates":1},user=self.user, limit=6,order_by="id")
        # if in_forex_table.get("status") == utils.ok:
        #     for fx in in_forex_table.get("data").get("rows"):
        #         name = fx.get("name")
        #         if name != reporting:
        #             hist = self.core.get_exchange_rate_history(reporting,name, 1)
        #             if hist.get("status") == utils.ok:
        #                 d = hist.get("data").get("rows")[0]
        #                 data = {
        #                     "date": dates.date_to_numeric(d.get("created_on")),
        #                     "from":reporting,
        #                     "to": name,
        #                     "rate": d.get("rate"),
        #                     "inverse": d.get("inverse")
        #                 }
        #                 res.append(data)
        return utils.respond(utils.ok,res)
    

    def get_exchange_gain_or_loss(self):
        res = {}
        # gain_or_loss = self.defaults.get(self.default_company).realized_gain_or_loss
        # rows = []
        # acc = self.dbms.get_list("GL_Entry", filters={"account": gain_or_loss,"docstatus":1, "posting_date__gt": self.past_30_days},user=self.user)
        # ag_acc = self.dbms.get_list("GL_Entry", filters={"against_account": gain_or_loss,"docstatus":1, "posting_date__gt": self.past_30_days},user=self.user)
        # if acc.get("status") == utils.ok:
        #     rows.extend(acc.get("data").get("rows"))
        # if ag_acc.get("status") == utils.ok:
        #     rows.extend(ag_acc.get("data").get("rows"))
        # for dt in range(30):
        #     date = dates.add_days(self.past_30_days,dt +1)
        #     res[str(date)] = {
        #         "date": dates.date_to_numeric(date),
        #         "value": 0
        #     }

        #     if len(rows) > 0:
        #         for tr in rows:
        #             t = Generate_Object(tr)
        #             key = str(t.posting_date)
        #             if res.get(key):
        #                 if t.account == gain_or_loss:
        #                     if t.transaction_debit_amount > 0:
        #                         res[key]["value"] += t.reporting_debit_amount
        #                     else:
        #                         res[key]["value"] -= t.reporting_credit_amount
        #                 else:
        #                     if t.transaction_credit_amount > 0:
        #                         res[key]["value"] += t.reporting_debit_amount
        #                     else:
        #                         res[key]["value"] -= t.reporting_credit_amount


        return utils.respond(utils.ok,res)
    
    