import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Employee_Promotion',
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
            id: "employee-no",
            fieldname: "employee_number",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Employee Number",
        },
        {
            id: "employee-name",
            fieldname: "employee_name",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "full_name",
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
        // {
        //     column_title: "Full Name",
        //     column_name: "name",
        //     column_type: "text",
        //     columns: 1,
        // },
        {
            column_title: "Employee ",
            column_name: "employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Promotion Date",
            column_name: "promotion_date",
            column_type: "text",
            columns: 1,
        },
        // {
        //     column_title: "ID",
        //     column_name: "id",
        //     column_type: "text",
        //     columns: 1,
        // }
        
    ]
}