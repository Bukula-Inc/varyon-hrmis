from controllers.utils import Utils

utils =Utils()
pp =utils.pretty_print
throw =utils.throw

def fetch_case_out_come_id(dbms, object):

    id =None
    disciplinary =None
    return_status =None
    if object.body.data:
        disciplinary =object.body.data
    else:
        return_status =utils.no_content
        return utils.respond(utils.no_content, ({"error_message": "No relation to the any case out comes was provided !"}))
    
    case_out_come =dbms.get_list("Case_Outcome", filters={"employee_disciplinary": disciplinary})
    if case_out_come.status ==utils.ok:
        id =case_out_come.data.rows[0].id
        return utils.respond(utils.ok, utils.from_dict_to_object({"rows":id}))
    else:
        return_status =case_out_come.status
        return utils.respond(return_status, ({"error_message": case_out_come.error_message}))
