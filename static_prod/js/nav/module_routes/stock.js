export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/stock",
                app: "stock_dashboard",
                title: "Dashboard",
                url: "stock",
                icon: "bar_chart_4_bars",
                page: "dashboard",
                content_type: "Dashboard",
                child_items: []
            }
        ]
    },
    
    {
        title: "Settings",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_setting",
                title: "Stock Setting",
                url: "stock_setting",
                icon: "settings",
                page: "new-form",
                content_type: "Stock Setting",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "warehouse",
                title: "Warehouse",
                url: "warehouse",
                icon: "factory",
                page: "list",
                content_type: "Warehouse",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/stock",
                        app: "warehouse",
                        title: "New Warehouse",
                        url: "warehouse",
                        icon: "add",
                        page: "new-form",
                        content_type: "Warehouse",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "uom",
                title: "Unit Of Measure",
                url: "uom",
                icon: "square_foot",
                page: "list",
                content_type: "Unit Of Measure",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/stock",
                        app: "uom",
                        title: "New Unit Of Measure",
                        url: "uom",
                        icon: "add",
                        page: "new-form",
                        content_type: "Unit Of Measure",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "brand",
                title: "Brand Categories",
                url: "brand_category",
                icon: "category",
                page: "list",
                content_type: "Brand category",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/stock",
                        app: "brand",
                        title: "New Brand Categories",
                        url: "brand_category",
                        icon: "add",
                        page: "new-form",
                        content_type: "Brand category",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "brand",
                title: "Brand",
                url: "brand",
                icon: "brand_family",
                page: "list",
                content_type: "Brand",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/stock",
                        app: "brand",
                        title: "New Brand",
                        url: "brand",
                        icon: "add",
                        page: "new-form",
                        content_type: "Brand",
                        child_items: []
                    },
                ]
            },
        ]
    },
    {
        title: "Items and Pricing",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "items",
                title: "Items",
                url: "items",
                icon: "production_quantity_limits",
                page: "list",
                content_type: "stock_items",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/stock",
                        app: "items",
                        title: "New Item",
                        url: "items",
                        icon: "add",
                        page: "new-form",
                        content_type: "stock_items",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "price_list",
                title: "Price List",
                url: "price_list",
                icon: "receipt_long",
                page: "list",
                content_type: "Price List",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/stock",
                        app: "price_list",
                        title: "New Price List",
                        url: "price_list",
                        icon: "add",
                        page: "new-form",
                        content_type: "Price List",
                        child_items: []
                    }
                ]
            },
            // {
            //     is_linked: true,
            //     is_multi_content: false,
            //     module: "app/stock",
            //     app: "item_manufacturer",
            //     title: "Item Manufacturer",
            //     url: "item_manufacturer",
            //     icon: "precision_manufacturing",
            //     page: "list",
            //     content_type: "Item Manufacturer",
            //     child_items: []
            // },
        ]
    },
    {
        title: "Stock Transactions",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "goods_received_note",
                title: "Goods Received Note",
                url: "goods_received_note",
                icon: "receipt_long",
                page: "list",
                content_type: "Goods Received Note",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "accounting",
                app: "delivery",
                title: "Delivery Note",
                url: "delivery",
                icon: "storefront",
                page: "list",
                content_type: "delivery note",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "accounting",
                        app: "delivery",
                        title: "Dashboard",
                        url: "delivery",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "delivery note",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "accounting",
                        app: "delivery",
                        title: "New Delivery Note",
                        url: "delivery",
                        icon: "post_add",
                        page: "new_form",
                        content_type: "delivery note",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "Accounts",
                app: "purchase_receipt",
                title: "Purchase Receipt",
                url: "delivery_note",
                icon: "sell",
                page: "list",
                content_type: "Purchase Receipt",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_transfer",
                title: "Stock Transfer",
                url: "stock_transfer",
                icon: "move_up",
                page: "list",
                content_type: "Stock Transfer",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/stock",
                        app: "stock_transfer",
                        title: "Initialize Stock Transfer",
                        url: "stock_transfer",
                        icon: "local_shipping",
                        page: "new-form",
                        content_type: "Stock Transfer",
                        child_items: []
                    },
                ]
            },
        ]
    },
    {
        title: "Stock Reports",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_ledger",
                title: "Stock Ledger",
                url: "stock_reports/stock_ledger",
                icon: "summarize",
                page: "report",
                content_type: "Stock Ledger",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_balance",
                title: "Stock Balance",
                url: "stock_reports/stock_balance",
                icon: "balance",
                page: "report",
                content_type: "Stock Balance",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_valuation",
                title: "Stock Valuation",
                url: "stock_reports/stock_valuation",
                icon: "join_inner",
                page: "report",
                content_type: "Stock Valuation",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_summary",
                title: "Stock Summary",
                url: "stock_reports/stock_summary",
                icon: "timeline",
                page: "report",
                content_type: "Stock Summary",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_aging",
                title: "Stock Aging",
                url: "stock_reports/stock_aging",
                icon: "pending_actions",
                page: "report",
                content_type: "Stock Aging",
                child_items: []
            },
        ]
    },
    // {
    //     title: "Serial No and Batch",
    //     routes: [
    //         // {
    //         //     is_linked: true,
    //         //     is_multi_content: false,
    //         //     module: "app/stock",
    //         //     app: "serial",
    //         //     title: "serial No",
    //         //     url: "serial_no",
    //         //     icon: "qr_code_2",
    //         //     page: "list",
    //         //     content_type: "serial No",
    //         //     child_items: []
    //         // },
    //         {
    //             is_linked: true,
    //             is_multi_content: false,
    //             module: "app/stock",
    //             app: "batch",
    //             title: "Batch",
    //             url: "batch",
    //             icon: "batch_prediction",
    //             page: "list",
    //             content_type: "Batch",
    //             child_items: []
    //         },
    //     ]
    // },
    {
        title: "Tools",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_entry",
                title: "Stock Entry",
                url: "stock_entry",
                icon: "folder_limited",
                page: "list",
                content_type: "Stock Entry",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_revaluation",
                title: "Stock Revaluation",
                url: "stock_revaluation",
                icon: "diamond",
                page: "list",
                content_type: "Stock Revaluation",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_reconciliation",
                title: "Stock Reconciliation",
                url: "stock_reconciliation",
                icon: "restart_alt",
                page: "list",
                content_type: "Stock Reconciliation",
                child_items: []
            },
            
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_check",
                title: "Stock Check",
                url: "stock_check",
                icon: "inventory",
                page: "list",
                content_type: "Stock Check",
                child_items: []
            },
            // {
            //     is_linked: false,
            //     is_multi_content: false,
            //     module: "app/stock",
            //     app: "stock_balance",
            //     title: "Quick Stock Balance",
            //     url: "quick_stock_balance",
            //     icon: "quick_reference_all",
            //     page: "list",
            //     content_type: "Quick Stock Balance",
            //     child_items: []
            // },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "quality_inspection",
                title: "Quality Inspection",
                url: "quality_inspection",
                icon: "24mp",
                page: "list",
                content_type: "Quality Inspection",
                child_items: []
            },
        ]
    },
    {
        title: "Key Reports",
        routes: [
            // {
            //     is_linked: true,
            //     is_multi_content: false,
            //     module: "app/stock",
            //     app: "items",
            //     title: "Item Wise Price List",
            //     url: "stock_reports/item_wise_price_list",
            //     icon: "bubble_chart",
            //     page: "report",
            //     content_type: "Item Wise Price List",
            //     child_items: []
            // },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/stock",
                app: "stock_analysis",
                title: "Stock Analysis",
                url: "stock_reports/stock_analysis",
                icon: "query_stats",
                page: "report",
                content_type: "Stock Analysis",
                child_items: []
            },
            
        ]
    },
    

]