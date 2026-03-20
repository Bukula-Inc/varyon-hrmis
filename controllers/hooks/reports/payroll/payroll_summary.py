from controllers.utils import Utils

utils = Utils()

def payroll_summary_report(dbms, object):
    payroll_data_result = []
    paye_filters = object.filters
    paye_filters.docstatus = 1
    payroll_processor = dbms.get_list("Payroll_Processor", filters=paye_filters,   privilege=True)
    if payroll_processor.status == utils.ok:
        payroll_data = payroll_processor.data.rows
        overrals = utils.from_dict_to_object({
            "name": " OVERALL TOTAL",
            "from_date": " ",
            "to_date": " ",
            "total_employees": " ",
            "total_basic": 0,
            "total_gross": 0,
            "total_net": 0,
            "total_earnings": 0,
            "total_deductions": 0,
            "is_opening_or_closing": True
        })
        for payroll in payroll_data:

            payroll_row = {
                "name": payroll.name,
                "from_date": payroll.from_date,
                "to_date": payroll.to_date,
                "total_employees": payroll.total_employees,
                "total_basic": payroll.total_basic,
                "total_gross": payroll.total_gross,
                "total_net": payroll.total_net,
                "total_earnings":payroll.total_earnings ,
                "total_deductions": utils.fixed_decimals(payroll.total_deductions, dbms.system_settings.currency_decimals),
            }
            overrals.total_basic += payroll.total_basic
            # overrals.total_employees += payroll.total_employees,
            overrals.total_gross += payroll.total_gross
            overrals.total_net += payroll.total_net
            overrals.total_earnings += payroll.total_earnings
            overrals.total_deductions += payroll.total_deductions
            payroll_data_result.append(payroll_row)
        payroll_data_result.append(overrals)
            

    return utils.respond(utils.ok, {'rows': payroll_data_result})