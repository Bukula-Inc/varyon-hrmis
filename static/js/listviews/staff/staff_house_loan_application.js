import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'House_Loan_Application',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
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
            model: 'Employee',
            linkfield: "name",
            columns: 1,
            placeholder: "Job Applicant",
        },
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            columns: 1,
            placeholder: "Department",
        },
    ],
    actions: {
        main: [
            
        ],
        row: [
            {
                fun: wipe_all_transactions,
                title: 'Get JSON',
                icon: 'code',
                icon_color: 'teal',
            },
        ]
    },
     
    columns: [
        {
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            columns: 1,
        },
    ]
}