import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Staff_Performance',
        title: "Staff Performance",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
        {
            id: "filter-leave-type",
            fieldname: "name",
            fieldtype: "link",
            model: "Leave_Type",
            placeholder: "Select Leave Type",
        },
    ],
    actions: [
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],

    columns: [
        {
            column_title: "Leave Type",
            column_name: "leave_type",
            width: 170,
        },
        {
            column_title: "Total Leave Days",
            column_name: "total_leave _days",
            width: 170,
        },
    ]
}