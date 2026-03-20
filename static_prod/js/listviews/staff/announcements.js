import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Announcement',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
     
        {
            id: "lannouncement",
            fieldname: "announcement",
            fieldtype: "link",
            model: 'Announcement',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
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
        // {
        //     column_title: "Full Name",
        //     column_name: "name",
        //     column_type: "text",
        //     columns: 1,
        // },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            columns: 1,
        },
        // {
        //     column_title: "Reviewee",
        //     column_name: "reviewee",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "ID",
        //     column_name: "id",
        //     column_type: "text",
        //     columns: 1,
        // }
        
    ]
}