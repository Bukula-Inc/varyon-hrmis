import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Long_Term_Sponsorship_Fund_Request',
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
            model: 'Long_Term_Sponsorship_Fund_Request',
            linkfield: "name",
            columns: 1,
            placeholder: "Name",
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
        {
            id: "reference",
            fieldname: "reference",
            fieldtype: "link",
            model: 'Long_Term_Sponsorship',
            linkfield: "name",
            columns: 1,
            placeholder: "Filter By reference",
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
            column_title: "Employee",
            column_name: "employee",
            column_type: "link",
            model: "Employee",
            columns: 1,
        },
        {
            column_title: "reference",
            column_name: "reference",
            column_type: "link",
            model: "Long_Term_Sponsorship",
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