import { wipe_all_transactions } from "../../listviews/core/functions.js"

export default {
    setup: {
        model: 'ECZ Imprest Report',
        title: "Imprest Report",
        report_type: "script",
        is_grid_layout: true,
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Select Department",
        },
        {
            id: "designation",
            fieldname: "designation",
            fieldtype: "link",
            model: 'Designation',
            placeholder: "Select Designation",
        },
        {
            id: "reports-to",
            fieldname: "reports_to",
            fieldtype: "link",
            model: 'Employee',
            columns: 1,
            placeholder: "Reports To",
        },
    ],
  
    actions: [],
    columns:
        [
            {
                column_title: "Imprest ID",
                column_name: "imprest_id",
                column_type: "text",
                columns: 1,
            },    
            {
                column_title: "Initiator",
                column_name: "initiator",
                column_type: "text",
                columns: 1,
            },
            {
                column_title: "Date of Retirement",
                column_name: "duration_from_date",
                column_type: "date",
                columns: 1,
            }, 
            // {
            //     column_title: "Mode of Travel",
            //     column_name: "mode_of_travel",
            //     column_type: "text",
            //     columns: 1,
            // }, 
            {
                column_title: "Purpose",
                column_name: "purpose",
                column_type: "text",
                columns: 1,
            }, 
            {
                column_title: "Requested Amount",
                column_name: "requested_amount",
                column_type: "float",
                columns: 1,
            }, 
            {
                column_title: "Approved Amount",
                column_name: "approved_amount",
                column_type: "float",
                columns: 1,
            }, 
            {
                column_title: "Retired Amount",
                column_name: "retired_amount",
                column_type: "float",
                columns: 1,
            }, 
            {
                column_title: "Balance",
                column_name: "balance",
                column_type: "float",
                columns: 1,
            }, 
            {
                column_title: "Status of Retirement",
                column_name: "",
                column_type: "text",
                columns: 1,
            }, 
        ]
}