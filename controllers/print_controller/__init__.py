import os
from django.shortcuts import render
from jinja2 import Environment, FileSystemLoader
from django.http import HttpResponse
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.html_generator import HTML_Generator
# import weasyprint


from weasyprint import HTML

utils = Utils()
dates = Dates()
generator = HTML_Generator()
pp = utils.pretty_print
throw = utils.throw

class Print_Controller:
    def __init__(self,request,model,print_format=None,doc=None,is_download_request=0,):
        self.request = request
        self.model = model
        self.print_format = print_format
        self.doc = doc
        self.is_download_request = is_download_request
        self.doc_exclusives = [
            "created_on", "creation_time", "docstatus", 
            "owner", "modified_by","status","id","utils",
            "doc_exclusives","idx","disabled","doctype","last_modified",
            "owner_name","modifier_name"
        ]

            
    def __get_print_format(self):
        pf_data = self.dbms.get_doc("Print_Format", self.print_format or self.default_print_format, privilege=True)
        return pf_data
    
    def __get_doc(self):
        doc_data = self.dbms.get_doc(self.model , self.doc, fetch_linked_fields=True, fetch_linked_tables=True, privilege=True, get_print_format=True)
        if doc_data.status == utils.ok:
            self.doc_data = doc_data.data
            self.default_print_format = self.doc_data.default_print_format
        return doc_data
    
    def __get_doc_print_config(self):
        doc_data = self.dbms.get_doc("Print_Configuration", self.model, privilege=True)
        return doc_data
    
    def update_print_count (self, document, update=False):
        check_result =  self.dbms.check_if_doc_exists("Printed_Document", document.name)
        if check_result:
            if update:
                result = self.dbms.get_doc("Printed_Document", document.name, privilege=True)
                if result.status == utils.ok:
                    result.data.print_count += 1
                    updated_doc = self.dbms.update("Printed_Document", result.data, privilege=True)
                    return updated_doc.data.print_count
            else:
                result = self.dbms.get_doc("Printed_Document", document.name, privilege=True)
                if result.status == utils.ok:
                    return result.data.print_count

        else: 
            if update:
                doc = utils.from_dict_to_object({})
                doc.name = document.name
                doc.document_type = document.doctype
                doc.print_count = 1
                created_doc = self.dbms.create("Printed_Document", doc, privilege=True)
                if created_doc.status == utils.ok:
                    return created_doc.data.print_count
                else: 
                    return 0
            else:
                pass
    
    def generate_print_doc(self, skip_validation=False, response_type="http", auto_print=True, is_preview=False, is_internal_processing=False):
        from controllers.dbms import DBMS
        validation = self.request
        if not skip_validation:
            validation = utils.validate_request(self.request, ignore_model=True)
            if validation.get("status") != utils.ok:
                return utils.respond(utils.internal_server_error, f"Something went wrong! {validation.get('error_message')}")
            
        val = validation.data if not skip_validation else validation
        self.dbms = DBMS(val)

        # add user and default company
        user = utils.from_dict_to_object()
        company = utils.from_dict_to_object()
        default_theme_color = "#151030"
        default_text_color = "#ffffff"
        default_secondary_color = "#d35611"
        if self.dbms.current_user:
            user = self.dbms.current_user
            if user.default_company:
                company_data = self.dbms.get_doc("Company", user.default_company,  privilege=True)
                if company_data.status == utils.ok:
                    company = company_data.data
                    if company.default_theme_color:
                        default_theme_color = company.default_theme_color
                    if company.default_theme_text_color:
                        default_text_color = company.default_theme_text_color
                    if  company.default_secondary_color:
                        default_secondary_color = company.default_secondary_color
        
        doc_data = self.__get_doc()
        if doc_data.status != utils.ok:
            return doc_data
        
        doc = doc_data.data
        self.doc_data = doc
        print_count = 1
        if not is_preview:
            res = self.update_print_count(doc, update=True) 
            print_count = res
        else:
            res = self.update_print_count(doc) 
            print_count =   res 

        doc["doc_dict"] = doc
        
        # pp(doc_data)
        doc["doc_exclusives"] = self.doc_exclusives
        doc["host"] = val.host
        doc["full_url"] = val.headers.Host
        doc["utils"] = utils
        doc["dates"] = dates
        doc["generator"] = generator
        doc["print_count"] = print_count or 1
        pf_data = self.__get_print_format()
        if pf_data.get("status") != utils.ok:
            return pf_data
        
        pf = pf_data.get("data")
        pf_html = f"""<div style="width:100%;font-family: arial !important; height:max-content" class="print-wrapper">{pf.get("html")}</div>"""
        html = """ <style> @media print { .show-on-print { display: block !important;}}</style><div class="show-on-print hidden">""" + pf_html
        html += "</div><script>window.onload = function() { window.print(); window.onafterprint = function(e){ window.close(); }}</script>"
        data = {}
        data["doctype"] = doc.get("doctype")
        data["doc_dict"] = doc
        data["utils"] = utils
        doc["generator"] = generator
        data["doc_exclusives"] = self.doc_exclusives
        data["default_user_company"]= company
        data["logged_in_user"] = user
        data["default_theme_color"] = default_theme_color
        data["default_text_color"] = default_text_color
        data["default_secondary_color"] = default_secondary_color
        
        pf_config = self.__get_doc_print_config()
        if pf_config.get("status") == utils.ok:
            pp(pf_config)
            config = pf_config.get("data").get("configuration_fields")
            if len(config) > 0:
                for field in config:
                    if field.get("include_in_print") == '1':
                        data[field.get("field_name")] = doc.get(field.get("field_name"))
                data["doc_dict"] = data
            else:
                for label, value in doc.items():
                    data[label] = value
        else:
            for label, value in doc.items():
                data[label] = value
            
        env = Environment(loader=FileSystemLoader('.'))
        template = env.from_string(html if auto_print else pf_html)
        rendered_html = template.render(data)
        if self.is_download_request == 1:
            pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[
                'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',
                'static/css/print_layout.css'
            ], 
                # scripts=[  "/static/js/tailwindcss.js"]
            )
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{doc.get("name")}.pdf"'

        else:
            response = HttpResponse(rendered_html, content_type='text/html')

            pdf = HTML(string=rendered_html).write_pdf()

            if is_internal_processing ==True:
                file_path = f"{utils.get_path_to_base_folder()}/media/{val.tenant}/private/{doc.name}.pdf"
                directory = os.path.dirname(file_path)
                os.makedirs(directory, exist_ok=True)

                with open(file_path, 'wb') as file:
                    file.write(pdf)

                return utils.respond(utils.ok, file_path)


        if response_type == "http":
            return utils.respond(utils.ok, response)
        elif response_type == "html":
            return utils.respond(utils.ok, rendered_html)