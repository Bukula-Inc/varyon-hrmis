import { wipe_all_transactions } from "../core/functions.js"
export default {
    setup: {
        model: 'Employee_Grievance',
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
            id: "subject",
            fieldname: "Grievance Subject",
            fieldtype: "link",
            model: 'Employee_Grievance',
            linkfield: "name",
            columns: 1,
            placeholder: "Select Grievance Subject",
            filters:{
                "raised_by": lite.employee_info?.name
            }
        },

        {
            id: "grievanc_type",
            fieldname: "Grievance Type",
            fieldtype: "link",
            model: 'Grievance_Type',
            linkfield: "name",
            columns: 1,
            placeholder: "Grievance Type",
            filters:{
                "raised_by": lite.employee_info?.name
            }
        },
      
    ],
    default_filters:{
        raised_by: lite.employee_info?.name
    },
    actions: {
        main: [
            
        ],
        row: [
       
        ]
    },
    columns: [
        {
            column_title: "Grievance Subject",
            column_name: "name",
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