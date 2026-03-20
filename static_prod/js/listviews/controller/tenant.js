export default {
    setup: {
        model: 'Tenant',
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
            model: 'Tenant',
            linkfield: "name",
            columns: 1,
            placeholder: "Tenant Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            id: "url",
            column_title:"URL",
            column_name: "tenant_url",
            fieldtype: "link",
            columns:3
        },
        {
            id: "subscription_frequency",
            column_title:"Subscription Frequency",
            column_name: "subscription_frequency",
            fieldtype: "subscription_frequency",
        },
        {
            id: "status",
            column_title:"Status",
            column_name: "status",
            fieldtype: "status",
        },
    ]
}