import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Training_Event',
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
            model: 'Training_Event',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
            filters:{
                "employee": lite.employee_info?.name  
            }
        },
        {
            id: "type",
            fieldlabel: "Type",
            fieldname: "type",
            fieldtype: "select",
            options: [
                "Seminar",
                "Theory",
                "Workshop",
                "Conference",
                "Exam",
            
                
            ],
            columns: 1,
            placeholder: " Enter Type",
            required: false,
            hidden: false,
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
            column_title: "Type",
            column_name: "type",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Location",
            column_name: "location",
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