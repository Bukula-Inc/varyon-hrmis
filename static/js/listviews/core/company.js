import { wipe_all_transactions } from "./functions.js"
export default {
    setup: {
        model: 'Company',
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
            id: "company-name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Company',
            columns: 1,
            placeholder: "Company Name",
        },
        {
            id: "country",
            fieldname: "country",
            fieldtype: "link",
            model: 'Country',
            columns: 1,
            placeholder: "Select Country",
        },
        {
            id: "industry",
            fieldname: "industry",
            fieldtype: "link",
            model: 'Industry',
            columns: 1,
            placeholder: "Industry",
        },

        {
            id: "sector",
            fieldname: "sector",
            fieldtype: "link",
            model: 'Sector',
            columns: 1,
            placeholder: "Select Sector",
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
            //     show_on_list_check: true,
            //     is_custom_button: true,
            //     classnames: 'bg-blue-800 text-white'
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
            // {
            //     fun: wipe_all_transactions,
            //     title: 'Get JSON',
            //     icon: 'code',
            //     icon_color: 'teal',
            // },
        ]
    },
    columns: [
        {
            column_title: "Logo",
            column_name: "company_logo",
            column_type: "image",
            columns: 1,
            sortable: false
        },
        {
            column_title: "Tax ID",
            column_name: "tax_identification_no",
            column_type: "text",
            columns: 1,
            sortable: true
        },
        {
            column_title: "Industry",
            column_name: "industry",
            column_type: "link",
            model: 'Indistry',
            columns: 1,
            sortable: true
        },
        {
            column_title: "Sector",
            column_name: "sector",
            column_type: "link",
            model: 'Sector',
            columns: 1,
            sortable: true
        },
        
    ]
}