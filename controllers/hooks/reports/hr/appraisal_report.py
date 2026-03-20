from controllers.utils import Utils

utils = Utils()
pp =utils.pretty_print

def appraisal_report(dbms, object):
    utils.pretty_print ("")
    appraisal_data_result = []
    appraisal_info = dbms.get_list("Appraisal",)
    if appraisal_info.status == utils.ok:
        appraisal_data = appraisal_info.data.rows
        for app in appraisal_data:
        
            if app.status == "Draft":
                continue 
        
            appraisal_row = {
                "appraisee_name": app.appraisee_name,  
                "appraiser_name": app.appraiser_name, 
                "appraisal_date": app.appraisal_date,
                "department": app.department,
                "appraisal_quarter": app.appraisal_quarter,
                "total_open_score": app.total_open_score,
                "total_closed_score": app.total_closed_score,
                "total_open_ended_questions": app.total_open_ended_questions,
                "total_closed_ended_questions":  app.total_closed_ended_questions,
                "overall_score": app.overall_score,
            }
            appraisal_data_result.append(appraisal_row)

    return utils.respond(utils.ok, {'rows': appraisal_data_result})
