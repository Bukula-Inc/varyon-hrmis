from controllers.core_functions.hr import Core_Hr
from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates


utils = Utils()
dates = Dates()

class Staff_Imprest:
    def __init__(self, dbms, object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
    
    @classmethod
    def staff_imprest_side_view(cls, dbms, object):
        cls.__init__(cls,dbms,object)
        return utils.respond(utils.ok,{
            "imprest_info": cls.get_imprest_info(cls,user= dbms.current_user.name ),
            "imprest_stats": cls.get_imprest_stats(cls,user= dbms.current_user.name ),
        })
    
    def get_imprest_info(self, user):
        imprest_list = []
        # imprest_info = self.dbms.get_list("Imprest",filters={'initiator':self.object.body.data.name}, user=self.user)
        imprest_info = self.dbms.get_list("Imprest",filters={'initiator':user}, privilege=True)
        if imprest_info.status == utils.ok:
            if len(imprest_info.data.rows) > 0:
                for imprest in imprest_info.data.rows:
                    imprest_list.append({
                        "name": imprest["name"],
                        "date": imprest["created_on"],
                    })
        return imprest_list
   
    def get_imprest_stats(self, user):
        imprest_stats = []
        status_counts = {}
        pending = 0
        approved = 0
        rejected = 0

        imprest_applications = self.dbms.get_list("Imprest",filters={'initiator':user}, privilege=True)

        if imprest_applications.status == utils.ok:
            if len(imprest_applications.data.rows) > 0:
                count_dict = {}  
                for application in imprest_applications.data.rows:
                    status = application['status']
                    if status in count_dict:
                        count_dict[status] += 1
                    else:
                        count_dict[status] = 1

                for status, count in count_dict.items():
                    status_counts = {"status": status, "count": count}

            imprest_stats.append(status_counts)
            return imprest_stats

