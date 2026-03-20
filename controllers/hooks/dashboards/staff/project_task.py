from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.object_generator import Generate_Object, Extract_Object
from controllers.core_functions.hr import Core_Hr
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Staff_Project_Task:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.hr = Core_Hr(dbms,object.user,object)
            
    @classmethod
    def staff_project_tasks(cls, dbms, object):
        cls.__init__(cls, dbms, object)
        status_counts = []
        tasks = []
        # count_dict = {}
        
        # project_tasks = cls.project_management.get_staff_tasks(filters={"individual":dbms.current_user.name})
        
        # for task in project_tasks:
        #     creation_date = task["creation_date"]
        #     task_name = task["task_name"]
        #     status = task["status"]
            
        #     tasks.append({"creation_date": creation_date, "task_name": task_name})
            
        #     if status in count_dict:
        #         count_dict[status] += 1
        #     else:
        #         count_dict[status] = 1
        
        # for status, count in count_dict.items():
        #     status_counts.append({"status": status, "count": count})
        
        res = {
            "tasks": tasks,
            "status_counts": status_counts
        }
        return utils.respond(utils.ok, res)


            
            
            
