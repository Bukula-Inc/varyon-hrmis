import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Advance Balance',
        title: "Advance Balance",
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
            column_title: "Disbursement Date",
            column_name: "disbursement_date",
            width: 200,
        },
        {
            column_title: "Due Date",
            column_name: "due_date",
            width: 200,
        },
        {
            column_title: "Applicant",
            column_name: "applicant",
            width: 200,
        },
        {
            column_title: "Advance Amount",
            column_name: "amount",
            width: 200,
            is_figure: true,
        },
        {
            column_title: "Paid Amount",
            column_name: "paid_amount",
            width: 200,
        },
        {
            column_title: "Outstanding Balance",
            column_name: "balance",
            width: 200,
        },
    ]
}