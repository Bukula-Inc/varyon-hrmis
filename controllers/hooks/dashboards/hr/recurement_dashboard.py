import numpy as np
from analytics.hr.recruitment import HR_Recruitment_Analytics
from controllers.utils import Utils

utils = Utils()
pp = utils.pretty_print


def convert_int64(data):
    if isinstance(data, dict):
        return {k: convert_int64(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_int64(i) for i in data]
    elif isinstance(data, np.int64):  # or check for np.integer to cover all numpy integers
        return int(data)
    else:
        return data

def get_recruitment_staff_planning(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)

    try:
        staff_planning = dbms.get_list("Staffing_Plan", privilege=True)
        if staff_planning.status == utils.ok:
            staff_planning = staff_planning.data.rows
            metrics = analytics.staff_planning(staff_planning)
            return utils.respond(utils.ok, {'staff_planning': staff_planning, 'metrics': metrics.data})
    
    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})
    
def get_recruitment_staffing(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)

    try:
        staffing_list = dbms.get_list("Staffing", privilege=True)
        if staffing_list.status == utils.ok:
            staffing_list = staffing_list.data.rows
            metrics = analytics.staffing(staffing_list)
            return utils.respond(utils.ok, {'staffing_list': staffing_list, 'metrics': metrics.data})
    
    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})
    
def get_recruitment_job_openings(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)
    
    try:
        job_openins = dbms.get_list("Job_Advertisement", privilege=True)
        if job_openins.status == utils.ok:
            job_openins = job_openins.data.rows
            metrics = analytics.job_openings(job_openins)
            return utils.respond(utils.ok, {'job_openings': job_openins, 'metrics': metrics.data})

    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})
    
def get_recruitment_job_applications(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)
    
    try:
        job_apps = dbms.get_list("Job_Application", privilege=True)
        if job_apps.status == utils.ok:
            job_apps = job_apps.data.rows
            metrics = analytics.job_applications(job_apps)
            return utils.respond(utils.ok, {'job_applications': job_apps, 'metrics': metrics.data})

    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})
    
def get_recruitment_interviews(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)
    
    try:
        interviews= dbms.get_list("Interview", privilege=True)
        if interviews.status == utils.ok:
            interviews = interviews.data.rows
            metrics = analytics.interviews(interviews)
            return utils.respond(utils.ok, {'interviews': interviews, 'metrics': metrics.data})

    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})
    
def get_recruitment_interview_types(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)
    
    try:
        interview_types = dbms.get_list("Interview_Type", privilege=True)
        if interview_types.status == utils.ok:
            interview_types = interview_types.data.rows
            metrics = analytics.interview_type(interview_types)
            return utils.respond(utils.ok, {'interview_types': interview_types, 'metrics': metrics.data})

    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})
    
def get_recruitment_interview_schedules(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)
    
    try:
        interview_schedules = dbms.get_list("Interview_Schedule", privilege=True)
        if interview_schedules.status == utils.ok:
            interview_schedules = interview_schedules.data.rows
            metrics = analytics.interview_schedule(interview_schedules)
            return utils.respond(utils.ok, {'interview_schedules': interview_schedules, 'metrics': metrics.data})

    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})
    
def get_recruitment_job_offers(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)
    
    try:
        job_offers = dbms.get_list("Job_Offer", privilege=True)
        if job_offers.status == utils.ok:
            job_offers = job_offers.data.rows
            metrics = analytics.job_offers(job_offers)
            return utils.respond(utils.ok, {'job_offers': job_offers, 'metrics': metrics.data})

    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})
    
def get_recruitment_appointment_letters(dbms, object):
    analytics =  HR_Recruitment_Analytics(dbms, object)
    
    try:
        appointment_letters = dbms.get_list("Appointment_Letter", privilege=True)
        if appointment_letters.status == utils.ok:
            appointment_letters = appointment_letters.data.rows
            metrics = analytics.appointment_letters(appointment_letters)
            return utils.respond(utils.ok, {'appointment_letters': appointment_letters, 'metrics': metrics.data})

    except Exception as e:
        return utils.respond(status=500, response={"error": str(e)})

def main_recrement_dashboard (dbms, object):
    analytics = HR_Recruitment_Analytics(dbms, object)

    employees = dbms.get_list("Employee", privilege=True)
    if employees and employees.status == utils.ok:
        employees = employees.data.rows
        employees_by_type = analytics.get_employee_metrics(employees)
        employees_by_type = employees_by_type.data if employees_by_type.status == utils.ok else {}
    else:
        employees_by_type = {}

    job_applications = get_recruitment_job_applications(dbms, object)
    if job_applications and job_applications.status == utils.ok:
        job_applications = job_applications.data.metrics
    else:
        job_applications = {}

    interview_types = get_recruitment_interview_types(dbms, object)
    if interview_types and interview_types.status == utils.ok:
        interview_types = interview_types.data.metrics
    else:
        interview_types = {}

    interview_schedules = get_recruitment_interview_schedules(dbms, object)
    if interview_schedules and interview_schedules.status == utils.ok:
        interview_schedules = interview_schedules.data.metrics
    else:
        interview_schedules = {}

    job_offers = get_recruitment_job_offers(dbms, object)
    if job_offers and job_offers.status == utils.ok:
        job_offers = job_offers.data.metrics
    else:
        job_offers = {}

    appointment_letters = get_recruitment_appointment_letters(dbms, object)
    if appointment_letters and appointment_letters.status == utils.ok:
        appointment_letters = appointment_letters.data.metrics
    else:
        appointment_letters = {}

    data = {
        'employees_by_type': employees_by_type,
        'job_applications': job_applications,
        'interview_types': interview_types,
        'interview_schedules': interview_schedules,
        'job_offers': job_offers,
        'appointment_letters': appointment_letters
    }
    pp(data)

    return utils.respond (status=utils.ok, response=data)