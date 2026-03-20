import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: "Employee Leave Balance",
        title: "Employee Leave Balance",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
     
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Employee',
            linkfield: "name",
            columns: 1,
            placeholder: "Employee",
        },

        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Department",
        },
        {
            id: "date",
            fieldname: "date",
            fieldtype: "date",
            model: '',
            placeholder: "Date",
        },
     
    ],
    actions: [
       
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],
    columns: [
        {
            column_title: "Employee",
            column_name: "employee",
            column_type: "text",
            width: 370,
            
        },
        {
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            width: 370,
            
        },
    
        {
            column_title: "Department",
            column_name: "department",
            column_type: "link",
            model: 'Department',
            width: 370,
            
        },
        {
            column_title: "Leave Type",
            column_name: "leave_type",
            column_type: "link",
            model: 'Leave_Type',
            width: 370,
            
        },
        {
            column_title: "Used Leave",
            column_name: "used_leave",
            column_type: "link",
            model: 'Leave_Type',
            width: 350,
            // sortable: true
        },
        {
            column_title: "Remaining Leave",
            column_name: "remaining_leave",
            column_type: "link",
            model: 'Leave_Type',
            width: 350,
            // sortable: true
        },
        
    
    ]
}