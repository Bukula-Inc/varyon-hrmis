class Project_Management_Templates:
    def __init__(self):
        pass

    @classmethod
    def project(cls, project_name,pm, start_date, end_date, description, logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>New Role</title>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height:170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 20px; margin: auto; text-align: center; margin-top: 30px;">New Project Role</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                        <div class="bg-white text-gray-800 p-6 mt-6 rounded-md shadow-md">
                            <ul class="list-none mb-4 pl-0">
                                <li class="mb-2">Dear <span class="font-bold text-blue-500">{pm}</span>, You Have A New Project Task</li>
                                <li class="mb-2">Project Task:  <span class="font-bold text-blue-500">{project_name}</span></li>
                                <li class="mb-2">Start Date:  <span class="font-bold text-blue-500">{start_date}</span></li>
                                <li class="mb-2">End Date:  <span class="font-bold text-blue-500">{end_date}</span></li>
                                <p class="text-sm mt-4">Task Description:  <span class="text-gray-600">{description}</span></p>
                                <a href="/app/project_management/project/?loc=project&type=list&document=project" class="inline-block mt-4 px-4 py-2 border border-blue-500 rounded-md bg-blue-600 text-white">See More</a>
                            </ul>
                        </div>  
                    <div style="width:80%; text-align: center; margin: 0 auto; margin-top: 40px;">
                    </div>
                    </div>
                    <div style="width: 100%; margin: 0 auto; background-color: white; height: 10vh; color: #2b2745;">
                        <div style="width: 80%; margin: 0 auto; border-top: 1px gray solid; padding-top: 5px; display: grid; grid-template-columns: 1fr 2fr;">
                            <div style="font-size: 12px; display: grid; grid-template-columns: 1fr 1fr;">
                                <div style="margin: auto 0;">Powered by</div>
                                <a href="https://www.startapperp.comt" style="margin: auto 0;"><img src="https://www.startapperp.com/static/images/logo/logo.svg" alt="" style="width: 70px; margin-top: 10px;"></a>
                            </div>
                            <div style="font-size: 12px; margin-top: 2px; text-align: right;">&copy; 2024 | All Rights Reserved</div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
        """
    @classmethod
    def project_team(cls, project_name, parent, start_date, end_date, description, logo=None):
        wrapper = "@media screen and (max-width:650px) { .wrapper{width: 100% !important }}"
        return f"""
            <!DOCTYPE html>
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>New Role</title>
            </head>
            <body style="width:100%; min-height: 100vh; background-color: #e3e3e3; padding:0; margin:0; font-family: Arial, Helvetica, sans-serif;">
                <div class="wrapper" style="width: 60%; min-height:170px; height: max-content; background-color: #2b2745; color: white; margin: 0 auto; overflow: hidden; line-height: 1.3em;">
                    <div style="width: 80%; margin: 0 auto; margin-top: 30px;">
                        <img src="https://{logo}" alt="" style="width: 120px;">
                    </div>
                    <h3 style="font-size: 20px; margin: auto; text-align: center; margin-top: 30px;">New Project Role</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                        <div class="bg-white text-gray-800 p-6 mt-6 rounded-md shadow-md">
                            <ul class="list-none mb-4 pl-0">
                                <li class="mb-2">Dear <span class="font-bold text-blue-500">{parent}</span>, You Have A New Project Task</li>
                                <li class="mb-2">Project Task:  <span class="font-bold text-blue-500">{project_name}</span></li>
                                <li class="mb-2">Start Date:  <span class="font-bold text-blue-500">{start_date}</span></li>
                                <li class="mb-2">End Date:  <span class="font-bold text-blue-500">{end_date}</span></li>
                                <p class="text-sm mt-4">Task Description:  <span class="text-gray-600">{description}</span></p>
                                <a href="/app/project_management/project/?loc=project&type=list&document=project" class="inline-block mt-4 px-4 py-2 border border-blue-500 rounded-md bg-blue-600 text-white">See More</a>
                            </ul>
                        </div>  
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
    def project_review_schedule(cls, title, review_date, project_name, project_management_team):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Project Task</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #172554; color: #000000;">
            <div style="max-width: 28rem; width: 80%; margin: 0 auto; padding: 2rem;">
                <img src="your_logo.png" alt="Your Logo" style="display: block; margin: 0 auto; width: 6rem; height: auto; margin-bottom: 1.5rem;">
                <h2 style="text-align: center; font-size: 1.875rem; font-weight: 800; margin-top: 0; margin-bottom: 0.75rem; color: #000000;">Project Review Schedule</h2>
                <div style="background-color: rgba(255, 255, 255, 0.9); border-radius: 1rem; box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15); color: #000000; overflow: hidden; padding: 1.5rem;">
                    <h1 style="font-size: 1.875rem; font-weight: 800; margin-bottom: 1rem; color: #172554; text-align: center;">Subject: {title}</h1>
                    <ul style="margin-bottom: 1rem; list-style: none; padding-left: 0;">
                        <li style="margin-bottom: 0.75rem; color:#172554;"><span style="color: #0f172a; font-size: 1.1rem;">Review Date:</span> {review_date}</li>
                        <li style="margin-bottom: 0.75rem; color:#172554;"><span style="color: #0f172a; font-size: 1.1rem;">Project Name:</span> {project_name}</li>
                        <li style="margin-bottom: 0.75rem; color:#172554;"><span style="color: #0f172a; font-size: 1.1rem;">Project Management Team:</span> {project_management_team}</li>
                    </ul>
                    <div>
                        <li>
                            <a href="/app/project_management/project_task/?loc=project_task&type=list&document=project task" style="display: inline-block; padding: 0.5rem 1rem; margin-top: 1rem; color: #000000; background-color: #3B82F6; border-radius: 0.375rem; text-align: center; text-decoration: none; transition: background-color 0.3s ease;">Confirm The Review Schedule</a>
                        </li>
                    </div>                    
                </div>
                
                <footer style="text-align: center; color: #64748b; margin-top: 2rem; font-size: 1.1rem;">
                    <p>&copy; 2024 PBS. All rights reserved.</p>
                </footer>
            </div>
        </body>
        </html>
        """

    @classmethod
    def tasks(cls, title, start_date,individual, end_date, description, logo=None):
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
                    <h3 style="font-size: 20px; margin: auto; text-align: center; margin-top: 30px;">New Project Task</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                        <div class="bg-white text-gray-800 p-6 mt-6 rounded-md shadow-md">
                            <ul class="list-none mb-4 pl-0">
                                <li class="mb-2">Dear <span class="font-bold text-blue-500">{individual}</span>, You Have A New Project Task</li>
                                <li class="mb-2">Project Task:  <span class="font-bold text-blue-500">{title}</span></li>
                                <li class="mb-2">Start Date:  <span class="font-bold text-blue-500">{start_date}</span></li>
                                <li class="mb-2">End Date:  <span class="font-bold text-blue-500">{end_date}</span></li>
                                <p class="text-sm mt-4">Task Description:  <span class="text-gray-600">{description}</span></p>
                                <a href="/app/project_management/project_task/?loc=project_task&type=list&document=project task" class="inline-block mt-4 px-4 py-2 border border-blue-500 rounded-md bg-blue-600 text-white">See More</a>
                            </ul>
                        </div>  
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
    def tasks_team(cls, title, start_date, end_date, team_name, description, logo=None):
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
                    <h3 style="font-size: 20px; margin: auto; text-align: center; margin-top: 30px;">New Project Task</h3>
                    <div style="width: 100%; min-height:70vh; margin-top: 40px; background-color: #ffffff; padding: 10px; color: #2b2745;">
                        <div class="bg-white text-gray-800 p-6 mt-6 rounded-md shadow-md">
                            <ul class="list-none mb-4 pl-0">
                                <li class="mb-2">Dear <span class="font-bold text-blue-500">{team_name}</span>, You Have A New Project Task</li>
                                <li class="mb-2">Project Task <span class="font-bold text-blue-500">{title}</span></li>
                                <li class="mb-2">Start Date: <span class="font-bold text-blue-500">{start_date}</span></li>
                                <li class="mb-2">End Date: <span class="font-bold text-blue-500">{end_date}</span></li>
                                <p class="text-sm mt-4">Task Description: <span class="text-gray-600">{description}</span></p>
                                <a href="/app/project_management/project_task/?loc=project_task&type=list&document=project task" class="inline-block mt-4 px-4 py-2 border border-blue-500 rounded-md bg-blue-600 text-white">See More</a>
                            </ul>
                        </div>                        
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
           
