class Auth_Email_Templates:
    def __init__(self) -> None:
        pass
    @classmethod
    def password_reset_template (cls, user):
        print (user)
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100%}}"
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Appointment Confirmation</title>
            <style>
                {wrapper}
            </style>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #172554; color: #FFFFFF;">
            <div class="wrapper" style="max-width: 28rem; width: 80%; margin: 0 auto; padding: 2rem;">
                <img src="your_logo.png" alt="Your Logo" style="display: block; margin: 0 auto; width: 6rem; height: auto; margin-bottom: 1.5rem;">
                <h2 style="text-align: center; font-size: 1.875rem; font-weight: 800; margin-top: 0; margin-bottom: 0.75rem;">Startapp</h2>
                <div style="background-color: rgba(255, 255, 255, 0.9); border-radius: 1rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); color: #FFFFFF; overflow: hidden;">
                    <div style="padding: 1.5rem;">
                        <h1 style="font-size: 1.875rem; font-weight: 800; margin-bottom: 1rem; color: #172554; text-align: center;">Password Reset</h1>
                        <div style="margin-bottom: 1rem; color: #172554;">
                            <p style="margin-bottom: 1rem;">Dear {user['first_name']} {user['last_name']},</p>
                            <p style="margin: 1rem 0;"></p>
                            <a href="{user['link']}" style="display: inline-block; background-color: #6B7280; color: #FFFFFF; font-size: 1rem; font-weight: 700; text-decoration: none; padding: 0.5rem 1.5rem; border-radius: 0.25rem; text-align: center;">Reset Password</a>
                        </div>
                    </div>
                    <footer style="text-align: center; color: #6B7280; margin-top: 2rem;">
                        <p>&copy; 2024 PBS. All rights reserved.</p>
                    </footer>
                </div>
            </div>
        </body>
        </html>
        """