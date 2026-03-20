from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

def training_program(dbms, object):
    results =utils.from_dict_to_object({})
    participation_metric =utils.from_dict_to_object({
        "labels": [],
        "value": [],
    })

    attendee =[]    

    total_programs = 0
    ongoing_training_programs = 0
    scheduled_training_programs = 0
    rejected_training_programs = 0  
    completed_training_programs = 0  

    training_programs = dbms.get_list("Training_Program", fetch_linked_tables=True, fetch_linked_fields=True)
    if training_programs.status == utils.ok:
        training_program_list =training_programs.data.rows
        total_programs =len(training_program_list)
        df_training_program =utils.to_data_frame(training_program_list)
        attendee =sum(df_training_program["attendee"], [])
        df_attendee =utils.to_data_frame(attendee)
        employees = df_attendee["linked_fields"].apply(lambda x: x["employee"]).to_list()
        emps =utils.group(employees, "gender" or "")

        if emps:
            for key, emp in emps.items():
                participation_metric.labels.append(key)
                participation_metric.value.append(len(emp))
                
    results.total_programs =total_programs
    results.participation_metric =participation_metric
    pp(results)

    return utils.respond(utils.ok, results) 

