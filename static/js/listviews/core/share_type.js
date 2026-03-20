export default {
    setup: {
        model: 'Share_Type',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
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
            model: 'Share',
            linkfield: "name",
            columns: 1,
            placeholder: "Share Name",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        
    ]
}