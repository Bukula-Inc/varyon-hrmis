from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion

utils = Utils()
dates = Dates()

def employee_separations(dbms, object):
    core_hr = Core_Hr (dbms)
    filters = DataConversion.safe_get (object, "filters")
    DataConversion.safe_get (filters, "docstatus", 1)
    employee_separation = core_hr.get_list("Final_Statement", filters=filters, privilege=True, fetch_linked_tables=True)
    
    separation_report = []

    for employee in employee_separation:
        assets = DataConversion.safe_get (employee, 'asset', [])
        total_assets = len(assets)
        settled_assets = [asset for asset in assets if DataConversion.safe_e (DataConversion.safe_get (asset, 'assets_status'), 'Settled', str, True)]
        unsettled_assets = [asset for asset in assets if DataConversion.safe_e (DataConversion.safe_get (asset, 'assets_status'), 'Settled', str, True)]
        settled_value = sum(DataConversion.convert_to_float (DataConversion.safe_get (asset, 'assets_amount', 0)) for asset in settled_assets)
        unsettled_value = sum(DataConversion.convert_to_float (DataConversion.safe_get (asset, 'assets_amount', 0)) for asset in unsettled_assets)
        
        report_entry = {}
        DataConversion.safe_set (report_entry, "employee_name", DataConversion.safe_get (employee, 'employee_name').strip())
        DataConversion.safe_set (report_entry, "department", DataConversion.safe_get (employee, 'department'))
        DataConversion.safe_set (report_entry, "company", DataConversion.safe_get (employee, 'company'))
        DataConversion.safe_set (report_entry, "designation", DataConversion.safe_get (employee, 'designation'))
        DataConversion.safe_set (report_entry, "date_of_joining", DataConversion.safe_get (employee, 'date_of_joining'))
        DataConversion.safe_set (report_entry, "separation_date", DataConversion.safe_get (employee, 'transaction_date'))
        DataConversion.safe_set (report_entry, "separation_type", DataConversion.safe_get (employee, 'statement_for'))
        DataConversion.safe_set (report_entry, "status", DataConversion.safe_get (employee, 'status'))
        DataConversion.safe_set (report_entry, "settled_value", settled_value)
        DataConversion.safe_set (report_entry, "unsettled_value", unsettled_value)
        DataConversion.safe_set (report_entry, "total_assets", total_assets)
        DataConversion.safe_set (report_entry, "total_asset_value", sum ([settled_value, unsettled_value]))
        DataConversion.safe_set (report_entry, "settled_assets", len(settled_assets))
        DataConversion.safe_set (report_entry, "unsettled_assets", len(unsettled_assets))
        DataConversion.safe_set (report_entry, "total_payable", DataConversion.safe_get (employee, 'total_payable', 0))
        DataConversion.safe_set (report_entry, "total_payable", DataConversion.safe_get (employee, 'total_payable', 0))

        DataConversion.safe_list_append (separation_report, report_entry)

    return utils.respond(utils.ok, {"rows": separation_report})