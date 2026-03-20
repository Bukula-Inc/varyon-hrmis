import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Separation_Type',
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
            model: 'Separation_Type',
            linkfield: "name",
            columns: 1,
            placeholder: "Separation Type",
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
        
    ]
}