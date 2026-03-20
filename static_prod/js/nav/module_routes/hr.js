export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/hr",
                app: "hr_dashboard",
                title: "Dashboard",
                url: "accounts",
                icon: "bar_chart_4_bars",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    {
        title: "HR Masters",
        routes: [
          
            {
                is_linked: true,
                module: "app/core",
                app: "branch",
                title: "Branch",
                url: "branch",
                icon: "business_center",
                page: "list",
                content_type: "branch",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     module: "app/hr",
            //     app: "hr_settings",
            //     title: "Hr Settings",
            //     url: "hr_settings",
            //     icon: "business_center",
            //     page: "new-form",
            //     content_type: "hr settings",
            //     child_items: []
            // },
            {
                is_linked: true,
                module: "app/core",
                app: "department",
                title: "Department",
                url: "department",
                icon: "diversity_3",
                page: "list",
                content_type: "department",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "designation",
                title: "Designation",
                url: "designation",
                icon: "work_history",
                page: "list",
                content_type: "designation",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "employee",
                title: "Employee",
                url: "employee",
                icon: "person_apron",
                page: "list",
                content_type: "employee",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "employee",
                title: "Employee Attendance",
                url: "employee_attendance",
                icon: "how_to_reg",
                page: "list",
                content_type: "employee attendance",
                child_items: []
            },
            {

                is_linked: true,
                module: "app/hr",
                app: "employee",
                title: "Employee Promotion",
                url: "employee_promotion",
                icon: "group_add",
                page: "list",
                content_type: "employee promotion",
                child_items: []
            },
            {

                is_linked: true,
                module: "app/hr",
                app: "employee",
                title: "Employee Files",
                url: "employee_files",
                icon: "supervisor_account",
                page: "list",
                content_type: "employee files",
                child_items: []
            },
            {

                is_linked: true,
                module: "app/hr",
                app: "employee",
                title: "Employment Type",
                url: "employment_type",
                icon: "for_you",
                page: "list",
                content_type: "employment type",
                child_items: []
            },
        ]
    },
    {
        title: "Employee Performance",
        routes: [
            {
                is_linked: true,
                module: "app/hr",
                app: " appraisal_setup",
                title: "Appraisal Setup",
                url: "appraisal_setup",
                icon: "person_add",
                page: "list",
                content_type: "appraisal setup",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "appraisal_quarter",
                title: "Appraisal Quarter",
                url: "appraisal_quarter",
                icon: "content_copy",
                page: "list",
                content_type: "appraisal quarter",
                child_items: []
            },
           
            {
                is_linked: true,
                module: "app/hr",
                app: "self_appraisal",
                title: "Self Appraisal",
                url: "self_appraisal",
                icon: "person",
                page: "list",
                content_type: "self appraisal",
                child_items: []
            },
                    
            {
                is_linked: true,
                module: "app/hr",
                app: "appraisal",
                title: "Appraisal",
                url: "appraisal",
                icon: "person",
                page: "list",
                content_type: "appraisal",
                child_items: []
            },
            
            {
                is_linked: true,
                module: "app/hr",
                app: "appraisal_question",
                title: "Open Ended Questions",
                url: "appraisal_question",
                icon: "article",
                page: "list",
                content_type: "Open Ended Question",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "appraisal_question",
                title: "Closed Ended Questions",
                url: "appraisal_question",
                icon: "inventory",
                page: "list",
                content_type: "Closed Ended Question",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "appraisal_question",
                title: "Closed Ended Question Options",
                url: "appraisal_question",
                icon: "list",
                page: "list",
                content_type: "Closed Ended Question Option",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "work_plan",
                title: "Work Plan",
                url: "work_plan/",
                icon: "table",
                page: "list",
                content_type: "work plan",
            },
            {          
                is_linked: true,
                module: "app/hr",
                app: "bonus_types",
                title: "Bonus Type",
                url: "bonus_types",
                icon: "format_image_left",
                page: "list",
                content_type: "bonus types",
                child_items: []
            },
            {

                is_linked: true,
                module: "app/hr",
                app: "bonus_planing",
                title: "Bonus Planing",
                url: "bonus_planing",
                icon: "workspace_premium",
                page: "list",
                content_type: "bonus planing",
                child_items: []
            },    
            {
                is_linked: true,
                module: "app/hr",
                app: "bonus",
                title: "Bonus",
                url: "bonus/",
                icon: "table",
                page: "list",
                content_type: "bonus",
            },
        ]
    },
    {
        title: "Leave",
        routes: [

             {
                is_linked: true,
                module: "app/hr",
                app: "leave_type",
                title: "Leave Type",
                url: "leave_type",
                icon: "description",
                page: "list",
                content_type: "leave type",
                child_items: []
            },
            
            {
                is_linked: true,
                module: "app/hr",
                app: "leave_policy",
                title: "Leave Policy",
                url: "leave_policy",
                icon: "leaderboard",
                page: "list",
                content_type: "leave policy",
                child_items: []
            },
         
            {
                is_linked: true,
                module: "app/hr",
                app: "leave",
                title: "Leave Allocation ",
                url: "leave_allocation",
                icon: "content_copy",
                page: "list",
                content_type: "leave allocation",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "leave_entry",
                title: "Leave Entry",
                url: "leave_entry",
                icon: "save",
                page: "list",
                content_type: "leave entry",
                child_items: []
            },
          
            {
                is_linked: true,
                module: "app/hr",
                app: "leave",
                title: "Leave Application",
                url: "leave_application",
                icon: "contact_page",
                page: "list",
                content_type: "leave application",
                child_items: []
            },
        
         
        ]
    },
    {
        title: "Internal Communications",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/hr",
                app: "memo",
                title: "Memo",
                url: "memo",
                icon: "fact_check",
                page: "list",
                content_type: "memo",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/hr",
            //     app: "query",
            //     title: "Query",
            //     url: "query",
            //     icon: "assignment_ind",
            //     page: "list",
            //     content_type: "query",
            //     child_items: []
            // },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/hr",
                app: "company_policies",
                title: "Company Policies",
                url: "company_policies",
                icon: "checklist_rtl",
                page: "list",
                content_type: "company policies",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/hr",
                app: "announcement",
                title: "Announcement",
                url: "announcement",
                icon: "campaign",
                page: "list",
                content_type: "announcement",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/hr",
            //     app: "employee_feedback",
            //     title: "Employee Feedback",
            //     url: "employee_feedback",
            //     icon: "clinical_notes",
            //     page: "list",
            //     content_type: "employee feedback",
            //     child_items: []
            // },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/hr",
                app: "bulletin",
                title: "Bulletin",
                url: "bulletin",
                icon: "voice_selection",
                page: "list",
                content_type: "bulletin",
                child_items: []
            },
          
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/hr",
            //     app: "suggestion_category",
            //     title: "Suggestion Category",
            //     url: "suggestion_category",
            //     icon: "inbox_customize",
            //     page: "list",
            //     content_type: "suggestion category",
            //     child_items: []
            // },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/hr",
            //     app: "suggestion_box",
            //     title: "Suggestion Box",
            //     url: "suggestion_box",
            //     icon: "demography",
            //     page: "list",
            //     content_type: "suggestion box",
            //     child_items: []
            // },
        
         
        ]
    },   
    {
        title: "Recruitment & Selection",
        routes: [
            {
                is_linked: true,
                module: "app/hr",
                app: "staffing_plan",
                title: "Staffing Plan",
                url: "staffing_plan",
                icon: "location_away",
                page: "list",
                content_type: "staffing plan",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "job_opening",
                title: "Job Opening",
                url: "job_opening",
                icon: "person_search",
                page: "list",
                content_type: "job opening",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "job_application",
                title: "Job Application",
                url: "job_application",
                icon: "draft",
                page: "list",
                content_type: "job application",
                child_items: []
            },
         
            {
                is_linked: true,
                module: "app/hr",
                app: "interview_type",
                title: "Interview Type",
                url: "interview_type",
                icon: "3p",
                page: "list",
                content_type: "interview type",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "interview_schedule",
                title: "Interview Schedule",
                url: "interview_schedule",
                icon: "copy_all",
                page: "list",
                content_type: "interview schedule",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "interview",
                title: "Interview",
                url: "interview",
                icon: "folder_shared",
                page: "list",
                content_type: "interview",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     module: "app/hr",
            //     app: "interview_feedback",
            //     title: "Interview Feedback",
            //     url: "interview_feedback",
            //     icon: "backup_table",
            //     page: "list",
            //     content_type: "interview feedback",
            //     child_items: []
            // },
            {
                is_linked: true,
                module: "app/hr",
                app: "job_offer",
                title: "Job Offer",
                url: "job_offer",
                icon: "text_snippet",
                page: "list",
                content_type: "Job offer",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "appointment_letter",
                title: "Appointment Letter",
                url: "appointment_letter",
                icon: "request_page",
                page: "list",
                content_type: "appointment letter",
                child_items: []
            },
        ]
    },

    {
        title: "Industrial Relations",
        routes: [
            {
                is_linked: true,
                module: "app/hr",
                app: "grievance_type",
                title: "Grievance Type",
                url: "grievance_type",
                icon: "add_task",
                page: "list",
                content_type: "grievance type",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "violation_type",
                title: "Violation Type",
                url: "violation_type",
                icon: "account_circle_off",
                page: "list",
                content_type: "violation type",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "disciplinary_committee",
                title: "Disciplinary Committee",
                url: "disciplinary_committee",
                icon: "sentiment_dissatisfied",
                page: "list",
                content_type: "Disciplinary Committee",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "employee_grievance",
                title: "Employee Grievance",
                url: "employee_grievance",
                icon: "sentiment_dissatisfied",
                page: "list",
                content_type: "employee grievance",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "employee_disciplinary",
                title: "Employee Disciplinary",
                url: "employee_disciplinary",
                icon: "person_alert",
                page: "list",
                content_type: "employee disciplinary",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "case_outcome",
                title: "Case Outcome",
                url: "case_outcome",
                icon: "patient_list",
                page: "list",
                content_type: "case outcome",
                child_items: []
            },        
           
        ]
    },

    {
        title: "Employee Seperation",
        routes: [
            {
                is_linked: true,
                module: "app/hr",
                app: "employee_separation",
                title: "Employee Seperation",
                url: "employee_separation",
                icon: "person_remove",
                page: "list",
                content_type: "employee seperation",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "exit_interview",
                title: "Exit Interview",
                url: "exit_interview",
                icon: "tv_signin",
                page: "list",
                content_type: "exit interview",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "final_statement",
                title: "Full & Final Statement",
                url: "final_statement",
                icon: "login",
                page: "list",
                content_type: "final statement",
                child_items: []
            },
           
        ]
    },

    {
        title: "Learning & Development",
        routes: [
            {
                is_linked: true,
                module: "app/hr",
                app: "Training_Program_Type",
                title: "Training Program Type",
                url: "training_program_type",
                icon: "health_and_safety",
                page: "list",
                content_type: "training program type",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "training_program",
                title: "Training Program",
                url: "training_program",
                icon: "health_and_safety",
                page: "list",
                content_type: "training Program",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "training_event",
                title: "Training Event",
                url: "training_event",
                icon: "add_business",
                page: "list",
                content_type: "training event",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "training_feedback",
                title: "Training Feedback",
                url: "training_feedback",
                icon: "import_contacts",
                page: "list",
                content_type: "training feedback",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "training_result",
                title: "Training Result",
                url: "training_result",
                icon: "add_to_queue",
                page: "list",
                content_type: "training result",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "training_program_application",
                title: "Training Program Application",
                url: "training_program_application",
                icon: "school",
                page: "list",
                content_type: "training program application",
                child_items: []
            },   
        ]
    },

    {
        title: "Reports",
        routes: [
            // {
            //     is_linked: false,
            //     module: "app/hr",
            //     app: "reports",
            //     title: "Monthly Attendance Sheet",
            //     url: "hr_reports/monthly_attendance",
            //     icon: "",
            //     page: "list",
            //     content_type: "",
            //     child_items: []
            // },
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "Employee Information",
                url: "hr_reports/employee_information",
                icon: "recent_actors",
                page: "report",
                content_type: "employee information",
                child_items: []
            },
         
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "Employee Leave Balance",
                url: "hr_reports/employee_leave_balance",
                icon: "remember_me",
                page: "report",
                content_type: "employee leave balance",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "Employee's on  Leave",
                url: "hr_reports/employee_on_leave",
                icon: "user_attributes",
                page: "report",
                content_type: "employee on leave",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "Recruitment Analytics",
                url: "hr_reports/recruitment_analytics",
                icon: "folder_managed",
                page: "report",
                content_type: "recruitment analytics",
                child_items: []
            },
        
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "Employee Exit",
                url: "hr_reports/employee_exit",
                icon: "contact_emergency",
                page: "report",
                content_type: "employee exit",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "Leave Summary",
                url: "hr_reports/leave_summary",
                icon: "summarize",
                page: "report",
                content_type: "leave summary",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "Training Program Feedback Report",
                url: "hr_reports/training_feedback_report",
                icon: "summarize",
                page: "report",
                content_type: "training feedback",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "Self Appraisal",
                url: "hr_reports/self_appraisal_report",
                icon: "recent_actors",
                page: "report",
                content_type: "self appraisal report",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/hr",
                app: "reports",
                title: "360 Degree Appraisal",
                url: "hr_reports/appraisal_report",
                icon: "recent_actors",
                page: "report",
                content_type: "360 degree appraisal report",
                child_items: []
            },
            
        ]
    },

]   