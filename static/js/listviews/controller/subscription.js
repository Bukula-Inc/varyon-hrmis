export default {
    setup: {
        model: 'Subscription',
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
            model: 'Subscription',
            linkfield: "name",
            columns: 1,
            placeholder: "Subscription Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            id: "tenant",
            column_title:"Tenant",
            column_name: "tenant",
            fieldtype: "text",
        },
        {
            id: "from",
            column_title:"Subscription From",
            column_name: "subscription_from",
            fieldtype: "text",
        },
        {
            id: "to",
            column_title:"Subscription To",
            column_name: "subscription_to",
            fieldtype: "text",
        },
        
    ]
}