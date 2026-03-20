import { wipe_all_transactions } from "./functions.js"
export default {
    setup: {
        model: 'Department',
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
            id: "department",
            fieldname: "departmant",
            fieldtype: "link",
            model: 'Department',
            linkfield: "name",
            columns: 1,
            placeholder: "Department Name",
        },
      
    ],
    actions: {
        main: [
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Wipe All Transactions',
            //     icon: 'recycling',
            //     icon_color: 'teal',
            //     show_on_list_check: false
            // },
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Delete this row',
            //     icon: 'recycling',
            //     icon_color: 'red',
            //     show_on_list_check: false,
            //     is_custom_button: true
            // },
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
            column_title: "Company",
            column_name: "company",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Cost Center",
            column_name: "cost_center",
            column_type: "text",
            columns: 1,
        },
    ]
}