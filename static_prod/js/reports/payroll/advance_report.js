import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Advance Report',
        title: "Advance Report",
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
            id: "filter-applicant",
            column_title: "Applicant",
            fieldname: "applicant",
            fieldtype: "link",
            model: "Employee",
            placeholder: "Enter Applicant",
        },
        {
            id: "filter-name",
            column_title: "Name",
            fieldname: "name",
            fieldtype: "link",
            model: "Advance_Application",
            placeholder: "Select Name",
        },   {
            id: "filter-Status",
            column_title: "Status",
            fieldname: "status",
            fieldtype: "link",
            model: "Doc_Status",
            placeholder: "Select Status",
        }
  
    ],
    actions: [
      {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],

    columns: [
        {
            column_title: "Date",
            column_name: "date",
            width: 200,
        },
        {
            column_title: "Applicant",
            column_name: "applicant",
            width: 200,
        },
        {
            column_title: "Name",
            column_name: "name",
            width: 200,
        },
        {
            column_title: "Principal Amount",
            column_name: "amount",
            width: 200,
            is_figure: true,
        },
        {
            column_title: "Application Status",
            column_name: "status",
            width: 200,
        },
        {
            column_title: "Settlement Status",
            column_name: "is_paid",
            width: 200,
        },
        {
            column_title: "Payment Method",
            column_name: "repayment_method",
            width: 200,
        },
        {
            column_title: "Total Interest",
            column_name: "overall_interest",
            width: 200,
        },
        {
            column_title: "Interest Paid to Date",
            column_name: "settled_interest",
            width: 200,
        },
      
        {
            column_title: "Paid Amount",
            column_name: "paid_amont",
            width: 200,
        },
        {
            column_title: " Last Payment Made",
            column_name: "recently_settled_amont",
            width: 200,
        },
    
        {
            column_title: "Outstanding Balance",
            column_name: "balance",
            width: 200,
        },
        {
            column_title: "Total Approved Applications",
            column_name: "approved",
            width: 200,
        },
        {
            column_title: "Total Pending Applications",
            column_name: "pending",
            width: 200,
        },
        {
            column_title: "Total Rejected Applications",
            column_name: "rejected",
            width: 200,
        },
    ]
}