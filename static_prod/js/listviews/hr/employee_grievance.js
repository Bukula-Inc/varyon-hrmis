import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Employee_Grievance',
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
            model: 'Employee_Grievance',
            linkfield: "name",
            columns: 1,
            placeholder: "Employee Grievance",
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
            column_title: "Raised By",
            column_name: "raised_by",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Grievance Against",
            column_name: "grievance_against",
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