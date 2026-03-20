from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.dict_to_object import Dict_To_Object
from controllers.tenant import Tenant_Controller

utils = Utils()
dates = Dates()
tc = Tenant_Controller()
pp = utils.pretty_print


class Calendar_Controller:
    def __init__(self) -> None:
        self.dbms = tc.get_admin_dbms()
    
    @classmethod
    def init_calendar_holidays (cls):
        cls.__init__ (cls)
        bj = tc.get_background_job_content("Calendar Holidays")
        if bj.get("status") == utils.ok:
            data = bj.get("data")
            if data.status.lower() == "idle":
                update = tc.update_background_job_status("Calendar Holidays", "Running")
                print(update)
                if update.get("status"):
                    tenants = tc.get_tenants ()
                    if tenants.get("status") == utils.ok:
                        for tenant in tenants.get("data"):
                            con = tc.connect_tenant (tenant_url=tenant.tenant_url)
                            # pp (con)
                            if con.status == utils.ok:
                                if dates.is_first_day_of_year ():
                                    this_years_holiday_list = dates._init_holidays ("ZM")
                                    obj = Dict_To_Object ({
                                        "calendar_holidays": this_years_holiday_list
                                    })
                                    holidays = con.create ("Calender", body=obj, skip_user_evaluation=True, privilege=True)
                                    if holidays.status == utils.ok:
                                        pp (holidays.data)

# def accrual_holidays_for_the_year (self, dbms, object): 
#     if dates.is_first_day_of_year ():
#         this_years_holiday_list = dates._init_holidays ("ZM")
#         obj = Dict_To_Object ({
#             "calendar_holidays": this_years_holiday_list
#         })

#         holidays = dbms.create ("Calender", body=obj, user_id=object.user)
#         if holidays.status == utils.ok:
#             pp (holidays.data)
