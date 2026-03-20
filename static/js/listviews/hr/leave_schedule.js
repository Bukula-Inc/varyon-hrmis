import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Leave_Schedule',
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
            model: 'Leave_Schedule',
            linkfield: "name",
            columns: 1,
            placeholder: "Leave Type",
        },
     
       
    ],
    actions: {
        main: [],
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
            column_title: "Department",
            column_name: "department",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Planner Full Names",
            column_name: "planner_full_names",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Planner Full Names",
            column_name: "planner_full_names",
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