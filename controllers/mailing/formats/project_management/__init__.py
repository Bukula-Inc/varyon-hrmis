from controllers.utils import Utils
from controllers.mailing import Mailing
from controllers.mailing.templates.default_template import Default_Template
utils = Utils()

class Project_Management_Formats:
    def __init__(self) -> None:
        pass
    def project_submit(dbms, object):
        object.doc_status = "Awaiting Commencement"
        mailing = Mailing(dbms=dbms)
        project_doc = object.body
        project_team = project_doc.project_team
        pm = project_doc.project_manager
        pm_email = project_doc.user
        project_name = project_doc.name
        email_content_pm = Default_Template.template(
            content=(
                f"<div style='font-family: Arial, Helvetica, sans-serif;'>"
                f"<p>Hello {pm},</p>"
                f"<p>You have a project assigned to you.</p>"
                f"<p><strong>Project Name:</strong> {project_name}</p>"
                f"<p><strong>Start Date:</strong> {project_doc.start_date}</p>"
                f"<p><strong>End Date:</strong> {project_doc.end_date}</p>"
                f"<p><strong>Description:</strong> {project_doc.description}</p>"
                f"</div>"
            ),
            subject="New Project Role"
        )
        mailing.send_mail(
            recipient=pm_email, 
            subject="New Project Role", 
            body=email_content_pm
        )        
        if project_team:
            team_members = dbms.get_list("Project_Team", fetch_linked_tables=True)
            if team_members.get("status") == utils.ok:
                team_data = team_members.get("data").get("rows")
                if team_data:
                    matching_team = None
                    for team_member in team_data:
                        team_name = team_member.get("name")
                        if team_name == project_team:
                            matching_team = team_member
                            break
                    if matching_team:
                        members = matching_team.get("team")
                        for user in members:
                            user_email = user.get("user")
                            email_content_team = Default_Template.template(
                                content=(
                                    f"<div style='font-family: Arial, Helvetica, sans-serif;'>"
                                    f"<p>Dear Team {project_team},</p>"
                                    f"<p>You have been assigned to project {project_name}.</p>"
                                    f"<p><strong>Start Date:</strong> {project_doc.start_date}</p>"
                                    f"<p><strong>End Date:</strong> {project_doc.end_date}</p>"
                                    f"<p><strong>Description:</strong> {project_doc.description}</p>"
                                    f"</div>"
                                ),
                                subject=f"Team {project_team} Project Task"
                            )
                            mailing.send_mail(
                                recipient=user_email, 
                                subject=f"Team {project_team} Project Task", 
                                body=email_content_team
                            )
        
    def on_submitting_task(dbms, object):
        object.doc_status = "Pending"
        mailing = Mailing(dbms=dbms)
        task_id = object.body
        data = dbms.get_doc("Project_Task", task_id.name)
        if data.get("status") != utils.ok:
            return data
        else:
            project_task = data.get("data")
            if project_task:
                task_team = project_task.get("team")
                assignee = project_task.get("individual")
                start_date = project_task.get("start_date")
                end_date = project_task.get("end_date")
                task_name = project_task.get("name")
                individual = project_task.get("individual")
                description = project_task.get("description")
                subject = f"{task_name}"                
                email_body = Default_Template.template(
                    content=f"""
                        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <p style="font-size: 16px; color: #555;">Hello <strong>{individual}</strong>,</p>
                            <p style="font-size: 15px; color: #555;">
                                You have been assigned a new task. Please review the details below:
                            </p>
                            <div style="border: 1px solid #ddd; padding: 15px; background-color: #f9f9f9; margin: 10px 0;">
                                <p style="font-size: 15px;">
                                    <strong>Task:</strong> <span style="color: #007BFF;">{subject}</span>
                                </p>
                                <p style="font-size: 15px;">
                                    <strong>Start Date:</strong> <span style="color: #007BFF;">{start_date}</span>
                                </p>
                                <p style="font-size: 15px;">
                                    <strong>End Date:</strong> <span style="color: #007BFF;">{end_date}</span>
                                </p>
                                <p style="font-size: 15px;">
                                    <strong>Description:</strong> {description}
                                </p>
                            </div>
                            <p style="font-size: 15px; color: #555;">
                                We appreciate your effort and commitment to ensuring this task is completed successfully.
                            </p>
                            <p style="font-size: 15px; color: #555;">
                                Best regards,<br>
                                <span style="font-weight: bold; color: #007BFF;">Your Project Management Team</span>
                            </p>
                        </div>
                    """,
                    subject=subject
                ) 
                
                mailing.send_mail(recipient=assignee, subject=subject, body=email_body)
                if not assignee:
                    task_team = project_task.get("team")
                    project_teams_data = dbms.get_list("Project_Team_Member", filters = {"parent": task_team}, fetch_linked_tables=True)
                    if project_teams_data:
                        data = project_teams_data.data.rows
                        for member in data:
                            first_name = member['first_name']
                            last_name = member['last_name']
                            user = member['user']
                            utils.pretty_print(user)
                            if user:
                                email_temp = Default_Template.template(
                                content=f"""
                                    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                                        <p style="font-size: 16px; color: #555;">Hello <strong>{last_name} {first_name}</strong>,</p>
                                        <p style="font-size: 15px; color: #555;">
                                            Your team, <strong style="color: #007BFF;">{task_team}</strong>, has been assigned to work on a new task. Here are the details:
                                        </p>
                                        <div style="border: 1px solid #ddd; padding: 15px; background-color: #f9f9f9; margin: 10px 0;">
                                            <p style="font-size: 15px;">
                                                <strong>Task:</strong> <span style="color: #007BFF;">{subject}</span>
                                            </p>
                                            <p style="font-size: 15px;">
                                                <strong>Start Date:</strong> <span style="color: #007BFF;">{start_date}</span>
                                            </p>
                                            <p style="font-size: 15px;">
                                                <strong>End Date:</strong> <span style="color: #007BFF;">{end_date}</span>
                                            </p>
                                            <p style="font-size: 15px;">
                                                <strong>Task Details:</strong> {description}
                                            </p>
                                        </div>
                                        <p style="font-size: 15px; color: #555;">
                                            Please coordinate with your team members to ensure the task is completed efficiently.
                                        </p>
                                        <p style="font-size: 15px; color: #555;">
                                            Thank you for your hard work and dedication.
                                        </p>
                                        <p style="font-size: 15px; color: #555;">
                                            Best regards,<br>
                                            <span style="font-weight: bold; color: #007BFF;">Your Project Management Team</span>
                                        </p>
                                    </div>
                                """,
                                subject=subject
                            )
                            mailing.send_mail(recipient=user, subject=subject, body=email_temp)
  
           