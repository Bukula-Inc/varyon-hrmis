import { wipe_all_transactions } from "./functions.js"
export default {
    setup: {
        model: 'Print_Format',
        list_height: 47,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    filters: [
        {
            id: "print-format-name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Print_Format',
            columns: 1,
            placeholder: "Print Format Name",
        },
        {
            id: "Model",
            fieldname: "app_model",
            fieldtype: "text",
            // model: 'Industry',
            columns: 1,
            placeholder: "Model",
        },
    ],
    actions: {
        main: [
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Delete this row',
            //     icon: 'recycling',
            //     icon_color: 'red',
            //     show_on_list_check: true,
            //     is_custom_button: true,
            //     classnames: 'bg-blue-800 text-white'
            // },
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Delete this row',
            //     icon: 'recycling',
            //     icon_color: 'red',
            //     show_on_list_check: false,
            //     is_custom_button: true
            // },
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
            column_title: "For Model",
            column_name: "app_model",
            column_type: "text",
            columns: 1,
            sortable: true
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
            sortable: true
        },
    ]
}