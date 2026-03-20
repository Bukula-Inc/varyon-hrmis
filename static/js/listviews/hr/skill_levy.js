import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Skill_Levy',
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
            model: 'Levy_Skill',
            linkfield: "name",
            columns: 1,
            placeholder: "Levy Skill",
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
            column_title: "Levy Percentage",
            column_name: "levy_percentage",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Expense Account",
            column_name: "expense_account",
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