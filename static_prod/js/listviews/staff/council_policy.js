import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Company_Policy',
        list_height: 50,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
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
            id: "company-policies",
            fieldname: "name",
            fieldtype: "link",
            model: 'Company_Policies',
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
          
        ]
    },
    columns: [
        // {
        //     column_title: "Full Name",
        //     column_name: "name",
        //     column_type: "text",
        //     columns: 1,
        // },
        {
            column_title: "Effective On",
            column_name: "effective_on",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Purpose of Policy",
            column_name: "purpose_of_policy",
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