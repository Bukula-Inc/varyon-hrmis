export default {
    setup: {
        model: 'Series',
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
            model: 'Series',
            linkfield: "name",
            columns: 1,
            placeholder: "Select Name",
        },
    ],
    actions: {
        main: [
            // {
            //     fun: null,
            //     title: 'Wipe All Transactions',
            //     icon: 'recycling',
            //     icon_color: 'teal',
            //     show_on_list_check: false
            // },
            // {
            //     fun: null,
            //     title: 'Delete this row',
            //     icon: 'recycling',
            //     icon_color: 'red',
            //     show_on_list_check: false,
            //     is_custom_button: true
            // },
        ],
        row: [
            // {
            //     fun: null,
            //     title: 'Get JSON',
            //     icon: 'code',
            //     icon_color: 'teal',
            // },
        ]
    },
    columns: [
        {
            column_title: "Name Format",
            column_name: "name_format",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Series Count",
            column_name: "series_count",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Series Digits",
            column_name: "series_digits",
            column_type: "figure",
            columns: 1,
        }
    ]
}