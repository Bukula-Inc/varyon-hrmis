export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "tenant_dashboard",
                title: "Dashboard",
                url: "tenant_dashboard",
                icon: "bar_chart_4_bars",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    {
        title: "Masters",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "domain_controller",
                title: "Domain Controller",
                url: "domain_controller",
                icon: "brunch_dining",
                page: "list",
                content_type: "Domain Controller",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "billing_config",
                title: "Billing Config",
                url: "billing_config",
                icon: "brunch_dining",
                page: "list",
                content_type: "Billing Config",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "module_group",
                title: "Module Group",
                url: "module_group",
                icon: "brunch_dining",
                page: "list",
                content_type: "Module Group",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "module_pricing",
                title: "Module Pricing",
                url: "module_pricing",
                icon: "brunch_dining",
                page: "list",
                content_type: "Module Pricing",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "license",
                title: "License",
                url: "license",
                icon: "brunch_dining",
                page: "list",
                content_type: "License",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/controller",
                app: "module",
                title: "Modules",
                url: "module",
                icon: "view_module",
                page: "list",
                content_type: "module",
                child_items: []
            },

        ],
    },
    {
        title: "Registrations & Subscriptions",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "tenant",
                title: "Tenants",
                url: "tenant",
                icon: "brunch_dining",
                page: "list",
                content_type: "Tenant",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "subscription",
                title: "Subscriptions",
                url: "subscription",
                icon: "database",
                page: "list",
                content_type: "Subscription",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "storage",
                title: "Storage",
                url: "storage",
                icon: "storage",
                page: "list",
                content_type: "Storage",
                child_items: []
            },
        ]
    },
    {
        title: "Cron Jobs",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "background_job",
                title: "Background Job",
                url: "background_job",
                icon: "brunch_dining",
                page: "list",
                content_type: "Background Job",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/controller",
                app: "background_job_results",
                title: "Background Job Results",
                url: "background_job_results",
                icon: "brunch_dining",
                page: "list",
                content_type: "Background Job Results",
                child_items: []
            },
        ]
    },
   
]