import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Exit_Interview_Question',
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
            id: "id",
            fieldname: "name",
            fieldtype: "link",
            model: 'Exit_Interview_Question',
            columns: 1,
            placeholder: "ID",
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
        // {
        //     column_title: "Job Title",
        //     column_name: "designation",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "Department",
        //     column_name: "department",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "Status",
        //     column_name: "status",
        //     column_type: "status",
        //     columns: 1,
        // },     
        
    ]
}