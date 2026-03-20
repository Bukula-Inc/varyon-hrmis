import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Request_For_Absence',
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
            model: 'Request_For_Absence',
            columns: 1,
            placeholder: "Select Request For Absence",
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
            column_title: "status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
       
    ]
}