from controllers.utils import Utils


utils =Utils()
pp =utils.pretty_print
throw =utils.throw

def before_skills_gap_submit(dbms, object):

    skill_gap =object.body
    training_program =skill_gap.linked_fields.training_program
    training_plan =None

    fetch_training_plan =dbms.get_doc("Training_Plan", "active", fetch_by_field="use_status", fetch_linked_tables=True )
    if fetch_training_plan.status !=utils.ok:
        throw("No active training plan was found !")
    else:
        training_plan =fetch_training_plan.data

    training_plan.listed_trianing_plans.append(utils.from_dict_to_object({        
        "training_program" : training_program.name,   
        "training_type" : training_program.type,  
        "course" : training_program.course,  
        "program_duration" : training_program.program_duration,   
        "certification_type" : training_program.certification_type,  
        "description" : training_program.description,  
        "training_expense": training_program.training_expense,
    }))
    try:
        tp_update =dbms.update("Training_Plan", training_plan, update_submitted=True)
    except Exception as e:
        pp(e)
