export default {
    setup: {
        model: 'Query',
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
            model: 'Query',
            columns: 1,
            placeholder: "Query Name",
            filters: {
                "employee": lite.employee_info?.name
                },
        }
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
            columns: 1,
        },
        {
            column_title: "Subject",
            column_name: "subject",
            column_type: "text",
            columns: 2,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
      
       
    ]
}