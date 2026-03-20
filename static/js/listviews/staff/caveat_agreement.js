import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Caveat_Agreement',
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
            id: "name-filter",
            fieldname: "name",
            fieldtype: "link",
            model: 'Caveat_Agreement',
            linkfield: "name",
            columns: 1,
            placeholder: "Caveat Agreement",
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
        owner: lite.user.name
    },
    columns: [   
        {
            column_title: "Name of First Part",
            column_name: "first_party",
            column_type: "text",
            columns: 1,
        }, 
        {
            column_title: "Address of Constraction Site",
            column_name: "constraction_site_address",
            column_type: "text",
            columns: 1,
        }, 
        {
            column_title: "Loan Amount",
            column_name: "in_house_loan",
            column_type: "text",
            columns: 1,
        }, 
    ]
}