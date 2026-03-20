import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Professional_Membership_Subscription',
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
            model: 'Professional_Membership_Subscription',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "employee_name",
            fieldname: "employee_name",
            fieldtype: "link",
            model: 'Professional_Membership_Subscription',
            linkfield: "employee_name",
            columns: 1,
            placeholder: "Employee Name",
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
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Job Title",
            column_name: "job_title",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Membership Type",
            column_name: "membership_type",
            column_type: "text",
            columns: 4,
        }
        
    ]
}