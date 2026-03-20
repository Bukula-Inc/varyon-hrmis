import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Transfer_FIle',
        title: "Bank Transfer FIle",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true,
        is_grid_layout: true,
    },
    filters: [
        {
            id: "from_date",
            fieldname: "from_date",
            fieldtype: "date",
            linkfield: "from_date",
            placeholder: "Select From Payroll Period",
        },
        {
            id: "to_date",
            fieldname: "to_date",
            fieldtype: "date",
            linkfield: "to_date",
            placeholder: "Select To Payroll Period",
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
            id: 'employee',
            column_title: "Employee No",
            column_name: "employee",
            columns: 7,
        },
        {
            id: 'employee_names',
            column_title: "Employee Names",
            column_name: "employee_names",
            columns: 7,
        },
        {
            id: 'bank_name',
            column_title: "Bank Name",
            column_name: "bank_name",
            columns: 7,
        },
        {
            id: 'bank_account_no',
            column_title: "Bank Account No",
            column_name: "bank_account_no",
            columns: 7,
        },
        {
            id: 'sort_code',
            column_title: "Sort Code",
            column_name: "sort_code",
            columns: 7,
        },
        {
            id: 'description',
            column_title: "Description",
            column_name: "description",
            columns: 7,
        },
        {
            id: 'amount',
            column_title: "Amount",
            column_name: "amount",
            columns: 7,
            is_figure: true,
        },
    ]
}