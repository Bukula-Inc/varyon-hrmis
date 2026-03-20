export default {
    setup: {
        model: 'Menu_Card',
        list_height: 50,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: false,
        allow_export_excel: false,
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Menu_Card',
            columns: 1,
            placeholder: "Name",
        },
        {
            id: "module",
            fieldname: "module",
            fieldtype: "link",
            model: 'Module',
            columns: 1,
            placeholder: "Select Module",
        },
    ],
    actions: {},
    columns: []
}