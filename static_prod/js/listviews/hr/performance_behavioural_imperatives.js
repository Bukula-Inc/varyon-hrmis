import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Performance_Behavioral_Imperative',
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
            id: "filter-b",
            fieldname: "Desired ECZ Value/behaviour",
            fieldtype: "link",
            model: 'Performance_Behavioral_Imperative',
            linkfield: "name",
            columns: 1,
            placeholder: "Desired ECZ Value/behaviour",
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
            column_title: "Is Active",
            column_name: "is_current",
            column_type: "check",
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