import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Project_Task',
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
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Project_Task',
            columns: 1,
            placeholder: "Select Task",
        },
        {
            id: "project",
            fieldname: "project",
            fieldtype: "link",
            model: 'Project',
            columns: 1,
            placeholder: "Select Project",
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
        individual: lite.user?.name
    },
    columns: [
        {
            column_title: "Project",
            column_name: "project",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Task Stating Date",
            column_name: "start_date",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Task Due Date",
            column_name: "end_date",
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