import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Disciplinary_Committee',
        list_height: 50,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
     
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Disciplinary_Committee',
            columns: 1,
            placeholder: "Committee Name",
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
            column_title: "Committee",
            column_name: "name",
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