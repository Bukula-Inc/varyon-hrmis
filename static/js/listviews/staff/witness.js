import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Witnessing',
        list_height: 440,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "witness",
            column_title: "Witness",
            fieldname: "witness",
            fieldtype: "link",
            model: "Employee",
            placeholder: "Select Witness",
        },
    ],
    default_filters:{
        employee: lite.employee_info?.name
    },
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
            column_title: "Document Type",
            column_name: "witness_names",
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