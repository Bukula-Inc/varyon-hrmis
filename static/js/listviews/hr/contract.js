import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Hr_Contract',
        list_height: 50,
        allow_submit: true,
        allow_cancel: false,
        allow_delete: true,
        allow_export_csv: true,
        allow_export_excel: true,
        allow_print: true
    },
    filters: [
     
        {
            id: "type",
            fieldname: "name",
            fieldtype: "link",
            model: 'Hr_Contract',
            linkfield: "name",
            columns: 1,
            placeholder: "Contract Type",
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
            column_title: "Employee No",
            column_name: "employee",
            column_type: "link",
            columns: 4,
        },
        {
            column_title: "Employee",
            column_name: "full_name",
            column_type: "text",
            columns: 4,
        },
        {
            column_title: "Status",
            column_name: "status",
            column_type: "status",
            columns: 1,
        },
        
    ]
}