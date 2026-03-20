export default {
    setup: {
        model: 'Payslip',
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
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Payslip',
            columns: 1,
            placeholder: "Payslip Name",
        }
    ],
    actions: {},
    columns: [
        {
            column_title: "Posting Date",
            column_name: "posting_date",
            column_type: "date",
            columns: 2,
        },
        {
            column_title: "From Date",
            column_name: "from_date",
            column_type: "date",
            columns: 1,
        },
        {
            column_title: "Employee",
            column_name: "employee",
            column_type: "link",
            model: "Employee",
            columns: 1,
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