import { wipe_all_transactions } from "../../listviews/core/functions.js"

export default {
    setup: {
        model: 'ECZ Loan Report',
        title: "Loan Report",
        report_type: "script",
        // is_grid_layout: true,
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
            id: "reports_to",
            fieldname: "reports_to",
            fieldtype: "link",
            model: 'Employee',
            columns: 250,
            placeholder: "Reports To",
        },
        {
            id: "cleared",
            column_title: "Status",
            fieldname: "cleared",
            fieldtype: "select",
            options: ["Open", "Closed"],
            placeholder: "Select Status",
        },  
    ],
  
    actions: [],
    columns:
        [
            {
                column_title: "Employee No",
                column_name: "employee",
                column_type: "link",
                width: 250,
            },  
            {
                column_title: "Loan",
                column_name: "loan_id",
                column_type: "link",
                width: 250,
            },  
            {
                column_title: "Loan Type",
                column_name: "loan_type",
                column_type: "text",
                width: 250,
            },  
            {
                column_title: "Disbursement Date",
                column_name: "disbursement_date",
                column_type: "date",
                width: 250,
            }, 
            {
                column_title: "Last Repayment Date",
                column_name: "due_date",
                column_type: "date",
                width: 250,
            },
            {
                column_title: "Repayment Period (Months)",
                column_name: "repayment_period",
                column_type: "text",
                width: 250,
            }, 
            {
                column_title: "Remaining Months",
                column_name: "remaining_months",
                column_type: "text",
                width: 250,
            }, 
            {
                column_title: "Loaned Amount",
                column_name: "loan_amount",
                column_type: "float",
                width: 250,
                is_figure: true,
                classnames: "text-right"
            }, 
            {
                column_title: "Interest Total",
                column_name: "interest_total",
                column_type: "float",
                width: 250,
                is_figure: true,
                classnames: "text-right"
            }, 
            {
                column_title: "Monthly Repayment",
                column_name: "monthly_repayment",
                column_type: "float",
                width: 250,
                is_figure: true,
                classnames: "text-right"
            },
            {
                column_title: "Recovered Amount",
                column_name: "paid",
                column_type: "float",
                width: 250,
                is_figure: true,
                classnames: "text-right"
            }, 
            {
                column_title: "Balance",
                column_name: "balance",
                column_type: "float",
                width: 250,
                is_figure: true,
                classnames: "text-right"
            }, 
        ]
}