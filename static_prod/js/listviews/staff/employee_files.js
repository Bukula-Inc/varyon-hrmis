import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Employee_Files',
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
            id: "filter-created_on-date",
            fieldname: "created_on",
            fieldtype: "date",
            mode:"single",
            columns: 1,
            placeholder: "Date",
            filters: {
                "employee": lite.employee_info?.name
            },
        },
        

       
    ],
    default_filters:{
        employee: lite.employee_info?.name
    },
    actions: {
        main: [
            
        ],
        row: [
        
        ]
    },
    columns: [
     
        {
            column_title: "Employee",
            column_name: "employee",
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
        },
     
        
    ]
}