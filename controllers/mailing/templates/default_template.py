from controllers.utils import Utils
utils = Utils()

class Default_Template:
    def __init__(self) -> None:
        pass

    @classmethod
    def news_letter_email_template(self,content, member, ssp, subject="", company=utils.from_dict_to_object()):
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
                        background-color: {background_color};
                        padding: 15px 0;
                        text-align: center;
                        color: {text_color};
                    }}
    
                </style>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 100vh; margin: 0 auto; background-color: white; box-sizing: border-box; padding: 0 20px;">
    
                    <!-- Header -->
                    <div style="width: 100%; height: 45px; background-color: {background_color}; color: {text_color}; font-size: 12px; padding-top: 15px;">
                    </div>
                    <h2 style="width: 100%; margin-top: 30px; font-size: 24px; font-weight: 600; color: #151030;">
                        Hello {member},
                    </h2>
                    <p style="font-size: 14px; margin-top: 10px; line-height: 1.6; color: #151030;">
                        You have received a newsletter from <strong>{ssp}</strong>. Please read through to stay updated with our latest news and announcements. Don't be left out!
                    </p>
                    <h3 style="width: 100%; margin-top: 40px; background-color: {background_color}; padding: 15px 0; color: {text_color}; text-align: center;">
                        NEWSLETTER: {subject}
                    </h3>
                    <div style="width: 100%; margin-top: 20px; font-size: 14px; color: #151030; line-height: 1.6; word-break: break-word;">
                        {content}
                    </div>
                    <div class="footer">
                        <small>
                            Powered By <a href="https://hrmis.exams-council.org.zm">ECZ HRMIS</a>
                        </small>
                    </div>
    
                </div>
                
            </body>
            </html>
        """
    @classmethod
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
    @classmethod
    def workflow(cls, data):
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
                    <h2 class="greetings">Greetings {data.approver_names},</h2>
            
                    <p style="margin-bottom: 20px;">
                        This is to inform you that a document '<strong>{data.document_type}</strong>' has been sent for your 
                        <strong>action</strong>. <br>
                        
            
                        <span class="details-title">Workflow Details</span>
                        <hr>
                        <small class="titles">Document Type:</small> <span>{data.document_type}</span> <br>
                        <small class="titles">Document ID/Name:</small> <span>{data.document_name}</span> <br>
                        <small class="titles">Doc Current Status:</small> <span>{data.current_status}</span> <br>
                        <small class="titles">Submitted By:</small> <span>{data.submitted_by}</span> <br>
                        <small class="titles">Submission Date:</small> <span>{data.submission_date}</span> <br>
                        <small class="titles">Comment/Remark:</small> <span>{data.comment}</span> <br>
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
                            {data.sender_names or "N/A"}, <br>
                            {data.sender_department or "N/A"}
                        </div>
                    </p>
                </div>
            </body>
            </html>
        """

        return cls.template(content, f"Workflow Action Required: {data.document_type}", data.company)

    @classmethod
    def workflow_doc_owner(cls, data):
        background_color = "#151030"
        btn_color = background_color
        text_color = "white"
        note_text = """
            Please note that this document is subject to being sent back to the previous approver 
            for corrections/comments or clarifications before it 
            gets to be sent to then next stage/final approval.
        """ if not data.is_final else ""
        final_text = f'concluding its final stage approval with the status of "<strong>{data.to_stage}</strong>"' if data.is_final else "before final approval."
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
                    <h2 class="greetings">Hello {data.owner_name},</h2>
            
                    <p style="margin-bottom: 20px;">
                        This is to inform you that your document '<strong>{data.document_type}</strong>' has progressed from 
                        <strong>{data.from_stage}</strong> to <strong>{data.to_stage}</strong> {final_text}
                        <br><br>
                        {note_text}
                        <br>
            
                        <span class="details-title">Document Details</span>
                        <hr>
                        <small class="titles">Document Type:</small> <span>{data.document_type}</span> <br>
                        <small class="titles">Document ID/Name:</small> <span>{data.document_name}</span> <br>
                        <small class="titles">Doc Current Status:</small> <span>{data.current_status}</span> <br>
                        <small class="titles">Submitted By:</small> <span>{data.submitted_by}</span> <br>
                        <small class="titles">Submission Date:</small> <span>{data.submission_date}</span> <br>
                        <small class="titles">Comment/Remark:</small> <span>{data.comment}</span> <br>
                        <hr>
            
                        To view the progress of the document/comments: <br>
            
                        <div class="link-wrapper">
                            <a class="doc-link" href="{data.doc_url}">
                                <span class="click-text">Click Here</span>
                            </a>  <br>
                        </div>
                    </p>
                </div>
            </body>
            </html>
        """

        return cls.template(content, f"Document Approval Progress: {data.document_type}", data.company)

    @classmethod
    def data_importation(cls, data):
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
                    <h2 class="greetings">Hello!</h2>
            
                    <p style="margin-bottom: 20px;">
                        This is to inform you that data importation process for the document '<strong>{data.file_name}</strong>' has concluded the operation. <br>
                        Below is the summary information of the importation process:
                        
            
                        <span class="details-title">Importation Summary</span>
                        <hr>
                        <small class="titles">Doc Owner:</small> <span>{data.owner}</span> <br>
                        <small class="titles">File Name:</small> <span>{data.file_name}</span> <br>
                        <small class="titles">Document Type:</small> <span>{utils.replace_character(data.model, '_', ' ')}</span> <br>
                        <small class="titles">Importation Status:</small> <span>{data.status}</span> <br>
                        <small class="titles">Total Records:</small> <span style="font-weight:bolder;font-size:20px">{data.total_rows}</span> <br>
                        <small class="titles">Total Successful:</small> <span style="font-weight:bolder;font-size:20px">{data.total_successful}</span> <br>
                        <small class="titles">Total Failed:</small> <span style="font-weight:bolder;font-size:20px; color:red">{data.total_failed}</span> <br>
                        <hr>
                    </p>
                </div>
            </body>
            </html>
        """

        return cls.template(content, f"Data Importation Concluded: {utils.replace_character(data.model, '_', ' ')}", data.company)

