from controllers.utils import Utils

utils = Utils()
def training_feedback_report_with_scores(dbms, object):
    feedback_entries = dbms.get_list("Training_Feedback", user=object.user)
    if feedback_entries.get("status") != utils.ok:
        return
    else:
        feedback_entries = feedback_entries.get("data", {}).get("rows", [])

    report_data = []
    total_scores = []

    for feedback_entry in feedback_entries:
        employee = feedback_entry.get("employee", "") 
        relevance = feedback_entry.get("relevance", "")
        content = feedback_entry.get("content", "")
        delivery = feedback_entry.get("delivery", "")
        organization = feedback_entry.get("organization", "")
        training_event = feedback_entry.get("training_event", "")

        # Map feedback to scores
        score_map = {
            "excellent": 5,
            "very good": 4,
            "good": 3,
            "fair": 2,
            "bad": 1
        }

        relevance_score = score_map.get(relevance.lower(), 0)
        content_score = score_map.get(content.lower(), 0)
        delivery_score = score_map.get(delivery.lower(), 0)
        organization_score = score_map.get(organization.lower(), 0)
        total_score = relevance_score + content_score + delivery_score + organization_score
        total_scores.append(total_score)

        overall_total_score = sum(total_scores)
        overall_percentage = (overall_total_score / (len(total_scores) * 20)) * 100 if total_scores else 0

        feedback_report_data = {
            "training_event": training_event,
            "employee": employee,
            "relevance": relevance,
            "content": content,
            "delivery": delivery,
            "organization": organization,
            "relevance_score": relevance_score,
            "content_score": content_score,
            "delivery_score": delivery_score,
            "organization_score": organization_score,
            "total_score": total_score,
            "overall_percentage_score": overall_percentage
        }

        report_data.append(feedback_report_data)

    return utils.respond(utils.ok, {'rows': report_data})