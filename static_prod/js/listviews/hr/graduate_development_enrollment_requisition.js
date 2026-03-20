import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Graduate_Development_Enrollment',
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
        // {
        //     column_title: "Status",
        //     column_name: "status",
        //     column_type: "status",
        //     columns: 1,
        // },
    ]
}