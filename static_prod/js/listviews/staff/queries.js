import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Query',
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
            model: 'Query',
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
        {
            column_title: "From",
            column_name: "employee",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
        // {
        //     column_title: "Maximum Consecutive Leaves Allowed",
        //     column_name: "maximum_leave",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "Is Carried Forward",
        //     column_name: "carry_forward",
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