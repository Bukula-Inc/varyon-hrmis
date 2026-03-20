export default {
    setup: {
        model: 'Module_Pricing',
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
            model: 'Module_Pricing',
            linkfield: "name",
            columns: 1,
            placeholder: "Module Pricing Name",
        },
    ],
    actions: {
        main: [],
        row:  []  
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