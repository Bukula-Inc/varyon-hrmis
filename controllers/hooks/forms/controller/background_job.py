from controllers.utils import Utils
utils = Utils()
throw = utils.throw
pp = utils.pretty_print


def idlelize_job(dbms, object):
    body = object.body.data
    data = dbms.get_doc("Background_Job", body.job, privilege=True)
    if data.status == utils.ok:
        data.data.status = "Idle"
        return dbms.update("Background_Job", data.data, privilege=True)
    return utils.respond(utils.ok, "An error occurred while updating background job!")
