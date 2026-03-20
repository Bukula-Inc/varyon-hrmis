import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Oath_Affirmation',
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
            id: "designation",
            fieldname: "designation",
            fieldtype: "link",
            model: 'Designation',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
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
            column_title: "Oath Taker",
            column_name: "employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Position",
            column_name: "new_position",
            column_type: "text",
            columns: 1,
        }
    ]
}