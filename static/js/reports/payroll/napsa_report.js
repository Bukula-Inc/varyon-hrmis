import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Napsa Report',
        title: "Napsa Report",
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
            model: "Payroll_Processor",
            linkfield: "from_date",
            placeholder: "Select From Date",
        },
        {
            id: "filter-to-date",
            fieldname: "to_date",
            fieldtype: "link",
            model: "Payroll_Processor",
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
            id: "filter-social-number",
            column_title: "Social Security Number",
            fieldname: "napsa",
            fieldtype: "link",
            model: "Employee",
            linkfield: "napsa",
            placeholder: "Enter Social Security Number",
           
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
            column_title: "Comapy NAPSA Account",
            column_name: "company_napsa_acc",
            width: 150,
        },
        {
            column_title: "Year",
            column_name: "year",
            width: 150,
        },
        {
            column_title: "Month",
            column_name: "month",
            width: 150,
        },
        {
            column_title: "SSNo",
            column_name: "napsa",
            width: 150,
        },
        {
            column_title: "NRC  Number",
            column_name: "id_no",
            width: 150,
        },
        {
            column_title: "Surname",
            column_name: "last_name",
            width: 150,
        },
        {
            column_title: "Firstname",
            column_name: "first_name",
            width: 150,
        },
        {
            column_title: "Other name",
            column_name: "middle_name",
            width: 150,
        },
        {
            column_title: "Date of Birth",
            column_name: "d_o_b",
            width: 150,
        },
     
      
        {
            column_title: "Gross Wage",
            column_name: "gross",
            width: 150,
            is_figure: true,
        },
        {
            column_title: "Employee's Share",
            column_name: "employee_share",
            width: 150,
            is_figure: true,
        },
        {
            column_title: "Employer's Share",
            column_name: "employer_share",
            width: 150,
            is_figure: true,
        },
    ]
}