from controllers.utils import Utils
from controllers.utils.object_generator import Generate_Object
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw



class Attendance:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.settings = {}
        self.past_7_days = dates.add_days(dates.today(), -7)
        system_settings = self.dbms.system_settings



    def employee_attendance(dbms,object):
        total_attendance=0
        total_employees_on_leave= 0
        absent_employees = 0
    
        


        attendance= dbms.get_list("Employee_Attendance", filters={"docstatus":1,"status__in":["Submitted"]})
        if attendance.status == utils.ok:
            total_attendance = len (attendance.data.rows)


        
        employees = dbms.get_list("Employee", filters={"status__in":["Active"]})
        if employees.status == utils.ok:
            total_employees = len (employees.data.rows)



        
        
        employees_on_leave = dbms.get_list("Employee", filters={"status__in":["On Leave"]})
        if employees_on_leave.status == utils.ok:
            total_employees_on_leave = len (employees_on_leave.data.rows)
    
        

        results = {
            "total_attendance": total_attendance,
            "total_employees_on_leave": total_employees_on_leave,
            "total_employees": total_employees,   

        }
        

        return utils.respond(utils.ok, results)
    

        
        






