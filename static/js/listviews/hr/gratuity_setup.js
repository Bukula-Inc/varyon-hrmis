import { create_user_accounts, deactivate_separated_employees } from "../../overrides/form/hr/core.js"
import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Gratuity_Configuration',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: false
    },
    filters: [
        {
            id: "employee-no",
            fieldname: "name",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Employee",
        },
        {
            id: "employee-name",
            fieldname: "full_name",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "full_name",
            columns: 1,
            placeholder: "Employee Names",
            default:"Kakuhu  Kabwe"
        },
    ],
    actions: {
        main: [
            // {
            //     fun: create_user_accounts,
            //     title: "Create User Account",
            //     icon: "app_registration",
            //     icon_color: "green",
            //     show_on_list_check: false,
            //     is_custom_button: false
            // },
            // {
            //     fun: deactivate_separated_employees,
            //     title: "Deactivate Separated Employees",
            //     icon: "group",
            //     icon_color: "red",
            //     show_on_list_check: false,
            //     is_custom_button: false
            // },
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
                column_title: "Gratuity Rate",
                column_name: "gratuity_rate",
                column_type: "text",
                columns: 1,
            },
            {
                column_title: "Debit Account",
                column_name: "debit_account",
                column_type: "text",
                columns: 1,
            },
            {
                column_title: "Credit Account",
                column_name: "credit_account",
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

// // import { wipe_all_transactions } from "../core/functions.js"
// export default {
//     setup: {
//         model: 'Graduate',
//         list_height: 50,
//         allow_submit: false,
//         allow_cancel: false,
//         allow_delete: true,
//         allow_export_csv: true,
//         allow_export_excel: true,
//         allow_print: true
//     },
//     filters: [
     
//     ],
//     actions: {
//         main: [
            
//         ],
//         row: [
//             // {
//             //     fun: wipe_all_transactions,
//             //     title: 'Get JSON',
//             //     icon: 'code',
//             //     icon_color: 'teal',
//             // },
//         ]
//     },
//     columns: [
//         {
//             column_title: "Gratuity Rate",
//             column_name: "gratuity_rate",
//             column_type: "text",
//             columns: 1,
//         },
//         {
//             column_title: "Debit Account",
//             column_name: "debit_account",
//             column_type: "text",
//             columns: 1,
//         },
//         {
//             column_title: "Credit Account",
//             column_name: "credit_account",
//             column_type: "text",
//             columns: 1,
//         },
//         {
//             column_title: "Status",
//             column_name: "status",
//             column_type: "status",
//             columns: 1,
//         },
//     ]
// }