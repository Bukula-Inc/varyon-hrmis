from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()

class Gratuity:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
    
    @classmethod
    def gratuity_side_view(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        return utils.respond(utils.ok,{
            "gratuity_info": cls.get_gratuity_info(cls),
            "gratuity_stats": cls.get_gratuity_stats(cls),
        })
    
    def get_gratuity_info(self):
        gratuity_info = []

        Gratuity_info = self.dbms.get_list("Graduate", privilege=True)
        if Gratuity_info.status == utils.ok:
            if len(Gratuity_info.data.rows) > 0:
                for gratuity in Gratuity_info.data.rows:
                    gratuity_info.append({
                        "employee_name": gratuity["employee"],
                        "date": gratuity["created_on"],
                    })
        return gratuity_info
   
    def get_gratuity_stats(self):
        gratuity_stats = []
        pending = 0
        approved = 0
        rejected = 0
        Submitted = 0

        gratuity_records = self.dbms.get_list("Graduate",privilege=True)
        if gratuity_records.status == utils.ok:
            if len(gratuity_records.data.rows) > 0:
                for records in gratuity_records.data.rows:
                    if records['status'] == 'Pending Approval':
                        pending += 1
                    elif records['status'] == 'Approved':
                         approved += 1
                    elif records['status'] == 'Rejected':
                        rejected += 1
                    elif records['status'] == 'Submitted':
                        Submitted +=1

            gratuity_stats.append({
                "pending": pending,
                "approved": approved,
                "rejected": rejected,
                "Submitted": Submitted,
            })

        return gratuity_stats
     



       
