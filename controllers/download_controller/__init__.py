import pandas as pd
from django.http import FileResponse
from controllers.hooks import download_data_customizer
import os
import weasyprint
from django.template import Context, Template
from jinja2 import Environment, FileSystemLoader
from controllers.utils import Utils
from controllers.utils.dates import Dates
utils = Utils()
dates = Dates()
pp = utils.pretty_print
throw = utils.throw

def test(first_name, last_name):
    return f"{first_name} - {last_name}"

class Download_Controller:
    def __init__(self, dbms, object, title=None):
        self.dbms = dbms
        self.object = object
        self.title = title
        self.settings = dbms.system_settings

    def get_report_template(self):
        template = None
        report_template = self.dbms.get_doc("Print_Format", self.object.model, privilege=True)
        if report_template.status == utils.ok:
            template = report_template.data.html
        else:
            report_template = self.dbms.get_doc("Template_Content", self.object.model, privilege=True)
            if report_template.status == utils.ok:
                template = report_template.data.content
            else:
                report_template = self.dbms.get_doc("Print_Format", "Default Report Template", privilege=True)
                if report_template.status == utils.ok:
                    template = report_template.data.html
        if not template:
            throw(f"Failed to fetch default print template for {self.object.model}")
        return template
    

    def render_template(self, template, context):
        return Template(template).render(context)

    def get_jinja2_environment(self):
        # Set up the Jinja2 environment
        env = Environment(loader=FileSystemLoader(searchpath="./"))
        env.globals['utils'] = utils
        return env

    def render_template(self, template, context):
        env = self.get_jinja2_environment()
        template = env.from_string(template)
        return template.render(context)

    def download_report(self, data, format, fields, title="temp_doc", skip_del=False):
        row_title = title
        title = f'{utils.replace_character(title," ", " ")} {dates.timestamp()}'
        response = None
        if not fields:
            throw("Please select report column fields before downloading!")
        if data:
            file_path = f"{utils.get_path_to_base_folder()}/media/{title}.{format}"
            df = utils.to_data_frame(data)
            fields.append("SN")
            df['SN'] = df.index + 1
            if fields:
                df = df[fields]
            else:
                fields = df.columns.tolist()
            renaming = {field: utils.capitalize(utils.replace_character(field, "_", " ")) for field in fields}
            fields = utils.get_object_values(renaming)
            df = df.rename(columns=renaming)
            if format == "csv":
                df.to_csv(file_path, index=False)
            elif format == "excel":
                file_path = f"{utils.get_path_to_base_folder()}/media/{title}.xlsx"
                with pd.ExcelWriter(file_path) as writer:
                    df.to_excel(writer, index=False, sheet_name=f"{self.title}")
            elif format == "pdf":
                pdf, path = self.generate_pdf(utils.df_to_dict(df) ,title, row_title, fields)
                file_path = path
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{title}.{format}')

            if skip_del ==False:
                try:
                    os.remove(file_path)
                except Exception as ex:
                    pp(f"FILE DELETION FAILED: {str(ex)}")
                return response

    
    def generate_pdf(self, data, title=None, row_title="", fields=[]):
        base_path = utils.get_path_to_base_folder()
        company = self.settings.linked_fields.default_company
        report_template = self.get_report_template()
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


        context_data = utils.from_dict_to_object({
            "data": data, 
            "fields": fields, 
            "title": row_title,
            "logo": f"{base_path}/media/{self.object.host}{company.company_logo}",
            "company": company,
            "filters": self.object.filters,
            "doctype": self.object.model,
            "host": self.object.host,
            "settings": self.settings,
            "default_user_company": company,
            "logged_in_user": user,
            "default_theme_color": default_theme_color,
            "default_text_color": default_text_color,
            "default_secondary_color": default_secondary_color,
            "todays_date": dates.today(),
        })

        if download_data_customizer.get(self.object.model):
            download_data_customizer.get(self.object.model)(self.dbms, self.object, context_data)

        html = self.render_template(report_template, context_data)
        file_path = f"{base_path}/media/{title}.pdf"
        weasyprint.HTML(string=html).write_pdf(file_path,stylesheets=[
            'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css', 'static/css/print_layout.css'
        ], page_size='A4 landscape')
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{title}.pdf')
        return response, file_path
        
