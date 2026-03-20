import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Clearance_Form',
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
            id: "bulletin",
            fieldname: "Announcement",
            fieldtype: "link",
            model: 'Announcement',
            linkfield: "name",
            columns: 1,
            placeholder: "Name",
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
            column_title: "Employee Name",
            column_name: "employee_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Job Title",
            column_name: "job_title",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Date of Engagement",
            column_name: "engagement_date",
            column_type: "text",
            columns: 1,
        },        
    ]
}