import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Verbal_Warning',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    filters: [
     
        {
            id: "employee_no",
            fieldname: "employee_no",
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
            column_title: "Issued To",
            column_name: "employee_full_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Advised Action",
            column_name: "advised_action",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Action Subject",
            column_name: "action_subject",
            column_type: "text",
            columns: 1,
        },
    ]
}