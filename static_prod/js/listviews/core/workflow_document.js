export default {
    setup: {
        model: 'Workflow_Doc',
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
            model: 'Workflow_Doc',
            linkfield: "name",
            columns: 1,
            placeholder: "Workflow Document Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            id: "for_doctype",
            column_name: "for_doctype",
            columns: 1,
            column_type:"text",
            column_title: "Document Type",
        },
        {
            id: "current_stage",
            column_name: "current_stage",
            columns: 1,
            column_type:"text",
            column_title: "Current Stage",
        }
    ]
}