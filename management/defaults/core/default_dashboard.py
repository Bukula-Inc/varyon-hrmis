default_dashboard = {
    "model":"Default_Dashboard",
    "data":[
        {
            "name": "Super Administrator",
            "module": "core",
            "app_name": "core_dashboard",
            "page_type":"dashboard",
            "content_type" :"Dashboard",
            "allowed_menus":[
                {"menu_card": "Core Dashboard"},
                {"menu_card": "Core"},
                {"menu_card": "Geo"},
                {"menu_card": "User Management"},
                {"menu_card": "Audit Trail"},
                {"menu_card": "Mailing"},
                {"menu_card": "Configurations"},
                {"menu_card": "Others"}
            ]
        },
        {
            "name": "Human Resource Management",
            "module": "hr",
            "app_name": "hr_dashboard",
            "page_type":"dashboard",
            "content_type" :"Dashboard",
            "allowed_menus":[
                {"menu_card": "HR Dashboard"},
                {"menu_card": "HR Masters"},
                {"menu_card": "Employee Performance"},
                {"menu_card": "Leave Management"},
                {"menu_card": "Internal Communications"},
                {"menu_card": "Recruitment & Selection"},
                {"menu_card": "Industrial Relations"},
                {"menu_card": "Employee Separation"},
                {"menu_card": "Training & Development"},
                {"menu_card": "HR Reports"},
            ]
        },
        {
            "name": "Payroll",
            "module": "payroll",
            "app_name": "payroll_dashboard",
            "page_type":"dashboard",
            "content_type" :"Dashboard",
            "allowed_menus":[
                {"menu_card": "Payroll Dashboard"},
                {"menu_card": "Payroll Setup"},
                {"menu_card": "Loans And Other Deductions"},
                {"menu_card": "Overtime"},
                {"menu_card": "Payroll Processor"},
                {"menu_card": "Payroll Reports"},
            ]
        },     
        {
            "name": "Staff Dashboard",
            "module": "staff",
            "app_name": "staff_dashboard",
            "page_type":"dashboard",
            "content_type" :"Dashboard",
            "allowed_menus":[
                {"menu_card": "Staff Dashboard"},
                {"menu_card": "Staff Info"},
                {"menu_card": "Staff Leave"},
                {"menu_card": "Staff Salary Info"},
                {"menu_card": "Staff Internal Communication"},
                {"menu_card": "Staff Expenses"},
                {"menu_card": "Staff Industrial Relations"},
                {"menu_card": "Staff Learning & Development"},
                {"menu_card": "Staff Separation"},
                {"menu_card": "Staff Welfare"},
                {"menu_card": "Staff Others"},
                {"menu_card": "Staff Loans And Other Deductions"},
            ]
        },          
    ]
}