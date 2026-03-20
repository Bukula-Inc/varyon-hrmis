export default {
    setup: {
        model: 'Email_Config',
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
            model: 'Email_Config',
            linkfield: "name",
            columns: 1,
            placeholder: "Email Config",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Email Address",
            column_name: "email_address",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Port No",
            column_name: "port_no",
            column_type: "text",
            columns: 1,
        },
    ]
}