export default [
    {
        app: "client_dashboard",
        title: "Dashboard",
        url: "client_dashboard",
        icon: "house",
        page: "dashboard",
        content_type: "Dashboard",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_quotation",
        title: "Quotations",
        url: "client_quotation",
        icon: "lan",
        page: "list",
        content_type: "client quotation",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_tax_invoice",
        title: "Invoices",
        url: "client_tax_invoice",
        icon: "lan",
        page: "list",
        content_type: "client tax invoice",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_receipt",
        title: "Customer Receipt",
        url: "client_receipt",
        icon: "lan",
        page: "list",
        content_type: "client receipt",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_statement",
        title: "Customer Statement",
        url: "portal_reports/client_statement",
        page: "report",
        icon: "account_balance_wallet",
        content_type: "customer statement",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_appointment",
        title: "Appointments",
        url: "client_appointment",
        icon: "book_online",
        page: "list",
        content_type: "Client Appointment",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_ticket",
        title: "Ticket Management",
        url: "client_ticket",
        page: "list",
        icon: "support",
        content_type: "Ticket",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_services",
        title: "Services Provided",
        url: "client_services",
        icon: "lan",
        page: "list",
        content_type: "Services Provided",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_contract",
        title: "Contract",
        url: "client_contract",
        icon: "contract_edit",
        page: "list",
        content_type: "Client Contract",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_faq",
        title: "Enquiry",
        url: "client_faq",
        icon: "help",
        page: "list",
        content_type: "Client Faq",
        child_items: [],
        party_type:"customer"
    },
    {
        app: "client_messaging",
        title: "Messaging",
        url: "client_messaging",
        icon: "mail",
        page: "list",
        content_type: "Messaging",
        child_items: [],
        party_type:"customer",
        display:false
    },


    // SUPPLIER START 

    {
        app: "supplier_portal_dashboard",
        title: "Dashboard",
        url: "supplier_portal_dashboard",
        icon: "dashboard",
        page: "dashboard",
        content_type: "supplier portal dashboard",
        child_items: [],
        party_type:"supplier"
    },

    {
        app: "supplier_rfq",
        title: "Request For Quotations",
        url: "supplier_rfq",
        icon: "request_quote",
        page: "list",
        content_type: "request for quotation",
        child_items: [],
        party_type:"supplier"
    },

    {
        app: "supplier_quotation",
        title: "Quotations",
        url: "supplier_rfq",
        icon: "receipt_long",
        page: "list",
        content_type: "quotation",
        child_items: [],
        party_type:"supplier"
    },

    // {
    //     app: "supplier_contract",
    //     title: "Contracts",
    //     url: "supplier_contract",
    //     icon: "receipt_long",
    //     page: "list",
    //     content_type: "contract",
    //     child_items: [],
    //     party_type:"supplier"
    // },
    // {
    //     app: "client_services",
    //     title: "Services Provided",
    //     url: "client_services",
    //     icon: "lan",
    //     page: "list",
    //     content_type: "Services Provided",
    //     child_items: [],
    //     party_type:"supplier"
    // },
    // {
    //     app: "supplier_receipting",
    //     title: "Receipting",
    //     url: "supplier_receipting/",
    //     icon: "receipt_long",
    //     page: "list",
    //     content_type: "receipting",
    //     child_items: [],
    //     party_type:"supplier"
    // },
    {
        app: "supplier_payment",
        title: "Payment",
        url: "supplier_paymentt",
        icon: "receipt_long",
        page: "list",
        content_type: "payments",
        child_items: [],
        party_type:"supplier"
    },
    {
        app: "supplier_purchase_order",
        title: "Purchase Order",
        url: "supplier_purchase_order",
        icon: "receipt_long",
        page: "list",
        content_type: "purchase order",
        child_items: [],
        party_type:"supplier"
    },
    {
        app: "supplier_tax_invoice",
        title: "Tax Invoice",
        url: "supplier_tax_invoice",
        icon: "receipt_long",
        page: "list",
        content_type: "tax invoice",
        child_items: [],
        party_type:"supplier"
    },
    {
        app:"supplier_statement",
        title: "Supplier Startment",
        url: "supplier_statemnent",
        icon: "speaker_notes",
        page: "report",
        content_type: "supplier statement",
        party_type: "supplier",
        child_items: [],
    },
    // SUPPLIER ENDS


    {
        app: "client_sla",
        title: "Service Level Agreement",
        url: "client_sla",
        icon: "handshake",
        page: "list",
        content_type: "service level agreement",
        child_items: [],
        party_type:"customer"
    },
    // {
    //     app: "client_messaging",
    //     title: "Messaging",
    //     url: "client_messaging",
    //     icon: "mail",
    //     page: "list",
    //     content_type: "Messaging",
    //     child_items: [],
    //     party_type:"customer",
    //     display:false
    // },
    // {
    //     app: "faqs",
    //     title: "FAQs",
    //     url: "/faqs",
    //     icon: "quiz",
    //     page: "",
    //     content_type: "FAQs",
    //     child_items: [],
    //     party_type:"customer"
    // },
    // {
    //     app: "client_feedback",
    //     title: "Feedback",
    //     url: "client_feedback",
    //     icon: "recommend",
    //     page: "list",
    //     content_type: "client feedback",
    //     child_items: [],
    //     party_type:"customer"
    // },
    // {
    //     app: "client_profile",
    //     title: "Profile",
    //     url: "client_profile",
    //     icon: "account_circle",
    //     page: "dashboard",
    //     content_type: "Client Profile",
    //     child_items: [],
    //     party_type:"customer"
    // }
]