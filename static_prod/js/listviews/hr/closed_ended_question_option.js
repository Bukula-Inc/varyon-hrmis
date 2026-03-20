export default {
    setup: {
        model: 'Appraisal_Question_Option',
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
            model: 'Appraisal_Question_Option',
            linkfield: "name",
            columns: 1,
            placeholder: "Closed Ended Question",
        },
      
    ],
    actions: {
        
    },
    columns: [
        {
            column_title: "Rate",
            column_name: "rate",
            column_type: "figure",
            columns: 1,
        },
           
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        }
        

    ]
}