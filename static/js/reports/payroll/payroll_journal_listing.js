import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Payroll Journal Listing',
        title: "Payroll Journal Listing",
        report_type: "script",
        is_grid_layout : true,
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [],
    actions: [
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
        {
            fun: () => {console.log('====================================');
            console.log("clicked");
            console.log('====================================');},
            title: 'Post To Pastel',
            icon: 'finance',
            icon_color: 'orange',
        },
    ],

    columns: [
        {
            column_title: "Acc Ref",
            column_name: "acc_ref",
            columns: 3,
        },
        {
            column_title: "Money Name",
            column_name: "money_name",
            columns: 3,
        },
        {
            column_title: "Incomes (Debits)",
            column_name: "income_debits",
            columns: 2,
            is_figure: true,
        },
        {
            column_title: "Deduction (Credits)",
            column_name: "deduction_credits",
            columns: 3,
            is_figure: true,
        },
    ]
}