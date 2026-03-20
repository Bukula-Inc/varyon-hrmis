import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'payroll Payable',
        title: "Payroll Payable",
        report_type: "script",
        is_grid_layout : true,
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
        {
            id: "filter-posting-date",
            fieldname: "posting_date",
            fieldtype: "link",
            model: "",
            placeholder: "Select From Date",
        },
   
    ],
    actions: [
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],

    columns: [
        {
            column_title: "Payable Account",
            column_name: "payable_account",
            columns: 3,
        },
        {
            column_title: "Against Account",
            column_name: "against_account",
            columns: 3,
        },
        {
            column_title: "Posting Date",
            column_name: "posting_date",
            columns: 2,
        },
       
        {
            column_title: "Debit",
            column_name: "dr",
            columns: 3,
            is_figure: true,
        },
        {
            column_title: "Credit",
            column_name: "cr",
            columns: 3,
            is_figure: true,
        },
        {
            column_title: "Balance",
            column_name: "balance",
            columns: 3,
            is_figure: true,
        },
    ]
}