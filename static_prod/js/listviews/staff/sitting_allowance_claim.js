import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Sitting_Allowance',
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
            model: 'Sitting_Allowance',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
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
            column_title: "Claim By",
            column_name: "claim_by",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Meeting Attended",
            column_name: "meeting_name",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Meeting Date",
            column_name: "meeting_date",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Claim Date",
            column_name: "claim_date",
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