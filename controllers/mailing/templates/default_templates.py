
class Default_Templates:
    def __init__(self) -> None:
        pass

    @classmethod
    def new_user_template(cls, company, host, email, password, user_name, logo=None):
        return f"""
            <div class="wrapper" style="width: 100%; line-height: 1.3em;">
                <div style="width: 100%; color: #151030;">
                    <h3 style="width: 100%; margin: 0 auto; margin-top: 30px;">Hello {user_name}</h3>
                    <p style="font-size: 12px; width: 100%; margin: 0 auto; margin-top: 30px; line-heig">
                        {company} has created a user account for you. To access
                        the system, visit <a href="https://{host}/auth/login" style="color: #ff6a00;">{host}</a>, provide the credentials below to login.
                    </p>
                    <div style="margin-top: 30px;">
                        <table style="border-collapse: collapse; border: 1px gray solid; margin: 0 auto; width: 98%; font-size: 12px;">
                            <tbody>
                                <tr>
                                    <td style="border-right: 1px gray solid; border-bottom: 1px gray solid; padding: 5px; width: 50%;">User Email</td>
                                    <td style="border-bottom: 1px gray solid; padding: 5px;">{email}</td>
                                </tr>
                                <tr>
                                    <td style="border-right: 1px gray solid; padding: 5px;">User Password</td>
                                    <td style="border-bottom: 1px gray solid; padding: 5px;">{password}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        """

    
    
    @classmethod
    def request_otp(cls,  host, otp, user_name, logo=None):
        wrapper = "@media screen and (max-width:750px) { .wrapper{width: 100% !important} .title{font-size: 20px !important;}}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>OTP</title>
                <style>
                    {wrapper}
                </style>
            </head>
            <body style="width:100%; min-height: 100dvh; background-color: #e3e3e3;  padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%;min-height:170px; height: max-content; background-color: #151030; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://startapperp.africa/img/logo/white.svg" alt="" style="width: 120px;">
                    </div>
                    <h3 class="title" style="font-size: 30px; margin: auto; text-align: center;margin-top: 30px;">User OTP Authentication.</h3>
                    <div style="width: 98%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #151030;">
                        <h3 style="width: 80%; margin: 0 auto; margin-top: 30px;">Hello {user_name}</h3>
                        <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 30px;">
                            Please type the OTP code below into your authentication page before proceeding to your portal
                        </p>
                        <div style="margin-top: 30px;">
                            <div class="title" style="width:max-content;font-size:40px; min-width:200px; text-align:center; font-weight:bold; padding: 20px 10px; border-radius:10px;margin:0 auto; background-color:#151030;color:white;">
                                {otp}
                            </div>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #151030;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;"> Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;">
                                    <img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="Varyon" style="width: 70px; margin-top: 10px;">
                                </a>
                            </div>
                            <div style="font-size: 12px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """
    

    @classmethod
    def new_site_registered(cls, company, host, email, password, user_name, logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100%  !important; } .title{font-size: 20px !important;}}"
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>New User</title>
                <style>
                    {wrapper}
                </style>
            </head>
            <body style="width:100%; min-height: 100dvh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%;min-height:170px; height: max-content; background-color: #151030; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{host}{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 30px; margin: auto; text-align: center;margin-top: 30px;">System Preparation Complete</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #151030;">
                        <h3 style="width: 80%; margin: 0 auto; margin-top: 30px;">Hello {user_name}</h3>
                        <p style="font-size: 14px; width: 80%; margin: 0 auto; margin-top: 30px;">
                            <strong> Congratulations!</strong> <br>
                            Varyon has completed preparing your system for {company}. To get yourself started, please visit <a href="https://{host}/auth/login" style="color: #ff6a00;">{host}</a> 
                            and provide the credentials below to login. <br>
                            Thank you for registering with ECZ HRMIS.
                        </p>
                        <div style="margin-top: 30px;">
                            <table style="border-collapse: collapse; border: 1px gray solid; margin: 0 auto; width: 80%; font-size: 12px;">
                                <tbody>
                                    <tr>
                                        <td style="border-right: 1px gray solid; border-bottom: 1px gray solid; padding: 5px; font-weight: bold; width: 50%;">User Email</td>
                                        <td style="border-bottom: 1px gray solid; padding: 5px;">{email}</td>
                                    </tr>
                                    <tr>
                                        <td style="border-right: 1px gray solid; padding: 5px; font-weight: bold;">User Password</td>
                                        <td style="border-bottom: 1px gray solid; padding: 5px;">{password}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div style="width:80%; text-align: center; margin: 0 auto; margin-top: 40px;">
                            <a href="https://{host}/auth/login" style="margin: 0 auto; background-color: #151030; color: white; padding: 10px; text-align: center;text-decoration: none; border-radius: 5px; font-size: 13px;">Click here to login</a>
                        </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #151030;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;"> Powered by</div>
                                <a href="https://www.startapperp.com" style="margin: auto 0;"><img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;"></a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """
