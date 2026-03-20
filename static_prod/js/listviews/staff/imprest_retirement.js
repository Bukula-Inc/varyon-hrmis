export default {
    setup: {
        model: "ECZ_Imprest_Retirement",
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
            id: "filter-created_on-date",
            fieldname: "created_on",
            fieldtype: "date",
            mode:"single",
            columns: 1,
            placeholder: "Date",
        },
        {
            id: "Imprest-retirement",
            fieldname: "name",
            fieldtype: "link",
            model: "Imprest_Retirement",
            columns: 1,
            placeholder: "Select Retirement",
            filters: {
                "initiator":  lite?.employee_info?.name 
                },
        },
        {
            id: "initiator",
            fieldname: "employee_no",
            fieldtype: "link",
            model: "Imprest",
            linkfield: "employee_no",
            columns: 1,
            placeholder: "Initiator",
            filters: {
                "initiator":  lite?.user?.name 
                },
        },
    ],
    default_filters:{
        employee_no:  lite?.employee_info?.name 
    },
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Initiator",
            column_name: "employee_no",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Retired Amount",
            column_name: "retired_amount",
            column_type: "float",
            columns: 1,
        },
        {
            column_title: "Balance",
            column_name: "balance_left",
            column_type: "float",
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