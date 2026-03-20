import {initiate_pre_payroll_payment} from '../../overrides/form/payroll/core.js'
export default {
    setup: {
        model: 'Payroll_Processor',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Payroll_Processor',
            columns: 1,
            placeholder: "Select Name",
        },
        {
            id: "country",
            fieldname: "country",
            fieldtype: "link",
            model: 'Country',
            columns: 1,
            placeholder: "Select Country",
        },
        {
            id: "currency",
            fieldname: "currency",
            fieldtype: "link",
            model: 'Currency',
            columns: 1,
            placeholder: "Select Currency",
        }
    ],
    actions: {
        main: [
            {
                fun: initiate_pre_payroll_payment,
                title: 'Pre Payroll Payment',
                icon: 'payments',
                icon_color: 'green'
            }            
        ],
        row: []
    },
    columns: [
        {
            column_title: "From Date",
            column_name: "from_date",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Total Employees",
            column_name: "total_employees",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Total Successful Payslips",
            column_name: "total_successful_payslips",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Total Failed Payslips",
            column_name: "total_failed_payslips",
            column_type: "text",
            columns: 1,
        }, 
        {
            column_title: "Total Gross",
            column_name: "total_gross",
            column_type: "figure",
            is_figure:true,
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 3,
        },
    ]
}