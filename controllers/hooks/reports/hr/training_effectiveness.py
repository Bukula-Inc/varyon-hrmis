from controllers.utils import Utils

utils =Utils()
pp =utils.pretty_print
throw =utils.throw

def organise_sores(score, score_list):
    if score:
        for index, value in score.items():
            score_list.append(utils.from_dict_to_object({
                index: len(value)
            }))

def training_effectiveness_report(dbms, object):
    return_data =[]
    try:
        fetch_training_feedback= dbms.get_list("Training_Feedback", fetch_linked_fields=True, fetch_linked_tables=True)
    except Exception as e:
        pp("An Error Occured: {e}")

    if fetch_training_feedback.status ==utils.ok:
        training_program =utils.group(fetch_training_feedback.data.rows, "training_program")

        for index, program in training_program.items():
        
            content_stats =[]
            relevance_stats =[]
            delivery_stats =[]
            organization_stats =[]
            overall_stats =[]
            impact_on_work_stats =[]
            recommendation_stats =[]
            work_performance_stats =[]

            content =utils.group(program, "content")
            organise_sores(content, content_stats)
            content_overal = max((list(d.items())[0] for d in content_stats), key=lambda x: x[1])[0]


            relevance =utils.group(program, "relevance")
            organise_sores(relevance, relevance_stats)
            relevance_overal = max((list(d.items())[0] for d in relevance_stats), key=lambda x: x[1])[0]


            delivery =utils.group(program, "delivery")
            organise_sores(delivery, delivery_stats)
            delivery_overal = max((list(d.items())[0] for d in delivery_stats), key=lambda x: x[1])[0]


            organization =utils.group(program, "organization")
            organise_sores(organization, organization_stats)
            organization_overal = max((list(d.items())[0] for d in organization_stats), key=lambda x: x[1])[0]


            overall =utils.group(program, "overall")
            organise_sores(overall, overall_stats)
            overall_overal = max((list(d.items())[0] for d in overall_stats), key=lambda x: x[1])[0]


            impact_on_work =utils.group(program, "impact_on_work")
            organise_sores(impact_on_work, impact_on_work_stats)
            impact_on_work_overal = max((list(d.items())[0] for d in impact_on_work_stats), key=lambda x: x[1])[0]


            recommendation =utils.group(program, "recommendation")
            organise_sores(recommendation, recommendation_stats)
            recommendation_overal = max((list(d.items())[0] for d in recommendation_stats), key=lambda x: x[1])[0]

            return_data.append(utils.from_dict_to_object({
                "program": index,
                "content": content_overal,
                "relevance": relevance_overal,
                "delivery": delivery_overal,
                "origization": organization_overal,
                "overall": overall_overal,
                "impact_on_work": impact_on_work_overal,
                "recommendation": recommendation_overal,
            }))

    return utils.respond(utils.ok, {"rows":return_data})



    

