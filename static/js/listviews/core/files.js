export default {
    setup: {
        model: 'File_Management',
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
            fieldname: "Files",
            fieldtype: "link",
            model: 'Files',
            linkfield: "name",
            columns: 1,
            placeholder: "Files",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: []
}