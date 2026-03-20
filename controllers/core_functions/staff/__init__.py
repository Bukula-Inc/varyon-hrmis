from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll

utils = Utils ()
throw = utils.throw
pp = utils.pretty_print

class Core_Staff:
    def __init__(self, dbms, object=None):
        self.dbms = dbms
        self.object = object
        self.core_payroll = Core_Payroll (self.dbms)
        self.core_hr = Core_Hr (self.dbms)
        self.logged_in_staff = self.check_is_staff_attached ()

    @staticmethod
    def validate_user (dbms, obj, key):
        if f"{dbms.validation.module}".lower() == "staff":
            match key:
                case "applicant":
                    obj.complex_filters = dbms.query_builder(applicant__isnull = False) & dbms.query_builder(applicant__name = dbms.system_settings.employee_info.name)
                case "planner":
                    obj.complex_filters = dbms.query_builder(planner__isnull = False) & dbms.query_builder(planner__name = dbms.system_settings.employee_info.name)
                case "appraisee":
                    obj.complex_filters = dbms.query_builder(appraisee__isnull = False) & dbms.query_builder(appraisee__name = dbms.system_settings.employee_info.name)
                case "employee_id":
                    obj.complex_filters = dbms.query_builder(employee_id__isnull = False) & dbms.query_builder(employee_id__name = dbms.system_settings.employee_info.name)
                case "employee_no":
                    obj.complex_filters = dbms.query_builder(employee_no__isnull = False) & dbms.query_builder(employee_no__name = dbms.system_settings.employee_info.name)
                case "raised_by":
                    obj.complex_filters = dbms.query_builder(raised_by__isnull = False) & dbms.query_builder(raised_by__name = dbms.system_settings.employee_info.name)
                case "issue_raiser":
                    obj.complex_filters = dbms.query_builder(issue_raiser__isnull = False) & dbms.query_builder(issue_raiser__name = dbms.system_settings.employee_info.name)
                case "subject":
                    obj.complex_filters = dbms.query_builder(subject__isnull = False) & dbms.query_builder(subject__name = dbms.system_settings.employee_info.name)
                case "initiator":
                    obj.complex_filters = dbms.query_builder(initiator__isnull = False) & dbms.query_builder(initiator__name = dbms.system_settings.employee_info.name)
                case "user":
                    obj.complex_filters = dbms.query_builder(owner__isnull = False) & dbms.query_builder(owner__name = dbms.system_settings.employee_info.user)
                case _:
                    obj.complex_filters = dbms.query_builder(employee__isnull = False) & dbms.query_builder(employee__name = dbms.system_settings.employee_info.name)

    def check_is_staff_attached (self):
        path = DataConversion.safe_get (self.dbms.validation, "path")
        user_name = DataConversion.safe_get (self.dbms.current_user, "name")
        if not path:
            throw ("Can't Satisfy this request")
        if not user_name:
            throw ("Can't Satisfy this request")
        path = "app/staff"
        if "staff" in path.lower():
            employee = self.core_hr.get_doc("Employee", user_name, fetch_by_field="user", privilege=True)
            if not employee:
                return False
            employee = employee[0]
            return employee
    