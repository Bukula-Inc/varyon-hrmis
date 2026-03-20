from controllers.utils import Utils
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import os
import pandas as pd
utils = Utils()
pp = utils.pretty_print
throw = utils.throw
class File_Controller:
    def __init__(self, dbms, files=[], ):
        self.dbms = dbms
        self.files = files
    
    def validate_files(self):
        if self.files:
            try:
                for key in utils.get_object_keys(self.files):
                    field_files = self.files.getlist(key)
                    if field_files:
                        for file in field_files:
                            file_size = file.size
                            if file_size > 50804608:
                                return utils.respond(utils.unprocessable_entity,"The file size is too large for the upload!")
                return utils.respond(utils.ok, "File validation successful!")
            except Exception as e:
                throw(f"File validation failed: {str(e)}")

    @classmethod
    def extract_data_importation_rows(cls, file_url=None, file=None):
        try:
            df = None
            file_path = ""
            if file and not file_url:
                file_path = file.name
            else:
                file_path = f"{utils.get_path_to_base_folder() + file_url}".strip()
            ext = file_path.split(".")[-1].lower()
            if ext == "csv":
                df = pd.read_csv(file_path if file_url else file)
            elif ext in ['xls', 'xlsx']:
                df = pd.read_excel(file_path if file_url else file, header=0, index_col=None)
            else:
                throw("You can only import data from Excel or CSV File!")
            # df.columns = df.columns.str.lower()
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            rows = utils.normalize_import_data(df.to_dict(orient="records"))
            if file:
                return utils.respond(utils.ok, {"columns":df.columns.to_list(), "rows":rows})
            return utils.respond(utils.ok, rows)
        except Exception as e:
            throw(f"Data Importation Failed: {e}")

    def __get_tenant_path(self):
        try:
            # Get the base path for the application
            base_app = utils.get_path_to_base_folder()
            if base_app:
                full_path = f"{base_app}/media/{self.dbms.tenant_db}/private/"
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                return utils.respond(utils.ok, {"full_path": full_path, "app_path": f"/media/{self.dbms.tenant_db}/private/"})
        except Exception as e:
            # Return the error response if an exception occurs
            return utils.respond(utils.not_found, f"{e}")
    
    def write_files(self):
        uploaded_files = {}
        try:
            validate = self.validate_files()
            if validate.status == utils.ok:
                for key in utils.get_object_keys(self.files):
                    field_files = self.files.getlist(key)
                    if field_files:
                        for file in field_files:
                            ext = Path(file.name).suffix[1:] if '.' in file.name else ''
                            file_name = file.name
                            file_size = file.size
                            ext = ext
                            path = self.__get_tenant_path()
                            if path.status != utils.ok:
                                return path
                            p = path.data
                            fs = FileSystemStorage(location = p.get("full_path"))
                            filename = fs.save(file_name, file)
                            if filename:
                                new_path = f"{p.get('app_path')}{filename}"
                                create = self.dbms.create("File_Management", {"name":filename,"description":"Upload file","file_path":new_path,"file_ext":ext,"file_size":file_size}, privilege=True)
                                if create.status == utils.ok:
                                    if not uploaded_files.get(key):
                                        uploaded_files[key] = [new_path]
                                    else:
                                        uploaded_files[key].append(new_path)
                return utils.respond(utils.ok, uploaded_files)
            return validate
        except Exception as e:
            return utils.respond(utils.internal_server_error,f"{str(e)}")
        

    def delete_files(self):
        base_path = utils.get_path_to_base_folder()
        processed_files = ""
        if self.files:
            for file in self.files:
                file_path = f"{base_path}{file}"
                try:
                    os.remove(file_path)
                    processed_files += f"""
                        <div><strong class='text-11'>{file_path.split("/")[-1]}</strong> deleted successfully!</div>
                    """
                except FileNotFoundError:
                    processed_files += f"""
                        <div><strong class='text-red-700'>{file_path.split("/")[-1]}</strong> not fount!</div>
                    """
                except PermissionError:
                    processed_files += f"""
                        <div><strong class='text-11'>{file_path.split("/")[-1]}</strong> deletion failed due to insufficient permissions!</div>
                    """
                except Exception as e:
                    processed_files += f"""
                        <div><strong class='text-11'>{file_path.split("/")[-1]}</strong> deletion failed:{str(e)}!</div>
                    """
        return utils.respond(utils.ok, processed_files)
    

    def extract_file_content(self):
        throw("Extracting file content!!!")