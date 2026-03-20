from  controllers.utils import Utils

utils = Utils ()

def get_bonus_type (dbms, object):
    bonus_type = dbms.get_doc ("Bonus_Type", object.body.data.name, user=object.user)
    if bonus_type.get ("status")!= utils.ok:
        return utils.respond (utils.no_content, response={"status": utils.no_content,"error_message":response_msg})
    return utils.respond (utils.ok, response=bonus_type.get ("data"))