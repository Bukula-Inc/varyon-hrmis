from controllers.utils import Utils
from controllers.core_functions.hr import Core_Hr
from datetime import datetime
from controllers.utils.data_conversions import DataConversion
import numpy as np

utils =Utils()
pp =utils.pretty_print


def employee_leave_balance_report(dbms, object):
    core_hr = Core_Hr (dbms)
    return_data =[]
    emps = {}
    leave_filters = utils.from_dict_to_object ({"leave_type": "Annual Leave",})
    emp_filters = utils.from_dict_to_object({})
    emp_filters.status__in =["On Leave", "Active", "Suspended"]
    if object.filters:
        if object.filters.department:
            DataConversion.safe_set (emp_filters, "department", object.filters.department)
        if object.filters.designation:
            DataConversion.safe_set (emp_filters, "designation", object.filters.designation)
        if object.filters.leave_type:
            DataConversion.safe_set (leave_filters, "leave_type", object.filters.leave_type)
        if object.filters.employee:
            DataConversion.safe_set (emp_filters, "name", object.filters.employee)

    employees = core_hr.get_list ("Employee", emp_filters)

    if employees:
        emps = utils.array_to_dict (employees, "name")

    leave_entries = core_hr.emp_leave_annual_days (all=True, return_by_employee=True, filters=leave_filters)
    if leave_entries:
        for entry in leave_entries:
            emp = DataConversion.safe_get (emps, DataConversion.safe_get (entry, "employee", None), None)
            if emp:
                used = DataConversion.safe_get (entry, "used_leave_days")
                avail = DataConversion.convert_to_float (DataConversion.safe_get (entry, "remaining_leave_days") - used)
                DataConversion.safe_list_append (return_data, {
                    "employee": DataConversion.safe_get (emp, "name", DataConversion.safe_get (entry, "employee")),
                    "employee_name": DataConversion.safe_get (emp, "full_name", f"""{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}"""),
                    "leave_type": DataConversion.safe_get (entry, 'leave_type', "Annual Leave"),
                    "used_leave": used,
                    "remaining_leave": avail,
                })
        return utils.respond(utils.ok, {"rows":return_data})

def hr_self_appraisal_report(dbms, object):
    return_data =[]
    filters =object.filters or utils.from_dict_to_object({})
    filters.docstatus =1

    fetch_self_appraisal =dbms.get_list("Appraise_Your_Self", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)
    if fetch_self_appraisal.status ==utils.ok:
        for appraisal in fetch_self_appraisal.data.rows:
            more_data =appraisal.linked_fields

            return_data.append({
                "appraisal_date": appraisal.created_on,
                "period_covered_for_the_assessment": appraisal.period_covered_for_the_assessment,
                "salary_grade": appraisal.salary_grade,
                "appraisee_name": appraisal.employee_id,
                "department": appraisal.department,
                "purpose_of_the_assessment": appraisal.purpose_of_the_assessment,
                "behavioral_imperatives_score": appraisal.behavioral_imperatives_score,
                "performance_objective_score": appraisal.performance_objective_score,
                "performance_kpi_qty": len(appraisal.performance_kpi) or 0,
                "overall_score": appraisal.overall_score,
            })

    return utils.respond(utils.ok, {"rows": return_data})

def employee_on_leave_report(dbms, object):
    core_hr = Core_Hr (dbms)
    return_data =[]
    from_d = None
    to_d = None
    emps = {}
    leave_filters = utils.from_dict_to_object ({})
    emp_filters = utils.from_dict_to_object({})
    emp_filters.status ="On Leave"
    if object.filters:
        if object.filters.department:
            DataConversion.safe_set (emp_filters, "department", object.filters.department)
        if object.filters.designation:
            DataConversion.safe_set (emp_filters, "designation", object.filters.designation)
        if object.filters.leave_type:
            DataConversion.safe_set (leave_filters, "leave_type", object.filters.leave_type)
        if object.filters.from_date:
            DataConversion.safe_set (leave_filters, "from_date", object.filters.from_date)
            from_d = datetime.strptime(DataConversion.safe_get(leave_filters, "from_date"), "%Y-%m-%d")
        if object.filters.to_date:
            DataConversion.safe_set (leave_filters, "to_date", object.filters.from_date)
            to_d = datetime.strptime(DataConversion.safe_get(leave_filters, "to_date"), "%Y-%m-%d")

        if from_d and to_d:
            if from_d > to_d:
                DataConversion.safe_set (leave_filters, "from_date__in", [to_d, from_d])
            else:
                DataConversion.safe_set (leave_filters, "from_date__in", [from_d, to_d])

    employees = core_hr.get_list ("Employee", emp_filters)
    if employees:
        emps = utils.array_to_dict (employees, "name")
    leave_applications = core_hr.get_list ("Leave_Application", leave_filters)
    if leave_applications:
        df = utils.to_data_frame (leave_applications)
        recent_by_employee = (
            df.dropna(subset=['employee', 'from_date'])
            .sort_values("from_date", ascending=False)
            .drop_duplicates(subset=["employee"])
            .reset_index(drop=True)
            .to_dict(orient='records')
        )
        for la in recent_by_employee:
            emp = DataConversion.safe_get (emps, DataConversion.safe_get (la, "employee", ''), None)
            if emp:
                employee_names =  DataConversion.safe_get (la, "employee_name", DataConversion.safe_get (emp, "full_name",
                    f"""{DataConversion.safe_get (emp, 'first_name')}
                        {DataConversion.safe_get (emp, 'middle_name', '')}
                        {DataConversion.safe_get (emp, 'last_name')}"""
                ))
                DataConversion.safe_list_append (return_data, {
                    "name":  DataConversion.safe_get (la, "employee", DataConversion.safe_get (emp, "name")),
                    "employee_name": employee_names,
                    "leave_type": DataConversion.safe_get(la, "leave_type", "Annual Leave"),
                    "designation": DataConversion.safe_get(emp, "designation"),
                    "department": DataConversion.safe_get (la, "department", DataConversion.safe_get (emp, "department", '')),
                    "from_date": DataConversion.safe_get (la, "from_date", DataConversion.safe_get (la, "from_time", '')),
                    "to_date": DataConversion.safe_get (la, "to_date", DataConversion.safe_get (la, "to_time", '')),
                    "total_days": DataConversion.safe_get (la, "time_duration_formatted", "0 Day")
                })
                # return_data.append ()

    return utils.respond(utils.ok, {"rows":return_data})

def recruitment_analytics_report(dbms, object):
    return_data =[]
    filters =object.filters or utils.from_dict_to_object({})
    filters.docstatus =1
    report_data =[]

    fetch_Job_advertisement = dbms.get_list("Job_Advertisement", filters=filters, fields=["name"])
    if fetch_Job_advertisement.status !=utils.ok:
        throw("Failed to fetch job advertisement data.")
    for Job_advertisement in fetch_Job_advertisement.data.rows:

        report_row =utils.from_dict_to_object({
            "job_advertisement": Job_advertisement.name,
            "job_application" : None,
            "shortlisted" : None,
            "interviewed" : None,
            "offered" : None
        })

        fetch_applications =dbms.get_list("Job_Application", filters={"docstatus": 1, "job_advertisement": Job_advertisement.name}, fields=["name"])
        if fetch_applications.status ==utils.ok:
            report_row.job_application =len(fetch_applications.data.rows)
        fetch_shortlisted =dbms.get_list("Applicant_Short_List", filters={"docstatus": 1, "job_advertisement": Job_advertisement.name}, fields=["name"])
        if fetch_shortlisted.status ==utils.ok:
            report_row.shortlisted =len(fetch_shortlisted.data.rows)
        fetch_interview =dbms.get_list("Interview", filters={"docstatus": 1, "job_advertisement": Job_advertisement.name}, fields=["name"])
        if fetch_interview.status ==utils.ok:
            report_row.interviewed =len(fetch_interview.data.rows)
        fetch_job_offer =dbms.get_list("Job_Offer", filters={"docstatus": 1, "job_advertisement": Job_advertisement.name}, fields=["name"])
        if fetch_job_offer.status ==utils.ok:
            report_row.offered =len(fetch_job_offer.data.rows)
        
        report_data.append(report_row)

    return utils.respond(utils.ok, {"rows":report_data})

def leave_summary_report(dbms, object):
    core_hr = Core_Hr (dbms)
    return_data =[]
    emps = {}
    leave_filters = utils.from_dict_to_object ({"leave_type": "Annual Leave"})
    emp_filters = utils.from_dict_to_object({})
    emp_filters.status__in =["On Leave", "Active", "Suspended"]
    if object.filters:
        if object.filters.department:
            DataConversion.safe_set (emp_filters, "department", object.filters.department)
        if object.filters.designation:
            DataConversion.safe_set (emp_filters, "designation", object.filters.designation)
        if object.filters.leave_type:
            DataConversion.safe_set (leave_filters, "leave_type", object.filters.leave_type)
        if object.filters.employee:
            DataConversion.safe_set (emp_filters, "name", object.filters.employee)

    employees = core_hr.get_list ("Employee", emp_filters)
    if employees:
        emps = utils.array_to_dict (employees, "name")

    totals = utils.from_dict_to_object ({
        "employee": "TOTAL",
        "used_leave_days": 0.00,
        "remaining_leave_days": 0.00,
        "total_days": 0.00,
        "is_closing": True,
    })
    leave_entries = core_hr.emp_leave_annual_days (all=True, return_by_employee=True, filters=leave_filters)
    if leave_entries:
        for entry in leave_entries:
            emp = DataConversion.safe_get (emps, DataConversion.safe_get (entry, "employee"))
            if emp:
                used = DataConversion.safe_get (entry, "used_leave_days")
                tot = DataConversion.convert_to_float (DataConversion.safe_get (entry, "remaining_leave_days") - used)
                avail = tot - used
                DataConversion.safe_list_append (return_data, {
                    "employee": DataConversion.safe_get (emp, "name", DataConversion.safe_get (entry, "employee")),
                    "employee_name": DataConversion.safe_get (emp, "full_name", f"""{DataConversion.safe_get (emp, 'first_name')} {DataConversion.safe_get (emp, 'middle_name', '')} {DataConversion.safe_get (emp, 'last_name')}"""),
                    "leave_type": DataConversion.safe_get (entry, 'leave_type', "Annual Leave"),
                    "used_leave_days": used,
                    "remaining_leave_days": avail,
                    "total_days": tot
                })
                DataConversion.safe_set (totals, "used_leave_days", DataConversion.safe_get (totals, "used_leave_days") + used)
                DataConversion.safe_set (totals, "remaining_leave_days", DataConversion.safe_get (totals, "remaining_leave_days") + avail)
                DataConversion.safe_set (totals, "total_days", DataConversion.safe_get (totals, "total_days") + tot)
        pp (totals)
        DataConversion.safe_list_append (return_data, totals)
    return utils.respond(utils.ok, {"rows":return_data})

def hr_appraisal_report(dbms, object):
    return_data =[]
    filters =object.filters or utils.from_dict_to_object({})
    filters.docstatus =1


    fetch_apprasial =dbms.get_list("Appraisal", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)
    if fetch_apprasial.status ==utils.ok:
        for appraisal in fetch_apprasial.data.rows:
            return_data.append({
                "appraisal_date": appraisal.appraisal_date,
                "appraisal_quarter": appraisal.appraisal_quarter,
                "appraiser_name": appraisal.appraiser_name,
                "appraisee_name": appraisal.appraisee_name,
                "department": appraisal.department,
                "total_open_ended_questions": appraisal.total_open_ended_questions,
                "total_closed_ended_questions": appraisal.total_closed_ended_questions,
                "total_open_score": appraisal.total_open_score,
                "total_closed_score": appraisal.total_closed_score,
                "overall_score": appraisal.overall_score,
            })

    return utils.respond(utils.ok, {"rows":return_data})

def industrial_relations_summary(dbms, object):
    return_data =[]
    filters =object.filters or utils.from_dict_to_object({})
    filters.docstatus =1

    total_grievance_types =0
    total_disciplinary_committee =0
    total_violation_type =0
    total_grievances =0
    total_charge =0
    total_case_outcome =0
    total_startment_forms =0


    fetch_grievance_type =dbms.get_list("Grievance_Type", fetch_linked_fields=True, fetch_linked_tables=True)
    fetch_violation_type =dbms.get_list("Appraisal", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)
    fetch_disciplinary_committee =dbms.get_list("Appraisal", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)
    fetch_grievance =dbms.get_list("Appraisal", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)
    fetch_disciplinary =dbms.get_list("Appraisal", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)
    fetch_case_outcome =dbms.get_list("Appraisal", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)
    fetch_startment_forms =dbms.get_list("Appraisal", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)
    fetch_charge_form =dbms.get_list("Appraisal", filters=filters, fetch_linked_fields=True, fetch_linked_tables=True)

    # GRIEVANCE
    if fetch_grievance_type.status ==utils.ok:
        grievance_type =fetch_grievance_type.data.rows
        total_grievances =len(grievance_type)
        

    # DISCIPLINARY COMMITTEE
    if fetch_disciplinary_committee.status ==utils.ok:
        disciplinary_committee =fetch_disciplinary_committee.data.rows
        total_disciplinary_committee =fetch_disciplinary_committee.data.rows

    # VIOLATION TYPE
    if fetch_violation_type.status ==utils.ok:
        violation_type =fetch_violation_type.data.rows
        total_violation_type =len(violation_type)

    # # GRIEVANCE
    if fetch_grievance.status ==utils.ok:
        grievance =fetch_grievance.data.rows
        total_grievances =len(grievance)

    # CHARGE
    if fetch_disciplinary.status ==utils.ok:
        charge =fetch_disciplinary.data.rows
        total_charge =len(charge)

    # CASE OUT COME
    if fetch_case_outcome.status ==utils.ok:
        case_outcome =fetch_case_outcome.data.rows
        total_case_outcome =len(case_outcome)

    # GRIEVANCE
    if fetch_startment_forms.status ==utils.ok:
        startment_forms =fetch_startment_forms.data.rows
        total_startment_forms =len(startment_forms)

    return utils.respond(utils.ok, {"rows":return_data})


def employee_info (dbms, object):
    return_data = []
    core_hr = Core_Hr (dbms)
    emp_filters = utils.from_dict_to_object({})
    if object.filters.department:
        DataConversion.safe_set (emp_filters, "department", object.filters.department)
    if object.filters.designation:
        DataConversion.safe_set (emp_filters, "designation", object.filters.designation)
    if object.filters.name:
        DataConversion.safe_set (emp_filters, "name", object.filters.name)

    if object.filters.status:
        emp_filters.status = object.filters.status

    get_all_emps = core_hr.get_employee_list (filters=emp_filters, fields=[
        "name", "first_name", "last_name", "middle_name", "gender", "d_o_b", "employee_grade", "email", "contact", "department", "designation", "id_no", "napsa", "nhima", "working_days", "working_hours", "status", "tpin", "date_of_joining"
    ],order=['id'])

    if get_all_emps:
        df = utils.to_data_frame (get_all_emps)
        df = df.replace({np.nan: "", None: ""})
        return_data = df.to_dict(orient="records")

    return utils.respond(utils.ok, {"rows": return_data})
