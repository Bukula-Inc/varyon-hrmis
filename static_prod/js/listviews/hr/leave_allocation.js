import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Leave_Allocation',
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
            linkfield: "name",
            columns: 1,
            placeholder: "Employee",
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
        {
            id: "leave-type",
            fieldname: "leave_type",
            fieldtype: "link",
            model: 'Leave_Type',
            columns: 1,
            placeholder: "Leave Type",
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
            column_title: "Allocation Type",
            column_name: "populate_by",
            column_type: "text",
            columns: 1,
        },        
    ]
}