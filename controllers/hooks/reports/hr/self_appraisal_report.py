from controllers.utils import Utils

utils = Utils()
pp =utils.pretty_print

def self_appraisal_report(dbms, object):
    self_appraisal_data_result = []
    self_appraisal_info = dbms.get_list("Appraise_Your_Self")
    pp(self_appraisal_info)
    utils.pretty_print (self_appraisal_info)
    if self_appraisal_info.status == utils.ok:
        self_appraisal_data = self_appraisal_info.data.rows
        for app in self_appraisal_data:
            if app["status"] == "Draft":
                continue
        
            self_appraisal_row = {
                "appraisee_name": app.appraisee_name,
                "appraisal_date": app.appraisal_closure_date,
                "department": app.department,
                "appraisal_quarter": app.appraisal_quarter,
                "total_open_score": app.total_open_score,
                "total_closed_score": app.total_closed_score,
                "total_open_ended_questions": app.total_open_ended_questions,
                "total_closed_ended_questions":  app.total_closed_ended_questions,
                "overall_score": app.overall_score,
            }
            self_appraisal_data_result.append(self_appraisal_row)

#     return utils.respond(utils.ok, {'rows': self_appraisal_data_result})
