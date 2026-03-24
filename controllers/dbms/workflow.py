from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.mailing import Mailing
from controllers.mailing.templates.default_template import Default_Template
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Workflow:
    def __init__(self,dbms):
        self.dbms = dbms
        self.usr = self.dbms.current_user
        self.workflow_template = utils.from_dict_to_object({ 
            "has_workflow": False,
            "status": "", 
            "current_stage": "",
            "allow_edit": True,
            "available_actions": []
        })

    def __send_notification (self, body, wf_stage, approvers:list):
        mailing = Mailing (dbms=self.dbms)
        doctype = utils.replace_character(body.doctype, '_',' ')
        sender = f'{self.usr.first_name or ""} {self.usr.middle_name or ""} {self.usr.last_name or ""}'

        em_body = utils.from_dict_to_object({
            "owner_name": f"{body.linked_fields.owner.first_name or ''}",
            "document_type": doctype,
            "document_name": body.name,
            "sender_email": self.usr.email,
            "from_stage":wf_stage.stage,
            "to_stage":wf_stage.next_stage,
            "stage_no":wf_stage.stage_no,
            "total_stages":wf_stage.total_stages or 10,
            "current_status": wf_stage.next_stage,
            "submission_date": dates.date_to_numeric(dates.today()),
            "comment": body.workflow_comment,
            "doc_url": self.generate_doc_url(body.doctype,body.name),
            "sender_names": sender,
            "submitted_by": sender,
            "sender_department": self.usr.department,
            "company": self.dbms.system_settings.linked_fields.default_company,
            "is_final":body.is_final
        })
        if approvers:
            for approver in utils.get_object_values(approvers):
                em_body.approver_names = approver.full_name
                em_body.approver_first_name = approver.first_name
                em_body.approver_last_name = approver.last_name
                em_body.approver_other_name = approver.other_name
                if approver.email != self.usr.email:
                    mailing.send_mail(recipient=approver.email, subject=f"Workflow Action Required: {doctype}", body=Default_Template.workflow(em_body))
        if body.owner:
            mailing.send_mail(recipient=body.owner, subject=f"Document Approval Progress: {doctype}", body=Default_Template.workflow_doc_owner(em_body))
        return True
        
    def get_workflow(self, model, workflow_name=None):
        wf = None
        extra_filters = {"disabled":0}
        if self.dbms.current_user:
            if workflow_name:
                wf = self.dbms.get_doc("Workflow", workflow_name, privilege=True, skip_workflows=True, extra_filters=extra_filters)
            else:
                user_group = self.dbms.current_user.user_group
                dept = self.dbms.current_user.department
                if user_group:
                    wf = self.dbms.get_doc("Workflow", f"{model} - {user_group} - (USER GROUP)", privilege=True, skip_workflows=True, extra_filters=extra_filters)
                elif dept:
                    wf = self.dbms.get_doc("Workflow", f"{model} - {dept}", privilege=True, skip_workflows=True, extra_filters=extra_filters)
                if not wf or (wf and wf.status != utils.ok):
                    wf = self.dbms.get_doc("Workflow", model, privilege=True, skip_workflows=True, extra_filters=extra_filters)
        else:
            wf = self.dbms.get_doc("Workflow", model, privilege=True, skip_workflows=True, extra_filters=extra_filters)
        return wf
    
    def get_workflow_doc(self, name):
        return self.dbms.get_doc("Workflow_Doc", name, privilege=True, skip_workflows=True)
    
    def get_workflow_approver_group(self, group_names):
        return self.dbms.get_list("Workflow_Approver_Role", filters={"parent__in": group_names}, privilege=True, fields=["parent", "approver"])
    

    def get_workflow_approver_group_users(self, roles=[], departments=[]):
        filters=utils.from_dict_to_object({"main_role__in":roles})
        if departments:
            filters.department__in = departments
            users = self.dbms.get_list("Lite_User", filters=filters, privilege=True)
            if users.status == utils.ok:
                return users
        if filters.department__in:
            del filters["department__in"]
        return self.dbms.get_list("Lite_User", filters=filters, privilege=True)
    
    def get_current_user_approver_stage(self, user_role, workflow_stages=[]):
        wfar = self.dbms.get_list("Workflow_Approver_Role", filters={"approver": user_role}, privilege=True, fields=["parent", "approver"], order_by=["id"])
        utils.evaluate_response(wfar, f"Failed to fetch workflow approver group for role {user_role}: {wfar.error_message}!")
        wfars = utils.array_to_dict(wfar.data.rows, "parent")
        for stg in utils.sort(workflow_stages, sort_by="stage_no"):
            if stg.approver_group in wfars:
                wfar.data.rows = [wfars[stg.approver_group]]
                break
        return wfar
    
    def update_workflow_doc(self, budy):
        pp("TO BE WORKED ON WHEN RECORD NAME CHANGES")
        
        
    def generate_doc_url(self,model, doc_name):
        # model_module = utils.get_model_module(model)
        model_module = utils.get_model_module("Workflow_Doc")
        if model_module.status != utils.ok:
            return False
        md = model_module.data
        entry = "app" if md.wrapper_module == "client_app" else "app" #to accommodate future entry points
        return f"""https://{self.dbms.host}/{entry}/staff/approval?module=staff&loc=approval&type=info&document=approval&doc={doc_name}"""
        return f"""https://{self.dbms.host}/{entry}/{md.module}/{md.app}?module={md.module}&loc={md.app}&type=info&document={md.content_type}&doc={doc_name}"""


    # initialize workflow
    def init_workflow(self, model, object, model_config=None):
        current_stage = {}
        has_workflow = False
        body = object.body
        status = object.doc_status
        workflow = self.get_workflow(model)
        if workflow.status == utils.ok:
            wf = utils.from_dict_to_object(workflow.data)
            if wf.disabled == 0:
                has_workflow = True
                stages = wf.workflow_stage
                sorted_list = utils.sort(stages, True, sort_by="stage_no")
                current_stage = sorted_list[0]
                doc = utils.from_dict_to_object({ 
                    "name": body.name, 
                    "current_stage_no": current_stage.stage_no,
                    "for_doctype": model, 
                    "current_stage": current_stage.stage,
                    "status": "Active",
                    "workflow_used": wf.name
                })
                wf_doc = self.dbms.create("Workflow_Doc", doc, privilege=True, skip_workflows=True)
                if wf_doc.status == utils.ok:
                    status = current_stage.stage
                    body.status = status
                    object.doc_status = status
                else:
                    throw(f"Failed to initialize workflow: {wf_doc.error_message}!")
        return utils.respond(utils.ok,{ 
            "has_workflow": has_workflow,
            "status": status, 
            "current_stage": current_stage
        })
    

    def fetch_doc_workflow(self, model, doc_name, doc_owner=None):
        current_stage = {}
        has_workflow = False
        status = ""
        allow_edit = True
        
        workflow_doc = self.get_workflow_doc(doc_name)
        if workflow_doc.status != utils.ok:
            return utils.respond(utils.ok, self.workflow_template)
        doc = workflow_doc.data
        workflow = self.get_workflow(model, doc.workflow_used)
        user_role = None
        available_actions = []
        if workflow.status != utils.ok or (workflow.status == utils.ok and workflow.data.disabled == 1):
            # return utils.respond(utils.ok, self.workflow_template)
            pass
        
        wf = workflow.data
        is_role_based_workflow = wf.is_role_based_workflow
        has_workflow=True if wf.disabled == 0 else False
            
        stages = utils.sort(wf.workflow_stage)
        grouped = utils.group(stages,"stage")
        usr = self.dbms.current_user

        if not usr or (usr and not usr.main_role):
            return utils.respond(utils.internal_server_error, "User/user role not found for the current logged in user!")
        
        user_role = usr.main_role
        status = doc.current_stage
        current_stage = grouped.get(status)
        if current_stage:
            if is_role_based_workflow:
                allow_edit = False
                approver_group = self.get_workflow_approver_group(utils.get_list_of_dicts_column_field(current_stage, "approver_group"))
                if approver_group.status != utils.ok:
                    throw(f"Failed to fetch workflow approver group:{approver_group.error_message}!")
                app_group = utils.group(approver_group.data.rows,"parent")
                #to skip other roles if document owner is the next approver in the workflow and document is still in draft state
                group_approver_roles = utils.get_list_of_dicts_column_field(approver_group.data.rows,"approver")
                if user_role not in group_approver_roles and (doc.current_stage == "Draft" and doc_owner == usr.name):
                    
                    approver_group = self.get_current_user_approver_stage(user_role, stages)
                    if approver_group.status != utils.ok:
                        throw(f"Failed to fetch workflow approver group:{approver_group.error_message}!")
                    approver_groups = approver_group.data.rows
                    app_group = utils.group(approver_groups,"parent")
                    role_group = approver_groups[0].get("parent","")
                    
                    for stg in utils.sort(stages,sort_by="stage_no"):
                        if stg.approver_group == role_group:
                            current_stage = grouped.get(stg.stage)
                            if doc.current_stage != current_stage[0].stage:
                                doc.current_stage = current_stage[0].stage
                                doc.current_stage_no = current_stage[0].stage_no
                                update = self.dbms.update("Workflow_Doc", doc, privilege=True)
                                if update.status != utils.ok:
                                    throw(f"Failed to update workflow document:{update.error_message}!")
                            break
                for stg in current_stage:
                    if stg.approver_group in app_group:
                        for grp in app_group.get(stg.approver_group):
                            if (grp.approver == user_role)  or (doc.current_stage == "Draft" and doc_owner == usr.name):
                                av_action = {
                                    "action": stg.action,
                                    "stage_no": stg.stage_no,
                                    "icon": stg.linked_fields.action.icon,
                                    "color": stg.linked_fields.action.color,
                                }
                                if wf.is_departmental_workflow:
                                    if(wf.department and wf.department == usr.department or not wf.is_departmental_workflow):
                                        if doc_owner == usr.name or wf.allow_non_owner_initialization:
                                            allow_edit = True
                                            available_actions.append(av_action)
                                        else:
                                            if doc_owner != usr.name:
                                                allow_edit = True
                                                available_actions.append(av_action)
                                    else:
                                        if wf.allow_none_departmental_approvers:
                                            allow_edit = True
                                            available_actions.append(av_action)
                                else:
                                    allow_edit = True
                                    available_actions.append(av_action)
                    elif doc.current_stage == "Draft" and doc_owner == usr.name and stg.stage == "Draft":
                        av_action = {
                            "action": stg.action,
                            "stage_no": stg.stage_no,
                            "icon": stg.linked_fields.action.icon,
                            "color": stg.linked_fields.action.color,
                        }
                        allow_edit = True
                        available_actions.append(av_action)
            else:
                # if usr.name == current_stage.approver or (current_stage.stage_no == 1 and doc_owner == usr.name):
                allow_edit = False
                current_stages = grouped.get(status)
                for stage in current_stages:
                    if stage.stage == status and stage.approver == usr.name or (current_stage.stage_no == 1 and doc_owner == usr.name):
                        allow_edit = True
                        if wf.is_departmental_workflow and wf.department and wf.department == usr.department or not wf.department:
                            available_actions.append({
                                "action": stage.action,
                                "stage_no": stage.stage_no,
                                "icon": stage.linked_fields.action.icon,
                                "color": stage.linked_fields.action.color,
                            })

        self.workflow_template.available_actions = available_actions
        self.workflow_template.status = status
        self.workflow_template.allow_edit = allow_edit if doc.linked_fields.current_stage.initial_docstatus not in [1,2,3,4] else False
        self.workflow_template.has_workflow = has_workflow
        self.workflow_template.comments = doc.comments
        return utils.respond(utils.ok, self.workflow_template)
            
    


    def update_workflow(self, params):
        
        headers = params.headers
        body = params.body
        doc_list = utils.string_to_json(getattr(headers, "Doc", []))
        model = getattr(headers, "Model", None)
        action = getattr(headers, "Action", None)
        incoming_workflow_stage = int(getattr(headers, "Stage-No", 0) or 0)
        if not model:
            throw("Model missing in headers")
        if not incoming_workflow_stage:
            throw("Stage No missing in headers")
        if not action:
            throw("Workflow Action missing in headers")
        if doc_list.status != utils.ok:
            throw("Doc missing in headers")
        comment = ""
        if params.body and utils.get_text_from_html_string(params.body.comment):
            comment = params.body.comment
        for doc in doc_list.data:
            doc_data = self.dbms.get_doc(model, doc, fetch_by_field="id", privilege=True, fetch_linked_tables=True)
            if doc_data.status != utils.ok:
                throw(f"Failed to fetch document:{doc_data.error_message}")
            body = doc_data.data
            workflow_doc = self.get_workflow_doc(body.name)
            if workflow_doc.status != utils.ok:
                throw(f"Failed to fetch workflow document:{workflow_doc.error_message}!")
            wd = workflow_doc.data
            
            workflow = self.get_workflow(model, wd.workflow_used)
            if workflow.status != utils.ok:
                throw(f"An error occurred while updating document workflow: {workflow.error_message}!")
                # return workflow
            wf = workflow.data
            stages = wf.workflow_stage
            grouped = utils.group(stages,"stage")
            is_role_based_workflow = wf.is_role_based_workflow
            for stage in stages:
                if stage.stage == wd.current_stage and stage.action == action:
                    initial_docstatus = None
                    update = None
                    allow_next_stage = False
                    approvers = {}

                    body.status = stage.next_stage
                    initial_docstatus = stage.linked_fields.next_stage.initial_docstatus
                    if comment:
                        comment_obj = {
                            "action": stage.action,
                            "from_status":stage.stage,
                            "to_status": stage.next_stage,
                            "stage_no":stage.stage_no,
                            "comment":comment,
                            "comment_owner": self.usr.email,
                            "comment_owner_first_name": self.usr.first_name,
                            "comment_owner_last_name": self.usr.middle_name,
                            "comment_owner_middle_name": self.usr.last_name,
                            "comment_owner_role": self.usr.main_role,
                            "comment_date": dates.today(),
                        }
                        if wd.comments:
                            wd.comments.append(comment_obj)
                        else:
                            wd.comments = [comment_obj]

                    if is_role_based_workflow:   
                        if grouped.get(stage.next_stage):
                            approver_group = self.get_workflow_approver_group(utils.get_list_of_dicts_column_field(grouped.get(stage.next_stage),"approver_group"))
                            if approver_group.status != utils.ok:
                                throw(f"Failed to fetch Workflow Approver Group: {approver_group.error_message}")
                            if approver_group.status != utils.ok:
                                throw(f"Workflow stage has no approvers!")
                            approver_roles = utils.get_list_of_dicts_column_field(approver_group.data.rows, "approver")
                            if not approver_roles:
                                throw(f"Workflow stage has no approver roles!")
                            
                            approver_users = self.get_workflow_approver_group_users(approver_roles, [body.department] if body.department else [])
                            if approver_users.status != utils.ok:
                                if approver_users.status == utils.no_content:
                                    throw(f"There are no users with the role <strong class='text-orange-500'>{approver_roles}</strong> in the system! <br> Please ensure approver roles have users existing in the system!")
                                else:
                                    throw(f"An error occurred while notifying workflow stage users: {approver_users.error_message}!")
                            users = approver_users.data.rows
                            group_content = grouped.get(stage.next_stage)
                            
                            if group_content:
                                for stage_content in group_content:
                                    if stage.next_stage == stage_content.stage:
                                        for user in users:
                                            if not approvers.get(user.email) and self.usr.name != user.email:
                                                approvers[user.email] = utils.from_dict_to_object({
                                                    "full_name":f"{user.first_name} {user.middle_name or ''} {user.last_name or ''}",
                                                    "first_name": user.first_name,
                                                    "last_name": user.last_name,
                                                    "other_name": user.middle_name,
                                                    "email":user.email
                                                })
                                        break

                        allow_next_stage = True
                    else:
                        group_content = grouped.get(stage.next_stage)
                        if group_content:
                            for stage_content in group_content:
                                if stage.next_stage == stage_content.stage and not approvers.get(stage_content.linked_fields.approver.email):
                                    approver = stage_content.linked_fields.approver
                                    approvers[approver.email] = utils.from_dict_to_object({
                                        "full_name":f"{approver.first_name} {approver.middle_name or ''} {approver.last_name or ''}",
                                        "first_name": approver.first_name,
                                        "last_name": approver.last_name,
                                        "other_name": approver.middle_name,
                                        "email":approver.email
                                    })

                        allow_next_stage = True
                    # finally update the content as all checks have passed
                    body.workflow_comment = comment
                    if allow_next_stage:
                        update = None
                        self.dbms.validation.workflow_doc_status = body.status
                        if initial_docstatus in [0,2,3]:
                            body.docstatus = initial_docstatus
                            update = self.dbms.update(model, body,  update_submitted=True)
                        if initial_docstatus == 1:
                            update = self.dbms.submit_doc(model, [body.id])
                        self.dbms.validation.workflow_doc_status = None
                        if update.status == utils.ok:
                            wd.current_stage = stage.next_stage
                            wd.current_stage_no = incoming_workflow_stage
                            wd_update = self.dbms.update("Workflow_Doc", wd, update_submitted=True)
                            if wd_update.status == utils.ok:
                                body.is_final = initial_docstatus in [1,2,3,4]
                                notify = self.__send_notification(body, stage, approvers)
                        return update
                    break