import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Interview_Schedule',
        list_height: 50,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    default_filters:{
        owner: lite.user?.name
    },
    filters: [
     
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Interview_Schedule',
            linkfield: "name",
            columns: 1,
            placeholder: "Select Interview Schedule",
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
    default_filters:{
        employee: lite.employee_info?.name
    },
    columns: [
        {
            column_title: "Scheduled On",
            column_name: "schedule",
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