import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Paye Report',
        title: "Paye Report",
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
            fieldname: "to_date",
            fieldtype: "link",
            model: "Payslip",
            linkfield: "to_date",
            placeholder: "Select To Date",
        },
        {
            id: "filter-employee",
            column_title: "Employee",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            placeholder: "Select Employee",
        },
        {
            id: "filter-paye-number",
            column_title: "Tax Identification No",
            fieldname: "tpin",
            fieldtype: "link",
            model: "Employee",
            linkfield: "tpin",
            placeholder: "Enter paye Number",
           
        },
        {
            id: "filter-id-number",
            column_title: "NRC  Number",
            fieldname: "id_no",
            fieldtype: "link",
            model: "Employee",
            linkfield: "id_no",
            placeholder: "Enter NRC Number",
           
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
            column_title: "tpin",
            column_name: "tpin",
            width: 200,
        },
        {
            column_title: "fullName",
            column_name: "employee_names",
            width: 250,
        },
        {
            column_title: "employmentNature",
            column_name: "employment_type",
            width: 250,
        },
        {
            column_title: "grossEmoluments",
            column_name: "gross",
            width: 200,
            is_figure: true,
        },
        {
            column_title: "chargeableEmoluments",
            column_name: "gross",
            width: 200,
            is_figure: true,
        },
        {
            column_title: "totalTaxCredit",
            column_name: "",
            width: 200,
            is_figure: true,
        },
        {
            column_title: "taxDeducted",
            column_name: "tax_deducted",
            width: 200,
            is_figure: true,
        },
        {
            column_title: "taxAdjusted",
            column_name: "tax_adjusted",
            width: 200,
            is_figure: true,
        },
    

    ]
}