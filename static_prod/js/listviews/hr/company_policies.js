import { wipe_all_transactions } from "../core/functions.js"

export default {
    setup: {
        model: 'Company_Policy',
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
            id: "company-policies",
            fieldname: "name",
            fieldtype: "link",
            model: 'Company_Policies',
            linkfield: "name",
            columns: 1,
            placeholder: "Company Policy",
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
        //  {
        //      column_title: "Full Name",
        //      column_name: "name",
        //      column_type: "text",
        //      columns: 1,
        //  },
        //  {
        //      column_title: "Effective On",
        //      column_name: "effective_on",
        //      column_type: "text",
        //      columns: 1,
        //  },
         {
             column_title: "Status",
             column_name: "status",
             column_type: "status",
             columns: 1,
         },
        
        
    ]
}