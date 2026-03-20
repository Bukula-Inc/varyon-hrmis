import pandas as pd
from controllers.utils import Utils
from controllers.utils.data_conversions import DataConversion

utils = Utils()
pp = utils.pretty_print
throw = utils.throw

def interview_rate(dbms, object):
    body =object.body
    technical_competence_grouped =[]
    behavioral_competence_grouped =[]
    interview_technical_competence =[]
    interview_behavioral_competence =[]
    fetch_interview_rating = dbms.get_list("Interview_Rating", filters={"interview": object.body.interview}, fields=["technical_competence", "behavioral_competence", "interviewer_name"], fetch_linked_tables=True)
    fetch_interview = dbms.get_doc("Interview", object.body.interview)

    if fetch_interview_rating.status !=utils.ok:
       throw(f"No interview ratings were found.") 

    if fetch_interview.status !=utils.ok:
        throw(f"The main interview document was not found")

    interview_rating =fetch_interview_rating.data.rows
    interview =fetch_interview.data

    if not interview.other_relevant_information:
        interview.other_relevant_information =[]

    if body.other_relevant_information:
        interview.other_relevant_information.append(utils.from_dict_to_object({
            "interviewer": body.interviewer_name,
            "notice_period": body.other_relevant_information[0].notice_period ,
            "expected_package": body.other_relevant_information[0].expected_package,
            "interviewer_comments": body.other_relevant_information[0].interviewer_comments,
            "present_or_previous_package": body.other_relevant_information[0].present_or_previous_package,
            "reason_for_leaving_employment": body.other_relevant_information[0].reason_for_leaving_employment
        }))

    for rating in interview_rating:
        technical_competence_grouped.extend(rating.technical_competence)
        behavioral_competence_grouped.extend(rating.behavioral_competence)

    technical =utils.group(technical_competence_grouped, "technical_question")
    behavioral =utils.group(behavioral_competence_grouped, "behavioral_question")

    total_technical_score =0.00
    total_behavioral_score =0.00

    for technical_competence in interview.technical_competence:
        summed_score =0
        technical[technical_competence.technical_question]
        for evaluation in technical[technical_competence.technical_question]:
            summed_score +=float(DataConversion.safe_get(evaluation, "technical_rating", 0) or 0) or 0
        technical_competence.rating =summed_score/len(DataConversion.safe_get(technical,DataConversion.safe_get(technical_competence,"technical_question", ""), None) or []) if summed_score >0 else 0         
        technical_competence.total_score =summed_score or 0
        total_technical_score +=DataConversion.safe_get(technical_competence, "rating", 0)

    for behavioral_competence in interview.behavioral_competence:
        summed_score =0
        behavioral[behavioral_competence.behavioral_question]
        for evaluation in behavioral[behavioral_competence.behavioral_question]:
            summed_score +=float(DataConversion.safe_get(evaluation, "behavioral_rating", 0) or 0) or 0
        behavioral_competence.rating =summed_score/len(behavioral[behavioral_competence.behavioral_question]) if summed_score >0 else 0 
        behavioral_competence.total_score =summed_score
        total_behavioral_score +=DataConversion.safe_get(behavioral_competence, "rating", 0)

    interview.technical_total =total_technical_score
    interview.behavioral_total =total_behavioral_score
    interview.overall_total =total_behavioral_score + total_technical_score

    update_main_interview_doc =dbms.update("Interview", interview, update_submitted=True)
    if update_main_interview_doc.status !=utils.ok:
        throw(f"An error occurred while trying to update the average scores :", update_main_interview_doc)
