export default {
    setup: {
        model: 'Workflow_Action',
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
            model: 'Workflow_Action',
            linkfield: "name",
            columns: 1,
            placeholder: "Workflow Action Name",
        },
      
    ],
    actions: {
        main: [],
        row: []
    },
    columns: [
        {
            id: "icon",
            column_name: "icon",
            columns: 1,
            column_type:"icon",
            column_title: "Icon",
        },
        {
            id: "status",
            column_name: "status",
            columns: 1,
            column_type:"status",
            column_title: "Status",
        },
        
    ]
}