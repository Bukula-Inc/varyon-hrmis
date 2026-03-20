export default [{
    title: "Dashboard",
    routes: [{
        is_linked: true,
        is_multi_content: true,
        module: "app/crm",
        app: "crm_dashboard",
        title: "Dashboard",
        url: "crm_dashboard",
        icon: "bar_chart_4_bars",
        page: "dashboard",
        content_type: "Dashboard",
        child_items: []
    }]
},
{
    title: "CRM MASTERS",
    routes: [        
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/core",
            app: "priority",
            title: "Priority",
            url: "priority",
            icon: "priority_high",
            page: "list",
            content_type: "priority",
            child_items:[
                {
                    is_linked: true,
                    is_multi_content: true,
                    module: "app/core",
                    app: "priority",
                    title: "New Priority",
                    url: "priority",
                    icon: "add",
                    page: "new-form",
                    content_type: "priority",
                    child_items:[]
                },
            ]
        },

        {
            is_linked: true,
            module: "app/core",
            app: "working_hours",
            title: "Working Hours",
            url: "working_hours",
            icon: "history",
            page: "list",
            content_type: "working hours",
            child_items: [
                {
                    is_linked: true,
                    module: "app/core",
                    app: "working_hours",
                    title: "Working Hours",
                    url: "working_hours",
                    icon: "add",
                    page: "new-form",
                    content_type: "working hours",
                    child_items: []
                },
            ]
        },
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "ticket_type",
            title: "Ticket Type",
            url: "ticket_type",
            icon: "format_size",
            page: "list",
            content_type: "ticket type",
            child_items:[
                {
                    is_linked: true,
                    is_multi_content: true,
                    module: "app/crm",
                    app: "ticket_type",
                    title: "New Ticket Type",
                    url: "ticket_type",
                    icon: "add",
                    page: "new-form",
                    content_type: "ticket type",
                    child_items:[]
                },
            ]
        },
        
    ],
    
},
{
    title: "CRM SUPPORT DESK",
    routes: [
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "support_desk",
            title: "Support Dashboard",
            url: "support_desk",
            icon: "dataset_linked",
            page: "dashboard",
            content_type: "Dashboard",
            child_items:[]
        },
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "customer_service",
            title: "Service/Product",
            url: "customer_service",
            icon: "dataset_linked",
            page: "list",
            content_type: "customer service",
            child_items:[]
        },
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "relation_manager",
            title: "Relationship Manager",
            url: "relation_manager",
            icon: "linked_services",
            page: "list",
            content_type: "relation manager",
            child_items:[]
        },
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "support_team",
            title: "Support Team",
            url: "support_team",
            icon: "group_add",
            page: "list",
            content_type: "support team",
            child_items:[]
        },
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "customer_info",
            title: "Customer Info",
            url: "customer_info",
            icon: "people",
            page: "list",
            content_type: "Customer Info",
            child_items:[
                {
                    is_linked: true,
                    is_multi_content: true,
                    module: "app/crm",
                    app: "customer_info",
                    title: "Add Customer Info",
                    url: "customer_info",
                    icon: "group_add",
                    page: "new-form",
                    content_type: "Customer Info",
                    child_items:[]
                },
            ]
        },
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "service_level_agreement",
            title: "Service Level Agreement",
            url: "service_level_agreement",
            icon: "handshake",
            page: "list",
            content_type: "service level agreement",
            child_items:[
                {
                    is_linked: true,
                    is_multi_content: true,
                    module: "app/crm",
                    app: "service_level_agreement",
                    title: "New Service Level Agreement",
                    url: "service_level_agreement",
                    icon: "add",
                    page: "new-form",
                    content_type: "service level agreement",
                    child_items:[]
                },
            ]
        },
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "escalation_rule",
            title: "Escalation Rules",
            url: "escalation_rule",
            icon: "escalator",
            page: "list",
            content_type: "escalation rule",
            child_items:[{
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "escalation_rule",
                title: "New Escalation Rules",
                url: "escalation_rule",
                icon: "add",
                page: "new-form",
                content_type: "escalation rule",
                child_items:[]
            },]
        },
        {
            is_linked: true,
            is_multi_content: true,
            module: "app/crm",
            app: "ticket",
            title: "Tickets",
            url: "ticket",
            icon: "dataset_linked",
            page: "list",
            content_type: "ticket",
            child_items:[
                {
                    is_linked: true,
                    is_multi_content: true,
                    module: "app/crm",
                    app: "ticket",
                    title: "New Tickets",
                    url: "ticket",
                    icon: "add",
                    page: "new-form",
                    content_type: "ticket",
                    child_items:[]
                },
            ]
        },
    ],
    
},



    {
        title: "CRM SALES PIPELINE",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "sales_person",
                title: "Sales Person",
                url: "sales_person",
                icon: "support_agent",
                page: "list",
                content_type: "sales person",
                child_items:[]
            },            
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "lead",
                title: "Lead",
                url: "lead",
                icon: "person",
                page: "list",
                content_type: "lead",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "prospect",
                title: "Prospect",
                url: "prospect",
                icon: "support",
                page: "list",
                content_type: "prospect",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "contract",
                title: "Contract",
                url: "contract",
                icon: "contract",
                page: "list",
                content_type: "contract",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "crm_customer",
                title: "Customer",
                url: "crm_customer",
                icon: "recent_patient",
                page: "list",
                content_type: "crm customer",
                child_items:[
                    {
                        is_linked: true,
                        is_multi_content: true,
                        module: "app/crm",
                        app: "crm_customer",
                        title: "New Customer",
                        url: "crm_customer",
                        icon: "add",
                        page: "new-form",
                        content_type: "crm customer",
                        child_items:[]
                    },
                ]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "opportunity",
                title: "Opportunity",
                url: "opportunity",
                icon: "vpn_key_alert",
                page: "list",
                content_type: "opportunity",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "appointment",
                title: "Appointment",
                url: "appointment",
                icon: "meeting_room",
                page: "list",
                content_type: "appointment",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "sales_stage",
                title: "Sales Stage",
                url: "sales_stage",
                icon: "approval",
                page: "list",
                content_type: "sales stage",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "lead_sourcce",
                title: "Lead Source",
                url: "lead_source",
                icon: "source_environment",
                page: "list",
                content_type: "lead source",
                child_items:[]
            },
        ]
    },
    // {
    //     title: "Campaign",
    //     routes: [
    //         {
    //             is_linked: true,
    //             is_multi_content: true,
    //             module: "app/crm",
    //             app: "campaign",
    //             title: "Social Media Campaign",
    //             url: "campaign",
    //             icon: "campaign",
    //             page: "list",
    //             content_type: "campaign",
    //             child_items:[]
    //         },
    //         {
    //             is_linked: true,
    //             is_multi_content: true,
    //             module: "app/crm",
    //             app: "email_campaign",
    //             title: "Email Campaign",
    //             url: "email_campaign",
    //             icon: "mail",
    //             page: "list",
    //             content_type: "email campaign",
    //             child_items:[]
    //         },
    //         {
    //             is_linked: true,
    //             is_multi_content: true,
    //             module: "app/crm",
    //             app: "news_letter",
    //             title: "News Letter",
    //             url: "news_letter",
    //             icon: "news",
    //             page: "list",
    //             content_type: "news letter",
    //             child_items:[]
    //         },
    //         {
    //             is_linked: true,
    //             is_multi_content: true,
    //             module: "app/crm",
    //             app: "email_group",
    //             title: "Email Group",
    //             url: "email_group",
    //             icon: "group",
    //             page: "list",
    //             content_type: "email group",
    //             child_items:[]
    //         },
    //     ]
    // },
    {
        title: "Reports",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "lead_details",
                title: "Lead Details",
                url: "crm_report/lead_details",
                icon: "real_estate_agent",
                page: "report",
                content_type: "lead details",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "sales_funnel",
                title: "Sales Funnel",
                url: "crm_report/sales_funnel",
                icon: "real_estate_agent",
                page: "report",
                content_type: "sales funnel",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "Prospect",
                title: "Prospect Summary",
                url: "crm_report/prospect_report",
                icon: "real_estate_agent",
                page: "report",
                content_type: "prospect report",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "opportunity_report",
                title: "Opportunity Report",
                url: "crm_report/opportunity_report",
                icon: "real_estate_agent",
                page: "report",
                content_type: "opportunity report",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "appointment_report",
                title: "Appointment",
                url: "crm_report/appointment_report",
                icon: "groups_3",
                page: "report",
                content_type: "appointment report",
                child_items:[]
            },
        ]
    },

    {
        title: "KNOWLEDGE BASE",
        routes: [
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "knowledge_base",
                title: "Knowledge Base",
                url: "knowledge_base",
                icon: "network_intelligence_update",
                page: "list",
                content_type: "knowledge base",
                child_items:[]
            },
            {
                is_linked: true,
                is_multi_content: true,
                module: "app/crm",
                app: "frequent_asked_question",
                title: "Frequent Asked Question",
                url: "frequent_asked_question",
                icon: "question_exchange",
                page: "list",
                content_type: "frequent asked question",
                child_items:[]
            },
        ]
    },
]
