from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def import_script_for_leave_type (dbms, doc, doctype):
    success = []
    failed = []
    extract_leave_type = doc.file_content
    for leave_type in extract_leave_type:
        leave_type.carry_forward = leave_type.carry_forward if leave_type.carry_forward else 0
        leave_type.is_compensatory = leave_type.is_compensatory if leave_type.is_compensatory else 0
        leave_type.allow_system_auto_accrual = leave_type.allow_system_auto_accrual if leave_type.allow_system_auto_accrual else 0
        if leave_type.allow_system_auto_accrual == 1:
            leave_type.accrual_frequency = leave_type.accrual_frequency if leave_type.accrual_frequency else "Dose Not Accrual"
        else:
            leave_type.accrual_frequency = None
        leave_type.total_days_allocated_per_month = leave_type.total_days_allocated_per_month if leave_type.total_days_allocated_per_month else 2
        leave_type.maximum_leave_allocated = leave_type.maximum_leave_allocated if leave_type.maximum_leave_allocated else 24
        leave_type.status = "Active"
        create_leave_types = dbms.create ("Leave_Type", utils.from_dict_to_object(leave_type), dbms.validation.user)

        if create_leave_types.status == utils.ok:
            leave_type["error"] = " - "
            leave_type["status"] = "Importation Successful"
            success.append(leave_type)
        else:
            leave_type["error"] = create_leave_types.error_message
            leave_type["status"] = "Importation Failed"
            failed.append(leave_type)
    
    doc.file_content = [*success, *failed]
    if failed and len(failed) > 0 and success and len(success) > 0:
        doc.status = "Partially Imported"
        doc.doc_status = "Partially Imported"
    elif len(failed) > 0 and len(success) == 0:
        doc.status = "Importation Failed"
        doc.doc_status = "Importation Failed"
    elif len(failed) == 0 and len(success) > 0:
        doc.status = "Importation Successful"
        doc.doc_status = "Importation Successful"
    update = dbms.update("Data_Importation", doc, dbms.current_user_id, update_submitted=True)
    # pp (update)
    return utils.respond(utils.ok, {"successful": success, "failed": failed})