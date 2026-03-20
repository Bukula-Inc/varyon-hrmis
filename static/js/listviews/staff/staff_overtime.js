export default {
    setup: {
        model: 'Overtime',
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
            model: "Overtime",
            columns: 1,
            placeholder: "Select Name",
            filters: {
                "applicant":  lite.employee_info?.name
            },
            
        },
        {
            id: "filter-Status",
            column_title: "Status",
            fieldname: "status",
            fieldtype: "select",
            placeholder: "Select Status",
            options: [
                "Draft",
                "Active",
                "Draft",
                "Active",
                "Pending Approved",
                "Submitted",
                "Approved",   
                "Rejected",
               
            ],
        },
      
    ],
    default_filters:{
        applicant: lite.employee_info?.name
    },
    actions: {
        
    },
    columns: [
        {
            column_title: "Name",
            column_name: "name",
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