class Default_Templates:
    def __init__(self) -> None:
        pass

    @classmethod
    def notification(cls, first_name, earnings, deductions,  subject,logo=None):
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
                    <h3 style="font-size: 20px; margin: auto; text-align: center; margin-top: 30px;">{subject}</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                        <h3 style="width: 80%; margin: 0 auto; margin-top: 30px;">Dear {first_name},</h3>
                      <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 30px;">
                        We are writing to inform you of some changes to your payroll earnings and deductions. As part of our ongoing efforts to improve our compensation package, we have made changes to your earnings and deductions on your payroll.
                    </p>
                    <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 15px;">Earnings:</p>
                    <ul>
                        <li>{earnings}</li>
                    </ul>
                    <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 15px;">Deductions:</p>
                    <ul>
                        <li>{deductions}</li>
                    </ul>
                    <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 15px;">
                        These changes will be effective starting today and will be reflected in your next paycheck. If you have any questions or concerns, please do not hesitate to reach out to our HR department.
                    </p>
                    <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 15px;">
                        Thank you for your hard work and dedication.
                    </p>
                    <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 15px;">
                        Best regards,
                    </p>
                    <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 15px;">
                        HR Team
                    </p>

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