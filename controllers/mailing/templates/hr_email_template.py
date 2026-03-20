class Default_Templates:
    def __init__(self) -> None:
        pass
    @classmethod
    def reverse_consideration(cls, subject, body, logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <style>{wrapper}</style>
            </head> 
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.5em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px"></h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 0.25rem; color: #2b2745;">
                        <div style="min-height: 70vh; display: grid; grid-template-rows: repeat(12, 1fr); width: 80%; margin: auto; row-gap: 2rem;">
                            <div style="grid-row: span 2;">
                                <h3 style="margin: 0 auto; margin-top: 30px; line-height: 1.5em;">
                                    Dear {body['applicant_name']},
                                </h3>
                            </div>
                            <div style="grid-row: span 6;">
                                <p style="text-align: justify; font-size: 15px; line-height: 1.7em; text-indent: 2em;">
                                    We regret to inform you that, after careful reconsideration, we have decided to cancel our previous consideration for the <strong>{body['position']}</strong> role at <strong>{body['company']}</strong> that was previously extended to you.
                                </p>
                                <p style="text-align: justify; font-size: 15px; line-height: 1.7em; text-indent: 2em; margin-top: 1em;">
                                    We appreciate the time you took to interview with us and understand that this news may be disappointing. Please know that this decision is not a reflection on your qualifications or potential as a candidate.
                                </p>
                                <p style="text-align: justify; font-size: 15px; line-height: 1.7em; text-indent: 2em; margin-top: 1em;">
                                    We wish you the very best in your continued job search and future endeavors.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """


    @classmethod
    def recruitment_and_selection(cls, document_type, subject, doc_body, company, adressed_to, emailers_name, job_position, remark_title=0, logo=None,uplodLink="", include_link="http://startappsolutions.com:8000/web/careers/", remark="", oath_of_secrecy = ""):
        add_remark = ""
    
        if doc_body is None:
            doc_body = ""
    
        if remark_title == 1:
            add_remark = "Important Notice"
    
        if include_link:
            include_link = f"""
                    <p style="text-align: center; margin-top: 20px;">
                        <a href="http://{include_link}" 
                            style="background-color: #2b2745; color: white; padding: 10px 20px; text-decoration: none; 
                                    border-radius: 5px; font-weight: bold; display: inline-block;">
                            Download Medical Clearance Required - Click Here
                        </a>
                    </p>
                """
        if uplodLink:
            uplodLink = f"""
                <p style="text-align: center; margin-top: 20px;">
                    <span>After the FIlling of the Downloaded Medical Clearance and successfully get policy clearance. <br />
                        you then now can follow the link by clicking on the Upload Medical and Police Clearance
                    </span>
                    <p style="padding: 10px; margin: 10px 0 10px 0">
                        <a href="http://{uplodLink}" 
                            style="background-color:#09368a; color: white; padding: 10px 20px; text-decoration: none; 
                                    border-radius: 5px; font-weight: bold; display: inline-block;">
                            Upload Medical and Police Clearance
                        </a>
                    </p>
                </p>
            """
        if remark:
            remark = f"""
                <p style="text-align: center; margin-top: 20px;">
                    <a href="{remark}" download
                        style="background-color: #2b2745; color: white; padding: 10px 20px; text-decoration: none; 
                                border-radius: 5px; font-weight: bold; display: inline-block;">
                        Download Medical Clearance Document
                    </a>
                </p>
            """
        if oath_of_secrecy:
            oath_of_secrecy = f"""
                <p style="text-align: center; margin-top: 20px;">
                    <a href="{oath_of_secrecy}" download
                        style="background-color: #2b2745; color: white; padding: 10px 20px; text-decoration: none; 
                                border-radius: 5px; font-weight: bold; display: inline-block;">
                        Download Oath Of Secrecy
                    </a>
                </p>
            """  
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{document_type}</title>
                <style>
                    body {{
                        width: 100%;
                        min-height: 100vh;
                        background-color: #f4f4f4;
                        font-family: 'Arial', sans-serif;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 700px;
                        background: white;
                        margin: 40px auto;
                        padding: 30px;
                        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                        border-radius: 10px;
                    }}
                    .header {{
                        background-color: #2b2745;
                        color: white;
                        text-align: center;
                        padding: 25px;
                        border-top-left-radius: 10px;
                        border-top-right-radius: 10px;
                    }}
                    .header img {{
                        width: 100px;
                    }}
                    .content {{
                        padding: 25px;
                        color: #333;
                        line-height: 1.6;
                    }}
                    .footer {{
                        text-align: center;
                        font-size: 12px;
                        color: gray;
                        padding: 25px;
                        border-top: 1px solid #ddd;
                        margin-top: 20px;
                    }}
                    .footer img {{
                        width: 70px;
                        margin-top: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <img src="https://{logo}" alt="Company Logo">
                        <h2>{document_type}</h2>
                    </div>
            
                    <div class="content">
                        <h3 style="color: #2b2745;">{company} - {document_type}</h3>
                        <p><strong>Subject:</strong> {subject}</p>
                        <p><strong>Dear {adressed_to},</strong></p>
                        <p>We are pleased to inform you that you have been considered for the position of <strong>{job_position}</strong> at <strong>{company}</strong>. Congratulations!</p>
                        <p>As part of the final steps in our hiring process, you are required to undergo a medical examination. Please download the medical clearance form from the link below and proceed with the required examination.</p>
                        <p>Once you have completed the medical examination, kindly submit the required documents to our HR department for further processing.</p>
                        <h4 style="margin-top: 20px;">{add_remark}</h4>
                        <p style="margin-top: 30px;">
                            Best regards, <br>
                            <strong>{emailers_name}</strong>, <br>
                            {job_position}, <br>
                            {company}
                        </p>
                        {include_link}
                        {uplodLink}
                    </div>
            
                    <div class="footer" style="background-color: #2b2745; color: white;">
                        <p>Powered by</p>
                        <a href="https://www.startapperp.com">
                            <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="Startup ERP">
                        </a>
                        <p>&copy; 2024 | All Rights Reserved</p>
                    </div>
                </div>
            </body>
            </html>
        """

        
    @classmethod
    def default_template(cls, document_type, subject, doc_body, company, adressed_to, emailers_name, job_position, remark_title=0, logo=None, include_link=None, remark=""):
        add_remark =""
        link_to_site =""
        if doc_body ==None:
            doc_body =""

        if remark_title ==1:
            add_remark ="Remark"

        if include_link:
           link_to_site= f"""
                <a href={include_link} style="margin: auto 0;">
                    Click here to visit our site for your response.
                </a>
            """

        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px">{document_type}</h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 0.25rem; color: #2b2745;">
                        <div style="min-height: 70vh; display: grid; grid-template-rows: repeat(12, 1fr); width: 80%; margin: auto; row-gap: 2rem;">
                            <div style="grid-row: span 1;">
                                <h3 style="margin: 0 auto; margin-top: 30px; line-height: 1.3em;">
                                    {company} {document_type}: {subject} <br>
                                    Dear {adressed_to},<br>
                                </h3>
                            </div>

                            <div style="grid-row: span 8; margin-top: 0;">
                                <p style="text-indent: 1rem;">
                                    {doc_body} 
                                </p>

                                <h3 style="margin-top: 1rem;">{add_remark}</h3>

                                <p style="text-indent: 1rem;">
                                    {remark}
                                </p>
                                <p style="text-indent: 1rem;">
                                    {link_to_site}
                                </p>
                                
                            </div>

                            <div style="grid-row: span 2; display: flex; align-items: end; height: 100%;">
                                <div style="align-self: end; margin-bottom: 0;">
                                    Best regards,<br>
                                    {emailers_name},<br> 
                                    {job_position} <br>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """   

    @classmethod
    def internal_communications(
        cls,
        document_type,
        subject,
        doc_body,
        company,
        adressed_to,
        remark,
        emailers_name,
        job_position,
        remark_title=0,
        logo=None,
    ):
        add_remark =""
        if remark_title ==1:
            add_remark ="Remark"

        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px">{document_type}</h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 0.25rem; color: #2b2745;">
                        <div style="min-height: 70vh; display: grid; grid-template-rows: repeat(12, 1fr); width: 80%; margin: auto; row-gap: 2rem;">
                            <div style="grid-row: span 2;">
                                <h3 style="margin: 0 auto; margin-top: 30px; line-height: 1.3em;">
                                    {company} {document_type}: {subject} <br>
                                    Dear {adressed_to},<br>
                                </h3>
                            </div>

                            <div style="grid-row: span 8;">
                                <p style="text-indent: 4rem;">
                                    {doc_body} 
                                </p>

                                <h3 style="margin-top: 1rem;">{add_remark}</h3>

                                <p style="text-indent: 2rem;">
                                    {remark}
                                </p>
                            </div>

                            <div style="grid-row: span 2; display: flex; align-items: end; height: 100%;">
                                <div style="align-self: end; margin-bottom: 0;">
                                    Best regards,<br>
                                    {emailers_name},<br> 
                                    {job_position} <br>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """  
    @classmethod
    def annoucement(cls, first_name, announcement, subject,logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>New User</title>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height:170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px;">{subject}</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                        <h3 style="width: 80%; margin: 0 auto; margin-top: 30px;">Hello {first_name}</h3>
                        <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 30px;">{announcement}</p>
                        <div style="width:80%; text-align: center; margin: 0 auto; margin-top: 40px;">
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;"><img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;"></a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """      
   
    @classmethod
    def bulletin(cls, first_name, bulletin, logo=None):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Announcement</title>
        </head>
        <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
            <div class="wrapper" style="width: 60%; min-height:170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                    <img src="https://{logo}" alt="" style="width: 120px;">
                </div>
                <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                    <h3 style="width: 80%; margin: 0 auto; margin-top: 30px;">Hello {first_name}</h3>
                    <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 30px;">{bulletin}</p>
                    <div style="width:80%; text-align: center; margin: 0 auto; margin-top: 40px;">
                    </div>
                </div>
                <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                    <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                        <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                            <div style="margin: auto 0;">Powered by</div>
                            <a href="https://www.startapperp.com" style="margin: auto 0;"><img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;"></a>
                        </div>
                        <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    @classmethod
    def appraisal(cls, appraiser_name, subject,body, logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>New User</title>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height:170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px;">{subject}</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                        <h3 style="width: 80%; margin: 0 auto; margin-top: 30px;">Hello {appraiser_name}</h3>
                        <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 30px;">{body}</p>
                        <div style="width:80%; text-align: center; margin: 0 auto; margin-top: 40px;">
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;"><img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;"></a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
    
    @classmethod
    def job_application(cls, sender, senders_job_title, receiver, job_position, contact,):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""   
            <div style="color: black;">         

                <h2 style="color: black;"> Subject: Acknowledgment of Your Job Application</h2><br>

                <h3 style="color: black;">Dear {receiver},</h3><br>

                <p style="text-indent: 2rem">
                    Thank you for your interest in the {job_position} role. We have successfully received your application materials, including your [].

                    Our hiring team is currently reviewing all applications, and we will contact you if your qualifications align with the requirements for this position. We appreciate the time and effort you put into applying and your interest in joining our team.

                    If you have any further questions or need to update your application, please feel free to reply to this email or contact us at {contact}.

                </p>

                Best regards,<br>
                {sender}<br>
                {senders_job_title}<br>
                {contact}
            </div>
        """ 
    
    # WRIITEN WARNING
    @classmethod
    def case_outcome_warning_mail(cls, sender=None, senders_job_title=None, receiver=None, body=None, company=None, subject=None, document_type=None, logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""   
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px">{document_type}</h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 0.25rem; color: #2b2745;">
                        <div style="min-height: 70vh; display: grid; grid-template-rows: repeat(12, 1fr); width: 80%; margin: auto; row-gap: 2rem;">
                            <div style="grid-row: span-2;">
                                <h3 style="margin: 0 auto; margin-top: 30px; line-height: 1.3em;">
                                    {company} {document_type}: {subject} <br>
                                    Dear {receiver},<br>
                                </h3>
                            </div>

                            <div style="grid-row: span-8; margin-top: 1rem;">
                                <p style="text-indent: 4rem;">
                                    {body} 
                                </p>
                            </div>

                            <div style="grid-row: span 2; display: flex; align-items: end; height: 100%;">
                                <div style="align-self: end; margin-bottom: 0;">
                                    Best regards,<br>
                                    {sender},<br> 
                                    {senders_job_title} <br>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
    @classmethod
    def grievance(cls, sender, receiver, company, body=None):

        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="#" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px"></h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 1rem 2rem; color: #2b2745;">
                        <div style="color: black;">         

                            <h2 style="color: black;"> Subject: Grievance</h2><br>

                            <h3 style="color: black;">Dear {receiver},</h3><br>

                            <p style="width: 70vw;">
                                {body}
                            </p>

                            Best regards,<br>
                            {sender}<br>
                            {company}<br>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
    
    def resolved_grievance(cls, sender, receiver, company, body=None, grieve_data=None):

        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="#" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px"></h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 1rem 2rem; color: #2b2745;">
                        <div style="color: black;">         

                            <h2 style="color: black;"> Subject: Grievance</h2><br>

                            <h3 style="color: black;">Dear {receiver},</h3><br>

                            <p style="width: 70vw;">
                                Your Issue Patterning {grieve_data.grievance_type} has been <b>Resolved</b>
                                {body}<br>
                                <p>Stay Safe!</p>
                            </p>

                            Best regards,<br>
                            {sender}<br>
                            {company}<br>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
    
    @classmethod
    def disciplinary(cls, sender, receiver, company, issue_date, violation_type, insert_date=None,  insert_time=None):
        
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="#" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px"></h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 1rem 2rem; color: #2b2745;">
                        <div style="color: black;">        

                            <h2 style="color: black;"> Subject: Disciplinary</h2><br>

                            <h3 style="color: black;">Dear {receiver},</h3><br>

                            <p style="text-indent: 2rem">
                                I am writing to formally inform you of a grievance related to your conduct on {issue_date}. 
                                This matter has been reviewed, 
                                and it has been determined that disciplinary action may be necessary due to 
                                {violation_type}.

                                The specific concerns are as follows:

                                {violation_type}
                                You are expected to attend a meeting to discuss this matter, 
                                where you will have the opportunity to respond and provide any relevant information. 
                                The meeting is scheduled for:

                                Date: {insert_date}
                                Time: {insert_time}
                                Location: [Insert location]

                                You have the right to bring a representative or a colleague to this meeting for support. 
                                If you have any questions or wish to provide a written response before the meeting, please feel free to do so.

                                It is our goal to handle this matter fairly and professionally, 
                                and we encourage open communication to reach a resolution. 
                                Please confirm your attendance at the meeting.
                            </p>

                            Best regards,<br>
                            {sender}<br>
                            {company}<br>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
    
    @classmethod
    def emp_promotion(cls, sender, receiver, company, promotion):
        
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="#" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px"></h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 1rem 2rem; color: #2b2745;">
                        <div style="color: black;">
                            Dear {receiver or ''},

                            I am writing to formally inform you of your promotion. <br/>

                            This promotion is in recognition of your strong performance, dedication, and the positive contributions you have made to the organization.
                            Your professionalism and commitment to excellence have been greatly appreciated, and we are confident in your ability to succeed.
                            Further information regarding your responsibilities and next steps will be communicated to you shortly. Should you have any questions in the meantime, please do not hesitate to reach out.

                            Congratulations on this well-earned achievement.

                            Sincerely,
                            {sender}
                            {company or ''}

                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
    
    @classmethod
    def basic_template(cls, sender, receiver, company, body, final_greetings=None):

        salutations =""
        if final_greetings ==None:
            salutations="Best regards"
        else:
            salutations =final_greetings
        
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="#" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px"></h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 1rem 2rem; color: #2b2745;">
                        <div style="color: black;">        

                            <h3 style="color: black;">Dear {receiver},</h3><br>

                            {body}

                            {salutations},<br>
                            {sender}<br>
                            {company}<br>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
    

    @classmethod
    def interview_schedule(cls, data):
        background_color = "#151030"
        btn_color = background_color
        text_color = "white"
        note_text = """
            Please be prepared for the interview. The details of the interview are provided below. 
            Ensure that you attend the interview on time.
        """
        interview_text = "Your interview has been scheduled. Please await further communication for your interview schedule."
        
        # Check if data contains company-related information and adjust styles accordingly
        company = data.get('company', None)
        if company:
            background_color = company.get('default_theme_color', background_color)
            btn_color = company.get('default_secondary_color', btn_color)
            text_color = company.get('default_theme_text_color', text_color)
        
        content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Interview Schedule Notification</title>
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
                        color: {text_color};
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
                    .click-text {{
                        color: {text_color} !important;
                        font-weight: bolder;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="greetings">Hello {data.get('owner_name', 'Applicant')},</h2>
    
                    <p style="margin-bottom: 20px;">
                        This is to inform you that your interview for the position of 
                        '<strong>{data.get('position_name', 'N/A')}</strong>' has been scheduled. {interview_text}
                        <br><br>
                        {note_text} 
                        <br>
    
                        <span class="details-title">Interview Details</span>
                        <hr>
                        <small class="titles">Position:</small> <span>{data.get('position_name', 'N/A')}</span> <br>
                        <small class="titles">Interview Date:</small> <span>{data.get('interview_date', 'TBD')}</span> <br>
                        <small class="titles">Interview Time:</small> <span>{data.get('interview_time', 'TBD')}</span> <br>
                        <small class="titles">Location:</small> <span>{data.get('interview_location', 'N/A')}</span> <br>
                        <small class="titles">Interviewer(s):</small> <span>{data.get('interviewer', 'HR Team')}</span> <br>
                        <hr>
    
                        To view more details or reschedule the interview, please click the link below: <br>
    
                        <div class="link-wrapper">
                            <a class="doc-link" href="{data.get('doc_url', 'http://example.com/interview-details')}">
                                <span class="click-text">Click Here</span>
                            </a>  <br>
                        </div>
                    </p>
                </div>
            </body>
            </html>
        """
        return content
    @classmethod
    def interview_schedule_inverviewer_template(cls, content, subject="Interview Schedule", company=None):
        background_color = "#151030"
        btn_color = "#151030"
        text_color = "white"
        logo_url = "/static/images/logo.png"
    
        if company:
            background_color = company.default_theme_color or background_color
            btn_color = company.default_secondary_color or btn_color
            text_color = company.default_theme_text_color or text_color
            if company.logo:
                logo_url = company.logo
    
        wrapper = """
        @media screen and (max-width: 650px) {
            .wrapper { width: 100% !important; }
            .title { font-size: 20px !important; }
            .details-table th, .details-table td { font-size: 13px !important; }
        }
        """
    
        # Applicant rows
        applicant_rows = ""
        for applicant in content.get("applicant", []):
            applicant_rows += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px;">{applicant.get("name", "")}</td>
                <td style="padding: 10px;">{applicant.get("interview_date", "N/A")}</td>
                <td style="padding: 10px;">{applicant.get("form_time", "N/A")}</td>
                <td style="padding: 10px;">{applicant.get("to_time", "N/A")}</td>
            </tr>
            """
    
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
            <style>{wrapper}</style>
        </head>
        <body style="margin:0; padding:0; background-color:#f3f3f3; font-family: 'Poppins', sans-serif;">
    
            <div class="wrapper" style="width:60%; margin: 40px auto; background: {background_color}; color: {text_color}; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.2); overflow:hidden;">
                
                <div style="padding: 30px; text-align:center;">
                    <img src="{logo_url}" alt="Company Logo" style="width: 120px;">
                    <h2 style="margin-top: 20px; font-size: 26px; color: {text_color};">Interview Schedule 📋</h2>
                </div>
    
                <div style="background: #ffffff; padding: 30px; color: #151030;">
                    <h3 style="margin-top: 0;">Dear {content['owner_name']},</h3>
                    <p style="font-size: 14px; line-height: 1.6;">
                        You are scheduled to conduct interviews for the following applicants. Kindly review the details below:
                    </p>
    
                    <div style="margin-top: 25px;">
                        <h4 style="color: {btn_color}; margin-bottom: 10px;">📍 Interview Location:</h4>
                        <div style="margin-top: 30px; text-align:left;">
                            <h2 style="padding: 12px 25px; background: linear-gradient(135deg, {btn_color}, #ffffff); color: #ffffff; border-radius: 6px; text-decoration: none; font-weight: 500;">{content.get('interview_location', '#')}</h2>
                        </div>
    
                        <h4 style="color: {btn_color}; margin-top: 20px; margin-bottom: 10px;">👥 Applicants:</h4>
                        <table class="details-table" style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                            <thead>
                                <tr style="background-color: #f0f0f0; color: #151030;">
                                    <th style="padding: 10px; text-align: left;">Name</th>
                                    <th style="padding: 10px; text-align: left;">Date</th>
                                    <th style="padding: 10px; text-align: left;">From Time</th>
                                    <th style="padding: 10px; text-align: left;">From Time</th>
                                   
                                </tr>
                            </thead>
                            <tbody>
                                {applicant_rows}
                            </tbody>
                        </table>
    
                    </div>
                    <p style="font-size: 14px; line-height: 1.6;">
                        If you are unable to attend physically the link to join virtually is below:
                    </p>
                    <div style="margin-top: 30px; text-align:left;">
                        <a href="{content.get('interview_link')}" style="padding: 12px 25px; background: linear-gradient(135deg, {btn_color}, #ffffff); color: #ffffff; border-radius: 6px; text-decoration: none; font-weight: 500;">Join virtually</a>
                    </div>
                </div>
    
                <div style="padding: 20px 30px; background: #fff; border-top: 1px solid #ddd; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                    <div style="display: flex; align-items: center; font-size: 12px;">
                        <span>Powered by&nbsp;</span>
                        <a href="https://www.startappsolutions.com/auth/login">
                            <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="Varyon" style="width: 70px; margin-top: 5px;">
                        </a>
                    </div>
                    <div style="font-size: 12px;">&copy; 2024 | All Rights Reserved</div>
                </div>
    
            </div>
        </body>
        </html>
        """
    @classmethod
    def interview_schedule_inverviewee_email_template(cls, interviewee_content, subject="Interview Invitation", company=None):
        background_color = "#151030"
        btn_color = "#151030"
        text_color = "white"
        logo_url = "/static/images/logo.png"
    
        if company:
            background_color = company.default_theme_color or background_color
            btn_color = company.default_secondary_color or btn_color
            text_color = company.default_theme_text_color or text_color
            if company.logo:
                logo_url = company.logo
    
        wrapper = """
        @media screen and (max-width: 650px) {
            .wrapper { width: 100% !important; }
            .title { font-size: 20px !important; }
            .details-list li { font-size: 13px !important; }
        }
        """
    
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
            <style>{wrapper}</style>
        </head>
        <body style="margin:0; padding:0; background-color:#f3f3f3; font-family: 'Poppins', sans-serif;">
    
            <div class="wrapper" style="width:60%; margin: 40px auto; background: {background_color}; color: {text_color}; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.2); overflow:hidden;">
                
                <div style="padding: 30px; text-align:center;">
                    <img src="{logo_url}" alt="Company Logo" style="width: 120px;">
                    <h2 style="margin-top: 20px; font-size: 26px; color: {text_color};">Congratulations! 🎉</h2>
                </div>
    
                <div style="background: #ffffff; padding: 30px; color: #151030;">
                    <h3 style="margin-top: 0;">Dear {interviewee_content['applicant']},</h3>
                    <p style="font-size: 14px; line-height: 1.6;">
                        We are pleased to inform you that you have been shortlisted for the position of 
                        <strong>{interviewee_content['position_name']}</strong>. We would like to invite you to attend an interview as part of the next stage in our recruitment process.
                    </p>
    
                    <div style="margin-top: 25px;">
                        <h4 style="color: {btn_color}; margin-bottom: 10px;">🗓️ Interview Schedule:</h4>
                        <ul class="details-list" style="list-style: none; padding-left: 0; font-size: 14px;">
                            <li><strong>Position:</strong> {interviewee_content['position_name']}</li><br>
                            <li><strong>Date:</strong> {interviewee_content.get("interview_date", "Monday, 6th May 2025")}</li><br>
                            <li><strong>Time:</strong> {interviewee_content.get("form_time", "10:00 AM")} to {interviewee_content.get("to_time", "11:00 AM")}</li><br>
                            <li><strong>Location:</strong> {interviewee_content['interview_location']}</li>
                        </ul>
                    </div>
    
                    <div style="margin-top: 30px;">
                        <p style="font-size: 14px; line-height: 1.6;">
                            Please ensure you are available at least 10 minutes before your scheduled time. Should you have any questions, feel free to contact our HR team.
                        </p>
                        <p style="font-size: 14px; line-height: 1.6;">
                            We look forward to speaking with you and learning more about your qualifications.
                        </p>
                    </div>
                </div>
    
                <div style="padding: 20px 30px; background: #fff; border-top: 1px solid #ddd; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                    <div style="display: flex; align-items: center; font-size: 12px;">
                        <span>Powered by&nbsp;</span>
                        <a href="https://www.startappsolutions.com/auth/login">
                            <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="Varyon" style="width: 70px; margin-top: 5px;">
                        </a>
                    </div>
                    <div style="font-size: 12px;">&copy; 2024 | All Rights Reserved</div>
                </div>
    
            </div>
        </body>
        </html>
        """
    @classmethod
    def charge_notice(cls, sender, receiver, company, offence, charger_contact):
        
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Memo</title>
                <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="#" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px"></h3>
                    <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 1rem 2rem; color: #2b2745;">
                        <div style="color: black;">
                            Dear {receiver or ''},

                           This email is to formally notify you that you have been charged with an offence of {offence}.

                            Please note that this charge is being taken seriously and will be addressed in accordance with the company's disciplinary procedures. You are required to provide a statement by filling a statement form within a period of 5 working days.
                            You will have the opportunity to respond to the charge and present any relevant information or evidence during the investigation process.
                            We will schedule a meeting on [date and time] to discuss the matter in detail. You are entitled to have a representative or support person present at this meeting if you wish.
                            Until the matter is resolved, we ask that you maintain confidentiality regarding this process.
                            If you have any questions or need clarification, please contact {sender} at {charger_contact}.

                            Sincerely,
                            {sender}
                            {company or ''}

                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """ 
    
    # @classmethod
    # def charge_notice(cls, sender, receiver, company, case, employee_of_subject, offence, link_to_declaration_form):
        
    #     wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
    #     return f"""
    #         <!DOCTYPE html>
    #         <html lang="en">
    #         <head>
    #             <meta charset="UTF-8">
    #             <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #             <title>Memo</title>
    #             <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
    #         </head>
    #         <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
    #             <div class="wrapper" style="width: 60%; min-height: 170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
    #                 <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
    #                     <img src="#" alt="" style="width: 120px;">
    #                 </div>
    #                 <h3 style="font-size: 30px; margin: auto; text-align: center; margin-top: 30px; margin-bottom: 20px"></h3>
    #                 <div style="min-height: 70vh; width: 100%; margin-top: 0.3rem; background-color: #ffffff; padding: 1rem 2rem; color: #2b2745;">
    #                     <div style="color: black;">
    #                         Dear {receiver or ''},

    #                         This email is to formally notify you that you have been selected to be part of disciplinary a committee. .

    #                         The committee is being created for the {case} {offence} involving {employee_of_subject}. In accordance with the disciplinary and grievances procedures code, you are required to provide a declaration if you have interest in the case. 
    #                         To do so, please follow the link below.

    #                         <a href="{link_to_declaration_form}">have interest</a>
    #                         <a href="{link_to_declaration_form}">have no interest</a>

    #                         Sincerely,
    #                         {sender}
    #                         {company or ''}

    #                     </div>
    #                 </div>
    #                 <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
    #                     <div style="width: 80%; margin: 0 auto; border-top: 1px solid gray; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
    #                         <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
    #                             <div style="margin: auto 0;">Powered by</div>
    #                             <a href="https://www.startapperp.com" style="margin: auto 0;">
    #                                 <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;">
    #                             </a>
    #                         </div>
    #                         <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
    #                     </div>
    #                 </div>
    #             </div>
    #         </body>
    #         </html>
    #     """ 
    


    # @classmethod
    # def basic_template(cls, sender, receiver, company, body, final_greetings=None):

    #     salutations =""
    #     if final_greetings ==None:
    #         salutations="Best regards"
    #     else:
    #         salutations =final_greetings
        
    #     wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
    #     return f"""
    #         <!DOCTYPE html>
    #             <html lang="en">
    #                 <head>
    #                     <meta charset="UTF-8">
    #                     <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #                     <title>{name}</title>
    #                     <script src="/static/js/tailwindcss.js"></script>
    #                     <link rel="stylesheet" href="/static/css/print_layout.css">
    #                     <!-- <script  src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script></head> -->
    #                 </head>
    #                 <body class="h-screen w-screen flex justify-center items-center p-4">
    #                     <div class="payslip border text-[10px] border-black max-w-3xl mx-auto text-sm">
    #                         <div class="p-3 h-[80px] flex items-center justify-between  gap-3">
    #                             <div class="h-[60px] w-[60px] overflow-hidden">
    #                                 <img src="http://{full_url}/{linked_fields.get('company').get('company_logo')}" class="logo" alt="">
    #                             </div>
    #                             <div class="w-[calc(100%-60px)] text-[12px]">
    #                                 <div class="flex w-full justify-center items-center">
    #                                     <div class="w-full flex justify-between text-center font-bold">
    #                                         <div class="w-[70%] flex justify-center">EXAMINATIONS COUNCIL OF ZAMBIA</div>
    #                                         <div class="flex justify-end text-[10px]">CURRENCY: {currency}</div>
    #                                     </div>
    #                                 </div>
    #                                 <div class="flex w-full justify-center border-t border-black pt-1 items-center">
    #                                     <div class="flex w-full font-bold justify-between">
    #                                         <div class="w-[70%] flex justify-center">Pay Statement For {to_date or '-'}</div>
    #                                         <div class="w-[30%] flex justify-end text-[10px]">EXCH. RATE: {convertion_rate or '-'}</div>
    #                                     </div>
    #                                 </div>
    #                             </div>
    #                         </div>
    #                         <div class="h-max p-1 w-full border border-slate-700/60">
    #                             <div class="grid grid-cols-12 border border-black">
    #                                 <div class="col-span-4 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Emp Name: <br> </b> {employee_names or '-'}</div>
    #                                 <div class="col-span-2 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Emp No: <br> </b> {employee or '-'}</div>
    #                                 <div class="col-span-2 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">NRC No: <br> </b>{linked_fields.employee.id_no or '-'}</div>
    #                                 <div class="col-span-2 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Eng. Date: <br> </b>{linked_fields.employee.date_of_joining or '-'}</div>
    #                                 <div class="col-span-2 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Basic: <br> </b>{utils.thousand_separator(basic_pay) or '-'}</div>
    #                             </div>
                                
    #                             <div class="grid grid-cols-6 border border-black">
    #                                 <div class="border-r border-black pl-1 text-[8px]"><b class="text-[8px]">Taxable: <br> </b>{utils.thousand_separator(gross) or '-'}</div>
    #                                 <div class="border-r border-black pl-1 text-[8px]"><b class="text-[8px]">Pay YTD: <br> </b>{utils.thousand_separator(ytd_net) or '-'}</div>
    #                                 <div class="border-r border-black pl-1 text-[8px]"><b class="text-[8px]">Tax Paid YTD: <br></b> {utils.thousand_separator(ytd_tax) or '-'}</div>
    #                                 <div class="border-r border-black pl-1 text-[8px]"><b class="text-[8px]">NAPSA YTD: <br> </b> {utils.thousand_separator(ytd_napsa) or '-'}</div>
    #                                 <div class="border-r border-black pl-1 text-[8px]"><b class="text-[8px]">Soc. Sec. No: <br> </b>{linked_fields.employee.napsa or '-'}</div>
    #                                 <div class="border-r border-black pl-1 text-[8px]"><b class="text-[8px]">Leave Days: <br> </b>{utils.thousand_separator(current_leave_value) or '-'}</div>
    #                             </div>
                                
    #                             <div class="grid grid-cols-12 border border-black">
    #                                 <div class="col-span-2 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Taxable This Month: </b></div>
    #                                 <div class="col-span-3 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Pension (PLA) YTD: <br> </b>{utils.thousand_separator(ytd_private_pension) or '-'}</div>
    #                                 <div class="col-span-3 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Gross Pay YTD: <br> </b>{utils.thousand_separator(ytd_gross) or '-'}</div>
    #                                 <div class="col-span-2 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Print Date: <br></b>{utils.today ()}</div>
    #                                 <div class="col-span-2 pl-1 border-r border-black text-[8px]"><b class="text-[8px]">Incremental Month: <br></b>{utils.thousand_separator(incremental) or '-'}</div>
    #                             </div>
                                
    #                             <div class="salary-components mb-2 bg-slate-300">
    #                                 <div class="bg-slate-400 grid grid-cols-2 gap-1 mt-1">
    #                                     <div class="bg-transparent">
    #                                         <div class="grid grid-cols-12 text-[8px] text-black gap-1 font-bold px-2">
    #                                             <div class="col-span-4 text-[8px] ">DEDUCTIONS</div>
    #                                             <div class="col-span-3 text-[8px] text-center">Outstanding <br>Months</div>
    #                                             <div class="col-span-3 text-[8px] text-center">Balance</div>
    #                                             <div class="col-span-2 text-[8px] text-center font-bold">This Month</div>
    #                                         </div>
    #                                     </div>
    #                                     <div class="bg-transparent">
    #                                         <div class="grid grid-cols-12 gap-1 font-bold text-black px-2">
    #                                             <div class="col-span-5 text-[8px]">INCOMES</div>
    #                                             <div class="col-span-4 text-[8px] text-center">Units</div>
    #                                             <div class="col-span-3 text-[8px] text-center font-bold">This Month</div>
    #                                         </div>
    #                                     </div>
    #                                 </div>
    #                                 <div class="grid grid-cols-2 gap-1 mt-1 p-1">
    #                                     <div class="bg-white">
    #                                         {if deductions %}
    #                                             {% for deduction in deductions %}
    #                                                 <div class="grid grid-cols-12 gap-1 text-[8px] py-1 px-2">
    #                                                     <div class="col-span-4">{ deduction.get("deduction") or '-' }</div>
    #                                                     <div class="col-span-3 text-center">{ utils.thousand_separator(deduction.get("outstanding")) or '0' }</div>
    #                                                     <div class="col-span-3 text-center">{ utils.thousand_separator(deduction.get("balance")) or '0.00' }</div>
    #                                                     <div class="col-span-2 text-center text-[8px] font-bold"></div>
    #                                                 </div>
    #                                             {% endfor %}
    #                                         {% endif %}
    #                                     </div>
    #                                     <div class="bg-white">
    #                                         {%if earnings %}
    #                                             {% for earning in earnings %}
    #                                                 <div class="grid grid-cols-12 gap-1 text-[8px] py-1 px-2">
    #                                                     <div class="col-span-5">{ earning.get("earning") }</div>
    #                                                     <div class="col-span-4 text-center">{ earning.get("units")  or '{1}' }</div>
    #                                                     <div class="col-span-3 text-center text-[8px] font-bold"></div>
    #                                                 </div>
    #                                             {% endfor %}
    #                                         {% endif %}
    #                                     </div>
    #                                 </div>
    #                             </div>
                                
    #                             <div class="grid grid-cols-2 border border-black ">
    #                                 <div class="col-span-1">
    #                                     <div class="w-full grid grid-cols-8">
    #                                         <div class="col-span-2 border-r pl-1 border-black text-[8px]"><b class="text-[8px]">Grade: <br> </b>{salary_grade or '-'}</div>
    #                                         <div class="col-span-2 border-r pl-1 border-black text-[8px]"><b class="text-[8px]">Pay Point: <br> </b>{pay_point or '-'}</div>
    #                                         <div class="col-span-4 border-r pl-1 border-black text-[8px]"><b class="text-[8px]">Total Deductions: <br> </b> {utils.thousand_separator(total_deductions) or '-'}</div>
    #                                     </div>
    #                                 </div>
    #                                 <div class="col-span-1">
    #                                     <div class="w-full grid grid-cols-8">
    #                                         <div class="col-span-2 border-r border-black text-[8px]"></div>
    #                                         <div class="col-span-2 border-r border-black text-[8px]"></div>
    #                                         <div class="col-span-4 border-r border-black text-[8px]"><b class="text-[8px]">Total Incomes: <br> </b> {utils.thousand_separator(total_earnings) or '-'}</div>
    #                                     </div>
    #                                 </div>
    #                             </div>
    #                             <div class="grid grid-cols-3 border border-black">
    #                                 <div class="col-span-1 border-r pl-1 border-black text-[8px]"><b class="text-[8px]">Dept: <br></b> {department or '-'}</div>
    #                                 <div class="col-span-1 border-r pl-1 border-black text-[8px]"><b class="text-[8px]">Job: <br></b> {designation or '-'}</div>
    #                                 <div class="col-span-1 border-r pl-1 border-black text-[8px]"><b class="text-[8px]">Net Pay (Bank): <br></b>{linked_fields.employee.bank_name or '-'}</div>
    #                             </div>
                                
    #                             <div class="grid grid-cols-8 border border-black">
    #                                 <div class="border-r pl-1 border-black col-span-2 text-[8px]"><b class="text-[8px]">Bank Name: <br></b>{linked_fields.employee.bank_name or '-'}</div>
    #                                 <div class="border-r pl-1 border-black col-span-2 text-[8px]"><b class="text-[8px]">Acc No: <br></b>{linked_fields.employee.account_no or '-'}</div>
    #                                 <div class="border-r pl-1 border-black col-span-4 text-[8px]"><b class="text-[8px]">ECZ HQs: <br></b>{company or '-'}</div>
    #                             </div>
    #                         </div>
    #                     </div>
    #                 </body>
    #             </html>
    #     """ 

        
    @classmethod
    def joboffer_template(cls, document_type: str="", subject: str="", doc_body: dict={}, company: str ="", adressed_to: str="", emailers_name: str="", job_position: str ="", remark_title: int=0, logo=None, include_link=None, remark: str=""):
   
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""<!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Job Offer</title>
            <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
            </head>
            <body class="w-full bg-[#e3e3e3] p-0 m-0 font-sans">
                <div class="wrapper w-3/5 min-h-[170px] h-max bg-[#2b2745] text-white mx-auto overflow-hidden leading-[1.3em]">
                    
                    <div class="w-4/5 mx-auto mt-8">
                        <img src="https://{logo}" alt="Company Logo" class="w-[120px]" />
                    </div>

                    <h3 class="text-[2rem] text-center font-semibold mx-auto text-center mt-8 mb-5">{document_type}</h3>

                    <div class="min-h-[70vh] w-full mt-1 bg-white p-1 text-[#2b2745]">
                        <div class="min-h-[70vh] grid grid-rows-7 w-4/5 mx-auto gap-y-8">
                        
                            <div class="row-span-1">
                                <h3 class="mx-auto mt-8 leading-[1.3em]">
                                    <div class="font-semibold text-[2rem] underline">{company} {document_type}: {subject}</div> <br />
                                    Dear <strong>{{adressed_to}}</strong>,<br />
                                </h3>
                            </div>

                            <div class="row-span-5">
                                <main class="mt-6 text-gray-700">

                                    <p class="mt-4">
                                        Congratulations! We're delighted to offer you the position of 
                                        <strong>{{job_position}}</strong> at <strong>{{company}}</strong>.
                                    </p>

                                    <p class="mt-4">
                                        Please find your official <strong>Appointment Letter</strong> attached to this email. 
                                        It contains detailed information about your role, start date, and other 
                                        terms of employment.
                                    </p>

                                    <p class="mt-4">
                                        We kindly ask you to review the document carefully and confirm your acceptance of this 
                                        offer by clicking the button below or replying to this email.
                                    </p>

                                    <div class="mt-8 text-sm">
                                        <p>
                                            <strong>Quick reply:</strong> You can reply to this email with 
                                            <code>ACCEPT</code> or <code>DECLINE</code>.
                                        </p>
                                    </div>

                                    <p class="mt-6">Sincerely,</p>
                                </main>
                            </div>

                            <div class="flex items-end h-full">
                                <div class="self-end mb-0">
                                    Best regards,<br />
                                    {emailers_name},<br />
                                    {job_position} <br />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="w-full mx-auto bg-white h-[10vh] text-[#2b2745]">
                        <div class="w-4/5 mx-auto border-t border-gray-400 pt-1 grid grid-cols-[1fr_2fr]">
                            <div class="text-[12px] grid grid-cols-2">
                                <div class="my-auto">Powered by</div>
                                    <a href="https://www.startapperp.com" class="my-auto">
                                        <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="Startapp Logo" class="w-[70px] mt-2.5" />
                                    </a>
                                </div>
                                <div class="text-[12px] mt-0.5 text-right">
                                    &copy; {{year}} | All Rights Reserved
                                </div>
                            </div>
                        </div>
                    </div>
            </body>
            </html>

        """   
                