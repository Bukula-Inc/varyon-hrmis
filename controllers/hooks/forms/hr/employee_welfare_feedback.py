
from controllers.utils.dates import Dates
from controllers.utils import Utils
from controllers.mailing.templates.default_template import Default_Template
utils = Utils()
dates = Dates()
from controllers.mailing import Mailing
throw = utils.throw
pp = utils.pretty_print

def employee_welfare_questions(dbms, object):
    pp(object)
    mailing = Mailing(dbms=dbms, object=object)
    object.doc_status = "Pending"    
    survey_name = object.body['other_survey_welfare']  or object.body['survey_welfare'] 
    get_emp_info = dbms.get_list("Employee", filters={"status": "Active"}, privilege=True)
    
    if get_emp_info:
        emp_list = get_emp_info.data.rows
        for emp in emp_list:
            email = emp['email']
            full_name = emp['full_name']
            
            content = f"""
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 1em;
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
                    .btn {{
                        text-decoration: none;
                        background-color: #151030;
                        color: white !important;
                        border-radius: 10px;
                        padding: 15px 30px;
                        display: inline-block;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Hello {full_name},</h2>
                    <p>We value your opinion! Please take a moment to share your feedback on the <strong>{survey_name}</strong> survey.</p>
                    <h3>Survey Details:</h3>
                    <p><strong>Survey Name:</strong> {survey_name}</p>
                    <p><strong>Purpose:</strong> Your feedback helps us improve employee welfare and work conditions.</p>
                    <p>Alternatively, you can go to the following link:</p>
                    <p>Thank you for your time and valuable input!</p>
                </div>
            </body>
            """

            mail = mailing.send_mail(
                recipient=email,
                subject=f"Your Feedback Matters – {survey_name} Survey",
                body=Default_Template.template(content, f"Employee Feedback Survey: {survey_name}")
            )
