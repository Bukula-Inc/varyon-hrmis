role = {
    "model":"Role",
    "data":[
        {
            "name": "Super Admin",
            "default_dashboard":"Super Administrator",
            "module":"core",
            "role_module": [
                {
                    "role_module": "core",
                    "default_dashboard": "Super Administrator",
                    "permit_all": 1,
                    "role_cards": [
                        {
                            "Core Dashboard": [
                                "Dashboard"
                            ],
                            "Core":[
                                "Location",
                                "Gender",
                                "Industry",
                                "Sector",
                                "Currency",
                                "Cost Center",
                                "Department",
                                "System Settings",
                                "Default Dashboards",
                                "Menu Card",
                            ],
                            "Geo":[
                                "Location",
                                "Countries",
                                "State",
                                "Province",
                                "District",
                                "City",
                                "Company",
                                "Share Type",
                                "Shareholders",
                                "Shares"
                            ],
                            "Company & Shares":[
                                "Company",
                                "Share Type",
                                "Shareholders",
                                "Shares"
                            ],
                            "Others":[
                                "Data Importation",
                                "Priority",
                                "Working Hours",
                                "Rating",
                                "Disabled Documents"
                            ],
                            "User Management":[
                                "User Account",
                                "Role",
                                "Workflow Management"
                                "Audit Trail Report"

                            ],
                            
                            "Configurations":[
                                "Naming Series",
                                "Document Status",
                                "Print Formats",
                                "Print Configuration"
                                "Email Configuration"
                            ],
                        }
                    ]
                },

            ],
        },
        
        {
            "name": "Chief Executive Officer",
            "default_dashboard":"Super Administrator",
            "module":"core",
            "role_module": [
                {
                    "role_module": "core",
                    "default_dashboard": "Super Administrator",
                    "permit_all": 1,
                    "role_cards": [
                            {
                                "Core Dashboard": [
                                    "Dashboard"
                                ],
                                "Core": [
                                    "Location",
                                    "Gender",
                                    "Industry", 
                                    "Sector", 
                                    "Currency",
                                    "Cost Center",
                                    "Department",
                                    "System Settings",
                                    "Default Dashboards",
                                    "Menu Card",
                                ],
                                "Geo": [
                                    "Location",
                                    "Countries",
                                    "State",  
                                    "Province",
                                    "District",
                                    "City",
                                ],
                                "Company & Shares": [
                                    "Company",
                                    "Share Type",
                                    "Shareholders",
                                    "Shares",
                                ],
                                "Others": [
                                    "Data Importation",
                                    "Priority",
                                    "Working Hours",
                                    "Rating",
                                    "Disabled Documents",
                                ],
                                "User Management": [
                                    "User Account",
                                    "Role",
                                    "Workflow Management",
                                    "Audit Trail Report",

                                ],
                                "Configurations": [
                                    "Naming Series",
                                    "Document Status",
                                    "Print Formats",
                                    "Print Configuration",
                                    "Email Configuration",

                                ],
                            }
                    ]
                }
            ],
        },
        {
            "name": "HR Manager",
            "default_dashboard":"Human Resource Management",
            "module":"hr",
            "role_module": [
                {
                    "role_module": "hr",
                    "default_dashboard": "Human Resource Management",
                    "permit_all": 1,
                    "role_cards": [
                        {
                            "HR Dashboard": [
                                "Dashboard"
                            ],
                            "HR Masters": [
                                "Location",
                                "HR Settings",
                                "Department", 
                                "Job Title",
                                "Employee",
                                "Employee Attendance", 
                                "Employee Promotion",
                                "Employee Files",
                                "Employment Type",
                            ],
                            "Employee Performance": [
                                "Open Ended Questions",
                                "Closed Ended Questions",
                                "Closed Ended Question Options",  
                                "Appraisal Quarter",
                                "Appraisal Setup", 
                                "360 Deg Appraisal",  
                                "Self Appraisal",
                                "Work Plan",
                                "Bonus Type",
                                "Bonus Planing"
                                "Bonus",
                            ],
                            "Leave Management": [
                                "Leave Type",
                                "Leave Policy",
                                "Leave Allocation",
                                "Leave Entry",
                                "Leave Application",
                            ],
                            
                            "Internal Communications": [
                                "Memo",
                                "Company Policies",
                                "Announcement",  
                                "Bulletin",
                            ],
                            "Recruitment & Selection": [
                                "Staffing Plan",
                                "Job Opening",
                                "Job Application",
                                "Interview Type",
                                "Interview Schedule",
                                "Interview",
                                "Job Offer",
                                "Appointment Letter",
                            ],
                            "Industrial Relations": [
                                "Grievance Type",
                                "Violation Type",
                                "Employee Grievance",
                                "Employee Disciplinary",
                                "Case Outcome",
                            ],
                            "Employee Separation": [
                                "Employee Seperation",
                                "Exit Interview",
                                "Full & Final Statement",
                            ],
                            "Training & Development": [
                                "Training Program Type",
                                "Training Program",
                                "Training Feedback",
                            ],
                            "HR Reports": [
                                "Monthly Attendance Sheet",
                                "Employee Information",
                                "Employee Leave Balance",
                                "Employee's on  Leave",
                                "Recruitment Analytics",
                                "Employee Exit",
                                "Leave Summary",
                                "Self Appraisal",
                                "360 Degree Appraisal",
                                "training_effectiveness",
                            ],
                        }
                    ]
                },
                {
                    "role_module": "payroll",
                    "default_dashboard": "Payroll",
                    "permit_all": 1,
                    "role_cards": [
                        {
                            "Payroll Dashboard": [
                                "Dashboard" 
                            ],
                            "Payroll Setup": [
                                "Payroll Setup",
                                "Income Tax Bands",
                                "Salary Component", 
                                "Employee Grade",
                            ],
                            "Salary Advance": [
                                "Advance Setup",
                                "Advance Applications",
                                "Advance Balances",  
                            ],
                            "Overtime": [
                                "Overtime Setup",
                                "Overtime Applicantions",
                            ],
                            "Commission": [
                                "Commission Setup",
                            ],
                            "Payroll Processor": [
                                "Run Payroll",
                                "Payslip",
                            ],
                            "Payroll Reports": [
                                "Monthly Attendance Sheet",
                                "Paye",
                                "Napsa",
                                "Nhima",
                                "Private Insurance",
                                "Overtime",
                                "Payroll Summary",
                            ],
                        }
                    ]
                }
            ],
        },
        {
            "name": "HR User",
            "default_dashboard":"Staff Dashboard",
            "module":"staff",
            "role_module": [
                {
                    "role_module": "staff",
                    "default_dashboard": "Staff Dashboard",
                    "permit_all": 1,
                    "role_cards": [
                        {
                            "Staff Dashboard": [
                                "Dashboard"
                            ],
                            "Staff Leave": [
                                "Leave Dashboard",
                                "Apply For Leave",
                                "Leave History", 
                            ],
                            "Staff Performance": [
                                "Work Plan",
                                "Self Rating",
                                "Task",  
                            ],
                            "Staff Salary Info": [
                                "Payslips",
                                "Apply For Advance",
                            ],
                            "Staff Overtime": [
                                "Apply For Overtime",
                            ],
                            "Staff Internal Communication": [
                                "Memo",
                                "Queries"
                                "Company Policy",
                                "Announcements",
                                "Feedback",
                                "Bulletin",
                                "Suggestion Box",
                            ],
                            "Staff Expenses": [
                                "Initialize Imprest",
                                "Imprest Retirement",
                                "Initialize Purchase Requisition",
                            ],
                            "Staff Industrial Relations": [
                                "Grievance",
                            ],
                            "Staff Training & Development": [
                                "Training Event",
                                "Apply For Training Program",
                                "Training Program Feedback",
                            ],
                            "Staff Separation": [
                                "Submit Resignation",
                            ],
                        }
                    ]
                }
            ],
        },
    ]
}