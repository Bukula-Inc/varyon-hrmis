import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Staff_Requisition',
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
            model: 'Staff_Requisition',
            linkfield: "name",
            columns: 1,
            placeholder: "Staff Requisition",
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
            column_title: "Job Title",
            column_name: "requisitioners_job_title",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Department",
            column_name: "staffing_department",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            columns: 4,
        },
        
    ]
}