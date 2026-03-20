from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import date

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

def probation_sv(dbms, object):

    returned_data =[]

    fetch_employees =dbms.get_list("Employee", filters={"inable_probation": 1})
    if fetch_employees.status ==utils.ok:
        employees =fetch_employees.data.rows
        for employee in employees:
            returned_data.append(utils.from_dict_to_object({
                "name": employee.full_name,
                "designation": employee.designation,
                "department": employee.department,
                "start_date": employee.date_of_joining,
                "probation_end_date": dates.add_days(employee.date_of_joining.strftime("%Y-%m-%d") or employee.date_of_joining, (30*3)),
            }))

    return utils.respond(utils.ok, returned_data)