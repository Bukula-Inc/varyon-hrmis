import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Leave_Policy',
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
            id: "leave-policy",
            fieldname: "leave_policy",
            fieldtype: "link",
            model: 'Leave_Policy',
            linkfield: "name",
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
        //     column_title: "Full Name",
        //     column_name: "name",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "Status",
        //     column_name: "status",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "Reviewee",
        //     column_name: "reviewee",
        //     column_type: "text",
        //     columns: 1,
        // },
        // {
        //     column_title: "ID",
        //     column_name: "id",
        //     column_type: "text",
        //     columns: 1,
        // }
        
    ]
}