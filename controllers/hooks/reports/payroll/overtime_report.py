from controllers.utils import Utils

utils = Utils()

def overtime_report(dbms, object):
    overtime_data_result = []
    sum_of_approved_overtimes = 0
    sum_of_rejected_overtimes = 0
    sum_of_pending_overtimes = 0
    sum_of_total_earning  = 0   
    overtime_filters = object.filters
    decimals = dbms.system_settings.currency_decimals

    pending = 0
    approved = 0
    rejected = 0
    
    approved = 0
    overtime_info = dbms.get_list("Overtime",filters= overtime_filters, privilege=True)
    if overtime_info.status == utils.ok:
        overtime_rows = overtime_info.data.rows
        for overtime in overtime_rows:
            if overtime["status"] == "Draft":
                continue 
            
            employee_data = dbms.get_list("Employee", filters={'name': overtime["applicant"]}, privilege=True)
            employees = employee_data.data.rows
            
            for employee in employees:
                if overtime["applicant"] == employee["name"]:
                    if overtime["status"] == 'Pending Approval':
                        pending += 1
                    elif overtime["status"] == 'Approved':
                        approved += 1
                    elif overtime["status"] == 'Rejected':
                        rejected += 1
                        
            overtime_data_result.append({
                "applicant": overtime.get('applicant'),
                "status": overtime.get('status'),
                "status_info": overtime.get('status_info'),
                "date": overtime.get('created_on'),
                "name": overtime.get('name'),
                "start_time": overtime.get('start_time'),
                "end_time": overtime.get('end_time'),
                "total_earning": utils.fixed_decimals(float(overtime.get('total_earning')), decimals),
                "approved_overtimes": approved,
                "pending_overtimes": pending,
                "rejected_overtimes": rejected,
            })

            sum_of_approved_overtimes += approved
            sum_of_rejected_overtimes += rejected
            sum_of_pending_overtimes += pending
            sum_of_total_earning  += utils.fixed_decimals(overtime.get('total_earning'),2)   

    overtime_data_result.append({
        "applicant": "Totals",
        "status":"",
        "status_info": "",
        "date": "",
        "name": "",
        "start_time": "",
        "end_time": "",
        "total_earning": sum_of_total_earning,
        "approved_overtimes": approved,
        "pending_overtimes": pending,
        "rejected_overtimes": rejected
        })

    return utils.respond(utils.ok, {
        'rows': overtime_data_result,
    })
