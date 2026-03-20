export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/payroll",
                app: "payroll_dashboard",
                title: "Dashboard",
                url: "payroll",
                icon: "bar_chart_4_bars",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    {
        title: "Payroll Setup",
        routes: [
            // {
            //     is_linked: true,
            //     is_multi_content: false,
            //     module: "app/payroll",
            //     app: "Payroll Settings",
            //     title: "Payroll Settings",
            //     url: "Payroll Settings",
            //     icon: "apartment",
            //     page: "list",
            //     content_type: "Payroll Settings",
            //     child_items: []
            // },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/payroll",
                app: "income_tax_band",
                title: "Income Tax Bands",
                url: "income_tax_band",
                icon: "credit_card_gear",
                page: "list",
                content_type: "income tax band",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/payroll",
                app: "salary_component",
                title: "Salary Component",
                url: "salary_component",
                icon: "credit_card_gear",
                page: "list",
                content_type: "salary component",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/payroll",
                app: "employee_grade",
                title: "Employee Grade",
                url: "employee_grade",
                icon: "credit_card_gear",
                page: "list",
                content_type: "employee grade",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/payroll",
            //     app: "deduction_register",
            //     title: "Deduction Register",
            //     url: "deduction_register",
            //     icon: "bar_chart_4_bars",
            //     page: "List",
            //     content_type: "Deduction Register",
            //     child_items: []
            // }
        ]
    },
    {
        title: "Salary Advance",
        routes: [
            {
                is_linked: false,
                module: "app/payroll",
                app: "salary_adavance",
                title: "Advance Setup",
                url: "advance_setup",
                icon: "settings",
                page: "list",
                content_type: "advance setup",
                child_items: []
            },
            {
                is_linked: false,
                module: "app/payroll",
                app: "salary_advance",
                title: "Advance Applications",
                url: "advance_application",
                icon: "payments",
                page: "list",
                content_type: "advance application",
                child_items: []
            },
            {
                is_linked: false,
                module: "app/payroll",
                app: "advance_balance",
                icon: "account_balance_wallet",
                title: "Advance Balances",
                url: "advance_balance",
                page: "report",
                content_type: "advance balance",
                child_items: []
            },
        ]
    },
    {
        title: "Overtime",
        routes: [
            {
                is_linked: true,
                module: "app/payroll",
                app: "overtime_setup",
                title: "Overtime Setup",
                url: "overtime_setup",
                icon: "settings",
                page: "list",
                content_type: "overtime setup",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/payroll",
                app: "overtime",
                title: "Overtime Applicantions",
                url: "overtime",
                icon: "work_history",
                page: "list",
                content_type: "overtime",
                child_items: []
            },
      
        ]
    },
    {
        title: "Commission",
        routes: [
            {
                is_linked: true,
                module: "app/payroll",
                app: "commission_setup",
                title: "Commission Setup",
                url: "commission_setup",
                icon: "settings",
                page: "list",
                content_type: "commission setup",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     module: "app/payroll",
            //     app: "overtime",
            //     title: "Overtime Applicantions",
            //     url: "overtime",
            //     icon: "work_history",
            //     page: "list",
            //     content_type: "overtime",
            //     child_items: []
            // },
      
        ]
    },
    {
        title: "Payroll Processor",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/payroll",
                app: "payroll_processor",
                title: "Run Payroll",
                url: "payroll_processor",
                icon: "memory",
                page: "list",
                content_type: "Payroll Processor",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/payroll",
                app: "payslip",
                title: "Payslip",
                url: "payslip",
                icon: "memory",
                page: "list",
                content_type: "Payslip",
                child_items: []
            }
        ]
    },
    {
        title: "Reports",
        routes: [
            {
                is_linked: false,
                module: "app/payroll",
                app: "monthly_attendance",
                title: "Monthly Attendance Sheet",
                url: "payroll_reports/monthly_attendance",
                icon: "groups",
                page: "report",
                content_type: "monthly attendance",
                child_items: []
            },
            {
                is_linked: false,
                module: "app/payroll",
                app: "paye_report",
                title: "Paye",
                url: "payroll_reports/paye_report",
                icon: "request_quote",
                page: "report",
                content_type: "paye report",
                child_items: []
            },
            {
                is_linked: false,
                module: "app/payroll",
                app: "napsa_report",
                title: "Napsa",
                url: "payroll_reports/napsa_report",
                icon: "wallet",
                page: "report",
                content_type: "napsa report",
                child_items: []
            },
            {
                is_linked: false,
                module: "app/payroll",
                app: "nhima_report",
                title: "Nhima",
                url: "payroll_reports/nhima_report",
                icon: "monitor_heart",
                page: "report",
                content_type: "nhima report",
                child_items: []
            },
            {
                is_linked: false,
                module: "app/payroll",
                app: "private_insurance_report",
                title: "Private Insurance" ,
                url: "payroll_reports/private_insurance_report",
                icon: "assured_workload",
                page: "report",
                content_type: "private insurance report",
                child_items: []
            },
            // {
            //     is_linked: false,
            //     module: "app/payroll",
            //     app: "statutory_report",
            //     title: "Statutory Report",
            //     url: "statutory_report",
            //     icon: "",
            //     page: "report",
            //     content_type: "statutory report",
            //     child_items: []
            // },
            {
                is_linked: false,
                module: "app/payroll",
                app: "overtime_report",
                title: "Overtime",
                url: "payroll_reports/overtime_report",
                icon: "overview",
                page: "report",
                content_type: "Overtime Report",
                child_items: [] 
            },
            {
                is_linked: false,
                module: "app/payroll",
                app: "payroll_summary",
                title: "Payroll Summary",
                url: "payroll_reports/payroll_summary",
                icon: "summarize",
                page: "report",
                content_type: "payroll summary",
                child_items: []
            },
        ]
    },
   

]