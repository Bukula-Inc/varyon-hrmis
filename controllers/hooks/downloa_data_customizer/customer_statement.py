from controllers.utils import Utils
# from controllers.hooks.reports.accounting.receivables_and_payables import trade_receivables
utils = Utils()
throw = utils.throw
pp = utils.pretty_print

# def on_customer_statement_download(dbms, object, data):
#     if data.filters and data.filters.customer:
#         data.customer = utils.from_dict_to_object()
#         customer = dbms.get_doc("Customer",data.filters.customer, privilege=True, fetch_linked_fields=False, fetch_linked_tables=False)
#         utils.evaluate_response(customer, f"Failed to fetch customer:{customer.error_message}!")
#         data.customer = customer.data
#         data.ageing_fields = []
#         data.ageing_analysis_data = []

#         receivables_report = trade_receivables(dbms,object, only_fetch_ages=True)
#         if receivables_report:
#             data.ageing_fields = utils.get_object_keys(receivables_report)
#             data.ageing_analysis_data = utils.get_object_values(receivables_report)
