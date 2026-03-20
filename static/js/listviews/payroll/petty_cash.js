export default {
    setup: {
        model: 'Petty_Cash',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "Petty_Cash",
            fieldname: "name",
            fieldtype: "link",
            model: "Petty_Cash",
            columns: 1,
            placeholder: "Select petty cash",
        },
        {
            id: "initiator",
            fieldname: "initiator",
            fieldtype: "link",
            model: "Petty_Cash",
            linkfield: "initiator",
            columns: 1,
            placeholder: "Initiator",
        },
    ],
    actions: {
        main: [
        ],
        row: [
        ]
    },
    columns: [
        {
            column_title: "Initiator",
            column_name: "initiator",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Requested Amount",
            column_name: "requested_amount",
            column_type: "figure",
            columns: 1,
            sortable: true,
            is_figure:true
        },
        {
            column_title: "Balance",
            column_name: "balance",
            column_type: "figure",
            columns: 1,
            sortable: true,
            is_figure:true
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },

    ]
}