from controllers.utils import Utils

utils = Utils()
throw = utils.throw
pp = utils.pretty_print


def disable_doc(dbms, object=None):
    body = object.body.data
    doc = dbms.get_doc(body.model, body.id, object.user)
    initial_status = None
    if doc.status == utils.ok:
        before = doc.data
        initial_status = before.status
        obj = before
        obj.disabled = 1
        obj.status = "Disabled"
        update = dbms.update(body.model, obj, object.user, update_submitted=True)
        if update.status == utils.ok:
            disabled = utils.from_dict_to_object({
                "name": obj.name,
                "doc_id":obj.id, 
                "initial_status": initial_status,
                "doc_name": obj.name,
                "document_type": utils.capitalize(utils.replace_character(obj.doctype,"_", " ")),
                "status":  body.status,
                "status":  before.get("status")
            })
            create = dbms.create("Disabled_Document", disabled, privilege=True)
        return update
    return doc


def enable_doc(dbms, object=None):
    body = object.body.data
    doc = dbms.get_doc(body.model, body.id, object.user)
    if doc.status == utils.ok:
        obj = doc.data
        disabled = dbms.get_list("Disabled_Document", filters={"doc_id": obj.id}, privilege=True)
        disabled.status == utils.ok or throw("Failed to fetch disabled document!")
        disabled_doc = disabled.data.rows[0]
        obj.disabled = 0
        obj.status = disabled_doc.initial_status
        update = dbms.update(body.model, obj, object.user, update_submitted=True)
        return update
    return doc

    