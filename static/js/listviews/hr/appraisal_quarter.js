import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Appraisal_Quarter',
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
            id: "appraisal-quarter",
            fieldname: "appraisal_quarter",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "full_name",
            columns: 1,
            placeholder: "Appraisal Quarter",
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
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
        
    ]
}