import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Nhima Report',
        title: "Nhima Report",
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
            id: "filter-nhima",
            column_title: "NHIMA Number",
            fieldname: "nhima",
            fieldtype: "link",
            model: "Employee",
            linkfield: "nhima",
            placeholder: "Enter Nhima Number",
           
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
            column_title: "Company NHIMA Account",
            column_name: "company_nhima_acc",
            width: 170,
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
            column_title: "NHIMA Number",
            column_name: "nhima",
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
            column_title: "Basic Salary",
            column_name: "basic_pay",
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