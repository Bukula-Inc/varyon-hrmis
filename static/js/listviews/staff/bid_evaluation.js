export default {
    setup: {
        model: 'Committee_Evaluations',
        list_height:45,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
    },
    filters: [
        {
            id: "committee-evalution",
            fieldname: "name",
            fieldtype: "link",
            model: 'Bid',
            columns: 1,
            placeholder: "Bid",
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
    default_filters:{
        committee_member: lite?.user?.email
    },
    columns: [
        {
            column_title: "Main Evaluation Reference",
            column_name: "bid_reference",
            column_type: "link",
            model: "Bid_Evaluation",
            columns: 1,
            icon:"credit_card",
            icon_color:"indigo"
        },
    ]
}