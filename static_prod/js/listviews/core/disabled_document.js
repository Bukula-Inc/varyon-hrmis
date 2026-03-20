import { wipe_all_transactions } from "./functions.js"
export default {
    setup: {
        model: 'Disabled_Document',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
     
        {
            id: "disabled-doc",
            fieldname: "name",
            fieldtype: "link",
            model: 'Disabled_Document',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
      
    ],
    actions: {
        main: [
            
        ],
        row: [
        ]
    },
    columns: [
        {
            column_title: "Document Type",
            column_name: "document_type",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Initial Status",
            column_name: "initial_status",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}