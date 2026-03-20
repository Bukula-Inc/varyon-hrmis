from controllers.utils import Utils

utils =Utils()
pp =utils.pretty_print
throw = utils.throw 

def after_module_pricing_fetch(dbms, object, result):
    if object.is_list_fetch:
        for mp in result:
            stock_item = dbms.get_doc("Stock_Item", mp.name, privilege=True,fetch_linked_tables=False, fetch_linked_fields=False)
            if stock_item.status == utils.ok:
                mp.item = stock_item.data
