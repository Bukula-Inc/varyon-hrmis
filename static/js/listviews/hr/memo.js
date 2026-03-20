import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Memo',
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
            model: 'Memo',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "subject",
            fieldname: "name",
            fieldtype: "link",
            model: 'Memo',
            linkfield: "subject",
            columns: 1,
            placeholder: "Mome Subject",
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
            column_title: "Subject",
            column_name: "subject",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "To",
            column_name: "to",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 4,
        }
        
    ]
}