from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()

class Overtime:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
    
    @classmethod
    def overtime_side_view(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        return utils.respond(utils.ok,{
            "overtime_info": cls.get_overtime_info(cls),
            "overtime_stats": cls.get_overtime_stats(cls),
        })
    
    def get_overtime_info(self):
        overtime_info = []

        Overtime_info = self.dbms.get_list("Overtime", privilege=True)
        if Overtime_info.status == utils.ok:
            if len(Overtime_info.data.rows) > 0:
                for overtime in Overtime_info.data.rows:
                    overtime_info.append({
                        "applicant_name": overtime["applicant"],
                        "overtime_date": overtime["created_on"],
                    })
        return overtime_info
   
    def get_overtime_stats(self):
        overtime_stats = []
        pending = 0
        approved = 0
        rejected = 0

        overtime_applications = self.dbms.get_list("Overtime",privilege=True)
        if overtime_applications.status == utils.ok:
            if len(overtime_applications.data.rows) > 0:
                for application in overtime_applications.data.rows:
                    if application['status'] == 'Pending Approval':
                        pending += 1
                    elif application['status'] == 'Approved':
                         approved += 1
                    elif application['status'] == 'Rejected':
                        rejected += 1

            overtime_stats.append({
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
            })

        return overtime_stats
     



       
