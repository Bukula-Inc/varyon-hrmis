from controllers.utils import Utils
from controllers.utils.dates import Dates

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

# def validate_clearance_data_table(body)

def update_clearance_form(dbms, object):
    data =object.body.data

    fetch_clearance_form =dbms.get_doc("Clearance_Form", data.name)
    if fetch_clearance_form.status !=utils.ok:
        throw(f"no clearance of the name 'data.name' was found.")
    clearance_form =fetch_clearance_form.data
    clearance_form.clearance_data =data.clearance_data
    # clearance_items =clearance_form.clearance_data
    grouped =utils.group(clearance_form.clearance_data, "hand_in_status")

    hand_in_status =list(grouped.keys())

    if not "Pending Hand Over" in hand_in_status:
        clearance_form.status ="Cleared"
        clearance_form.cleared =1
        fetch_employee =dbms.get_list("Employee", clearance_form.employee)
        if fetch_employee.status ==utils.ok:
            emp_data =fetch_employee.data
            emp_data.status ="Separated"
            update_employee =dbms.update("Employee", emp_data)
            if update_employee.status !=utils.ok:
                throw(f"An error occurred while updating the separating employee {emp_data.full_name}: {update_employee}")

    update_clearance_form =dbms.update("Clearance_Form", clearance_form, update_submitted=True)
    if update_clearance_form.status !=utils.ok:
        throw("the update of the clearance form 'data.name', was unsuccessful due to: update_clearance_form")
    
    return utils.respond(update_clearance_form.status, update_clearance_form.data or update_clearance_form.error_message)