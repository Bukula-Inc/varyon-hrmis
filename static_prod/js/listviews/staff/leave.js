export default {
    setup: {
        model: 'Leave_Application',
        list_height: 30,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    filters: [
        {
            id: "filter-from-date",
            fieldname: "from_date",
            fieldtype: "date",
            mode:"single",
            columns: 1,
            placeholder: "Date",
        },
        {
            id: "filter-Status",
            column_title: "Status",
            fieldname: "status",
            fieldtype: "link",
            model: "Doc_Status",
            placeholder: "Select Status",
        },
      
     
    ],
    default_filters:{
        employee: lite.employee_info?.name
    },
    actions: {
        
    },
    columns: [
  
        {
            column_title: "From Date",
            column_name: "from_date",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Employee Name",
            column_name: "employee_name",
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