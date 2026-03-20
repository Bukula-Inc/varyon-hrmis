from controllers.utils import Utils
utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def validate_workflow(obj):
    body = obj.body
    if body.is_departmental_workflow:
        if not body.department:
            throw("Department is required for departmental workflows")
        if not body.record_type or ( "-" not in body.record_type or body.department not in body.record_type):
            body.name = f"{body.record_type} - {body.department}"
    else:
        body.department = ""
        body.name = body.record_type
    
    if not len(body.workflow_stage):
        throw("Add at least two workflow stages!")
    
    for idx, stage in enumerate(body.workflow_stage):
        # pp(idx, stage)
        stage.stage_no = idx + 1
        if not stage.stage:
            throw(f"Add stage to workflow stage row no {stage.stage_no}")
        if not stage.action:
            throw(f"Add action to workflow stage row no {stage.stage_no}")
        if not stage.next_stage:
            throw(f"Add next stage to workflow stage row no {stage.stage_no}")
        if body.is_role_based_workflow:
            if not stage.approver_group:
                throw(f"Add approver group to workflow stage row no {stage.stage_no}")
            else:
                stage.approver = ""
        else:
            if not stage.approver:
                throw(f"Add approver to workflow stage row no {stage.stage_no}")
            else:
                stage.approver_group = ""
def before_workflow_save(dbms, object):
    validate_workflow(object)

def before_workflow_update(dbms, object):
    validate_workflow(object)
    # pp(object)
    


def before_workflow_doc_fetch(dbms, obj):
    if dbms.validation.get("module") and dbms.validation.get("module").lower().strip() == "staff":
       if obj.is_list_fetch:
            docs = ["Draft", "Active", "Disabled"]
            unwanted_statuses = dbms.get_list("Doc_Status", privilege=True, filters={"initial_docstatus__in": [1,2,3,4]}, fields=["name"])
            if unwanted_statuses.status == utils.ok:
                docs.extend(utils.get_list_of_dicts_column_field(unwanted_statuses.data.rows, "name", return_unique_values=True))
            obj.complex_filters=~dbms.query_builder(current_stage__name__in=docs)
            
            user_role = dbms.current_user.main_role
            approver = dbms.get_list("Workflow_Approver_Role", filters={"approver":user_role}, privilege=True)
            if approver.status == utils.ok:
                approver_groups = utils.get_list_of_dicts_column_field(approver.data.rows, "parent", return_unique_values=True)
                workflow_stage = dbms.get_list("Workflow_Stage", privilege=True, filters={"approver_group__in": approver_groups})
                if workflow_stage.status == utils.ok:
                    stages = utils.get_list_of_dicts_column_field(workflow_stage.data.rows, "stage", return_unique_values=True)
                    obj.filters.update({"current_stage__in": stages})
            else:
                throw("You are not allowed to view records under approval procedures!")


