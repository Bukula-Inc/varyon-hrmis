export default {
    setup: {
        model: 'Form_Customization',
        list_height: 50,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Form_Customization',
            columns: 1,
            placeholder: "Name",
        },
        {
            id: "form",
            fieldname: "form",
            fieldtype: "link",
            model:"Model",
            columns: 1,
            placeholder: "Select Form Type",
        }
    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}