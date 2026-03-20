from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.object_generator import Generate_Object, Extract_Object
from controllers.core_functions.hr import Core_Hr
from datetime import datetime, timedelta
utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Staff_Overtime_Statistics:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_30_days = dates.add_days(dates.today(), -30)
        self.hr = Core_Hr(dbms,object.user,object)
        self.employee = None
        system_settings =  self.dbms.system_settings
        if system_settings:
            self.settings = utils.from_dict_to_object(system_settings)
            self.defaults =  self.settings.accounting_defaults
            comp = getattr(self.defaults, self.settings.default_company)
            cd = self.dbms.get_doc("Company",comp.name,fetch_linked_fields=True,privilege=True)
            cd.status == utils.ok or throw("Failed to fetch company info!")
            self.company = utils.from_dict_to_object(cd.data)
        

    @classmethod
    
    def staff_overtime_statistics(cls, dbms, object):
        cls.__init__(cls, dbms, object)
        employee = cls.hr.get_list("Employee", filters={"user":dbms.current_user.name}, privilege=True, fetch_linked_fields=True, fetch_linked_tables=True)
        if employee:
                employee = employee[0]
        
        result = {
            "total_applications": 0,
            "total_overtime_hours": 0.0,
            "total_earnings": 0.0,
            "overtime_details": []
        }
        
        time_format = "%H:%M" 
        overtime = dbms.get_list("Overtime", filters={"applicant": employee.id, "docstatus": 1}, privilege=True)
        
        if overtime.status == utils.ok:
            overtime_data = overtime.data.rows
            result["total_applications"] = len(overtime_data)
            
            for data in overtime_data:
                status = data.status
                name = data.name
                start_time = data.start_time
                end_time = data.end_time
                purpose = data.purpose
                total_earning = utils.fixed_decimals(data.total_earning, 2)
                
                start_time_t = datetime.strptime(start_time, time_format).time()
                end_time_t = datetime.strptime(end_time, time_format).time()
                
                start_datetime = datetime.combine(datetime.today(), start_time_t)
                end_datetime = datetime.combine(datetime.today(), end_time_t)
                
                if end_datetime < start_datetime:
                    end_datetime += timedelta(days=1)
                
                overtime_hours = (end_datetime - start_datetime).total_seconds() / 3600.0
                
                result["total_overtime_hours"] +=  utils.fixed_decimals(overtime_hours,2)
                result["total_earnings"] += utils.fixed_decimals(total_earning, 2)
                
                result["overtime_details"].append({
                    "status": status,
                    "name": name,
                    "start_time": start_time,
                    "end_time": end_time,
                    "purpose": purpose,
                    "total_earning": total_earning,
                    "overtime_hours": utils.fixed_decimals(overtime_hours,2)
                })
        return utils.respond(utils.ok, result)
