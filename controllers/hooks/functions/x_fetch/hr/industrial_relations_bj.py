from controllers.utils import Utils
from controllers.utils.dates import Dates

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw

class Industrial_Relations:
    def __init__(self, dbms, object):
        self.dbms =dbms
        self.object =object
        self.today =dates.today()

    def emplyees_suspended_or_terminated(self):
        out_come_list =[]
        filters =["start_date", "effective_date"]
        for flter in filters:
            fetch_out_come =self.dbms.get_list("Case_Outcome", filters={flter: self.today}, fetch_linked_fields=True,)
            if fetch_out_come.status ==utils.ok:
                out_come_list +=fetch_out_come.data.rows
        if len(out_come_list) >0:
            for out_come in out_come_list:
                employee =out_come.linked_fields.subject
                employee_disciplinary =out_come.linked_fields.employee_disciplinary

                if out_come.suspension ==1 or out_come.suspension=="1" and out_come.start_date:
                    employee.status = "Suspended"
                    employee.is_separated = 2

                elif out_come.termination ==1 or out_come.termination =="1" and out_come.effective_date:
                    employee.status = "Terminated"
                    employee.is_separated = 1

                employee.last_day_of_work = out_come.start_date                
                employee_disciplinary.status ="Closed"


                try:
                    self.dbms.update ("Employee", employee, )
                    self.dbms.update ("Employee_Disciplinary", employee_disciplinary, )
                except Exception as e:
                    pp(e) 

        return utils.respond(utils.ok, {})

    @classmethod
    def employee_from_case_out_come(cls, dbms, object):
        instance =cls(dbms, object)
        return instance.emplyees_suspended_or_terminated()

