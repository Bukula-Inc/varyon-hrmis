export default {
    setup: {
        model: 'Pre_Payroll_payment',
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
            model: 'Pre_Payroll_payment',
            columns: 1,
            placeholder: "Name",
        }
    ],
    actions: {
        main: [
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Delete Selected',
            //     icon: 'recycling',
            //     icon_color: 'red'
            // }
        ],
        row: [
            // {
            //     fun: 'function name',
            //     title: 'Delete Selected',
            //     icon: 'recycling',
            //     icon_color: 'red'
            // }
        ]
    },
    columns: [
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },

    ]
}