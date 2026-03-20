from controllers.utils import Utils

utils =Utils()
pp =utils.pretty_print
throw =utils.throw
update_sp ={}
resulting_status =200

def create_job_openning_from_staffing_plan(dbms, object):
    staffing_plan =object.body.data
    system_settings =dbms.system_settings
    jos =0

    for staff_details in staffing_plan.staffing_details:
        job_opening =utils.from_dict_to_object({
            "status": "Submitted",
            "vacancies": staff_details.vacancies,
            "publish": staff_details.publish_job_offer,
            "publish_salary": staff_details.publish_salary,
            "description": "",
            "lower_range": staff_details.estimated_cost,
            "upper_range": 0.00,
            "designation": staff_details.designation,
            "company": staffing_plan.company,
            "department": staff_details.department,
            "currency": system_settings.default_currency,
        },)

        try:
            create_jp =dbms.create("Job_Advertisement", job_opening)
            jos +=1
        except Exception as e:
            pp("An Error Occured : {e}")

    # staffing_plan.create_job_offers =1
    # staffing_plan.status ="Submitted"

    # try:
    #     update_sp =dbms.update("Staffing_Plan", staffing_plan, update_submitted=True)
    # except Exception as e:
    #     pp("An ErrorOccuered While Updating A Staff Plan,  : {e}")

    # resulting_status =None
    # if update_sp:
    #     if update_sp.status !=utils.ok:
    #         resulting_status =update_sp.status
    #     else:
    #         resulting_status =utils.ok
    # else:
    #     resulting_status =utils.ok
    
    return utils.respond(utils.ok, {"created_job_opennings": jos})