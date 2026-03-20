import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Scholarship',
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
            id: "employee-no",
            fieldname: "name",
            fieldtype: "link",
            model: 'Scholarship',
            columns: 1,
            placeholder: "Employee",
            filters:{
                "employee": lite.employee_info?.name 
            }
        },
    ],
    default_filters:{
        employee: lite.employee_info?.name
    },
    actions: {
        main: [
            
        ],
        row: [
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Get JSON',
            //     icon: 'code',
            //     icon_color: 'teal',
            // },
        ]
    },
    columns: [
        {
            column_title: "First Name",
            column_name: "first_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Last Name",
            column_name: "last_name",
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