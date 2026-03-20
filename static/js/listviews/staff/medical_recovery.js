import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Recovery_Of_Medical_Bills',
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
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Recovery_Of_Medical_Bills',
            linkfield: "name",
            columns: 1,
            placeholder: "Employee",
        },
    ],
    actions: {
        main: [
            
        ],
        row: [
            {
                fun: wipe_all_transactions,
                title: 'Get JSON',
                icon: 'code',
                icon_color: 'teal',
            },
        ]
    },
    default_filters:{
        employee: lite.employee_info?.name
    },
    columns: [
        {
            column_title: "Welfare",
            column_name: "welfare",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            columns: 1,
        },
        
    ]
}