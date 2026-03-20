import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Transport_Request',
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
            id: "id",
            fieldname: "name",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Select Employee",
            filters:{
                "employee": lite.employee_info?.name  
            }
        },
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            mode:"Department",
            columns: 1,
            placeholder: "Select Department",
        },
    ],
    default_filters:{
        employee: lite.employee_info?.name
    },
    actions: {
        main: [
            
        ],
        row: [
            {
                fun: wipe_all_transactions,
                title: 'Get JSON',
                icon: 'code',
                icon_color: 'teal',
            },
        ]
    },
    columns: [
       
       
        {
            column_title: "Employee Name",
            column_name: "full_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Department",
            column_name: "department",
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