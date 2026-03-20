import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Employee Welfare Report',
        title: "Employee Welfare Report",
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
            placeholder: "Select Dates",
        },
        {
            id: "to-date",
            fieldname: "to_date",
            fieldtype: "date",
            placeholder: "Select Dates",
        },

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
  
    actions: [
 
    ],

    columns: [
        {
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            width: 240,
         
        },

        {
            column_title: "Department",
            column_name: "department",
            column_type: "text",
            width: 240,
            sortable: true
        },
        {
            column_title: "Welfare Type",
            column_name: "welfare_type",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Welfare Expense",
            column_name: "welfare_expense",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Company Covered Expense",
            column_name: "company_covered_expense",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Staff Covered Expense",
            column_name: "staff_covered_expense",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Payment Length Unit",
            column_name: "pay_length_unit",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Payment Length",
            column_name: "payment_length",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Company Contribution %",
            column_name: "company_contribution_percent",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Staff Contribution %",
            column_name: "staff_contribution_percent",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Days Since Submission",
            column_name: "days_since_submission",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Weeks Since Submission",
            column_name: "weeks_since_submission",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Monthly Welfare Expense",
            column_name: "monthly_welfare_expense",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Quarterly Welfare Expense",
            column_name: "quarterly_welfare_expense",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Yearly Welfare Expense",
            column_name: "yearly_welfare_expense",
            column_type: "text",
            width: 240,
        },
    ]
}
