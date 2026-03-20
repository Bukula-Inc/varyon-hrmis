from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import date

utils =Utils()
dates =Dates()
pp =utils.pretty_print
throw =utils.throw


class BJ_Reminders:
    def __init__(self, dbms, object):
        self.dbms =dbms
        self.object =object
        self.today =dates.today()

    def due_probation(self):
        employee_list =[]
        list_of_probastion =[]
        to_days_confirmed =[]
        probation_lengths =None
        fetch_employees_on_probation =self.dbms.get_list("Employee", filters={"inable_probation": 1})
        if fetch_employees_on_probation.status ==utils.ok:
            employee_list =fetch_employees_on_probation.data.rows
            emp_by_probation =utils.group(employee_list, "probation")
            list_of_probastion =[k for k in emp_by_probation]
        if len(list_of_probastion) >0:
            fetch_probations =self.dbms.get_list("Probation", filters={"name__in": list_of_probastion}, fields=["name","probation_length"], as_dict=True )
            if fetch_probations.status ==utils.ok:
                probation_lengths =fetch_probations.data
        if probation_lengths !=None:
            for emp in employee_list:
                pp(emp.name, dates.add_days(emp.date_of_joining.strftime("%Y-%m-%d"), (probation_lengths[emp.probation].probation_length*30)))
                if dates.add_days(emp.date_of_joining.strftime("%Y-%m-%d"), (probation_lengths[emp.probation].probation_length*30)) ==self.today:
                    to_days_confirmed.append(emp)

        if len(to_days_confirmed) >0:
            for emp in to_days_confirmed:
                "Send email..." 
                pp(to_days_confirmed)



    def work_aniversaries(self):
        today =dates.string_to_date(self.today)
        employees_with_anniversaries =[]
        fetch_employees =self.dbms.get_list("Employee", filters={"date_of_joining__lt": dates.add_days(dates.today(), ((11*30) + 28))})
        if fetch_employees.status ==utils.ok:
            employees_with_anniversaries.extend([
                emp for emp in fetch_employees.data.rows
                if (
                    (isinstance(emp.date_of_joining, date) and emp.date_of_joining.month == today.month and emp.date_of_joining.day == today.day) or
                    (isinstance(emp.date_of_joining, str) and dates.string_to_date(emp.date_of_joining).month == today.month and dates.string_to_date(emp.date_of_joining).day == today.day)
                )
            ])

        if len(employees_with_anniversaries) >0:
            for emp in employees_with_anniversaries:
                pp("Send email...")


    def birthdays(self):
        today =dates.string_to_date(self.today)
        employees_with_birthday =[]
        fetch_employees =self.dbms.get_list("Employee",)
        if fetch_employees.status ==utils.ok:
            employees_with_birthday.extend([
                emp for emp in fetch_employees.data.rows
                if (
                    (isinstance(emp.d_o_b, date) and emp.d_o_b.month == today.month and emp.d_o_b.day == today.day) or
                    (isinstance(emp.d_o_b, str) and dates.string_to_date(emp.d_o_b).month == today.month and dates.string_to_date(emp.date_of_joining).day == today.day)
                )
            ])

        if len(employees_with_birthday) >0:
            for emp in employees_with_birthday:
                pp("Send email...")

    def holiday(self):
        today =dates.string_to_date(self.today)
        todays_holidays =[]
        fetch_marching_dates =self.dbms.get_list("Calender_Holidays", filters={"date_formate": "2025-10-18"}, fetch_linked_fields=True)
        if fetch_marching_dates.status ==utils.ok:
            todays_holidays =utils.group(fetch_marching_dates.data.rows, "parent")
        if len(todays_holidays) >0:
            pp("Send Email....")


    def due_work_plan_tasks(self):
        today =dates.string_to_date(self.today)
        employees_with_todays_deadline =[]
        fetch_marching_dates =self.dbms.get_list("Performance_Agreement_KPIs", filters={"to_date": self.today}, fetch_linked_fields=True)
        if fetch_marching_dates.status ==utils.ok:
            employees_with_todays_deadline =utils.group(fetch_marching_dates.data.rows, "parent")
        if len(employees_with_todays_deadline) >0:
            pp("Send Email....")


    def due_leave_date(self):
        fetch_leave_days =self.dbms.get_list("Leave_Entry", filters={"to_date": self.today})
        if fetch_leave_days.status ==utils.ok:
            for due_leave in fetch_leave_days.data.rows:
                pp("Send Email.....")

    def due_job_opening(self):
        fetch_due_job_opening =self.dbms.get_list("Job_Offer", filters={"offer_due_date": self.today})
        if fetch_due_job_opening.status ==utils.ok:
            for due_leave in fetch_due_job_opening.data.rows:
                pp("Send Email.....")

    def interview(self):
        fetch_interview =self.dbms.get_list("Interview", filters={"schedule": self.today})
        if fetch_interview.status ==utils.ok:
            for due_leave in fetch_interview.data.rows:
                pp("Send Email.....")

    def contract_expiry(self):
        fetch_hr_contract =self.dbms.get_list("Hr_Contract", filters={"end_date": self.today})
        if fetch_hr_contract.status ==utils.ok:
            for due_leave in fetch_hr_contract.data.rows:
                pp("Send Email.....")

    # def exit_interview(self):
    #     fetch_interview =self.dbms.get_list("Exit_Interview", filters={"schedule": self.today})
    #     if fetch_interview.status ==utils.ok:
    #         for due_leave in fetch_interview.data.rows:
    #             pp("Send Email.....")

    def training_program(self):
        fetch_training_program =self.dbms.get_list("Training_Program", filters={"end_date": self.today})
        if fetch_training_program.status ==utils.ok:
            for due_leave in fetch_training_program.data.rows:
                pp("Send Email.....")


    def traning_plan(self):
        pass

    @classmethod
    def  init_reminders(cls, dbms, object):
        instance =cls(dbms, object)

        instance.due_probation()
        instance.work_aniversaries()
        instance.birthdays()
        instance.holiday()
        instance.due_work_plan_tasks()
        # instance.due_leave_date()
        # instance.due_job_opening()
        # instance.interview()
        # instance.contract_expiry()
        # instance.exit_interview()
        instance.training_program()
        # instance.traning_plan()

        return utils.respond(utils.ok, utils.from_dict_to_object({"condition": "Done"}))