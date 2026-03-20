import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Job_Application',
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
            model: 'Job_Application',
            linkfield: "name",
            columns: 1,
            placeholder: "Job Application",
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
            column_title: "Job Opening",
            column_name: "job_opening",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Email",
            column_name: "email",
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