from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.core_functions.core import Core
from controllers.file_controller import File_Controller
utils = Utils()
throw = utils.throw
pp = utils.pretty_print

def on_data_importation_save(dbms,object):
    if not object.body.skip_extraction:
        rows = File_Controller.extract_data_importation_rows(object.body.file_url)
        rows.status == utils.ok or throw(rows.error_message)
        object.body.file_content = rows.data
        object.body.total_rows = len(rows.data)
    pp(object.body.file_content)

def on_data_importation_update(dbms,object):
    core = Core(dbms,object)
    body = object.body
    file_url = body.file_url
    if not object.body.skip_extraction:
        doc = dbms.get_doc("Data_Importation", body.name, user=object.user)
        doc.status == utils.ok or throw(f"Failed to update doc: {doc.error_message}")
        d = doc.data
        if d.file_url != file_url:
            rows = core.extract_data_importation_rows(object.body)
            rows.status == utils.ok or throw(rows.error_message)
            object.body.file_content = rows.data
            object.body.total_rows = len(rows.data)
        else:
            object.body.file_content = object.body.file_content

def on_data_importation_submit(dbms,object):
    object.doc_status = "Pending Importation"

