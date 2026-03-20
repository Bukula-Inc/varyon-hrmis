from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates
from datetime import datetime
from controllers.core_functions.hr import Core_Hr

dates = Dates ()

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw

def get_overtime_details(dbms, object):
    overtime_info = []
    overtime_stats = {}

    overtime_applications = dbms.get_list("Overtime",filters= {'applicant':object.body.data.name },user=object.user)
    if overtime_applications.status == utils.ok:
        if len(overtime_applications.data.rows) > 0:
            for application in overtime_applications.data.rows:
                
                overtime_info.append({
                    "applicant_name": application["applicant"],
                    "overtime_date": application["created_on"],
                })
              

                status = application['status']
                if status in overtime_stats:
                    overtime_stats[status] += 1
                else:
                    overtime_stats[status] = 1

    overtime_stats = [{"status": status, "count": count} for status, count in overtime_stats.items()]

    return utils.respond (utils.ok,  {
        "overtime_info": overtime_info,
        "overtime_stats": overtime_stats
    })


def get_ot_claim (dbms, object):
    core_hr = Core_Hr (dbms)
    applicant = DataConversion.safe_get (object.body.data, "emp")
    if not applicant:
        throw ("Claimer Employee is <strong class='test-rose-600'>Missing</strong>")
    
    emp = core_hr.get_doc ("Employee", applicant)
    if not emp:
        throw ("Claimer Employee is <strong class='test-rose-600'>Missing</strong>")
    
    query = """
        SELECT * FROM staffs_to_work_this_overtime
        WHERE (cleared = 0 OR cleared IS NULL)
        AND employee_id = %s
    """

    ots = core_hr.fetch_data_from_sql (query, (DataConversion.safe_get (emp, 'id', 0),))
    if len (ots) <= 0:
        throw (f"Claimer <strong class='text-orange-600'>{applicant}</strong> has no <strong class='text-rose-600'>Overtime</strong>")
    return_list = []
    ot_sup = core_hr.get_doc ("Overtime_Configuration", core_hr.company)
    hrs = core_hr.get_company_settings ()
    wrk_days = DataConversion.convert_to_int (DataConversion.safe_get (hrs, "working_days", 22))
    wrk_hrs = DataConversion.convert_to_int (DataConversion.safe_get (hrs, "working_hrs", 8))
    rate_by_working_days = DataConversion.safe_get (ot_sup, "sunday_work", 1.5)
    rate_by_holidays = DataConversion.safe_get (ot_sup, "sunday_work", 2)

    sunday_work = DataConversion.safe_get (hrs, "sunday_work", 0)
    saturday_work = DataConversion.safe_get (hrs, "saturday_work", 0)

    for ot in ots:
        weekends = DataConversion.get_weekends (DataConversion.convert_datetime_to_string (DataConversion.safe_get (ot, "from_date"), "%Y-%m-%d"))
        rate = rate_by_working_days
        day = weekends[1]
        if weekends[0]:
            if DataConversion.safe_e (day, "saturday", str, True) and not saturday_work or (DataConversion.safe_e (day, "sunday", str, True) and not sunday_work):
                rate = rate_by_holidays

        DataConversion.safe_list_append (return_list, {
            "day": day,
            "date_of_work": DataConversion.safe_get (ot, "from_date"),
            "rate": rate,
            "emp_wrk_hrs": DataConversion.convert_to_int (DataConversion.safe_get (emp, "working_hours", wrk_hrs)),
            "emp_wrk_days": DataConversion.convert_to_int (DataConversion.safe_get (emp, "working_days", wrk_days)),
            "emp_basic": DataConversion.convert_to_float (DataConversion.safe_get (emp, "basic_pay", 0))
        })

    return utils.respond(utils.ok, return_list)