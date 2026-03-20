from controllers.utils import Utils
from controllers.utils.dates import Dates 
from controllers.core_functions.hr import Core_Hr

utils = Utils ()
pp = utils.pretty_print
dates = Dates ()
def get_holidays (dbms, object):
    core_hr = Core_Hr (dbms=dbms)
    holidays_list = core_hr.get_list("Calender", filters={"name": dates.get_split_date ()['year']}, fetch_linked_tables=True)
    return_data = {
        "status": utils.internal_server_error,
        "data": []
    }
    if holidays_list:
        holidays_arr = []
        for holiday in holidays_list[0].calendar_holidays:
            holidays_arr.append (holiday.date_formate)
        return_data = {
            "status": utils.ok,
            "data": holidays_arr, 
            "settings": core_hr.get_company_settings (dbms.system_settings.default_company)
        }
    # pp (return_data)
    return utils.respond (status=return_data['status'], response=return_data)