import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Express_Mail',
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
            id: "id",
            fieldname: "name",
            fieldtype: "link",
            model: 'Express_Mail',
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "employee-name",
            fieldname: "employee_name",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "full_name",
            columns: 1,
            placeholder: "Employee Name",
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
        
    ]
}