import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Charge_Form',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    default_filters:{
        employee: lite.employee_info?.name
    },
    filters: [
     
        {
            id: "charge",
            fieldname: "charge",
            fieldtype: "link",
            model: 'Charge_Form',
            linkfield: "name",
            columns: 1,
            placeholder: "Filter By ID",
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