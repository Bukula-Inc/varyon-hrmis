import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Allowance_and_Benefit',
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
            id: "allowance_and-benefit",
            fieldname: "Allowance and Benefit",
            fieldtype: "link",
            model: 'Allowance_and_Benefit',
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
        // {
        //     column_title: "Affects Payroll",
        //     column_name: "affects_payroll",
        //     column_type: "text",
        //     columns: 1,
        // },
        
    ]
}