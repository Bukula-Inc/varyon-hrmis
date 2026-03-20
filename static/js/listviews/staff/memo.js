import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Memo',
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
            id: "filter-created_on-date",
            fieldname: "created_on",
            fieldtype: "date",
            mode:"single",
            columns: 1,
            placeholder: "Date",
        },
        {
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Memo',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
            filters: {
                "employee": lite.employee_info?.name
                },
        },
     
       
    ],
    default_filters:{
        employee: lite.employee_info?.name
    },
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
            column_title: "To",
            column_name: "to",
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