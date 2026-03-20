import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Performance_Key_Area',
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
            id: "filter-pa",
            fieldname: "Key Performance Area",
            fieldtype: "link",
            model: 'Performance_Key_Area',
            linkfield: "name",
            columns: 1,
            placeholder: "Key Performance Area",
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
            column_title: "Key Area",
            column_name: "area_type",
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