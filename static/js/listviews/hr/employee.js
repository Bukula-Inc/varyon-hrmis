import { create_user_accounts, deactivate_separated_employees, separate_with_separated_employees, normalize_emp_info, add_paye_to_all_employees  } from "../../overrides/form/hr/core.js"
import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Employee',
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
            
            {
                fun: separate_with_separated_employees,
                title: "Separate With Separated Employees",
                icon: "group",
                icon_color: "purple",
                show_on_list_check: false,
                is_custom_button: false
            },
            {
                fun: normalize_emp_info,
                title: "Normalize Employees Basic Info",
                icon: "how_to_reg",
                icon_color: "purple",
                show_on_list_check: false,
                is_custom_button: false
            },
            {
                fun: add_paye_to_all_employees,
                title: "Attach Paye To all Employees",
                icon: "attach_file",
                icon_color: "purple",
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
            column_title: "Department",
            column_name: "department",
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