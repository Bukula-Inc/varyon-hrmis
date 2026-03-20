export default [
    {
        title: "Dashboard",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "accounting_dashboard",
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
        title: "Accounting Masters",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "accounts",
                title: "Chart Of Accounts",
                url: "accounts",
                icon: "account_tree",
                page: "list",
                content_type: "accounts",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "accounts",
                        title: "New Account",
                        url: "accounts",
                        icon: "bar_chart_4_bars",
                        page: "new-form",
                        content_type: "accounts",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "accounting_defaults",
                title: "Accounting Defaults (Settings)",
                url: "accounting_defaults",
                icon: "component_exchange",
                page: "list",
                content_type: "accounting defaults",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "accounting_period",
                title: "Accounting Period",
                url: "accounting_period",
                icon: "calendar_month",
                page: "list",
                content_type: "Accounting Period",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "company",
                title: "Company",
                url: "company",
                icon: "home_repair_service",
                page: "list",
                content_type: "Company",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "currency",
                title: "Currency",
                url: "currency",
                icon: "paid",
                page: "list",
                content_type: "Currency",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/core",
                app: "currency",
                title: "Exchange Rates",
                url: "currency",
                icon: "trending_down",
                page: "list",
                content_type: "Exchange Rate",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/accounting",
                app: "accounting_items",
                title: "Items",
                url: "accounting_items",
                icon: "production_quantity_limits",
                page: "list",
                content_type: "items",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/accounting",
                        app: "accounting_items",
                        title: "New Items",
                        url: "accounting_items",
                        icon: "add",
                        page: "new-form",
                        content_type: "items",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "gl_entry",
                title: "GL Entries",
                url: "gl_entry",
                icon: "calendar_month",
                page: "list",
                content_type: "gl entry",
                child_items: []
            }
        ]
    },
    {
        title: "Customer",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "receivables",
                title: "Dashboard",
                url: "receivables",
                icon: "dashboard",
                page: "list",
                content_type: "Dashboard",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "trading",
                title: "Customer",
                url: "trading",
                icon: "partner_exchange",
                page: "list",
                content_type: "customer",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "trading",
                        title: "Dashboard",
                        url: "trading",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "customer",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "trading",
                        title: "New Customer",
                        url: "trading",
                        icon: "person_add",
                        page: "new-form",
                        content_type: "customer",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "receivables",
                title: "Quotations",
                url: "receivables",
                icon: "request_quote",
                page: "list",
                content_type: "Quotation",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "receivables",
                        title: "Dashboard",
                        url: "receivables",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "Quotation",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "receivables",
                        title: "New Quotation",
                        url: "receivables",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "Quotation",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "receivables",
                title: "Tax Invoice",
                url: "receivables",
                icon: "receipt_long",
                page: "list",
                content_type: "tax invoice",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "receivables",
                        title: "Dashboard",
                        url: "receivables",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "tax invoice",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "receivables",
                        title: "New Tax Invoice",
                        url: "receivables",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "tax invoice",
                        child_items: []
                    },
                ]
            },
            
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "invoicing",
                title: "Credit Note",
                url: "invoicing",
                icon: "storefront",
                page: "list",
                content_type: "credit note",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "invoicing",
                        title: "Dashboard",
                        url: "invoicing",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "credit note",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "invoicing",
                        title: "New Credit Note",
                        url: "invoicing",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "credit note",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "delivery",
                title: "Delivery Note",
                url: "delivery",
                icon: "storefront",
                page: "list",
                content_type: "delivery note",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
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
                        module: "app/accounting",
                        app: "delivery",
                        title: "New Delivery Note",
                        url: "delivery",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "delivery note",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "receipting",
                title: "Receipting",
                url: "receipting",
                icon: "receipt",
                page: "list",
                content_type: "receipt",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "receipting",
                        title: "Dashboard",
                        url: "receipting",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "receipt",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "receipting",
                        title: "New Receipt",
                        url: "receipting",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "receipt",
                        child_items: []
                    }
                ]
            },
        ]
    },
    {
        title: "Supplier",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "payables",
                title: "Dashboard",
                url: "payables",
                icon: "dashboard",
                page: "list",
                content_type: "Dashboard",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "trading",
                title: "Supplier",
                url: "trading",
                icon: "partner_exchange",
                page: "list",
                content_type: "supplier",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "trading",
                        title: "Dashboard",
                        url: "trading",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "supplier",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "trading",
                        title: "New Supplier",
                        url: "trading",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "supplier",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "payables",
                title: "Purchase Invoice",
                url: "payables",
                icon: "receipt_long",
                page: "list",
                content_type: "purchase invoice",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "payables",
                        title: "Dashboard",
                        url: "payables",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "Purchase Invoice",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "payables",
                        title: "New Purchase Invoice",
                        url: "payables",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "Purchase Invoice",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "payables",
                title: "Purchase Order",
                url: "payables",
                icon: "shopping_cart",
                page: "list",
                content_type: "purchase order",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "payables",
                        title: "Dashboard",
                        url: "payables",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "purchase order",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "payables",
                        title: "New Purchase Order",
                        url: "payables",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "purchase order",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "receipting",
                title: "Payments",
                url: "receipting",
                icon: "credit_score",
                page: "list",
                content_type: "payment",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "receipting",
                        title: "Dashboard",
                        url: "receipting",
                        icon: "dashboard_customize",
                        page: "list",
                        content_type: "payment",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "receipting",
                        title: "New Payment",
                        url: "receipting",
                        icon: "post_add",
                        page: "new-form",
                        content_type: "payment",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Accounts payable",
                url: "accounting_reports/accounts_payable",
                icon: "chart_data",
                page: "report",
                content_type: "accounts payable",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Accounts payable Summary",
                url: "accounting_reports/accounts_payable_summary",
                icon: "monitoring",
                page: "report",
                content_type: "accounts payable summary",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Purchase Register",
                url: "",
                icon: "credit_score",
                page: "list",
                content_type: "",
                child_items: []
            },

        ]
    },
    {
        title: "Banking",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "banking",
                title: "Banks Accounts",
                url: "banking",
                icon: "account_balance",
                page: "list",
                content_type: "Bank Account",
                child_items: [{
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "banking",
                        title: "Banking Dashboard",
                        url: "banking",
                        icon: "account_balance",
                        page: "list",
                        content_type: "Bank Account",
                        child_items: []
                    },
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "banking",
                        title: "New Bank Account",
                        url: "banking",
                        icon: "account_balance",
                        page: "new-form",
                        content_type: "Bank Account",
                        child_items: []
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "bank_transaction",
                title: "Bank Transactions",
                url: "banking",
                icon: "account_balance",
                page: "list",
                content_type: "Transaction Entries",
                child_items: []
            },

            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "cashbook_report",
                title: "Cashbook Report",
                url: "accounting_reports/cashbook_report",
                icon: "order_approve",
                page: "report",
                content_type: "Cashbook Report",
                child_items: []
            }
        ]
    },
    {
        title: "Cashbook",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/accounting",
                app: "journal_entry",
                title: "Journal Entry",
                url: "journal_entry/",
                icon: "local_atm",
                page: "list",
                content_type: "journal entry",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: false,
                        module: "app/accounting",
                        app: "journal_entry",
                        title: "New Journal Entry",
                        url: "journal_entry/",
                        icon: "local_atm",
                        page: "new-form",
                        content_type: "Journal Entry",
                        child_items: []
                    }
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "imprest",
                title: "Imprest",
                url: "imprest/",
                icon: "request_quote",
                page: "list",
                content_type: "Imprest",
                child_items: [
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/accounting",
                        app: "imprest",
                        title: "New Imprest",
                        url: "imprest/",
                        icon: "request_quote",
                        page: "new-form",
                        content_type: "Imprest",
                        child_items: []
                    },
                ]
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
                module: "app/accounting",
                app: "imprest_report",
                title: "Imprest Report",
                url: "accounting_reports/imprest_report/",
                icon: "summarize",
                page: "report",
                content_type: "Imprest Report",
                child_items: []
            }
        ]
    },
    {
        title: "Financial Reports",
        routes: [
            
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Trial balance",
                url: "accounting_reports/trial_balance",
                icon: "balance",
                page: "report",
                content_type: "trial balance",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Statement Of Profit Or Loss & Other Comprehensive Income",
                url: "accounting_reports/income_statement",
                icon: "chart_data",
                page: "report",
                content_type: "income statement",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Statement Of Financial Position",
                url: "accounting_reports/balance_sheet",
                icon: "pie_chart",
                page: "report",
                content_type: "balance sheet",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/accounting",
            //     app: "reports",
            //     title: "Gross Profit",
            //     url: "accounting_reports/gross_profit",
            //     icon: "request_quote",
            //     page: "report",
            //     content_type: "gross profit",
            //     child_items: []
            // },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/accounting",
            //     app: "reports",
            //     title: "Profitability Analysis",
            //     url: "accounting_reports/gross_profit",
            //     icon: "legend_toggle",
            //     page: "report",
            //     content_type: "profitability analysis",
            //     child_items: []
            // },

        ]
    },
    // {
    //     title: "Budgeting",
    //     routes: [{
    //             is_linked: false,
    //             is_multi_content: true,
    //             module: "app/accounting",
    //             app: "budget",
    //             title: "Budget",
    //             url: "accounting-reports/budget",
    //             icon: "checklist_rtl",
    //             page: "list",
    //             content_type: "budget",
    //             child_items: []
    //         },
    //         {
    //             is_linked: false,
    //             is_multi_content: true,
    //             module: "app/accounting",
    //             app: "budget",
    //             title: "Budget Variance Report",
    //             url: "accounting-reports/budget-variance-report/",
    //             icon: "incomplete_circle",
    //             page: "list",
    //             content_type: "budget variance",
    //             child_items: []
    //         },
    //         {
    //             is_linked: false,
    //             is_multi_content: true,
    //             module: "app/accounting",
    //             app: "budget",
    //             title: "Monthly Distribution",
    //             url: "accounting-reports/monthly-distribution",
    //             icon: "calendar_view_week",
    //             page: "list",
    //             content_type: "monthly distribution",
    //             child_items: []
    //         },
    //         {
    //             is_linked: false,
    //             is_multi_content: true,
    //             module: "app/accounting",
    //             app: "reports",
    //             title: "Budget Analysis",
    //             url: "accounting_reports/budget_analysis",
    //             icon: "donut_small",
    //             page: "report",
    //             content_type: "budget analysis",
    //             child_items: []
    //         },

    //     ]
    // },
    
    {
        title: "Reports",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/accounting",
                app: "reports",
                title: "Account Transactions",
                url: "accounting_reports/account_transactions",
                icon: "chart_data",
                page: "report",
                content_type: "account transactions",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Trade Receivables",
                url: "accounting_reports/trade_receivables",
                icon: "summarize",
                page: "report",
                content_type: "Trade Receivables",
                child_items: []
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Trade Payables",
                url: "accounting_reports/trade_payables",
                icon: "summarize",
                page: "report",
                content_type: "Trade Payables",
                child_items: []
            },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/accounting",
            //     app: "reports",
            //     title: "Sales Report",
            //     url: "accounting_reports/sales_report",
            //     icon: "analytics",
            //     page: "report",
            //     content_type: "Sales Report",
            //     child_items: []
            // },
            // {
            //     is_linked: true,
            //     is_multi_content: true,
            //     module: "app/accounting",
            //     app: "reports",
            //     title: "Purchase Report",
            //     url: "accounting_reports/purchase_report",
            //     icon: "analytics",
            //     page: "report",
            //     content_type: "Purchase Report",
            //     child_items: []
            // },
            
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Customer Statement",
                url: "accounting_reports/statements",
                icon: "lab_profile",
                page: "report",
                content_type: "customer statement",
                // child_items: [{
                //         is_linked: true,
                //         is_multi_content: true,
                //         module: "app/accounting",
                //         app: "reports",
                //         title: "Customer Statement",
                //         url: "accounting_reports/statements",
                //         icon: "quick_reference",
                //         page: "report",
                //         content_type: "customer statement",
                //         child_items: []
                //     },
                //     // {
                //     //     is_linked: true,
                //     //     is_multi_content: true,
                //     //     module: "app/accounting",
                //     //     app: "reports",
                //     //     title: "Customer Transactions",
                //     //     url: "accounting_reports/statements",
                //     //     icon: "summarize",
                //     //     page: "report",
                //     //     content_type: "customer transactions",
                //     //     child_items: []
                //     // },
                // ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/accounting",
                app: "reports",
                title: "Supplier Statement",
                url: "accounting_reports/statements",
                icon: "quick_reference",
                page: "report",
                content_type: "supplier statement",
                // child_items: [{
                //         is_linked: true,
                //         is_multi_content: true,
                //         module: "app/accounting",
                //         app: "reports",
                //         title: "Supplier Statement",
                //         url: "accounting_reports/statements",
                //         icon: "list_alt_add",
                //         page: "report",
                //         content_type: "supplier statement",
                //         child_items: []
                //     },
                //     {
                //         is_linked: true,
                //         is_multi_content: true,
                //         module: "app/accounting",
                //         app: "reports",
                //         title: "Supplier Transactions",
                //         url: "accounting_reports/statements",
                //         icon: "summarize",
                //         page: "report",
                //         content_type: "supplier transactions",
                //         child_items: []
                //     },
                // ]
            }
        ]
    },
    {
        title: "Taxes",
        routes: [
            {
                is_linked: true,
                is_multi_content: false,
                module: "app/accounting",
                app: "tax_template",
                title: "Tax Templates",
                url: "tax_template",
                icon: "data_thresholding",
                page: "list",
                content_type: "Tax Template",
                child_items: []
            },
            // {
            //     is_linked: false,
            //     is_multi_content: true,
            //     module: "app/accounting",
            //     app: "tax_schedules",
            //     title: "Tax Schedules",
            //     url: "accounting_reports/tax_schedules",
            //     icon: "pending_actions",
            //     page: "report",
            //     content_type: "schedule 1",
            //     child_items: [{
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 1",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 1",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 2",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 2",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 3",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 3",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 4",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 4",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 5",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 5",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 6",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 6",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 7",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 7",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 8",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 8",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 9",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 9",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 10",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 10",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 11",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 11",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 12",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 12",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 13",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 13",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 14",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 14",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_schedules",
            //             title: "Schedule 15",
            //             url: "accounting_reports/tax_schedules",
            //             icon: "pending_actions",
            //             page: "report",
            //             content_type: "Schedule 15",
            //             child_items: []
            //         },
            //     ]
            // },
            // {
            //     is_linked: false,
            //     is_multi_content: true,
            //     module: "app/accounting",
            //     app: "tax_sections",
            //     title: "Tax Sections",
            //     url: "tax_sections",
            //     icon: "widgets",
            //     page: "report",
            //     content_type: "section a",
            //     child_items: [{
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_sections",
            //             title: "Section A",
            //             url: "tax_sections",
            //             icon: "widgets",
            //             page: "report",
            //             content_type: "section a",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_sections",
            //             title: "Section B",
            //             url: "tax_sections",
            //             icon: "widgets",
            //             page: "report",
            //             content_type: "section b",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_sections",
            //             title: "Section C",
            //             url: "tax_sections",
            //             icon: "widgets",
            //             page: "report",
            //             content_type: "section c",
            //             child_items: []
            //         },
            //         {
            //             is_linked: false,
            //             is_multi_content: true,
            //             module: "app/accounting",
            //             app: "tax_sections",
            //             title: "Section C",
            //             url: "tax_sections",
            //             icon: "widgets",
            //             page: "report",
            //             content_type: "section c",
            //             child_items: []
            //         },
            //     ]
            // },
        ]
    },
]