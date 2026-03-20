import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'employee_seperation',
        title: "Employee Separation",
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
            id: "from-date",
            fieldname: "from_date",
            fieldtype: "date",
            placeholder: "Select Dates",
        },
        {
            id: "to-date",
            fieldname: "to_date",
            fieldtype: "date",
            placeholder: "Select Dates",
        },
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Select Department",
        },
        {
            id: "designation",
            fieldname: "designation",
            fieldtype: "link",
            model: 'Designation',
            placeholder: "Select Designation",
        },
        {
            id: "reports-to",
            fieldname: "reports_to",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Reports To",
        },
    ],
  
    actions: [
 
    ],

    columns: [
        {
            column_title: "Employee",
            column_name: "employee",
            column_type: "text",
            width: 240,
         
        },

        {
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            width: 240,
            sortable: true
        },
        {
            column_title: "Date of Joining",
            column_name: "date_of_joining",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Relieving Date",
            column_name: "resignation_date",
            column_type: "text",
            width: 240,
        },
        {
            column_title: "Exit Interview",
            column_name: "interview_summary",
            column_type: "text",
            width: 240,
    
        },
        {
            column_title: "Department",
            column_name: "department",
            model: 'Department',
            width: 240,
        
        },
        {
            fieldlabel: "Job Title",
            column_name: "Designation",
            model: 'Designation',
            width: 240,
        
        },
        {
            column_title: "Reported To",
            column_name: "reports_to",
            width: 240,
        },
    ]
}