export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/project_management",
                app: "project_dashboard",
                title: "Dashboard",
                url: "project_management",
                icon: "bar_chart_4_bars",
                page: "project_dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
   
    {
        title: "Projects",
        routes: [
        
            {
                is_linked: true,
                module: "app/project_management",
                app: "project_type",
                title: "Project Type",
                url: "project_type",
                icon: "text_fields",
                page: "list",
                content_type: "project type",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/project_management",
                app: "project_plan",
                title: "Project Plan",
                url: "project_plan",
                icon: "planner_review",
                page: "list",
                content_type: "project plan",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/project_management",
                app: "project",
                title: "Project",
                url: "project",
                icon: "energy_program_saving",
                page: "list",
                content_type: "project",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/project_management",
                app: "project_task",
                title: "Task",
                url: "project_task",
                icon: "work",
                page: "list",
                content_type: "project task",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/project_management",
                app: "project_manager",
                title: "Project Manager",
                url: "project_manager",
                icon: "manage_accounts",
                page: "list",
                content_type: "project manager",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/project_management",
                app: "project_management_team",
                title: "Project Management Team",
                url: "project_management_team",
                icon: "diversity_3",
                page: "list",
                content_type: "project management team",
                child_items: []
            }, 
        ]
    },
    {
        title: "Project Expense",
        routes: [
            // {
            //     is_linked: true,
            //     module: "app/project_management",
            //     app: "timesheet",
            //     title: "Timesheet",
            //     url: "timesheet",
            //     icon: "double_arrow",
            //     page: "list",
            //     content_type: "timesheet",
            //     child_items: []
            // },
            {
                is_linked: true,
                module: "app/project_management",
                app: "project_expense",
                title: " Project Expense",
                url: "project_expense",
                icon: "monetization_on",
                page: "list",
                content_type: "project expense",
                child_items: []
            },
         
        ]
    },
    
    // {
    //     title: "Time Tracking",
    //     routes: [
    //         {
    //             is_linked: false,
    //             module: "app/project_management",
    //             app: "",
    //             title: "Project Setting",
    //             url: "leave-type",
    //             icon: "",
    //             page: "list",
    //             content_type: "leave_type",
    //             child_items: []
    //         },

        // {
            //     is_linked: true,
            //     module: "app/project_management",
            //     app: "activity_type",
            //     title: "Activity Type",
            //     url: "activity_type",
            //     icon: "file_open",
            //     page: "list",
            //     content_type: "activity type",
            //     child_items: []
            // },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/project_management",
            //     app: "activity_cost",
            //     title: "Activity Cost",
            //     url: "activity_cost",
            //     icon: "attach_money",
            //     page: "list",
            //     content_type: "activity cost",
            //     child_items: []
            // },
     
         
    //     ]
    // },
       
       
    {
        title: "Reports",
        routes: [
            {
                is_linked: true,
                module: "app/project_management",
                app: "project_report",
                title: "Project Summary",
                url: "project_management_report/project_report",
                icon: "work",
                page: "report",
                content_type: "project report",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/project_management",
                app: "task_progress_report",
                title: "Task Progress Report",
                url: "project_management_report/task_progress_report",
                icon: "pending",
                page: "report",
                content_type: "task progress report",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     module: "app/project_management",
            //     app: "project_summary",
            //     title: "Project Expense",
            //     url: "project_management_report/expense_summary",
            //     icon: "local_atm",
            //     page: "report",
            //     content_type: "expense summary",
            //     child_items: []
            // },
            {
                is_linked: true,
                module: "app/project_management",
                app: "timesheet",
                title: "Timesheet Report",
                url: "project_management_report/timesheet",
                icon: "double_arrow",
                page: "report",
                content_type: "timesheet",
                child_items: []
            },
            //     {
            //     is_linked: true,
            //     module: "app/project_management",
            //     app: "project_risk_report",
            //     title: "Project Risk Report",
            //     url: "project_management_report/project_risk_report",
            //     icon: "",
            //     page: "report",
            //     content_type: "project risk report",
            //     child_items: []
            // },
        ]
    },

]