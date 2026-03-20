from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr


utils = Utils()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw

class Leave_Controller:
    def __init__(self, dbms, object) -> None:
        self.dbms = dbms
        self.object = object
        self.core_hr = Core_Hr (dbms)

    @classmethod
    def employee_from_leave (cls, dbms, object):
        instance = cls (dbms, object)
        try:
            employees_lst = instance.core_hr.get_list ("Employee", filters={"status": "On Leave"}) 
            emp_lst_data = utils.array_to_dict (employees_lst, "name")
            leave_apps = instance.core_hr.get_list ("Leave_Application", filters={"to_date__e": dates.today ()})
            if leave_apps:
                for leave_app in leave_apps:
                    employee = DataConversion.safe_get(emp_lst_data, DataConversion.safe_get (leave_app, "employee"))
                    if employee:
                        DataConversion.safe_set (employee, "status", "Active")
                        r = dbms.update ("Employee", employee)
                        pp ("====================>>>>>>>>>>>>>>>>>>>> UPDATED <<<<<<<==========", r)
        except Exception as e:
            pp (f"ERROR: {e}")


    @classmethod
    def init_leave_accrual (cls, dbms, object):
        if dates.is_first_day_of_current_month ():
            instance = cls (dbms, object)
            try:
                hr_ss = instance.core_hr.get_company_settings (instance.core_hr.company)

                working_hours = hr_ss.get("working_hrs", None) if hr_ss else 8
                leave_policy = instance.core_hr.get_doc ("Leave_Policy", "Annual Leave")

                if leave_policy:
                    policy_for = DataConversion.safe_get (leave_policy, "policy_for")
                    policy_details = DataConversion.safe_get (leave_policy, "policy_details", [])
                    column = ''
                    match policy_for:
                        case "Employee Grade":
                            column = 'employee_grade'
                        case "Employment Type":
                            column = 'employment_type'
                        case "Designation":
                            column = 'designation'
                        case _:
                            column = 'employee_grade'

                    grouped_policy = utils.array_to_dict (policy_details, "policy_type")
                    employee_lst = instance.core_hr.get_list ("Employee", {"status__in": ["Active", "On Leave", "Suspended"]})
                    emp_df = utils.to_data_frame (employee_lst)
                    if column in emp_df.columns:
                        grouped_emp = (
                            emp_df.groupby(column)
                            .apply(lambda x: x.to_dict(orient="records"))
                            .to_dict()
                        )
                        for key, emp_docs in grouped_emp.items ():
                            policy_type = DataConversion.safe_get (grouped_policy, key)
                            total_days_allocated_per_month = DataConversion.convert_to_float (DataConversion.safe_get (policy_type, "total_days_allocated_per_month", 0))
                            for emp in emp_docs:
                                try:
                                    full_name = DataConversion.safe_get (emp, "full_name", f"{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}")
                                    new_entry = utils.from_dict_to_object ()
                                    DataConversion.safe_set (new_entry, "allocated_leave_days", total_days_allocated_per_month)
                                    DataConversion.safe_set (new_entry, "used_leave_days", 0)
                                    DataConversion.safe_set (new_entry, "total_days", total_days_allocated_per_month)
                                    DataConversion.safe_set (new_entry, "remaining_leave_days", total_days_allocated_per_month)
                                    DataConversion.safe_set (new_entry, "leave_type", "Annual Leave")
                                    DataConversion.safe_set (new_entry, "status", "Submitted")
                                    DataConversion.safe_set (new_entry, "is_active", 1)
                                    DataConversion.safe_set (new_entry, "employee", DataConversion.safe_get (emp, "name"))
                                    DataConversion.safe_set (new_entry, "employee_name", full_name)
                                    DataConversion.safe_set (new_entry, "from_date", dates.get_first_date_of_current_month ())
                                    DataConversion.safe_set (new_entry, "to_date", dates.get_first_date_of_current_month ())
                                    DataConversion.safe_set (new_entry, "entry_type", "Allocation")
                                    DataConversion.safe_set (new_entry, "reference", None)
                                    DataConversion.safe_set (new_entry, "leave_days_in_working_hours",
                                        instance.core_hr.to_and_from_hours_to_days (DataConversion.safe_get(new_entry, "remaining_leave_days", 0),
                                            working_hours=DataConversion.convert_to_float(working_hours))
                                    )
                                    r = dbms.create ("Leave_Entry", new_entry)
                                    pp (f"==================>>>>>>>>> {full_name} <<<<<<<<<<<==================", r)
                                except Exception as e:
                                    pp (f"ERROR: {e}")
                                    pass
            except Exception as e:
                pp (f"ERROR AT TOP LAYER: {e}")