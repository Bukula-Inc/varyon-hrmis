export default {
    setup: {
        model: 'District',
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
            model: 'District',
            linkfield: "name",
            columns: 1,
            placeholder: "District Name",
        },
    ],
    actions: {
        main: [],
        row: []
    },
    columns: []
}