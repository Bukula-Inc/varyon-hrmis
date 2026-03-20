import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Bulletin',
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
            id: "bulletin",
            fieldname: "Bulletin",
            fieldtype: "link",
            model: 'Bulletin',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
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