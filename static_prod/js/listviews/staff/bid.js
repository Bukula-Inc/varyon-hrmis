export default {
    setup: {
        model: 'Bid',
        list_height:45,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
    },
    filters: [
        {
            id: "bid",
            fieldname: "name",
            fieldtype: "link",
            model: 'Bid',
            columns: 1,
            placeholder: "Bid Name",
        },
        {
            id: "issue-date",
            fieldname: "issue_date",
            fieldtype: "date",
            columns: 1,
            placeholder: "From Date",
        },
        {
            id: "To Date",
            fieldname: "due_date",
            fieldtype: "date",
            columns: 1,
            placeholder: "To Date",
        },
        {
            id: "supplier",
            fieldname: "supplier",
            fieldtype: "link",
            model: 'Supplier',
            columns: 1,
            placeholder: "Select Supplier",
        },
    ],
    actions: {
        main: [
            // {
            //     fun: 'function name',
            //     title: 'Delete Selected',
            //     icon: 'delete',
            //     icon_color: 'red'
            // }
        ],
        row: [
            // {
            //     fun: 'function name',
            //     title: 'Delete Selected',
            //     icon: 'delete',
            //     icon_color: 'red'
            // }
        ]
    },
    columns: [
        {
            column_title: "Supplier",
            column_name: "supplier",
            column_type: "link",
            model: "Supplier",
            columns: 1,
            icon:"group",
            icon_color:"pink"
        },
        {
            column_title: "Order Date",
            column_name: "issue_date",
            column_type: "date",
            columns: 1,
            icon:"event_available",
            icon_color:"orange"
        },
        {
            column_title: "Total Amount",
            column_name: "inclusive_total_amount",
            column_type: "figure",
            columns: 1,
            icon:"credit_card",
            icon_color:"indigo"
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
            icon:"adjust",
            icon_color:"green"
        },
    ]
}