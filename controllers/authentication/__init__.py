import re
from django.contrib.auth.hashers import check_password, make_password
from controllers.mailing import Mailing
from controllers.mailing.templates.default_template import Default_Template
from controllers.utils import Utils
from controllers.utils.dates import Dates
from controllers.utils.jwt import JWT
from controllers.core_functions.core.user_controller import User_Controller
# import jwt
from django.conf import settings

jwt = JWT()

utils = Utils ()
pp = utils.pretty_print
throw = utils.throw
dates = Dates()

class Authentication:
    def __init__(self):
        self.exception_paths = [
            "/app/fuel_master/fuel_auth",
            "/app/fuel_master/fuel_portal",
        ]

    def create_auth_trail(self, user=None, message="", status="Submitted", email="", password="", token=None):
        return self.dbms.create("Auth_Trail",{
            "user":user.name if user else None, 
            "token": token,
            "activity_type": "Login",
            "activity_time": dates.time(),
            "first_name":user.first_name if user else "", 
            "last_name":user.last_name if user else "",
            "email":email,
            "password":password,
            "status": status,
            "message": message
        }, privilege=True, create_trail=False)



    def login (self, dbms, data, is_company_switching=False, company=None):
        self.tenant = dbms.tenant_id
        self.dbms = dbms
        try: 
            email = data.email
            password = data.password
            results = dbms.get_users(id=email, fetch_by_email=True, fetch_password=True)
            if results.status == utils.ok:
                user = results.data
                message = ""
                if user:
                    if user.disabled == 1:
                        message = "This user account is disabled!"
                        self.create_auth_trail(user,message, "Rejected",email)
                        return utils.respond(utils.unauthorized, message )
                    elif user.status != "Active":
                        message = "This user account is not fully approved to access the system"
                        self.create_auth_trail(user,message, "Rejected", email)
                        return utils.respond(utils.unauthorized, message)
                    else:
                        user.tenant = self.tenant
                        # get user dashboard url
                        if check_password (data.password, user.password):
                            dbms.current_user = user
                            dbms.current_user_id = user.id
                            user_controller = User_Controller(dbms, user.id, None)
                            user_content = user_controller.get_user_default_dashboard()
                            user_content.status == utils.ok or utils.throw(f"Failed to get user info: {user_content.error_message}")
                            usr_dashboard = user_content.data
                            user.company_id = ""

                            if is_company_switching:
                                if not company:
                                    throw("Please provide company for switching!")
                                else:
                                    user.default_company = company
                                    user.tenant = f"{dbms.tenant_db}&%{dbms.tenant_id}"
                                    
                            usr_company = dbms.get_doc("Company",user.default_company, privilege=True, fetch_linked_fields=False, fetch_linked_tables=False)
                            if usr_company.status == utils.ok:
                                user.company_id = usr_company.data.id

                            token = jwt.generate_token(user)
                            trail = self.create_auth_trail(user, message, "Submitted",email, "", token)
                            if trail.status == utils.ok:
                                return utils.respond(utils.ok, {"token": token, "dashboard": usr_dashboard.dashboard, "url": usr_dashboard.url})
                            else:
                                return utils.respond(utils.internal_server_error, f"Failed to create authentication trail: {trail.error_message}")
                        message = "Invalid credentials"
                        trail = self.create_auth_trail(user,message, "Rejected",email, password)
                        return utils.respond(utils.unauthorized, message)
            message = "Account not recognized!"
            self.create_auth_trail(user,message, "Rejected", email, password)
            return utils.respond(utils.unauthorized, message)
        except Exception as e:
            message = f'Error during login: {e}'
            self.create_auth_trail(user,message, "Rejected", email, password)
            return utils.respond(utils.internal_server_error, message)
        

    
    def validate_request(self, request):
        path = request.path
        decoded_data = utils.from_dict_to_object()
        if (self.find_app_from_path(path, "app") or self.find_app_from_path(path, "api")) and path not in self.exception_paths:
            cookie = request.headers.get("Cookie")
            api_key = request.headers.get("Api-Key")
            if api_key:
                try:
                    decoded_api = utils.decode_client_api_key(api_key)
                    tenant_db = re.split("[&%]", decoded_api.get("tnt"))
                    if tenant_db:
                        request.tenant_db = tenant_db[0]
                        decoded_data.tenant_db = request.tenant_db
                        decoded_data.tenant_id = tenant_db[2]
                        request.api_key = api_key
                        return utils.respond(utils.ok, decoded_data)
                except Exception as e:
                    return utils.respond(utils.unauthorized, str(e))
            try:
                if cookie:
                    cookie_str = ""
                    is_api_key = False
                    if "lite_user" in cookie or "api_key=" in cookie:
                        if "lite_user" in cookie:
                            cookie_str = cookie.split('_user=')[1]
                        elif "api_key=" in cookie:
                            is_api_key = True
                            cookie_str = cookie.split('i_key=')[1]
                    if cookie_str:
                        token = cookie_str 
                        data = utils.from_dict_to_object()
                        # if a cookie is used to authenticate.
                        if not is_api_key:
                            decoded_token = jwt.decode_token(token, settings.SECRET_KEY)
                            data = utils.from_dict_to_object(decoded_token.get("data"))

                        # if token is used to authenticate.
                        else:
                            decoded_token = utils.decode_client_api_key(token)
                            # if it was a portal authentication
                            if decoded_token.api_key:
                                tenant_decoded_api_key = utils.decode_client_api_key(decoded_token.api_key)
                                if tenant_decoded_api_key.tnt:
                                    data.tnt = tenant_decoded_api_key.tnt
                        if data:
                            request.tenant_id = data.tnt
                            tenant_db = re.split("[&%]", request.tenant_id)
                            if tenant_db:
                                request.tenant_db = tenant_db[0]
                                decoded_data.tenant_db = request.tenant_db
                                request.tenant_id = tenant_db[2]
                                decoded_data.tenant_id = request.tenant_id
                                decoded_data.token = data
                            request.jwt_token = decoded_token
                        return utils.respond(utils.ok, decoded_data)
                else:
                    return utils.respond(utils.ok, {"message": "COOKIE NOT FULLY VALIDATED!"})
            except Exception as e:
                return utils.respond(utils.internal_server_error, f"{e}")
        return utils.respond(utils.ok, utils.from_dict_to_object({}))
    
    def find_app_from_path (self, string, word):
        return word in string
    
    

    def validate_password_reset(self, dbms, data):
        from controllers.tenant import Tenant_Controller
        tc = Tenant_Controller()
        try:
            if not data.email:
                return utils.respond(utils.not_found, "Email required!")
            if not data.reset_code:
                return utils.respond(utils.not_found, "Reset Code is required!")
            if not data.pwd:
                return utils.respond(utils.not_found, "Password is required")
            if not data.pwd1:
                return utils.respond(utils.not_found, "Confirmation Password is required")
            
            if data.pwd != data.pwd1:
                return utils.respond(utils.unprocessable_entity, "The two passwords do not match!")
            if not self.validate_password(data.pwd):
                return utils.respond(utils.unprocessable_entity, "New password must contain at least include uppercase and lowercase letters, numbers & special characters! ")

            user_pool = dbms.get_doc("User_Pool", data.email,privilege=True)
            if user_pool.status != utils.ok:
                return utils.respond(utils.unprocessable_entity, f"Provided Email '{data.email}' not recognized!")
            tenant = dbms.get_doc("Tenant", user_pool.data.tenant, privilege=True)

            if tenant.status != utils.ok:
                return utils.respond(utils.unprocessable_entity, "An error occurred while resetting your password. Please contact administrator")
            tnt_dbms = tc.connect_tenant(tenant.data.db_name)
            results = tnt_dbms.get_users(id=data.email, fetch_by_email=True,fetch_password=True)
            if results.status != utils.ok:
                return results
            usr = results.data
            password_reset_code = tnt_dbms.get_list("Password_Reset",filters={"code":data.reset_code, "user":data.email,"request_date":dates.today(),"status":"Active"},privilege=True, order_by=["-id"], limit=1)
            if password_reset_code.status != utils.ok:
                return utils.respond(utils.forbidden, "The password reset code provided might have been already used or expired!")
            reset = password_reset_code.data.rows[0]
            usr.password = utils.encrypt_password(data.pwd).data.encrypted

            update = tnt_dbms.update("Lite_User", usr, privilege=True, skip_hooks=True,skip_audit_trail=True)
            if update.status != utils.ok:
                return utils.respond(utils.unprocessable_entity, f"An error occurred while updating your new password: {update.error_message}")
            if update.status != utils.ok:
                return utils.respond(utils.unauthorized, "Failed to update new password. Please contact administrator")
            reset.status = "Used"
            update = tnt_dbms.update("Password_Reset", reset, privilege=True)
            return utils.respond(utils.ok, "New Password updated successfully!")
        except Exception as e:
            pp(str(e))
            return utils.respond(utils.internal_server_error, f"An error occurred while processing your password reset password. Try again later.")
        

        


    def request_password_reset (self, dbms, data):
        from controllers.tenant import Tenant_Controller
        tc = Tenant_Controller()
        try:
            if not data.email:
                return utils.respond(utils.not_found, "Email required!")
            user_pool = dbms.get_doc("User_Pool", data.email,privilege=True)
            if user_pool.status != utils.ok:
                return utils.respond(utils.unprocessable_entity, f"Provided Email '{data.email}' not recognized!")
            tenant = dbms.get_doc("Tenant", user_pool.data.tenant, privilege=True)

            if tenant.status != utils.ok:
                return utils.respond(utils.unprocessable_entity, "An error occurred while resetting your password. Please contact administrator")
            tnt_dbms = tc.connect_tenant(tenant.data.db_name)
            mailing = Mailing (dbms=tnt_dbms)
            results = tnt_dbms.get_users (id=data.email, fetch_by_email=True)
            if results.status == utils.ok:
                user = results.data
                passcode = utils.generate_dashed_otp(10,group_size=2, separator=" ")
                expiry = dates.add_minutes_to_time(dates.time(), 10)
                pass_data = {
                    "name": f"{user.name}-{passcode}-{expiry}",
                    "code":passcode,
                    "user":user.name, 
                    "request_date": dates.today(), 
                    "expiry_time": expiry,
                    "status":"Active"
                }

                create = tnt_dbms.create("Password_Reset", pass_data, privilege=True)

                if create.status != utils.ok:
                    return utils.respond(utils.internal_server_error, "An error occurred while generating reset code. Please once more.")
                if user:
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
                                .code {{
                                    font-size: 30px;
                                    font-weight: bold;
                                    margin-top: 10px;
                                }}
                                
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <h2>Hello {user['first_name']}!</h2>
                                <p>You requested to reset your password on {tenant['data']['name']}'s ECZ HRMIS.</p>
                                <p>To proceed with the password reset, click the button below:</p>
                                <div style="margin:30px 0">
                                    <a href="https://hrmis.exams-council.org.zm/auth/password_reset?stg=2" class="btn">Reset Password</a>
                                </div>
                                <p>Alternatively, you can go to the following link:</p>
                                <a href="https://hrmis.exams-council.org.zm/auth/password_reset?stg=2">https://hrmis.exams-council.org.zm/auth/password_reset?stg=2</a>
                                <div style="margin-top:20px">
                                    <p>You will be required to provide the password reset code below:</p>
                                    <div class="code">{passcode}</div>
                                    <p>Note: This code will expire at {expiry}.</p>
                                </div>
                            </div>
                        </body>
                        </html>
                    """
                    mail = mailing.send_mail(recipient=data.email, subject="Request For Password Reset", body=Default_Template.template(content,"Requesting For Password Reset"))
                    return utils.respond(utils.ok, "Reset Passcode has been sent to your email.")
            return utils.respond(utils.unauthorized, "Invalid Email")
        except Exception as e:
            return utils.respond(utils.internal_server_error, f"An error occurred while processing your password reset password. Try again later.")
        

    @classmethod
    def validate_password(cls, password):
        if re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password):
            return True
        else:
            return False