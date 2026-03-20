import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Leave_Entry',
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
            id: "leave-entry",
            fieldname: "leave_entry",
            fieldtype: "link",
            model: 'Leave_Entry',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
      
    ],
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
            column_name: "employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Leave Type",
            column_name: "leave_type",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Total Days",
            column_name: "total_days",
            column_type: "float",
            is_figure:true,
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