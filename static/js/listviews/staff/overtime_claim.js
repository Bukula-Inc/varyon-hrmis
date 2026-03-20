export default {
    setup: {
        model: 'Overtime_CLaim',
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
            model: 'Overtime_CLaim',
            columns: 1,
            placeholder: "Select Name",
        },
      
    ],
    actions: {
        
    },
    default_filters:{
        employee: lite.employee_info?.name
    },
    columns: [
        {
            column_title: "Employee",
            column_name: "fullname",
            column_type: "text",
            columns: 1,
        },
          {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        }
        
    ]
}