import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Certificate_Of_Service',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    default_filters:{
        employee_id: lite.employee_info?.name
    },
    filters: [
     
        {
            id: "employee_id",
            fieldname: "employee_id",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "name",
            columns: 1,
            placeholder: "Employee No",
        },
        {
            id: "employee_name",
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
        {
            column_title: "Staff",
            column_name: "employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "NAPSA Membership Number",
            column_name: "napsa_membership_number",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Occupation",
            column_name: "state_occupation",
            column_type: "text",
            columns: 1,
        },
    ]
}