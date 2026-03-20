import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Employee Welfare Report',
        title: "Medical Deductions Report",
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
            id: "from_date",
            fieldname: "from_date",
            fieldtype: "date",
            placeholder: "Select Dates",
        },
        {
            id: "to_date",
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
            id: "reports_to",
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
            column_title: "Employee No",
            column_name: "employee",
            column_type: "link",
            width: 240,
        },
        {
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            width: 240,
         
        },

        {
            column_title: "Department",
            column_name: "department",
            column_type: "link",
            width: 240,
            sortable: true
        },
        {
            column_title: "Total Medical Bill",
            column_name: "welfare_expense",
            column_type: "text",
            width: 240,
            is_figure: true,
        },
        {
            column_title: "Council Covered Bill",
            column_name: "company_covered_expense",
            column_type: "text",
            width: 240,
            is_figure: true,
        },
        {
            column_title: "Staff Bill Recoverable",
            column_name: "staff_covered_expense",
            column_type: "text",
            width: 240,
            is_figure: true,
        },
        {
            column_title: "Recovery Period (Months)",
            column_name: "payment_length",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Remaining Period (Months)",
            column_name: "remaining_months",
            column_type: "text",
            width: 240,
        },

        {
            column_title: "Monthly Recovery Amount",
            column_name: "monthly_welfare_expense",
            column_type: "text",
            width: 240,
            is_figure: true,
        },
        {
            column_title: "Total Recovered Amount",
            column_name: "total_recovered_amount",
            column_type: "text",
            width: 240,
            is_figure: true,
        },
        {
            column_title: "Staff Bill Balance",
            column_name: "staff_bill_balance",
            column_type: "text",
            width: 240,
            is_figure: true,
        },
    ]
}
