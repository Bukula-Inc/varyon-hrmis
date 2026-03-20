export default {
    setup: {
        model: 'Module',
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
            model: 'Module',
            linkfield: "name",
            columns: 1,
            placeholder: "Module Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            id: "title",
            column_title:"Module Title",
            column_name: "title",
            column_type: "text",
        },
        {
            id: "icon",
            column_title:"Module Icon",
            column_name: "icon",
            column_type: "icon",
        },
    ]
}