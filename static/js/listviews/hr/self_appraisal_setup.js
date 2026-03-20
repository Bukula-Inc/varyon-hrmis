export default {
    setup: {
        model: 'Self_Appraisal_Setup',
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
            fieldname: "Setup",
            fieldtype: "link",
            model: 'Self_Appraisal_Setup',
            columns: 1,
            placeholder: "Select Setup Name",
        },
     
        {
            id: "appraisee",
            fieldname: "appraisee",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Select Appraisee",
        },
        {
            id: "appraisal-quarter",
            fieldname: "appraisal_quarter",
            fieldtype: "link",
            model: 'Appraisal_Quarter',
            columns: 1,
            placeholder: "Appraisal Quarter",
        },
        
      
    ],
    actions: {
        
    },
    columns: [
        // {
        //     column_title: "Appraisee",
        //     column_name: "appraisee_name",
        //     column_type: "text",
        //     columns: 1,
        // },
        {
            column_title: "Expected On",
            column_name: "appraisal_closure_date",
            column_type: "text",
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