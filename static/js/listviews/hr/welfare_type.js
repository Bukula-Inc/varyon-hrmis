import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Welfare_Type',
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
            id: "welfare-type",
            fieldname: "name",
            fieldtype: "link",
            model: 'Welfare_Type',
            columns: 1,
            placeholder: "Pick Welfare Type",
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
            column_name: "limit_qty",
            column_type: "text",
            columns: 1,
        }, 
        {
            column_title: "Period Units",
            column_name: "limit_unit",
            column_type: "text",
            columns: 1,
        },   
        {
            column_title: "Council Percentage",
            column_name: "limit_unit",
            column_type: "text",
            columns: 1,
        },       
    ]
}