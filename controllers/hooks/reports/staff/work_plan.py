from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from controllers.core_functions.payroll import Core_Payroll



utils = Utils()

def staff_work_plan_report(dbms, object):
    hr = Core_Hr(dbms, object.user, object)
    work_plan_data_result = []
    work_plan_filters = object.filters.copy()  # Copy filters to avoid modifying the original object

    # Get the current employee information
    employee = hr.get_list("Employee", filters={"user": dbms.current_user.name}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
    if employee:
        employee = employee[0]
        work_plan_filters["employee"] = employee['name']  # Add the employee name to the filters

    # Fetch the staff work plan list based on the filters
    staff_work_plan_list = dbms.get_list(
        "Work_Plan",
        filters=work_plan_filters,
        fetch_linked_fields=True,
        fetch_linked_tables=True,
        privilege=True
    )

    if staff_work_plan_list.status == utils.ok:
        work_plan_data = staff_work_plan_list.data.rows
        for plan in work_plan_data:
            for task in plan.work_plan_task:
                # Create a dictionary for each task in the work plan
                work_plan_row = {
                    "name": plan.name,
                    "period": plan.period,
                    "title": task.title,
                    "out_come": task.out_come,
                    "expected_start_date": task.expected_start_date,
                    "expected_end_date": task.expected_end_date,
                    "progress_tracker": task.progress_tracker,
                }
                work_plan_data_result.append(work_plan_row)

    # Return the collected data
    return utils.respond(utils.ok, {'rows': work_plan_data_result})
