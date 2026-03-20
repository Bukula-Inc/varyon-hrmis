import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Exit_Interview',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
        // {
        //     id: "id",
        //     fieldname: "name",
        //     fieldtype: "link",
        //     model: 'Exit_Interview',
        //     columns: 1,
        //     placeholder: "ID",
        // },
        // {
        //     id: "employee-name",
        //     fieldname: "employee_name",
        //     fieldtype: "link",
        //     model: 'Employee',
        //     linkfield: "full_name",
        //     columns: 1,
        //     placeholder: "Employee Name",
        // },
        // {
        //     id: "id",
        //     fieldname: "name",
        //     fieldtype: "link",
        //     model: 'Company',
        //     columns: 1,
        //     placeholder: "Company",
        // },
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
    default_filters:{
        employee: lite.employee_info?.name
    },
    columns: [
       
       
        {
            column_title: "Employee Name",
            column_name: "employee_name",
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