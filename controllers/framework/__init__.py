from controllers.utils import Utils
from controllers.framework.core.company_switcher import Company_Switcher
from controllers.file_controller import File_Controller
utils = Utils()
pp = utils.pretty_print
throw = utils.throw
class Core:
    def __init__(self, dbms, object) -> None:
        self.dbms = dbms
        self.object = object
        self.xfun = self.object.headers.Xfun
        self.body = self.object.body.data
        self.mapper = {
            # getting system settings
            "get_system_settings": self.get_system_settings,
            "get_approval_doc_config": self.get_approval_doc_config,
            "get_doc_print_format": self.get_print_format,
            "switch_company": self.switch_company,
            "get_model_path":self.get_model_path,
            "delete_files":self.delete_files,
            
        }

    @classmethod
    def init(cls, dbms, object):
        instance = cls(dbms, object)
        # cls.__init__(cls, dbms, object)
        return instance.mapper[instance.xfun]()
        # return cls.mapper[cls.xfun](cls)
    
    def get_system_settings(self):
        return self.dbms.get_system_settings(user=self.dbms.current_user_id)
        

    def get_approval_doc_config(self):
        if not self.body.doc:
            throw("Doc is missing in the body!")
        doc = utils.from_dict_to_object()
        wf_doc = self.dbms.get_doc("Workflow_Doc", self.body.doc, privilege=True)
        if wf_doc.status != utils.ok:
            throw(f"An error occurred while fetching approval doc: {wf_doc.error_message}!")
        doc = self.dbms.get_doc(wf_doc.data.for_doctype, wf_doc.data.name, privilege=True)
        if doc.status != utils.ok:
            throw(f"Failed to fetch workflow document: {doc.error_message}")
        self.body.model = wf_doc.data.for_doctype
        try:
            doc_path = self.get_model_path()
            if doc_path.status != utils.ok:
                throw(f"Failed to fetch doc dor approval:{doc_path.error_message}")
            return utils.respond(utils.ok,{"data":doc.data, "model_path":doc_path.data})
        except Exception as e:
            throw(f"Failed to fetch document path for approval:{str(e)}!")
        
        

    
    def get_print_format(self):
        from controllers.print_controller import Print_Controller
        validated = utils.validate_keys(["model","doc"],self.body)
        if validated.status != utils.ok:
            return validated
        pc = Print_Controller(self.object,self.body.model,self.body.format or None, self.body.doc, False)
        return pc.generate_print_doc(True, response_type="html", auto_print=False, is_preview=True)

    # switch company for multi-company
    def switch_company(self):
        return Company_Switcher.switch_company(self.dbms, self.object)
    

    # get model path for linked fields in front-end
    def get_model_path(self):
        if not self.body.model:
            throw("Model parameter missing in body!")
        result = utils.get_model_module(self.body.model)
        if result.status == utils.ok:
            return result
        throw(f"Model path for <span class='text-orange-700 font-semibold'>{utils.capitalize(utils.replace_character(self.body.model,'_',' '))}</span> does not exist!")


    # to delete files
    def delete_files(self):
        if not self.body.files:
            throw("Body missing files!")
        if not isinstance(self.body.files, str) and not isinstance(self.body.files, list):
            throw("Files must be in a form of a string or list!")
        if isinstance(self.body.files, str):
            self.body.files = [self.body.files]
        fc = File_Controller(self.dbms,self.body.files)
        return fc.delete_files()