
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
from controllers.utils import Utils
from controllers.utils.dates import Dates

utils = Utils()
dates = Dates()

pp = utils.pretty_print
throw = utils.throw



class Mailing:
    def __init__(self,dbms,object=None):
        self.dbms = dbms
        self.object = object
        # self.config = utils.from_dict_to_object ()
        # email_config = self.__get_email_config()
        # self.config = email_data
        # ============================== to be updated later ===================
        # self.server_name = "mail.exams-council.org.zm"
        self.email_address = "hradmin@exams-council.org.zm"
        self.server_name = "192.9.200.33"
        self.email_password = "12345@abc"
        self.port_no = 587
        # self.email_address = "admin@startappsolutions.com"
        # self.server_name = "smtp.office365.com"
        # self.email_password = "erpteam@probase"

        
    def __get_email_config(self):
        email_config = self.dbms.get_doc("Email_Config", "Email Config", privilege=True)
        if email_config.status != utils.ok:
            throw(f'Failed to get email configuration: {email_config.error_message}')
        return email_config

    def send_mail(self,  recipient, subject, body, cc=None, attachment=None):
        MESSAGE = MIMEMultipart("alternative")
        MESSAGE["subject"] = f"{subject}"
        MESSAGE["To"] = recipient
        MESSAGE["From"] = self.email_address
        MESSAGE.preamble = """Your mail reader does not support the report format. Please visit us online!"""
        if cc:
            if isinstance(cc, list):
                MESSAGE["Cc"] = ", ".join(cc)
            else:
                MESSAGE["Cc"] = cc

        if attachment and type(attachment) ==str:             
            try:
                path =""
                if utils.get_path_to_base_folder() not in attachment:
                    path  = f"{utils.get_path_to_base_folder()}{attachment}"
                else:
                    path =attachment
                file_name =os.path.basename(path)

                with open(path, "rb") as attachment_path:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment_path.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={file_name}',
                    )
                    MESSAGE.attach(part)
            except Exception as e:
                pp(f"An Error ocurred {e}")

        try:
            HTML_BODY = MIMEText(body, "html")
            MESSAGE.attach(HTML_BODY)
            server = smtplib.SMTP(f"{self.server_name}:{self.port_no}")
            # Credentials (if needed) for sending the mail
            password = self.email_password
            server.starttls()
            server.login(self.email_address, password)
            server.sendmail(self.email_address, recipient, MESSAGE.as_string())
            server.quit()
            
            return  utils.respond(utils.ok, "Email sent successfully!")
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"{e}")