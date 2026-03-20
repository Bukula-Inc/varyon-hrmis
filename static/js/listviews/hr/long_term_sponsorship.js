import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Long_Term_Sponsorship',
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
            model: 'Long_Term_Sponsorship',
            linkfield: "name",
            columns: 1,
            placeholder: "name",
        },
        {
            id: "employee",
            fieldname: "employee",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "name",
            columns: 1,
            placeholder: "Filter By Employee",
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
            column_title: "Last Name",
            column_name: "last_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "First Name",
            column_name: "first_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Last Name",
            column_name: "last_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Job Title",
            column_name: "designation",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
    ]
}