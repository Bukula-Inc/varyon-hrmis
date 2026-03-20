import { wipe_all_transactions } from "../../listviews/core/functions.js";

export default {
    setup: {
        model: 'Audit_Trail_Report',
        title: "Audit_Trail Report",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        is_grid_layout : true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
        {
            id: "audit-trail",
            fieldname: "owner",
            fieldtype: "link",
            model:"Lite_User",
            placeholder: "Created By",
        },
        // {
        //     id: "date_range",
        //     fieldname: "datetime",
        //     fieldtype: "DateRange",
        //     placeholder: "Select date range",
        // },
        // {
        //     id: "customer",
        //     fieldname: "customer",
        //     fieldtype: "link",
        //     placeholder: "Select customer",
        // },
    ],
    actions: [
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],

    columns: [
        {
            column_title: "Created On",
            column_name: "created_on",
            column_type: "date",
            columns: 3,
            sortable: true
        },
        {
            column_title: "Last Modified On",
            column_name: "last_modified",
            column_type: "date",
            columns: 3,
            sortable: true
        },
        {
            column_title: "Created By",
            column_name: "owner",
            column_type: "link",
            columns: 3,
            sortable: true
        },
        {
            column_title: "Document Type",
            column_name: "document_type",
            column_type: "text",
            columns: 3,
            sortable: true
        },
        {
            column_title: "Document Name",
            column_name: "doc_name",
            column_type: "text",
            columns: 3,
            sortable: true
        },
        // {
        //     column_title: "Status",
        //     column_name: "status",
        //     column_type: "status",
        //     columns: 3,
        //     sortable: true
        // },
    ]
};
