export default {
    setup: {
        model: 'Doc_Status',
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
            id: "doc-status-name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Doc_Status',
            columns: 1,
            placeholder: "Select Docstatus",
        },
      
    ],
    actions: {
        main: [
           
        ],
        row: [
           
        ]
    },
    columns: [
        {
            column_title: "Initial Doc Status",
            column_name: "initial_docstatus",
            column_type: "figure",
            columns: 1,
            is_figure:true
        },
        {
            column_title: "Status Color",
            column_name: "status_color",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Text Color",
            column_name: "inner_color",
            column_type: "text",
            columns: 1,
        },
        
        
    ]
}