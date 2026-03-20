export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_dashboard",
                title: "Dashboard",
                url: "staff_dashboard",
                icon: "person_apron",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    {
        title: "Leave",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_leave",
                title: "Leave Dashboard",
                url: "staff_leave",
                icon: "free_cancellation",
                page: "list",
                content_type: "Leave",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_leave",
                title: "Apply For Leave",
                url: "staff_leave",
                icon: "calendar_add_on",
                page: "new-form",
                content_type: "Leave",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_leave_history",
                title: "Leave History",
                url: "staff_leave_history",
                icon: "event_repeat",
                page: "report",
                content_type: "staff leave history",
                child_items: []
            },
        ]
    },
    {
        title: "Performance",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_workplan",
                title: "Work Plan",
                url: "staff_workplan",
                icon: "person_apron",
                page: "list",
                content_type: "Workplan",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_appraisal",
                title: "Self Rating",
                url: "staff_appraisal",
                icon: "how_to_reg",
                page: "list",
                content_type: "staff appraisal",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/staff",
            //     app: "staff_appraisal",
            //     title: "360 Deg Appraisal",
            //     url: "staff_appraisal_360/",
            //     icon: "360",
            //     page: "list",
            //     content_type: "360 Deg Appraisal",
            //     child_items: []
            // },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/staff",
            //     app: "staff_performance",
            //     title: "Performance Report",
            //     url: "staff_performance",
            //     icon: "browse_activity",
            //     page: "report",
            //     content_type: "staff performance",
            //     child_items: []
            // },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/staff",
            //     app: "staff_assignment",
            //     title: "Assignments",
            //     url: "staff_assignment",
            //     icon: "assignment_add",
            //     page: "list",
            //     content_type: "Assignments",
            //     child_items: []
            // },
        ]
    },
    {
        title: "Salary Info",
        routes: [
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/staff",
            //     app: "staff_earnings_and_deductions",
            //     title: "Your Earnings",
            //     url: "staff_earnings_and_deductions",
            //     icon: "add_chart",
            //     page: "list",
            //     content_type: "Earnings",
            //     child_items: []
            // },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/staff",
            //     app: "staff_earnings_and_deductions",
            //     title: "Your Deductions",
            //     url: "staff_earnings_and_deductions",
            //     icon: "remove",
            //     page: "list",
            //     content_type: "Deductions",
            //     child_items: []
            // },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_payslip",
                title: "Payslips",
                url: "staff_payslip",
                icon: "receipt_long",
                page: "list",
                content_type: "Payslip",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_advance",
                title: "Apply For Advance",
                url: "staff_advance",
                icon: "database",
                page: "list",
                content_type: "Staff Advance ",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/staff",
            //     app: "staff_advance_history",
            //     title: "Advance History",
            //     url: "staff_advance_history",
            //     icon: "manage_search",
            //     page: "report",
            //     content_type: "advance_history",
            //     child_items: []
            // }
        ]
    },
    {
        title: "Commission Management",
        routes: [
           
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_commission",
                title: "Commission",
                url: "staff_commission",
                icon: "database",
                page: "list",
                content_type: "Staff Commission",
                child_items: []
            },
        ]
    },
    {
        title: "Overtime",
        routes: [
           
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_overtime",
                title: "Apply For Overtime",
                url: "staff_overtime",
                icon: "database",
                page: "list",
                content_type: "Staff Overtime",
                child_items: []
            },
        ]
    },
    
    {
        title: "Internal Communication",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_memo",
                title: "Memo",
                url: "staff_memo",
                icon: "note_alt",
                page: "list",
                content_type: "memo",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_query",
                title: "Queries",
                url: "staff_query",
                icon: "query_stats",
                page: "list",
                content_type: "query",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_policy",
                title: "Company Policy",
                url: "staff_policy",
                icon: "policy",
                page: "list",
                content_type: "company policy",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_announcement",
                title: "Announcements",
                url: "staff_announcement",
                icon: "campaign",
                page: "list",
                content_type: "announcements",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_employee_feedback",
                title: "Feedback",
                url: "staff_employee_feedback",
                icon: "clinical_notes",
                page: "list",
                content_type: "employee feedback",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_bulletin",
                title: "Bulletin",
                url: "staff_bulletin",
                icon: "voice_selection",
                page: "list",
                content_type: "bulletin",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_suggestion_box",
                title: "Suggestion Box",
                url: "staff_suggestion_box",
                icon: "demography",
                page: "list",
                content_type: "staff suggestion box",
                child_items: []
            },
            
        ]
    },
    {
        title: "Expenses",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_imprest",
                title: "Initialize Imprest",
                url: "staff_imprest",
                icon: "request_quote",
                page: "list",
                content_type: "Imprest",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "imprest",
                title: "Imprest Retirement",
                url: "imprest/",
                icon: "task",
                page: "list",
                content_type: "Imprest Retirement",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_purchase_requisition",
                title: "Initialize Purchase Requisition",
                url: "staff_purchase_requisition",
                icon: "shopping_cart",
                page: "list",
                content_type: "requisition",
                child_items: []
            },
            
        ]
    },    
    {
        title: "Industrial Relations",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_employee_grievance",
                title: "Grievance",
                url: "staff_employee_grievance",
                icon: "sentiment_dissatisfied",
                page: "list",
                content_type: "staff employee grievance",
                child_items: []
            },
         
            
        ]
    },
    {
        title: "Learning & Development",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "staff_training_event",
                title: "Training Event",
                url: "staff_training_event",
                icon: "add_business",
                page: "list",
                content_type: "training_event",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "training_program_application_form",
                title: "Apply For Training Program",
                url: "training_program_application_form",
                icon: "edit_note",
                page: "list",
                content_type: "training program application form",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/staff",
                app: "training_program_feedback",
                title: "Training Program Feedback",
                url: "training_program_feedback",
                icon: "quick_phrases",
                page: "list",
                content_type: "training program feedback",
                child_items: []
            },
         
            
        ]
    },
    {
        title: "Seperation",
        routes: [
            {
                is_linked: true,
                module: "app/staff",
                app: "resignation",
                title: "Submit Resignation",
                url: "resignation",
                icon: "person_remove",
                page: "list",
                content_type: "resignation",
                child_items: []
            },
         
            
        ]
    },
    
]