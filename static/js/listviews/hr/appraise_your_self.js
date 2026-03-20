import { create_user_accounts, deactivate_separated_employees } from "../../overrides/form/hr/core.js"
import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Appraise_Your_Self',
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
        {
            id: "employee-department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            columns: 1,
            placeholder: "Employee Department",
        },
    ],
    actions: {
        main: [
            {
                fun: create_user_accounts,
                title: "Create User Account",
                icon: "app_registration",
                icon_color: "green",
                show_on_list_check: false,
                is_custom_button: false
            },
            {
                fun: deactivate_separated_employees,
                title: "Deactivate Separated Employees",
                icon: "group",
                icon_color: "red",
                show_on_list_check: false,
                is_custom_button: false
            },
        ],
        row: [
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Get JSON',
            //     icon: 'code',
            //     icon_color: 'teal',
            // },
        ]
    },
    columns: [
        {
            column_title: "Employee",
            column_name: "full_name",
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