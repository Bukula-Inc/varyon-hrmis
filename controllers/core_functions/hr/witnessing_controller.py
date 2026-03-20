from controllers.utils import Utils

utils = Utils ()

class Witnessing ():
    def __init__(self, core_hr):
        self.core_hr = core_hr
        
    def send_mail_to_witnesses (self, data):
        """"
            Data: {
                company: {
                    default_theme_color,
                    default_secondary_color,
                    default_theme_text_color
                }
                witness_name: str,
                document_type: str,
                document_name: str,
                applicant: str,
                submission_date: str,
                applicant_dept: str
            }
        
        """
        data = utils.from_dict_to_object (data)

        return self.template(self.generate_template(data))


    def template(self,content,subject="", company=utils.from_dict_to_object()):
        background_color = "#151030"
        text_color = "white"
        if company:
            background_color = company.default_theme_color
            text_color = company.default_theme_text_color

        style = "@media screen and (max-width:720px) { .wrapper{width: 100% !important}}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Mail Template</title>
                <style>
                    {style}

                    .footer {{
                        font-size: 0.9em;
                        color: #666666;
                        margin-top: 20px;
                    }}
                </style>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width:60%; min-height: 100vh; margin: 0 auto; background-color: white;">
                    <!-- head -->
                    <div style="width: 100%; height: 45px; background-color: {background_color}; color: {text_color}; font-size: 12px; padding-top: 15px;">
                        <div style="width:90%; height: 100%; margin: auto auto;"></div>
                    </div>
                    <!-- head -->
                    <!-- body section -->
                    <div style="width:90%; min-height: calc(100vh - 10vh); margin: 20px auto;">
                        <h3>{subject}</h3>
                        {content}
                        <div class="footer" style="color:#545351;font-size:12px;">
                            <p>If you did not initiate this action, believe it was not intended for you, or have any concerns regarding your account, please disregard this email or contact our support team for assistance.</p> 
                            <p>&copy; <a href="https://hrmis.exams-council.org.zm">ECZ HRMIS</a>. All rights reserved.</p>
                        </div>
                    </div>
                    <!-- body section -->
                    <!-- footer -->
                    <div style="width: 100%; height: 5vh; background-color: {background_color}; padding-top:15px; ; color: {text_color};">
                        <div style="width:max-content; margin:0 auto;">
                            <small style="color: white; text-decoration: none; font-size: 11px; width: 200px;"> Powered By <a href="https://hrmis.exams-council.org.zm">ECZ HRMIS</a></small>
                        </div>
                    </div>
                    <!-- footer -->
                </div>
            </body>
            </html>
        """
    
    def generate_template (self, data):
        background_color = "#151030"
        btn_color = background_color
        text_color = "white"
        if data.company:
            background_color = data.company.default_theme_color
            btn_color = data.company.default_secondary_color
            text_color = data.company.default_theme_text_color
        content = f"""
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: .9em;
                        line-height: 1.5;
                        color: #333;
                    }}
                    .container {{
                        padding: 20px;
                        background-color: #f9f9f9;
                        border-radius: 10px;
                        max-width: 600px;
                        margin: auto;
                    }}
                    .greetings {{
                        font-weight: bolder;
                        margin-bottom: 20px;
                    }}
                    .details-title {{
                        font-size: 20px;
                        font-weight: bolder;
                        margin-top: 20px;
                        display: block;
                        background-color: {background_color};
                        color:{text_color};
                        padding: 10px 10px;
                        border-radius: 4px;
                    }}
                    .titles {{
                        margin-bottom: 20px;
                        width: 500px !important;
                        padding-right: 10px;
                        font-weight: bolder;
                    }}
                    .signature {{
                        margin-top: 20px;
                        font-weight: bold;
                        font-size: .8em;
                    }}
                    .link-wrapper {{
                        height: 50px;
                        margin-top: 30px;
                    }}
                    .doc-link {{
                        color: {text_color} !important;
                        text-decoration: none !important;
                        border-radius: 10px;
                        padding: 10px 40px;
                        background-color: {btn_color};
                        margin: 10px 0;
                    }}
                    .click-text{{
                        color: {text_color} !important;
                        font-weight: bolder;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="greetings">Greetings {data.witness_name},</h2>
            
                    <p style="margin-bottom: 20px;">
                        This is to inform you that a document '<strong>{data.document_type}</strong>' has been sent for your 
                        <strong>action</strong>. <br>
                        
            
                        <span class="details-title">Witnessing Details</span>
                        <hr>
                        <small class="titles">Document Type:</small> <span>{data.document_type}</span> <br>
                        <small class="titles">Document ID/Name:</small> <span>{data.document_name}</span> <br>
                        <small class="titles">Submitted By:</small> <span>{data.applicant}</span> <br>
                        <small class="titles">Submission Date:</small> <span>{data.submission_date}</span> <br>
                        <small class="titles">Comment/Remark:</small>{data.witness_name} has attached you as a witness to the {data.document_type}. the Document can't processed until you approve <span></span> <br>
                        <hr>
            
                        To view the document, take necessary action: <br>
            
                        <div class="link-wrapper">
                            <a class="doc-link" href="{data.doc_url}">
                                <span class="click-text">Click Here</span>
                            </a>  <br>
                        </div>
            
                        Please take the necessary action at your earliest convenience.
            
                        If you have any questions or need further information, feel free to reach out to {data.sender_email}.
                        <div class="signature">
                            Regards, <br>
                            {data.applicant or "N/A"}, <br>
                            {data.applicant_dept or "N/A"}
                        </div>
                    </p>
                </div>
            </body>
            </html>
        """

        return content