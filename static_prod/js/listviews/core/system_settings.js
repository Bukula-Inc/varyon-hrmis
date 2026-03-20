export default {
    setup: {
        model: 'System_Settings',
        list_height: 480,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    filters: [
     
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'System_Settings',
            linkfield: "name",
            columns: 1,
            placeholder: "System Settings",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Default Company",
            column_name: "name",
            column_type: "link",
            columns: 1,
        },
        {
            column_title: "Default Currency",
            column_name: "name",
            column_type: "link",
            columns: 1,
        },
    ]
}