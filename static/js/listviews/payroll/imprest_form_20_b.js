;
export default {
    setup: {
        model: "Imprest_Form_20_B",
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true,
    },
    filters: [
        {
            id: "filter-created_on-date",
            fieldname: "created_on",
            fieldtype: "date",
            mode:"single",
            columns: 1,
            placeholder: "Date",
        },
        {
            id: "imprest",
            fieldname: "name",
            fieldtype: "link",
            model: "ECZ_Imprest",
            columns: 1,
            placeholder: "Select imprest",
        },
        

    ],
    actions: {
        main: [],
        row: []
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
            column_title: "Approved Amount",
            column_name: "approved_amount",
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
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}