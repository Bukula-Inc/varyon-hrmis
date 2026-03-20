import { wipe_all_transactions } from "../../listviews/core/functions.js"

export default {
    setup: {
        model: 'Leave Summary',
        title: "Leave Summary",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
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
    columns:
        [
            {
                column_title: "Employee Name",
                column_name: "employee",
                column_type: "text",
                width: 300,
            },
             {
                column_title: "Full Names",
                column_name: "employee_name",
                column_type: "text",
                width: 300,
            },
            {
                column_title: "Type",
                column_name: "leave_type",
                column_type: "text",
                width: 300,
            },
            {
                column_title: "Accrued",
                column_name: "total_days",
                column_type: "text",
                width: 300,
            },
            {
                column_title: "Days Taken",
                column_name: "used_leave_days",
                column_type: "text",
                width: 300,
            },
            {
                column_title: "Total Days",
                column_name: "total_days",
                column_type: "text",
                width: 300,
            },
            {
                column_title: "Balance",
                column_name: "remaining_leave_days",
                column_type: "text",
                width: 300,
            },  
        ]
}