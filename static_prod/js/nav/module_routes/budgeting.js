export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/budgeting",
                app: "budgeting_dashboard",
                title: "Dashboard",
                url: "budgeting",
                icon: "calculate",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    {
        title: "Budgeting Masters",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/budgeting",
                app: "budget_setup",
                title: "Budget Setup",
                url: "budget_setup",
                icon: "post_add",
                page: "list",
                content_type: "Budget Setup",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/budgeting",
                app: "departmental_budget",
                title: "Departmental Budget",
                url: "departmental_budget",
                icon: "account_balance",
                page: "list",
                content_type: "Departmental Budget",
                child_items: [],
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/budgeting",
                app: "budget_item",
                title: "Budget Item",
                url: "budget_item",
                icon: "production_quantity_limits",
                page: "list",
                content_type: "budget item",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/budgeting",
                        app: "budget_item",
                        title: "New Item",
                        url: "budget_item",
                        icon: "add",
                        page: "new-form",
                        content_type: "budget item",
                        child_items: []
                    },
                ]
            },
            
        ],
    },
]