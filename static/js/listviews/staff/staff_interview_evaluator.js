import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Interview_Rating',
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
            model: 'Interview_Rating',
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
      default_filters:{
        evaluator: (lite?.user?.first_name  + " " + lite?.user?.last_name)
    },
    columns: [
        {
            column_title: "Rate",
            column_name: "rating_complement",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            columns: 1,
        },
    ]
}