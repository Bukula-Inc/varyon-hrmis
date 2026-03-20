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
        },   {
            id: "filter-from-date",
            fieldname: "from_date",
            fieldtype: "date",
            mode:"single",
            columns: 1,
            placeholder: "Date",
        },
    ],
    default_filters:{
        employee: lite.employee_info?.name
    },
    actions: {},
    columns: [
        {
            column_title: "Employee",
            column_name: "employee",
            column_type: "text",
            columns: 2,
        },
        {
            column_title: "Department",
            column_name: "department",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Gross",
            column_name: "gross",
            column_type: "figure",
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