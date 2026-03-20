

export default {
    setup: {
        model: 'Lite_User',
        // list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "first_name",
            fieldname: "first_name",
            fieldtype: "link",
            model: 'Lite_User',
            columns: 1,
            placeholder: "Lite User",
        },
    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "Last Name",
            column_name: "last_name",
            column_type: "text",
            model: 'Lite_User',
            columns: 1,
        },
        {
            column_title: "First Name",
            column_name: "first_name",
            column_type: "text",
            model: 'Lite_User',
            columns: 1,
        },
        {
            column_title: "Email Name",
            column_name: "email",
            column_type: "text",
            model: 'Lite_User',
            columns: 1,
        },
        {
            column_title: "Gender",
            column_name: "gender",
            column_type: "text",
            model: 'Lite_User',
            columns: 1,
        },
    ]
}