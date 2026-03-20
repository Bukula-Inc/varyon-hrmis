export default {
    setup: {
        model: 'Rating',
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
            model: 'Rating',
            // linkfield: "name",
            columns: 1,
            placeholder: "Feedback Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: []
}