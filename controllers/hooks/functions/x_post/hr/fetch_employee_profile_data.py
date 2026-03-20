from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.hr import Core_Hr


utils =Utils()
pp =utils.pretty_print
throw =utils.throw
dates =Dates()

def fetch_employee_profile_data(dbms, object):

    core_hr =Core_Hr(dbms, object)
    petty_cash =None
    imprest =None
    expense_list =None
    earnings_list =None

    returned_data =utils.from_dict_to_object({
        "top_cards": utils.from_dict_to_object({}),
        "job_personal_info": utils.from_dict_to_object({}),
        "work_plan": utils.from_dict_to_object({}),
        "brief_descriptions": utils.from_dict_to_object({}),
        "leave_types": utils.from_dict_to_object({}),
        "appraisal": utils.from_dict_to_object({})
    })

    pie_chart_data =utils.from_dict_to_object({
        "labels": None,
        "value": None
    })
    expense_distribution =utils.from_dict_to_object({
        "labels": None,
        "value": None
    })
    income_distribution =utils.from_dict_to_object({
        "labels": None,
        "value": None
    })

    leave_entries =None
    emp_info =object.body.data.employee
    emp =None
    emp_linked_info =None

    # DATA TO RETURN
    leave_balance =None
    total_income =None
    total_expanse =None

    # JOB AND PERSONAL INFO
    full_name =None
    email =None
    emergancy_contact =None
    company =None
    department =None
    job_title =None
    supervisor =None

    # Quatorly And Monthly work plan
    # Brief DISCRIPTIONS
    salary =None
    startionary =None
    bonus =None
    image =""
    joined_on =None
    qualification =None
    date_of_birth =None
    staff_leave_days =[]
    earnings =[]
    earnings_amounts =[]
    work_plan_data =None
    years_of_service = 0

    try:
        fetch_empolyee_data =dbms.get_doc("Employee", emp_info)
        if fetch_empolyee_data.status ==utils.ok:
            emp =fetch_empolyee_data.data
            earnings =[x.earning for x in emp.earnings]
            emp_linked_info =fetch_empolyee_data.data.linked_fields
            years_of_service =int(dates.date_difference(str(emp.date_of_joining or ""), str(dates.today()))/365) or 0
        else: 
            return utils.respond(fetch_empolyee_data.status, "No matching employee Found!")
        fetch_emp_leave =core_hr.get_employee_leave_days(emp_info)
        
        fetch_petty_cash =dbms.get_list("Petty_Cash", filters={"docstatus":1, "initiator": emp_info})
        if fetch_petty_cash.status ==utils.ok:
            petty_cash =fetch_petty_cash.data.rows

        fetch_imprest =dbms.get_list("Imprest", filters={"docstatus":1, "initiator": emp_info})
        if fetch_imprest.status ==utils.ok:
            imprest =fetch_imprest.data.rows
        
        fetch_salary_components =dbms.get_list("Salary_Component", filters={"name__in": earnings})
        if fetch_salary_components.status ==utils.ok:
            earnings_list =fetch_salary_components.data.rows
            income_distribution.labels =[x.name for x in earnings_list]
            earnings_amounts =[float(emp.basic_pay) *(float(x.percentage)/100) if x.value_type =="Percentage" else float(x.fixed_amount) for x in fetch_salary_components.data.rows]
            income_distribution.value =earnings_amounts
            
        fetch_leave_entrires =dbms.get_list("Leave_Entry", filters={"docstatus":1, "employee": emp_info})
        if fetch_leave_entrires.status ==utils.ok:
            leave_entries =utils.group(fetch_leave_entrires.data.rows, "leave_type")
            pie_chart_data.labels =[x for x in leave_entries.keys()]
            pie_chart_data.value =[sum(y.used_leave_days for y in x) for x in leave_entries.values()]
            leave_balance =sum([y.remaining_leave_days for x in leave_entries.values() for y in x])
                        
            for leave_type, leave_values in leave_entries.items():
                staff_leave_days.append(utils.from_dict_to_object({
                    "leave_type": leave_type,
                    "total_leave_days": sum([x.allocated_leave_days for x in leave_values]),
                    "used_leave_days": sum([x.remaining_leave_days for x in leave_values]),
                }))


        fetch_work_plan =dbms.get_list("Work_Plan", filters={"employee": emp_info}, fetch_linked_tables=True,)
        if fetch_work_plan.status ==utils.ok:
            work_plan_tasks =([plan.work_plan_task[0] for plan in fetch_work_plan.data.rows])
            grouped_work_plan =utils.group(work_plan_tasks, "progress_tracker")
            labels =[]
            values =[]
            for k, v in grouped_work_plan.items():
                labels.append(k)
                values.append(len(v)) 

            work_plan_status_data =utils.from_dict_to_object({
                "labels": labels,
                "values": values,
            })
            work_plan_data =work_plan_status_data
        else:
            work_plan_data =utils.from_dict_to_object({
                "labels": [],
                "values": [],
            })

        pp(work_plan_data)


    except Exception as e:
        throw(e)
         

    if petty_cash and imprest:
        expense_list =[float(x.requested_amount) for x in petty_cash] + [float(x.retired_amount) for x in imprest]
        expense_distribution.labels =[x.name for x in petty_cash] + [x.name for x in imprest]
        expense_distribution.value =[float(x.requested_amount) for x in petty_cash] + [float(x.retired_amount) for x in imprest]
    elif petty_cash:
        expense_list =[float(x.requested_amount) for x in petty_cash]
        expense_distribution.labels =[x.name for x in petty_cash]
        expense_distribution.value =[float(x.requested_amount) for x in petty_cash]
    elif imprest:
        expense_list =[float(x.retired_amount) for x in imprest]
        expense_distribution.labels =[x.name for x in imprest]
        expense_distribution.value =[float(x.retired_amount) for x in imprest]
       
    total_expanse =sum(expense_list or []) 
    total_income =sum(earnings_amounts or [])

    # if leave_entries:
    #     latest =leave_entries[0]
    #     grouped_entries =utils.group(leave_entries, "leave_type")
    #     leave_balance =fetch_emp_leave.overall_totals.remaining_days

    returned_data.top_cards =utils.from_dict_to_object({
        "leave_balance" : leave_balance,
        "total_income" : total_income,
        "total_expanse" : total_expanse,
        "years_of_service": years_of_service
    })



    returned_data.job_personal_info =utils.from_dict_to_object({
        "full_name": emp.full_name,
        "contact": emp.contact,
        "email": emp.email,
        "emergancy_contact": None,
        "company": emp.company,
        "department": emp.department,
        "job_title": emp.designation,
        "supervisor": emp.report_to,
    })


    returned_data.brief_descriptions =utils.from_dict_to_object({        
        "salary": 200,
        # emp.basic_pay,
        "startionary": startionary,
        "bonus": startionary,
        "status": emp.status,
        "image": "",
        "joined_on": emp.date_of_joining,
        "qualification": None,
        "date_of_birth": emp.d_o_b,
    })


    returned_data.leave_types =utils.from_dict_to_object({        
        "distribution": pie_chart_data,
        "staff_leave_days": staff_leave_days,
    })

    returned_data.appraisal =utils.from_dict_to_object({        
        "distribution": work_plan_data,
    })

    returned_data.work_plan =utils.from_dict_to_object({        
        "distribution": income_distribution,
    })

    return utils.respond(utils.ok, returned_data)
