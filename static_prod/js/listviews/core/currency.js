export default {
    setup: {
        model: 'Currency',
        list_height: 47,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: false
    },
    filters: [
        {
            id: "currency-name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Currency',
            columns: 1,
            placeholder: "Currency Name",
        },
        {
            id: "symbol",
            fieldname: "symbol",
            fieldtype: "link",
            model: 'Currency',
            linkfield: "symbol",
            columns: 1,
            placeholder: "Currency Symbol",
        },
    ],
    actions: {
        main: [
            
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
            column_title: "Country",
            column_name: "country",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Currency Symbol",
            column_name: "symbol",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        }
    ]
}