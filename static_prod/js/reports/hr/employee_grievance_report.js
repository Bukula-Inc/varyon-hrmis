import { wipe_all_transactions } from "../../listviews/core/functions.js";

export default {
    setup: {
        model: 'Employee Grievance',
        title: "Employee Grievance Report",
        model: "Employee Grievance Report",
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
            id: "from-date",
            fieldname: "from_date",
            fieldtype: "date",
            placeholder: "Select Start Date",
        },
        {
            id: "to-date",
            fieldname: "to_date",
            fieldtype: "date",
            placeholder: "Select End Date",
        },
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Select Department",
        },
        {
            id: "grievance-type",
            fieldname: "grievance_type",
            fieldtype: "select",
            options: ["Harassment", "Salary Issue", "Workplace Safety", "Discrimination", "Others"],
            placeholder: "Select Grievance Type",
        },
        {
            id: "status",
            fieldname: "status",
            fieldtype: "select",
            options: ["Pending", "Resolved", "Escalated"],
            placeholder: "Select Status",
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
            column_title: "Raised On",
            column_name: "created_on",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Raised By",
            column_name: "raised_by",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Raised Against",
            column_name: "grievance_against",
            column_type: "text",
            width: 240,
            sortable: true
        },
        {
            column_title: "Total Grievances Received",
            column_name: "grievances_received_by_employee",
            column_type: "text",
            width: 240,
            sortable: true
        },
        {
            column_title: "Grieved Reports To",
            column_name: "reports_to",
            column_type: "text",
            width: 240,
            sortable: true
        },
        {
            column_title: "Grievance Type",
            column_name: "grievance_type",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Subject",
            column_name: "subject",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Resolution Date",
            column_name: "resolution_date",
            column_type: "date",
            width: 240,
        },
        {
            column_title: "Resolved By",
            column_name: "resolved_by",
            width: 240,
        },
    ]
};
