import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Employee_Transfer_Memo',
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
            id: "employee",
            fieldname: "employee",
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
            column_title: "Transfer Employee",
            column_name: "transfer_employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "New Location",
            column_name: "new_location",
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