import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Training_Result',
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
            model: 'Training_Result',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Training_Event',
            linkfield: "name",
            columns: 1,
            placeholder: "Training Event",
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
            column_title: "Type",
            column_name: "type",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Location",
            column_name: "location",
            column_type: "text",
            columns: 1,
        },
        
    ]
}