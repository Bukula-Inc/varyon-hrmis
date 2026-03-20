export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/pos",
                app: "POD Dashboard",
                title: "POS Dashboard",
                url: "pos_dashboard",
                icon: "bar_chart_4_bars",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    {
        title: "POS Masters",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/pos",
                app: "pos_dashboard",
                title: "Initialize POS",
                url: "pos_dashboard",
                icon: "bar_chart_4_bars",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/pos",
                app: "pos_setup",
                title: "POS Setup",
                url: "pos_setup/",
                icon: "settings",
                page: "list",
                content_type: "pos setup",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/pos",
                app: "sale_point",
                title: "Sale Point",
                url: "sale_point",
                icon: "point_of_sale",
                page: "list",
                content_type: "sale point",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/pos",
                app: "cashier",
                title: "Cashier",
                url: "cashier",
                icon: "support_agent",
                page: "list",
                content_type: "cashier",
                child_items: []
            },
        ]
    },
    {
        title: "POS Accounting",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/pos",
                app: "pos_opening_entry",
                title: "Opening Entry",
                url: "pos_opening_entry/",
                icon: "login",
                page: "list",
                content_type: "pos opening entry",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/pos",
                app: "pos_closing_entry",
                title: "Closing Entry",
                url: "pos_closing_entry/",
                icon: "move_item",
                page: "list",
                content_type: "pos closing entry",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/pos",
                app: "banking_sheet",
                title: "Banking Sheet",
                url: "banking_sheet",
                icon: "account_balance",
                page: "list",
                content_type: "banking sheet",
                child_items: []
            },
        ]
    },
    {
        title: "POS Reports",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/pos",
                app: "pos_invoice",
                title: "POS Invoice",
                url: "pos_invoice",
                icon: "description",
                page: "list",
                content_type: "pos invoice",
                child_items: []
            },
        ]
    },
]