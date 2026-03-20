export default {
    setup: {
        model: 'Audit_Trail',
        list_height: 50,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Audit_Trail',
            columns: 1,
            placeholder: "Name",
        },
        {
            id: "doctype",
            fieldname: "doctype",
            fieldtype: "text",
            columns: 1,
            placeholder: "Doctype",
        },
        {
            id: "created-at-from",
            fieldname: "created_at",
            fieldtype: "date",
            mode: "single",
            columns: 1,
            placeholder: "From Date",
        },
    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "Created By",
            column_name: "owner",
            column_type: "link",
            model:"Lite_User",
            columns: 1,
            icon: "credit_card",
            icon_color: "indigo"
        },
        {
            column_title: "Document Type",
            column_name: "document_type",
            column_type: "text",
            columns: 1,
            icon: "event_available",
            icon_color: "orange"
        },
        {
            column_title: "Document Name",
            column_name: "doc_name",
            column_type: "text",
            columns: 1,
            icon: "event_available",
            icon_color: "orange"
        },
        
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}