import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Employee_Attendance',
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
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
        {
            column_title: "Attendance Date",
            column_name: "attendance_date",
            column_type: "text",
            columns: 1,
        },
      
        
    ]
}