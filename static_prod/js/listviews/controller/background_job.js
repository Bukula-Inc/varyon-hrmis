export default {
    setup: {
        model: 'Background_Job',
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
            model: 'Background_Job',
            linkfield: "name",
            columns: 1,
            placeholder: "Background Job Name",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            column_title: "Module",
            column_name: "module",
            column_type: "module",
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