import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Job_Advertisement',
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
            fieldname: "name",
            fieldtype: "link",
            model: 'Staffing_Plan',
            linkfield: "name",
            columns: 1,
            placeholder: "ID",
        },

        {
            id: "status",
            fieldname: "status",
            fieldtype: "select",
            options: [
                "",
                "open",
                "closed",
            ],
            columns: 1,
            placeholder: "Status",
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
        designation: lite.employee_info?.designation
    },
    columns: [
        
        {
            column_title: "Department",
            column_name: "department",
            column_type: "text",
            columns: 1,
        },
        {
            column_title: "Vacancies",
            column_name: "vacancies",
            column_type: "text",
            columns: 1,
        },
        
      
        
    ]
}