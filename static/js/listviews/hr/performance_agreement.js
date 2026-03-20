import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Performance_Agreement',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    default_filters:{
        planner: lite.employee_info?.name
    },
    filters: [
     
        {
            id: "Performance_Agreement",
            fieldname: "Performance Agreement",
            fieldtype: "link",
            model: 'Performance_Agreement',
            columns: 1,
            placeholder: "Filter By Employee",
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
            column_title: "Period",
            column_name: "period",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Agreement Due Date",
            column_name: "agreement_due_date",
            column_type: "text",
            columns: 1,
        }, 
    ]
}