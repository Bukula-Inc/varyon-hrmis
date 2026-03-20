import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Employee_Feedback',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    filters: [
     
        {
            id: "employee-feedback",
            fieldname: "employee_feedback",
            fieldtype: "link",
            model: 'Employee_Feedback',
            linkfield: "name",
            columns: 1,
            placeholder: "Name",
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
    columns: [
        {
            column_title: "Email",
            column_name: "email",
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