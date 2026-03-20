import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Leave Application',
        title: "Employee's Leave",
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
            id: "name",
            fieldname: "name",
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
            placeholder: "Leave Type",
        },
        {
            id: "from-date",
            fieldname: "from_date",
            fieldtype: "date",
            model: '',
            placeholder: "From Date",
        },
        {
            id: "to-date",
            fieldname: "to_date",
            fieldtype: "date",
            model: '',
            placeholder: "To Date",
        },
    ],
    actions: [
       
       
    ],
    columns: [
        {
            column_title: "Employee",
            column_name: "name",
            column_type: "text",
            width: 100,
            
        },
        {
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            width: 200,
            
        },
        {
            column_title: "Leave Type",
            column_name: "leave_type",
            column_type: "link",
            model: 'Leave_Type',
            width: 200,
            
        },
        {
            column_title: "Department",
            column_name: "department",
            column_type: "link",
            model: 'Department',
            width: 200,
            
        },
        {
            column_title: "From Date",
            column_name: "from_date",
            column_type: "text",
            width: 200,
            
        },

        {
            column_title: "To Date",
            column_name: "to_date",
            column_type: "text",
            model: '',
            width: 200,
        },
        {
            column_title: "Total Days",
            column_name: "total_days",
            column_type: "text",
            model: '',
            width: 100,
        },

        {
            column_title: "Leave Approver",
            column_name: "leave_approver",
            column_type: "text",
            model: 'Employee',
            width: 110,
        },
        {
            column_title: "Leave Approver Name",
            column_name: "leave_approver_name",
            column_type: "text",
            model: 'Employee',
            width: 200,
        },

    
     
    ]
}