from datetime import datetime
from controllers.core_functions.hr import Core_Hr
from controllers.utils.dict_to_object import Dict_To_Object
from analytics.hr import HR_Analytics
from controllers.utils import Utils
from controllers.utils.dates import Dates
from datetime import datetime

utils = Utils()
throw = utils.throw
pp = utils.pretty_print
dates = Dates()

class Recruitment_Dashboard:
    def __init__(self,dbms,object):
        self.dbms = dbms
        self.object = object
        self.user = object.user
        self.vacancy:int = 0
        self.applications:int = 0
        self.interviews:int = 0
        self.offers:int = 0
        self.published:int = 0
        self.settings = {}
        self.core = Core_Hr(dbms, object.user, object)
        self.analytics =  HR_Analytics(dbms, object)
        

    @classmethod
    def dashboard (cls, dbms, object):
        cls.__init__(cls, dbms, object)
        cls.overalls (cls)
        
        return utils.respond (utils.ok, {
            "retention": cls.retention (cls),
            "overall_overview": {"new_application": cls.applications, "new_offers": cls.offers, "new_interview": cls.interviews, "new_vacancies": cls.vacancy,},
            "overview": { "published": cls.published, "candidates": 0, "selected_candidates": 0, "hired_candidates": 0,"offered_candidates": 0, },
            "job_application": cls.job_application(cls),
            "job_offers": cls.job_offers(cls),
            "get_interviews": cls.get_interviews(cls),
            "job_opening": cls.job_opening(cls),
            "total_applicants_selected": cls.selected_candidates(cls),
            "hired_candidates": cls.hired_candidates(cls),
        })
    def job_application(self):
        job_application = self.core.job_application()
        if job_application is not None:return {"total_job_application": len(job_application)}
        else:return {"total_job_application": 0}
        
    def job_offers(self): 
        job_offres = self.core.job_offer()
        if job_offres is not None:
            return {"total_job_offers": len(job_offres)}
        
    def get_interviews(self):
        interviews = self.core.interviews()
        if interviews:
            return {"new_interviews": len(interviews)}
    def selected_candidates(self):
        selected_emps = self.core.interviews_schedule()
        if selected_emps:
            return {
                "total_applicants_selected": len(selected_emps)
            }
    def hired_candidates(self):
        get_hired_candidates = self.core.appointment_letter()
        if get_hired_candidates:
            return {
                "hired_candidates": len(get_hired_candidates)
            }   
        
    def job_opening(self):
        job_opening_data = {}  
        total_vacancies_published = 0
        job_openings = self.core.job_opening() 
        if job_openings:
            for job_op in job_openings:
                department = job_op.get("department")  
                publish = job_op.get("publish")
                if publish == 1:
                    total_vacancies_published += 1
                if department:
                    job_opening_data[department] = job_opening_data.get(department, 0) + 1
        job_opening_data["total_vacancies_published"] = total_vacancies_published
        return job_opening_data


                    
    def overalls (self):
        job_applications = self.core.get_list ("Job_Application", filters={"status": "Submitted"})
        job_offers = self.core.get_list ("Job_Offer", filters={"status": "Submitted"})
        interviews = self.core.get_list ("Interview", filters={"status": "Submitted"})
        job_opening = self.core.get_list ("Job_Advertisement", filters={"status": "Submitted"})
        
        if job_applications:
            self.applications += len (job_applications)
        if job_offers:
            self.offers += len (job_offers)
        if interviews:
            self.interviews += len (interviews)
        if job_opening:
            for job_open_ing in job_opening:
                if job_open_ing.publish:
                    self.published += 1

    def retention (self):
        hires:int = 0
        a_year:int = 0
        two_year:int = 0
        three_year_plus:int = 0
        resigned:int = 0
        termination:int = 0
        retired:int = 0
        employee_on_full_time = 0
        on_probation=0
        employees = self.core.get_list ("Employee")
        vacancies_ = self.core.get_list ("Staffing_Plan", filters={"status": "Submitted"})

        if employees:
            for employee in employees:
                if employee.status == "Terminated":
                    termination += 1
                if employee.status == "Resigned":
                    resigned += 1
                if employee.status == "Retired":
                    retired += 1
                if employee.employment_type == "Full Time":
                    employee_on_full_time +=1
                if employee.inable_probation == 1:
                    on_probation +=1
                if dates.months_since (date=employee.date_of_joining, months=3):
                    hires += 1
                if dates.years_since (date=employee.date_of_joining, years=1):
                    a_year += 1
                if dates.years_since (date=employee.date_of_joining, years=2):
                    two_year += 1
                if dates.years_since (date=employee.date_of_joining, years=3):
                    three_year_plus += 1
        if vacancies_:
            for vacancy in vacancies_:
                if vacancy.staffing_details and len (vacancy.staffing_details):
                    for vanc_ in vacancy.staffing_details:
                        self.vacancy += vanc_.vacancies

        return {
            "total_employees": len(employees),
            "employee_on_full_time": employee_on_full_time,
            "on_probation": on_probation,
            "hires": hires,
            "a_year": a_year,
            "two_year": two_year,
            "three_year_plus": three_year_plus,
            "resigned": resigned,
            "termination": termination,
            "retired": retired,
            "vacancies": self.vacancy,
        }