from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()

class Advance:
    def __init__(self, dbms, obj):
        self.dbms = dbms
        self.obj = obj
        self.user = obj.user
        self.settings = {}
    
    @classmethod
    def advance_side_view(cls, dbms, obj):
        instance = cls(dbms, obj)
        return utils.respond(utils.ok, {
            "advance_info": instance.get_advance_info(),
            "advance_stats": instance.get_advance_stats(),
        })
    
    def get_advance_info(self):
        advance_info = []

        advance_info_list = self.dbms.get_list("Advance_Application", privilege=True)
        if advance_info_list.status == utils.ok and advance_info_list.data.rows:
            for advance in advance_info_list.data.rows:
                advance_info.append({
                    "applicant_name": advance["applicant"],
                    "advance_date": advance["created_on"],
                })
        return advance_info
   
    def get_advance_stats(self):
        advance_stats = {
            "pending": 0,
            "approved": 0,
            "rejected": 0
        }

        advance_applications = self.dbms.get_list("Advance_Application", privilege=True)
        if advance_applications.status == utils.ok and advance_applications.data.rows:
            for application in advance_applications.data.rows:
                if application['status'] == 'Pending Approval':
                    advance_stats["pending"] += 1
                elif application['status'] == 'Approved':
                    advance_stats["approved"] += 1
                elif application['status'] == 'Rejected':
                    advance_stats["rejected"] += 1

        return advance_stats

     



       
