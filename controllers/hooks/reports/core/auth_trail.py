from controllers.utils import Utils

utils =Utils()
pp =utils.pretty_print
throw =utils.throw

utils =Utils()

def auth_trail_report(dbms, object):
    auth_trail_data =[]
    auth_filters =object.filters
    fecth_auth_trail_data =dbms.get_list("Auth_Trail", filters=auth_filters)
    if fecth_auth_trail_data.status !=utils.ok:
            return None
    else:
        for auth in fecth_auth_trail_data.data.rows:
               auth_trail_data.append(utils.from_dict_to_object({
                "date": auth.created_on,
                "activity_time": auth.activity_time,
                "name": auth.first_name + " " + auth.last_name,
                "email": auth.email,
                "activity_type": auth.activity_type,
                "message": auth.message,
                "status": auth.status,                
               }  ))  
    return utils.respond(utils.ok, {"rows": auth_trail_data})

