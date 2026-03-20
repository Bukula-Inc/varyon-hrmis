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
            column_title: "Profile",
            column_name: "profile",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Profile",
            column_name: "profile",
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