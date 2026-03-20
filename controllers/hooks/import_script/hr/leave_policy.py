from controllers.utils import Utils
import pandas as pd
import re
import json
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def format_and_parse_to_dataframe(data_str):
    formatted_str = data_str.replace("'", "\"")
    formatted_str = re.sub(r'(\w+):', r'"\1":', formatted_str)
    formatted_str = re.sub(r':\s*([a-zA-Z ]+)(,|\})', r': "\1"\2', formatted_str)
    try:
        data_list = json.loads(formatted_str)
        if not (isinstance(data_list, list) and all(isinstance(item, dict) for item in data_list)):
            raise ValueError("Input data is not in the expected format")
        df = pd.DataFrame(data_list)
        return df
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError("Invalid data format") from e


def import_script_for_leave_policy (dbms, doc, doctype):
    success = []
    failed = []
    extract_leave_policy = doc.file_content
    for leave_policy in extract_leave_policy:
        try:
            df = format_and_parse_to_dataframe(leave_policy.policy_details)
            leave_policy.policy_details = df.to_dict (orient="records")
        except ValueError as e:
            print(e)
            pass
        pp (leave_policy.policy_details)
        leave_policy.status = "Active"
        cre_del = dbms.create ("Leave_Policy", utils.from_dict_to_object (leave_policy), dbms.validation.user)
        pp(cre_del)
        if cre_del.status == utils.ok:
            leave_policy["error"] = " - "
            leave_policy["status"] = "Importation Successful"
            success.append(leave_policy)
        else:
            leave_policy["error"] = cre_del.error_message
            leave_policy["status"] = "Importation Failed"
            failed.append(leave_policy)
    
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