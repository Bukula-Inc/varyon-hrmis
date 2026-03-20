def after_system_settings_fetch(dbms,params,object):
    pass
    # obj = object.rows[0]
    # company = dbms.get_doc("Company",obj.default_company,params.headers.User)
    # cost_center = dbms.get_doc("Cost_Center",obj.default_cost_center,params.headers.User)
    # currency = dbms.get_doc("Currency",obj.default_currency,params.headers.User)
    # obj.company_info = company.get("data")
    # obj.cost_center_info = cost_center.get("data")
    # obj.currency_info = currency.get("data")