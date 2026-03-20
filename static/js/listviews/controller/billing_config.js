export default {
    setup: {
        model: 'Billing_Config',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    filters: [
     
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Billing_Config',
            linkfield: "name",
            columns: 1,
            placeholder: "Config Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
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