export default {
    setup: {
        model: 'Training_Program_Application',
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
            id: "employee-no",
            fieldname: "name",
            fieldtype: "link",
            model: 'Training_Program_Application',
            columns: 1,
            placeholder: "Employee",
        },
    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "First Name",
            column_name: "first_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Last Name",
            column_name: "last_name",
            column_type: "text",
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