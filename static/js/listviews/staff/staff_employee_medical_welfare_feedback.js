import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Employee_Welfare_Survey',
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
            model: 'Employee_Welfare_Feedback',
            linkfield: "name",
            columns: 1,
            placeholder: "Name",
        },
     
       
    ],
    default_filters:{
        raised_by: lite.employee_info?.name
    },
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
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        }
        
    ]
}