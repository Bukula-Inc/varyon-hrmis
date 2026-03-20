export default {
    setup: {
        model: 'House_Loan_Agreement',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    default_filters:{
        borrower: lite.employee_info?.name
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Salary_Advance_Configuration',
            columns: 1,
            placeholder: "Select Name",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Borrower",
            column_name: "borrower_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Advance Amount",
            column_name: "advance_amount",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Location",
            column_name: "location",
            column_type: "text",
            columns: 1,
        },
    ]
}