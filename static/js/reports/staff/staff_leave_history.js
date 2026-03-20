import { wipe_all_transactions } from "../../listviews/core/functions.js"

export default {
    setup: {
        model: 'staff leave summary',
        title: "Leave Summary",
        report_type: "script",
        is_grid_layout: true,
        include_opening: true,
        include_closing: true,
        allow_print: false,
        allow_download_csv: false,
        allow_download_excel: false,
        allow_download_pdf: false
    },
    filters: [
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Select Department",
        },
        {
            id: "designation",
            fieldname: "designation",
            fieldtype: "link",
            model: 'Designation',
            placeholder: "Select Designation",
        },
        {
            id: "reports-to",
            fieldname: "reports_to",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Reports To",
        },
    ],
  
    actions: [],
    columns: [
        
        {
            column_title: "Leave Type",
            column_name: "leave_type",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Total Accrued",
            column_name: "total_days",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Available Leave Days",
            column_name: "remaining_leave_days",
            column_type: "text",
            columns: 1,
        }, 
        {
            column_title: "Used Leave Days",
            column_name: "used_leave_days",
            column_type: "text",
            columns: 1,
        }, 
    ]
}