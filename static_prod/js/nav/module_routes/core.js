export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "data-importation",
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
        title: "Core",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "core",
                title: "Branch",
                url: "branch",
                icon: "brunch_dining",
                page: "list",
                content_type: "branch",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "core",
                title: "Gender",
                url: "gender",
                icon: "male",
                page: "list",
                content_type: "gender",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "industry",
                title: "Industry",
                url: "industry",
                icon: "work_history",
                page: "list",
                content_type: "Industry",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "sector",
                title: "Sector",
                url: "sector",
                icon: "bar_chart_4_bars",
                page: "list",
                content_type: "Sector",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "currency",
                title: "Currency",
                url: "currency",
                icon: "calendar_month",
                page: "list",
                content_type: "Currency",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "cost_center",
                title: "Cost Center",
                url: "cost_center",
                icon: "hub",
                page: "list",
                content_type: "Cost Center",
                child_items: []
            },
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
                is_multi_content: true,
                module: "app/core",
                app: "system_settings",
                title: "System Settings",
                url: "system_settings",
                icon: "tune",
                page: "list",
                content_type: "System Settings",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "default_dashboard",
                title: "Default Dashboards",
                url: "default_dashboard",
                icon: "tune",
                page: "list",
                content_type: "Default Dashboard",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "menu_card",
                title: "Menu Card",
                url: "menu_card",
                icon: "settings",
                page: "list",
                content_type: "Menu Card",
                child_items: []
            },
        ]
    },
    {
        title: "Geo",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "core",
                title: "Location",
                url: "location",
                icon: "location_on",
                page: "list",
                content_type: "Location",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "core",
                title: "Countries",
                url: "country",
                icon: "globe_asia",
                page: "list",
                content_type: "country",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "core",
                title: "State",
                url: "state",
                icon: "apartment",
                page: "list",
                content_type: "State",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "core",
                title: "Province",
                url: "province",
                icon: "emoji_transportation",
                page: "list",
                content_type: "province",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "core",
                title: "District",
                url: "district",
                icon: "family_home",
                page: "list",
                content_type: "District",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "core",
                title: "City",
                url: "city",
                icon: "electric_car",
                page: "list",
                content_type: "City",
                child_items: []
            },
        ]
    },
    {
        title: "Company & Shares",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "company",
                title: "Company",
                url: "company",
                icon: "add_business",
                page: "list",
                content_type: "Company",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "share_management",
                title: "Share Type",
                url: "share_management",
                icon: "partner_reports",
                page: "list",
                content_type: "Share Type",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "share_management",
                title: "Shareholders",
                url: "share_management",
                icon: "partner_reports",
                page: "list",
                content_type: "Shareholders",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "share_management",
                title: "Shares",
                url: "share_management",
                icon: "partner_reports",
                page: "list",
                content_type: "Shares",
                child_items: []
            },
        ]
    },
    {
        title: "Others",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "data_importation",
                title: "Data Importation",
                url: "data_importation",
                icon: "partner_reports",
                page: "list",
                content_type: "data importation",
                child_items: []
            },
            
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/core",
            //     app: "priority",
            //     title: "Priority",
            //     url: "priority",
            //     icon: "priority_high",
            //     page: "list",
            //     content_type: "priority",
            //     child_items:[
            //         {
            //             is_linked: true,
            //             is_multi_content: true,
            //             module: "app/core",
            //             app: "priority",
            //             title: "New Priority",
            //             url: "priority",
            //             icon: "add",
            //             page: "new-form",
            //             content_type: "priority",
            //             child_items:[]
            //         },
            //     ]
            // },
            {
                is_linked: true,
                module: "app/core",
                app: "working_hours",
                title: "Working Hours",
                url: "working_hours",
                icon: "history",
                page: "list",
                content_type: "working hours",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/core",
                app: "rating",
                title: "Rating",
                url: "rating",
                icon: "star",
                page: "list",
                content_type: "Rating",
                child_items: []
            },
            {
                is_linked: true,
                module: "app/core",
                app: "disabled_document",
                title: "Disabled Documents",
                url: "disabled_document",
                icon: "lock",
                page: "list",
                content_type: "Disabled Document",
                child_items: []
            },

            // {
            //     is_linked: false,
            //     is_multi_content: false,
            //     module: "app/core",
            //     app: "core",
            //     title: "Error Log",
            //     url: "error_log",
            //     icon: "warning",
            //     page: "list",
            //     content_type: "error log",
            //     child_items: []
            // },
            // {
            //     is_linked: false,
            //     is_multi_content: false,
            //     module: "app/core",
            //     app: "core",
            //     title: "File Management",
            //     url: "files",
            //     icon: "folder_open",
            //     page: "list",
            //     content_type: "file management",
            //     child_items: []
            // },
        ]
    },
    {
        title: "User Management",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "core",
                title: "User Account",
                url: "user",
                icon: "manage_accounts",
                page: "list",
                content_type: "User",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "core",
                title: "Role",
                url: "role",
                icon: "verified_user",
                page: "list",
                content_type: "Role",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "core",
                title: "Workflow Management",
                url: "workflow",
                icon: "account_tree",
                page: "list",
                content_type: "Workflow",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "audit_trail",
                title: "Audit Trail Report",
                url: "audit_trail",
                icon: "data_loss_prevention",
                page: "list",
                content_type: "audit trail",
                child_items: []
            },
        ]
    },
    
    
    {
        title: "Configurations",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "series",
                title: "Naming Series",
                url: "series",
                icon: "signature",
                page: "list",
                content_type: "Series",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "doc_status",
                title: "Document Status",
                url: "doc_status",
                icon: "inventory",
                page: "list",
                content_type: "Doc Status",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "print_format",
                title: "Print Formats",
                url: "print_format",
                icon: "edit_note",
                page: "list",
                content_type: "Print Format",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "print_configuration",
                title: "Print Configuration",
                url: "print_configuration",
                icon: "print_connect",
                page: "list",
                content_type: "Print Configuration",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/core",
                app: "core",
                title: "Email Configuration",
                url: "email_config",
                icon: "mail",
                page: "list",
                content_type: "Email Config",
                child_items: []
            }
        ]
    }
]