import { wipe_all_transactions } from "./functions.js"
export default {
    setup: {
        model: 'Branch',
        list_height: 50,
        allow_submit: false,
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
            model: 'Branch',
            columns: 1,
            placeholder: "Branch Name",
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
            column_title: "Latitude",
            column_name: "latitude",
            column_type: "text",
            columns: 1,
        },        
        {
            column_title: "Longitude",
            column_name: "longitude",
            column_type: "text",
            columns: 1,
        },        
    ]
}