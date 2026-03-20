import { wipe_all_transactions } from "../../listviews/core/functions.js"

export default {
    setup: {
        model: 'Employee Seperation Report',
        title: "Employee Separation Report",
        report_type: "query",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
        {
            id: "employee_name",
            fieldname: "employee_name",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "name",
            columns: 1,
            placeholder: "Employee Name",
        },
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Department",
        },
        {
            id: "separation_date",
            fieldname: "separation_date",
            fieldtype: "date",
            model: '',
            placeholder: "Separation Date",
        },
        {
            id: "separation_type",
            fieldname: "separation_type",
            fieldtype: "select",
            options: ["Voluntary", "Involuntary"],
            placeholder: "Separation Type",
        },
        {
            id: "status",
            fieldname: "status",
            fieldtype: "select",
            options: ["Active", "Completed", "Cancelled"],
            placeholder: "Status",
        }
    ],
    actions: [
        {
            fun: wipe_all_transactions,
            title: 'Export JSON',
            icon: 'download',
            icon_color: 'blue',
        },
        {
            title: 'Generate Exit Documents',
            icon: 'file-text',
            icon_color: 'green',
        }
    ],
    columns: [
        {
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "link",
            model: 'Employee',
            width: 200,
            sortable: true
        },
        {
            column_title: "Council",
            column_name: "company",
            column_type: "link",
            model: 'Company',
            width: 200,
            sortable: true
        },
        {
            column_title: "Department",
            column_name: "department",
            column_type: "link",
            model: 'Department',
            width: 200,
            sortable: true
        },
        {
            fieldlabel: "Job Title",
            column_name: "designation",
            column_type: "text",
            width: 200,
            sortable: true
        },
        {
            column_title: "Date of Joining",
            column_name: "date_of_joining",
            column_type: "text",
            width: 200,
            sortable: true
        },
        {
            column_title: "Total Assets",
            column_name: "total_assets",
            column_type: "text",
            width: 200,
            sortable: true
        },
        {
            column_title: "Settled Assets",
            column_name: "settled_assets",
            column_type: "text",
            width: 200,
            sortable: true
        },
        {
            column_title: "Unsettled Assets",
            column_name: "unsettled_assets",
            column_type: "text",
            width: 200,
            sortable: true
        },
        {
            column_title: "settled Assets Value",
            column_name: "settled_value",
            column_type: "text",
            width: 200,
            sortable: true
        },
        {
            column_title: "Unsettled Assets Value",
            column_name: "unsettled_value",
            column_type: "text",
            width: 200,
            sortable: true
        },
        {
            column_title: "Total Assets Value",
            column_name: "total_asset_value",
            column_type: "text",
            width: 200,
            sortable: true
        },  
        {
            column_title: "Total Receivables",
            column_name: "total_receivables",
            column_type: "text",
            width: 200,
            sortable: true
        }, 
        {
            column_title: "Total Payable",
            column_name: "total_payable",
            column_type: "text",
            width: 200,
            sortable: true
        },  
    ]
}