import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Performance_Agreement',
        list_height: 440,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "work_plan",
            fieldname: "name",
            fieldtype: "link",
            model: 'Work_Plan',
            columns: 1,
            placeholder: "Work Plan",
            filters:{
                "employee": lite.employee_info?.name  
            }
        },
        {
            id: "filter-Status",
            column_title: "Status",
            fieldname: "status",
            fieldtype: "link",
            model: "Work_Plan",
            placeholder: "Select Status",
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
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}