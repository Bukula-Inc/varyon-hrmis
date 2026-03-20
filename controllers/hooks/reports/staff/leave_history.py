from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from django.db.models import Sum

utils = Utils()
pp =utils.pretty_print
throw =utils.throw

def staff_leave_summary(dbms, object):
    core_hr = Core_Hr(dbms=dbms, obj=object,)
    try:
        leave_entries = core_hr.get_list("Leave_Entry")
        leave_types = core_hr.get_list("Leave_Type")
        employee = core_hr.get_list("Employee", filters={"user": dbms.current_user.name}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if employee:
            employee = employee[0]

    except Exception as e:
        return utils.respond(utils.error, {'message': str(e)})

    if not leave_types:
        return utils.respond(utils.ok, {'rows': []})

    leave_type_dict = {leave_type.name: leave_type for leave_type in leave_types if leave_types is not None}
    report_data = []

    for leave_entry in leave_entries:
        if leave_entry.employee ==  employee.name:
            leave_type = leave_type_dict.get(leave_entry.leave_type)
            if leave_type:
                report_data.append({
                    "employee": leave_entry.employee,
                    "name": leave_entry.name,
                    "leave_type": leave_entry.leave_type,
                    "from_date": leave_entry.from_date,
                    "to_date": leave_entry.to_date,
                    "total_days": leave_entry.remaining_leave_days + leave_entry.used_leave_days,
                    "used_leave_days": leave_entry.used_leave_days,
                    "remaining_leave_days": leave_entry.remaining_leave_days,
                    "is_paid": "Paid Leave" if leave_type.is_compensatory else "Unpaid Leave",
                    "converted_to_value_on": leave_type.convert_to_value_on
                })

    return utils.respond(utils.ok, {'rows': report_data})
