from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Memo:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.get_system_settings()
        if system_settings.get("status") == utils.ok:
            self.settings = Generate_Object(system_settings.get("data"))



    def memo(dbms,object):
        
        memo_list = []



        memo = dbms.get_list("Memo",filters={"status__in":["Active"]}, user=object.user)
        if memo.get("status") == utils.ok:
            if len (memo.get ("data").get ("rows")) > 0:
                for mem in memo.get ("data").get ("rows"):
                    memo_list.append({
                        "name": mem["name"],
                        "date": mem["date"] ,
                        "from": mem["sender"]
                        })
    
        
        
     
                    



        results = {
            # "checkins": checkin,
            "memo_list": memo_list,

        }
        

        return utils.respond(utils.ok, results)
   

    
    






