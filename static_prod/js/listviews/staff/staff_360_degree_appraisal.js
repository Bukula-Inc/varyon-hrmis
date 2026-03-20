export default {
    setup: {
        model: 'Appraisal',
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
            model: 'Appraisal',
            columns: 1,
            placeholder: "Select Setup Name",
            filters:{
                "appraisee": lite.employee_info?.name 
            }
        },
        {
            id: "appraisal-quarter",
            fieldname: "appraisal_quarter",
            fieldtype: "link",
            model: 'Appraisal',
            columns: 1,
            placeholder: "Appraisal Quarter",
            filters:{
                "appraisee": lite.employee_info?.name 
            }
        },
        {
            id: "filter-Status",
            column_title: "Status",
            fieldname: "status",
            fieldtype: "link",
            model: "Appraisal",
            placeholder: "Select Status",
            filters:{
                "appraisee": lite.employee_info?.name 
            }
        },
        
      
    ],
    default_filters:{
        appraisee: lite.employee_info?.name
    },
    actions: {
        
    },
    columns: [
        {
            column_title: "Appraisee",
            column_name: "appraisee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Appraisal Date",
            column_name: "appraisal_date",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
      
    ]
}