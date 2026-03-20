import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Employee_Disciplinary',
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
            model: 'Employee_Disciplinary',
            linkfield: "name",
            columns: 1,
            placeholder: "Employee Disciplinary",
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
            column_title: "Employee",
            column_name: "employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Violation Type",
            column_name: "violation_type",
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