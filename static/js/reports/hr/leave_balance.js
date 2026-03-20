import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Leave Allocation',
        title: "Leave Allocation",
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
            width: 350,
            // sortable: true
        },
        {
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            width: 350,
            // sortable: true
        },
      
        {
            column_title: "Council",
            column_name: "company",
            column_type: "link",
            model: 'Company',
            width: 350,
        },
        {
            column_title: "Department",
            column_name: "department",
            column_type: "link",
            model: 'Department',
            width: 350,
            // sortable: true
        },
    ]
}