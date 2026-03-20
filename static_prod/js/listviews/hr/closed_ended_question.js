export default {
    setup: {
        model: 'Closed_Ended_Question',
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
            model: 'Closed_Ended_Question',
            linkfield: "name",
            columns: 1,
            placeholder: "Closed Ended Question",
        },
      
    ],
    actions: {
        
    },
    columns: [
           
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        }
    ]
}