import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: "Monthly_Attendance",
        title: "Monthly_Attendance",
        report_type: "script",
        is_grid_layout: true,
        include_opening: false,
        include_closing: false,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [
        {
            id: "filter-date",
            fieldname: "posting_date",
            fieldtype: "date",
            placeholder: "Select Dates",
        },
        {
            id: "filter-employee-id",
            fieldname: "employee_id",
            fieldtype: "link",
            model: 'Employee',
            placeholder: "Select Employee ID",
        },
        // {
        //     id: "cost-center",
        //     fieldname: "cost-center",
        //     fieldtype: "link",
        //     model: 'Cost_Center',
        //     placeholder: "Select Cost Center",
        // },
    ],
    selectors: [],
    actions: [
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
        // {
        //     fun: wipe_all_transactions,
        //     title: 'Test Button',
        //     icon: 'code',
        //     background_color: 'teal',
        //     color: 'white',
        //     is_action_button: true
        // },
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],

    columns: [
        {
            column_title: "Date",
            column_name: "posting_date",
            column_type: "date",
            columns: 6,
            classname: "fonb-semibold"
        },

        {
            column_title: "Employee ID",
            column_name: "employee_id",
            column_type: "text",
            columns: 6,
            sortable: true
        },
        {
            column_title: "Employee's Full Name",
            column_name: "employee_full_name",
            column_type: "text",
            columns: 6,
        },
        {
            column_title: "Day",
            column_name: "day",
            column_type: "text",
            columns: 6,
        },
        {
            column_title: "Time In",
            column_name: "time_in",
            column_type: "text",
            columns: 6,
            classname: "text-start"
        },
        {
            column_title: "Time Out",
            column_name: "time_out",
            column_type: "text",
            columns: 6,
        },
    ]
}