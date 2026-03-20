import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Leave_Type',
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
            model: 'Leave_Type',
            linkfield: "name",
            columns: 1,
            placeholder: "Leave Type",
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
            column_title: "Maximum Consecutive Leave Days Allowed",
            column_name: "maximum_leave_allocated",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Is Carried Forward",
            column_name: "carry_forward",
            column_type: "check",
            columns: 1,
        },
    ]
}