from controllers.utils import Utils

utils =Utils()
pp =utils.pretty_print
throw =utils.throw


def audit_trail(dbms, object):
    audit_trail_data =[]
    audit_filters =object.filters
    fetch_audit_trail_data =dbms.get_list("Audit_Trail", filters=audit_filters)
    if fetch_audit_trail_data.status !=utils.ok:
        return fetch_audit_trail_data.error_message
    else:
        pp(fetch_audit_trail_data.data.rows)
        for trail in fetch_audit_trail_data.data.rows:
            # audit_trail_data.append(trail)
            audit_trail_data.append(utils.from_dict_to_object({  
                "created_on": trail.created_on,
                "last_modified": trail.last_modified,
                "doc_name": trail.doc_name,
                "document_type": trail.document_type,
                "name": trail.name,
                "owner": trail.owner,
            }))
    
    return utils.respond(utils.ok, {"rows": audit_trail_data})

            
