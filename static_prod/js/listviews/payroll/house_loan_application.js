

export default {
    setup: {
        model: 'House_Loan_Application',
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
            model: 'House_Loan_Application',
            columns: 1,
            placeholder: "Name",
        },
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
            column_title: "Date of Engagement",
            column_name: "date_of_engagement",
            column_type: "date",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}