from controllers.core_functions.core import Core
from controllers.utils import Utils

utils = Utils()
pp = utils.pretty_print
throw = utils.throw
def start_data_importation(dbms, object):
    try:
        core = Core(dbms, object.user, object)
        docs = object.body.data.doc
        if docs and len(docs) > 0:
            importations  = []
            for doc in docs:
                doc_data = dbms.get_doc("Data_Importation", doc, fetch_by_field="id", privilege=True)
                if doc_data.status != utils.ok:
                    return doc_data
                dc = doc_data.data
                importation = core.start_data_importation(utils.from_dict_to_object(dc))
                importations.append(importation)
            return utils.respond(utils.ok, importations)
    except Exception as e:
        pp(f"xxxxxxxxxxxxxxxxxxxxxxxx An error occurred while importating data: {str(e)} xxxxxxxxxxxxxxxxxxxxxxxx")
    throw("Submission ID's not found!")