from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

# def create_non_existent_record(dbms, existing_records, record_name, model):
#     if record_name and  not existing_records.get(record_name.lower()):
#         new_record = dbms.create(model, {"name":record_name}, privilege=True)
#         if new_record.status == utils.ok:
#             existing_records[record_name.lower()] = new_record.data
# def import_script_for_employees(dbms, doc, doctype):
#     print (doctype)
#     success = []
#     failed  = []
#     updated = []
    # depts = utils.from_dict_to_object()
    # desig = utils.from_dict_to_object()
    # branches = utils.from_dict_to_object()
    # employement_types = utils.from_dict_to_object()
    # users = utils.from_dict_to_object()
    # employee_objects = utils.array_to_dict(doc.file_content, "name", True)
    # existing_employees = []
    # processed_ids = []
    # branch = dbms.get_list("Branch", privilege=True, as_dict=True, as_dict_key="name", lower_dict_keys=True)
    # emp_type = dbms.get_list("Employment_Type", privilege=True, as_dict=True, as_dict_key="name", lower_dict_keys=True)
    # designations = dbms.get_list("Designation", privilege=True, as_dict=True, as_dict_key="name", lower_dict_keys=True)
    # departments = dbms.get_list("Department", privilege=True, as_dict=True, as_dict_key="name", lower_dict_keys=True)
    # user_list = dbms.get_list("Lite_User", privilege=True, as_dict=True, as_dict_key="name")
    # if departments.status == utils.ok:
    #     depts = departments.data
    # if designations.status == utils.ok:
    #     desig = designations.data
    # if emp_type.status == utils.ok:
    #     employement_types = emp_type.data
    # if branch.status == utils.ok:
    #     branches = branch.data
    # if user_list.status == utils.ok:
    #     users = user_list.data
    # for idx, emp in enumerate(doc.file_content):
    #     normalized = utils.normalize_row_columns(emp)
    #     normalized.status = "Active"
    #     normalized.company =  dbms.system_settings.default_company
    #     create_non_existent_record(dbms,depts,normalized.department,"Department")
    #     create_non_existent_record(dbms,desig,normalized.designation,"Designation")
    #     create_non_existent_record(dbms,branches,normalized.branch,"Branch")
    #     create_non_existent_record(dbms,employement_types,normalized.employment_type,"Employment_Type")

    #     try:
    #         # if the supervisor do'es not exist
    #         if normalized.reports_to:
    #             if normalized.reports_to == normalized.name:
    #                 normalized.reports_to = ""
    #             elif (not existing_employees or normalized.reports_to.lower() not in existing_employees) and normalized.reports_to.lower() not in processed_ids:
    #                 supervisor = employee_objects.get(normalized.reports_to.lower())
    #                 if supervisor:
    #                     supevisor = utils.normalize_row_columns(supevisor)
                    
    #                     supevisor.status = "Active"
    #                     supevisor.company = dbms.system_settings.default_company
    #                     if supevisor.email and users.get(supevisor.email):
    #                         supevisor.user_id = supevisor.email
    #                     create = dbms.create("Employee", supevisor, privilege=True, owner_id=doc.owner_id)
    #                     if create.status == utils.ok:
    #                         existing_employees.append(supevisor.name.lower())
    #                         success.append(supevisor)
    #                     else:
    #                         supevisor.error_message = utils.get_text_from_html_string(create.error_message)
    #                         failed.append(supevisor)
    #                     updated.append(supevisor)
    #                     processed_ids.append(supevisor.name.lower())
    #                 pp("Supervisor not found in importation document!")
    #         if normalized.name.lower() not in existing_employees and  normalized.name.lower() not in processed_ids:
                
    #             if normalized.email and users.get(normalized.email):
    #                 normalized.user_id = normalized.email
    #             normalized.full_name = f"{normalized.get ('first_name')} {normalized.get ('middle_name', '')} {normalized.get ('last_name')}"
    #             create = dbms.create("Employee", normalized, privilege=True, owner_id=doc.owner_id)
    #             if create.status == utils.ok:
    #                 existing_employees.append(normalized.name.lower())
    #                 success.append(normalized)
    #             else:
    #                 normalized.error_message = utils.get_text_from_html_string(create.error_message)
    #                 failed.append(normalized)
    #             updated.append(normalized)
    #             processed_ids.append(normalized.name.lower())
    #     except Exception as e:
    #         pp(f"XXXXXXXXXXXXXXXXXXXXXXXXX {str(e)} XXXXXXXXXXXXXXXXXXXXXXXXX")

#     doc.successful_rows = success
#     doc.failed_rows = failed
#     doc.total_successful = len(success) or 0
#     doc.total_failed = len(failed) or 0
#     doc.file_content = updated
#     if doc.total_successful == updated:
#         doc.status = "Importation Successful"
#     elif doc.total_successful == 0:
#         doc.status = "Importation Failed"
#     elif doc.total_successful > 0:
#         doc.status = "Partially Imported"
#     update = dbms.update("Data_Importation", doc, privilege=True)

def format_number(number):
    return str(number).zfill(4)

def import_script_for_employees (dbms, doc, doctype):
    success = []
    failed  = []
    updated = []
    total = len (doc.file_content)
    for idx, emp in enumerate(doc.file_content):
        normalized = utils.normalize_row_columns(emp)

        name = DataConversion.safe_get (normalized, "name")
        # if name:
        DataConversion.safe_set (normalized, "name", format_number (name))
        normalized.status = "Active"
        normalized.company =  dbms.system_settings.default_company
        salutation = "Mr"
        if str (DataConversion.safe_get (normalized, 'gender')).lower () == "female":
            salutation = "Miss"
        DataConversion.safe_set (normalized, "full_name", f"{DataConversion.safe_get (normalized, 'first_name')} {DataConversion.safe_get (normalized, 'middle_name', '')} {DataConversion.safe_get (normalized, 'last_name')}")
        DataConversion.safe_set (normalized, "contact", f"0{DataConversion.safe_get (normalized, 'contact')}")

        create = dbms.create("Employee", utils.from_dict_to_object ({
            # "name": str(name),
            "first_name": DataConversion.safe_get (normalized, 'first_name'),
            "middle_name": DataConversion.safe_get (normalized, 'middle_name', ''),
            "last_name": DataConversion.safe_get (normalized, 'last_name'),
            "full_name": DataConversion.safe_get (normalized, f"{DataConversion.safe_get (normalized, 'first_name')} {DataConversion.safe_get (normalized, 'middle_name', '')} {DataConversion.safe_get (normalized, 'last_name')}"),
            "gender": DataConversion.safe_get (normalized, 'gender'),
            "d_o_b": DataConversion.safe_get (normalized, 'd_o_b'),
            "salutation": DataConversion.safe_get (normalized, 'salutation', salutation),
            "id_no": DataConversion.safe_get (normalized, 'id_no'),
            "nhima": DataConversion.safe_get (normalized, 'nhima'),
            "napsa": DataConversion.safe_get (normalized, 'napsa'),
            "tpin": DataConversion.safe_get (normalized, 'tpin'),
            "employment_type": DataConversion.safe_get (normalized, 'employment_type'),
            "company": DataConversion.safe_get (normalized, 'company'),
            "date_of_joining": DataConversion.safe_get (normalized, 'date_of_joining'),
            "last_day_of_work": DataConversion.safe_get (normalized, 'last_day_of_work'),
            "create_user": DataConversion.safe_get (normalized, 'create_user', 'Link User'),
            "user": DataConversion.safe_get (normalized, 'user'),
            "email": DataConversion.safe_get (normalized, 'email',),
            "contact": DataConversion.safe_get (normalized, 'contact'),
            "designation": DataConversion.safe_get (normalized, 'designation'),
            "branch": DataConversion.safe_get (normalized, 'branch'),
            "department": DataConversion.safe_get (normalized, 'department'),
            "inable_probation": DataConversion.safe_get (normalized, 'inable_probation', 0),
            "probation": DataConversion.safe_get (normalized, 'probation', ''),
            "employee_saved": DataConversion.safe_get (normalized, 'employee_saved', 1),
            "report_to": DataConversion.safe_get (normalized, 'report_to', ''),
            "leave_approver": DataConversion.safe_get (normalized, 'leave_approver', ''),
            "shift_approver": DataConversion.safe_get (normalized, 'shift_approver',''),
            "requisition": DataConversion.safe_get (normalized, 'requisition', ''),
            "basic_pay": DataConversion.safe_get (normalized, 'basic_pay', 0.00),
            "bank_name": DataConversion.safe_get (normalized, 'bank_name', ''),
            "sort_code": DataConversion.safe_get (normalized, 'sort_code', ''),
            "account_no": DataConversion.safe_get (normalized, 'account_no', ''),
            "employee_grade": DataConversion.safe_get (normalized, 'employee_grade'),
            "tax_band": DataConversion.safe_get (normalized, 'tax_band', 'PAYE'),
            "working_days": DataConversion.safe_get (normalized, 'working_days', 22),
            "working_hours": DataConversion.safe_get (normalized, 'working_hours', 8),
            "currency": DataConversion.safe_get (normalized, 'currency'),
            "is_separated": DataConversion.safe_get (normalized, 'is_separated', 0),
            "is_separated_emp_paid": DataConversion.safe_get (normalized, 'is_separated_emp_paid', "Unsettled"),
            "end_of_contract": DataConversion.safe_get (normalized, 'end_of_contract'),
            "contract": DataConversion.safe_get (normalized, 'contract', ''),
        }), privilege=True)

        if create.status == utils.ok:
            pp (create.data.name, create.data.full_name)
            success.append(normalized)
        else:
            normalized.error_message = utils.get_text_from_html_string(create.error_message)
            failed.append(normalized)
        # else:
        #     normalized.error_message = "Name is Not There"
        #     failed.append(normalized)

        updated.append(normalized)

    doc.successful_rows = success
    doc.failed_rows = failed
    doc.total_successful = len(success) or 0
    doc.total_failed = len(failed) or 0
    doc.file_content = updated
    if doc.total_successful == total:
        doc.status = "Importation Successful"
    elif doc.total_successful == 0:
        doc.status = "Importation Failed"
    elif doc.total_successful > 0:
        doc.status = "Partially Imported"
    update = dbms.update("Data_Importation", doc, privilege=True)
