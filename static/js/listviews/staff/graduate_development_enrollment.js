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
    default_filters:{
        requisitioned_by: lite.employee_info?.name
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
    default_filter:{
        requisitioned_by: lite.employee_info?.name
    },
    columns: [
        {
            column_title: "Job title",
            column_name: "position",
            column_type: "link",
            model: "Designation",
            columns: 1,
        },
        {
            column_title: "Number Required",
            column_name: "number_required",
            column_type: "int",
            columns: 1,
        },
    ]
}