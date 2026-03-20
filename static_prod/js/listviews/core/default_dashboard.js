import { wipe_all_transactions } from "./functions.js"
export default {
    setup: {
        model: 'Default_Dashboard',
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
            id: "default-dashboard",
            fieldname: "name",
            fieldtype: "link",
            model: 'Default_Dashboard',
            linkfield: "name",
            columns: 1,
            placeholder: "Default Dashboard",
        },
        {
            id: "module",
            fieldname: "module",
            fieldtype: "link",
            model: 'Module',
            linkfield: "module",
            columns: 1,
            placeholder: "Select Module",
        },
      
    ],
    actions: {
        main: [
            
        ],
        row: [
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Get JSON',
            //     icon: 'code',
            //     icon_color: 'teal',
            // },
        ]
    },
    columns: [
        {
            column_title: "Module",
            column_name: "module",
            column_type: "link",
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