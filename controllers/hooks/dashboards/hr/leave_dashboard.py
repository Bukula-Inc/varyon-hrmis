import pandas as pd
from controllers.core_functions.hr import Core_Hr
from controllers.utils.data_conversions import DataConversion
from analytics.hr import HR_Analytics
from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import date, timedelta

utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Leave_Dashboard:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.core = Core_Hr(dbms, object.user, object)
        self.hr_s = self.core.get_company_settings (self.core.company)
        self.analytics = HR_Analytics(dbms, object)
        self.fetch_leave_entries =self.core.get_leave_entries(fetch_linked_fields=True)
        self.past_7_days = dates.add_days(dates.today(), -7, return_date_object=True)
        self.emps = self.core.get_list ("Employee", filters={"status__in": ["On Leave", "Active", "Suspended"]})
        self.employee = utils.array_to_dict (self.emps, "name")
        self.fetch_leave_application = self.core.get_list ("Leave_Application", order_by='-id')


    @classmethod
    def dashboard(cls, dbms, object):
        leave_dashboard = cls(dbms, object)
        return utils.respond(utils.ok, {
            "leave_calendar": leave_dashboard.calender (),
            "leave_department": leave_dashboard.used_and_unused(),
            "leave_utilization": leave_dashboard.leave_utilization (),
            "leave_values": leave_dashboard.leave_summary (),
            "recent_applications": leave_dashboard.recent_applications (),
        })

    def leave_utilization (self):
        try:
            utilization_list = utils.from_dict_to_object({})
            if self.fetch_leave_application:
                df = utils.to_data_frame (self.fetch_leave_application)
                grouped_by_applications = (
                    df.dropna(subset=['department'])
                    .groupby(["department", "leave_type"])
                    .agg({"total_days": "sum"})
                    .reset_index()
                    .to_dict(orient='records')
                )
                if grouped_by_applications:
                    label = []
                    val = set ()
                    value = []
                    for la in grouped_by_applications:
                        if la.get ("leave_type", None) not in label:
                            label.append (la.get ("leave_type", None))
                        if la.get ("department", None) not in val:
                            val.add(la.get ("department", None))
                            value.append ({
                                "name": la.get ("department", None),
                                "data": [la.get ("total_days", 0.00)]
                            })
                        else:
                            for vl in value:
                                if val.get ("name", None) == la.get ("department"):
                                    val.get ("data", []).append (la.get ("total_days", 0.00))
                            data = value.get (la.get ("department")).get ("data")
                            data.append (la.get ("total_days", 0.00))
                    utilization_list.labels = label
                    utilization_list.vals = value
            return utilization_list
        except Exception as err:
            pp ("Error in Leave Utilizations", err)

    def recent_applications (self):
        try:
            applications = []
            if self.fetch_leave_application:
                applications = self.fetch_leave_application[-18:]
            return applications
        except Exception as err:
            pp ("Error in Recent Application", err)
            pass

    def used_and_unused (self):
        try:
            used = utils.from_dict_to_object ({"label": [], "value": []})
            df = utils.to_data_frame (self.fetch_leave_application)
            grouped_by_applications = (
                df.dropna(subset=['department'])
                .groupby("department")
                .agg({
                    "total_days": "sum",
                })
                .reset_index()
                .to_dict(orient='records')
            )
            pp (grouped_by_applications)
            if grouped_by_applications:
                for application in grouped_by_applications:
                    used.label.append (application.get ("department", None))
                    used.value.append (application.get ("total_days", None))
            return used
        except Exception as err:
            pp ("Error in Used and Unused Leave", err)
            pass

    def leave_summary (self):
        try:
            leave_entries = self.core.get_leave_entries ()
            unused_val = 0.00
            used_val = 0.00
            if leave_entries:
                df = utils.to_data_frame (leave_entries)
                total_remaining = float (df['remaining_leave_days'].sum())
                total_used = float (df['used_leave_days'].sum())
                days = {
                    "unused": total_remaining - total_used,
                    "used": total_used
                }
                unused_vs_used = utils.from_dict_to_object ({"label": ["Used Days", "Unused Days"], "value": [total_used or 0, total_remaining or 0]})
                grouped_by_emp = df.groupby("employee").agg({
                    "remaining_leave_days": "sum",
                    "used_leave_days": "sum"
                }).reset_index().to_dict(orient='records')
                if grouped_by_emp:
                    for employee in grouped_by_emp:
                        pp (employee)
                        emp = self.employee.get (DataConversion.safe_get(employee, 'employee', None))
                        if emp:
                            leave_val = self.core.emp_get_leave_value (DataConversion.safe_get (emp, "id"), DataConversion.safe_get (emp, 'working_days', DataConversion.safe_get (self.hr_s, "working_days", 22)))
                            unused_val += DataConversion.safe_get (leave_val, "remaining_days_val")
                            used_val += DataConversion.safe_get (leave_val, "used_days_val")

                return {
                    "days_stats": {
                        "days": days,
                        "values": {
                            "used": used_val,
                            "unused": unused_val
                        },
                        "used_vs_unused": unused_vs_used,
                    }
                }
        except Exception as err:
            pp ("Error in Leave Summary", err)
            pass
    def calender (self):
        try:
            obj_applications = utils.from_dict_to_object ({})
            applications = self.core.get_list ("Leave_Application",)
            if applications:
                days = set ()
                for app in applications:
                    emp = self.employee[app.employee]
                    if app.from_date.day not in days:
                        days.add (app.from_date.day)
                        obj_applications[app.from_date.day] = [
                            {
                                "employee": app.employee,
                                "leave_type": app.leave_type,
                                "total_days": app.total_days,
                                "employee_name": app.employee_name or f"{emp.first_name} {emp.middle_name or ''} {emp.last_name}",
                                "department": app.department,
                                "to_date": app.to_date,
                                "from_date": app.from_date,
                                "to_time": app.to_time,
                                "from_time": app.to_date,
                                "time_duration_formatted": app.time_duration_formatted,
                                "image": emp.img or None,
                                "leave_mode": app.leave_mode,
                                "on": app.from_date.day
                            }
                        ]
                    else:
                        obj_applications[app.from_date.day].append ({
                            "employee": app.employee,
                            "leave_type": app.leave_type,
                            "total_days": app.total_days,
                            "employee_name": app.employee_name or f"{emp.first_name} {emp.middle_name or ''} {emp.last_name}",
                            "department": app.department,
                            "to_date": app.to_date,
                            "from_date": app.from_date,
                            "to_time": app.to_time,
                            "from_time": app.to_date,
                            "time_duration_formatted": app.time_duration_formatted,
                            "image": emp.img or None,
                            "leave_mode": app.leave_mode,
                            "on": app.from_date.day
                        })
            return obj_applications
        except Exception as err:
            pp ("Error in Calendar", err)
            pass

    def get_month_start_end(self, some_date=None):
        if some_date is None:
            some_date = date.today()
        first_day = some_date.replace(day=1)
        if some_date.month == 12:
            next_month = some_date.replace(year=some_date.year + 1, month=1, day=1)
        else:
            next_month = some_date.replace(month=some_date.month + 1, day=1)

        last_day = next_month - timedelta(days=1)

        return first_day, last_day