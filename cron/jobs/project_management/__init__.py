from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import datetime, date
from controllers.mailing.templates.default_template import Default_Template

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

class Overdue_Task_controller:
    def __init__(self, dbms=None, tc=None) -> None:
        self.dbms = dbms
        self.tc = tc
    
    def overdue_task(self):
        try:
            tasks = self.dbms.get_list("Project_Task", filters={"status": "Pending"}, privilege=True)            
            if tasks and hasattr(tasks, 'data') and hasattr(tasks.data, 'rows'):
                tasks_data = tasks.data.rows
                for task in tasks_data:
                    end_date = task.get('end_date')
                    project = task.get('project')
                    if isinstance(end_date, str):
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                    if end_date < date.today():
                        task['status'] = "Overdue"
                        update = self.dbms.update("Project_Task",task,skip_hooks=True,privilege=True,skip_audit_trail=True) 
                        if update.status == utils.ok:
                            pm = self.dbms.get_list("Project", filters = {"name",  project}, privilege=True)
                return utils.respond(utils.ok,{"message": "Overdue tasks updated successfully"} )
            else:
                return utils.respond(utils.no_content, {  "error_message": "No tasks found"})
        except Exception as e:
            pp(f"Exception occurred: {str(e)}")    
    @classmethod
    def process_project_overdue_tasks(cls, dbms, tc=None):
        instance = cls(dbms, tc)        
        return instance.overdue_task()
