import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Transport_Request',
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
            model: 'Transport_Request',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "full_name",
            fieldname: "full_name",
            fieldtype: "link",
            model: 'Transport_Request',
            linkfield: "full_name",
            columns: 1,
            placeholder: "Mome Applicant",
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
            column_title: "Applicant",
            column_name: "full_name",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Duration",
            column_name: "duration",
            column_type: "text",
            columns: 4,
        },
    ]
}