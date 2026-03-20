import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Payroll Summary',
        title: "Payroll Summary",
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
            id: "filter-from-date",
            fieldname: "from_date",
            fieldtype: "link",
            model: "Payslip",
            linkfield: "from_date",
            placeholder: "Select From Date",
        },
        {
            id: "filter-to-date",
            fieldname: "_dattoe",
            fieldtype: "link",
            model: "Payslip",
            linkfield: "to_date",
            placeholder: "Select to Date",
        },
        {
            id: "filter-name",
            column_title: "Name",
            fieldname: "name",
            fieldtype: "link",
            model: "Payroll_Processor",
            placeholder: "Select Name",
        }
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
            column_title: "Name",
            column_name: "name",
            width: 170,
        },
        {
            column_title: "From Date",
            column_name: "from_date",
            width: 170,
        },
        {
            column_title: "To Date",
            column_name: "to_date",
            width: 170,
        
        },
        {
            column_title: "Total Employees",
            column_name: "total_employees",
            width: 170,
        },
        {
            column_title: "Total Basic",
            column_name: "total_basic",
            width: 170,
            is_figure: true,
        },
        {
            column_title: "Total Earnings",
            column_name: "total_earnings",
            width: 300,
            is_figure: true,
        },
        {
            column_title: "Total Deductions",
            column_name: "total_deductions",
            width: 300,
            is_figure: true,
        },
        {
            column_title: "Total Net",
            column_name: "total_net",
            width: 300,
            is_figure: true,
        },
    ]
}