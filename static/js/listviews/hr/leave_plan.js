import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Leave_Plan',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
     
        {
            id: "planner",
            fieldname: "planner",
            fieldtype: "link",
            model: 'Leave_Plan',
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
            column_title: "Planner",
            column_name: "planner",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Handover To",
            column_name: "handed_over_to",
            column_type: "text",
            columns: 1,
        }, 
    ]
}