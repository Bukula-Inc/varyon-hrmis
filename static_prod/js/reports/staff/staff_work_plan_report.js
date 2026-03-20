import { wipe_all_transactions } from "../../listviews/core/functions.js"

export default {
    setup: {
        model: 'staff_work_plan_report',
        title: "Staff Work Plan Report",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: false,
        allow_download_csv: false,
        allow_download_excel: false,
        allow_download_pdf: false
    },
    filters: [
        // {
        //     id: "department",
        //     fieldname: "department",
        //     fieldtype: "link",
        //     model: 'Department',
        //     placeholder: "Select Department",
        // },
        // {
        //     id: "designation",
        //     fieldname: "designation",
        //     fieldtype: "link",
        //     model: 'Designation',
        //     placeholder: "Select Designation",
        // },
        // {
        //     id: "reports-to",
        //     fieldname: "reports_to",
        //     fieldtype: "link",
        //     model: 'Employee',
        //     columns: 1,
        //     placeholder: "Reports To",
        // },
    ],
  
    actions: [],
    columns: [
        {
                    column_title: "Expected Start Date",
                    column_name: "expected_start_date",
                    column_type: "text",
                    width: 300,
            },  
            {
                column_title: "Expected End Date",
                column_name: "expected_end_date",
                column_type: "text",
                width: 300,
            },
        
            {
                column_title: "Name",
                column_name: "name",
                column_type: "text",
                width: 300,
            },
            {
                column_title: "Period",
                column_name: "period",
                column_type: "text",
                width: 300,
            },
            {
                column_title: "Task Name",
                column_name: "title",
                column_type: "text",
                width: 300,
            },
            {
                column_title: "Outcome",
                column_name: "out_come",
                column_type: "text",
                width: 300,
            },
 
          {
            column_title: "Task Status",
            column_name: "progress_tracker",
            column_type: "text",
            width: 300,
          },
    ]
}