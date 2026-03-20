import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Form_Of_Agreement_For_A_Personal_Loan',
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
            fieldname: "Name",
            fieldtype: "link",
            model: 'Personal_Loan_Agreement',
            linkfield: "name",
            columns: 1,
            placeholder: "Personal loan agreement",
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
            column_title: "Status",
            column_name: "status",
            column_type: "text",
            columns: 1,
        },
    ]
}