import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Interview',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
     
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Job_Applicant',
            linkfield: "name",
            columns: 1,
            placeholder: "Job Applicant",
        },
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Interview',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "schedule",
            fieldname: "schedule",
            fieldtype: "link",
            model: 'Interview',
            linkfield: "schedule",
            columns: 1,
            placeholder: "Scheduled On",
        },
        // {
        //     id: "status",
        //     fieldname: "status",
        //     fieldtype: "select",
        //     options: [
        //         "Pending",
        //         "Under Review",
        //         "Cleared",
        //         "Rejected",

        //     ],
        //     columns: 1,
        //     placeholder: "Status",
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
    columns: [
        
        {
            column_title: "Applicant",
            column_name: "short_listed_applicant",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Applicant Email",
            column_name: "email",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Applicant Contact No",
            column_name: "contact_no",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Designation",
            column_name: "offered_job_title",
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