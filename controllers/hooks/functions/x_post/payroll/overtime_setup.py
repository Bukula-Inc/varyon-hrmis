from controllers.utils import Utils 
utils = Utils ()

def get_overtime_setup (dbms, object):
    overtime_setup = dbms.get_doc ("Overtime_Configuration", name=object.body.data.name, user=object.user)
    if overtime_setup.get ("status") == utils.ok:
        return utils.respond(utils.ok, overtime_setup.get ("data"))
    return utils.respond (utils.no_content, response={"status": utils.no_content,"error_message":"No Overtime Settings"})

