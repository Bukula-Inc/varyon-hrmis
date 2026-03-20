import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Express_Mail',
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
            model: 'Express_Mail',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "officer_name",
            fieldname: "officer_name",
            fieldtype: "link",
            model: 'Express_Mail',
            linkfield: "officer_name",
            columns: 1,
            placeholder: "Officer Name",
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
            column_title: "Staff's Name",
            column_name: "officer_name",
            column_type: "text",
            columns: 4,
        },        
    ]
}