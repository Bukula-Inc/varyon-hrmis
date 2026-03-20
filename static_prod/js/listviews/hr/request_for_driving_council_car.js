import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Request_For_Council_Car',
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
            id: "employee",
            fieldname: "employee",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "employee",
            columns: 1,
            placeholder: "Filter By Employee",
        },
    ],
    actions: {
        main: [],
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
            column_title: "Requester Name",
            column_name: "drivers_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "License Number",
            column_name: "drivers_license_number",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            columns: 1,
        },
        
    ]
}