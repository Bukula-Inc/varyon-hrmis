import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Interview_Feedback',
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
            model: 'Interview',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },
        {
            id: "interviewer",
            fieldname: "interviewer",
            fieldtype: "link",
            model: 'Interview_Feedback',
            linkfield: "interviewer",
            columns: 1,
            placeholder: "Interviewer",
        },
        {
            id: "result",
            fieldname: "result",
            fieldtype: "select",
            options: [
                "Cleared",
                "Rejected",

            ],
            columns: 1,
            placeholder: "Result",
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
            column_title: "Interviewer",
            column_name: "interviewer",
            column_type: "text",
            columns: 1,
        },
      
        {
            column_title: "Result",
            column_name: "result",
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