import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Overtime Report',
        title: "Overtime Report",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
         {
            id: "filter-start-time",
            fieldname: "start_time",
            fieldtype: "link",
            model: "Overtime",
            linkfield: "start_time",
            placeholder: "Select Start Time",
        },
        {
            id: "filter-end-time",
            fieldname: "end_time",
            fieldtype: "link",
            model: "Overtime",
            linkfield: "end_time",
            placeholder: "Select End Time",
        },
        {
            id: "filter-applicant",
            column_title: "Applicant",
            fieldname: "applicant",
            fieldtype: "link",
            model: "Employee",
            placeholder: "Enter Applicant",
        },
        {
            id: "filter-name",
            column_title: "Name",
            fieldname: "name",
            fieldtype: "link",
            model: "Overtime",
            placeholder: "Select Name",
        },   {
            id: "filter-Status",
            column_title: "Status",
            fieldname: "status",
            fieldtype: "link",
            model: "Doc_Status",
            placeholder: "Select Status",
        }
  
    ],
    actions: [
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],

    columns: [
        {
            column_title: "Applicant",
            column_name: "applicant",
            width: 170,
        },
        {
            column_title: "Name",
            column_name: "name",
            width: 170,
        },
        {
            column_title: "Date",
            column_name: "date",
            width: 170,
        },
        {
            column_title: "Start Time",
            column_name: "start_time",
            width: 170,
        },
        {
            column_title: "End Time",
            column_name: "end_time",
            width: 170,
        },
        {
            column_title: "Total Earning",
            column_name: "total_earning",
            width: 170,
            is_figure: true,
        },
        {
            column_title: "Status",
            column_name: "status",
            width: 170,
        },
        // {
        //     column_title: "Total Overtime Applications",
        //     column_name: "overtime_application",
        //     width: 170,
        // },
        {
            column_title: "Total Approved Overtimes",
            column_name: "approved_overtimes",
            width: 170,
        },
        {
            column_title: "Total Pending Overtimes",
            column_name: "pending_overtimes",
            width: 170,
        },
        {
            column_title: "Total Rejected Overtimes",
            column_name: "rejected_overtimes",
            width: 170,
        },
    ]
}