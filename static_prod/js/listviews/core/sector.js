import { wipe_all_transactions } from "./functions.js"
export default {
    setup: {
        model: "Sector",
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
            id: "sector-name",
            fieldname: "name",
            fieldtype: "link",
            model: "Sector",
            columns: 1,
            placeholder: "Sector Name",
        },
        {
            id: "economic-impact",
            fieldname: "market_size",
            fieldtype: "link",
            model: "Sector",
            linkfield: "market_size",
            columns: 1,
            placeholder: "Sector Name",
        },
    ],
    actions: {
        main: [
            // {
            //     fun: wipe_all_transactions,
            //     title: "Delete this row",
            //     icon: "recycling",
            //     icon_color: "red",
            //     show_on_list_check: true,
            //     is_custom_button: true,
            //     classnames: "bg-blue-800 text-white"
            // },
            // {
            //     fun: wipe_all_transactions,
            //     title: "Delete this row",
            //     icon: "recycling",
            //     icon_color: "red",
            //     show_on_list_check: false,
            //     is_custom_button: true
            // },
        ],
        row: [
            // {
            //     fun: wipe_all_transactions,
            //     title: "Get JSON",
            //     icon: "code",
            //     icon_color: "teal",
            // },
        ]
    },
    columns: [
        {
            column_title: "Market Size",
            column_name: "market_size",
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

        {
            column_title: "Creation Date",
            column_name: "created_on",
            column_type: "text",
            columns: 1,
            sortable: true
        }
    ]
}