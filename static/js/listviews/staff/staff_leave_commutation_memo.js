import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Leave_Commutation_Memo',
        list_height: 50,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: false,
        allow_export_excel: false,
        allow_print: false
    },
    default_filters: [
        {

        }
    ],
    filters: [
        {
            id: "leave-type",
            fieldname: "leave_type",
            fieldtype: "link",
            model: 'Leave_Type',
            filters: {
                is_commutable: 1,
            },
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
            column_title: "Employee Name",
            column_name: "employee_name",
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