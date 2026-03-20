import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Suggestion_Box',
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
    },
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Suggestion_Box',
            linkfield: "name",
            columns: 1,
            placeholder: "Suggestion Box",
            filters:{
                "employee": lite.employee_info?.name  
            }
        }
     
       
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
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Suggestion Category",
            column_name: "category",
            column_type: "text",
            columns: 1,
        },
        
    ]
}