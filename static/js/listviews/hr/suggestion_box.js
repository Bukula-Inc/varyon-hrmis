import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Suggestion_Box',
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
            model: 'Suggestion_Box',
            linkfield: "name",
            columns: 1,
            placeholder: "Suggestion Box",
        }
     
       
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
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Suggestion Category",
            column_name: "category",
            column_type: "text",
            columns: 1,
        },
        
    ]
}