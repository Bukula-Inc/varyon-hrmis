import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Interview_Type',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Interview_Type',
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
            column_title: "Description",
            column_name: "description",
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