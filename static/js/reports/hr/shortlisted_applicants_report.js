import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Short Listed Applicants',
        title: "Short Listed Applicants",
        report_type: "script",
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true,
        is_grid_layout : false,
    },
    // setup: {
    //     model: 'Short Listed Applicants',
    //     title: "Short Listed Applicants",
    //     report_type: "script",
    //     include_opening: true,
    //     include_closing: true,
    //     allow_print: true,
    //     allow_download_csv: true,
    //     allow_download_excel: true,
    //     allow_download_pdf: true,
    //     is_grid_layout : true,
    // },
    filters: [
        {
            id: "job-advertisement-filter",
            fieldname: "job_advertisement",
            fieldtype: "link",
            model: 'Job_Advertisement',
            placeholder: "Job Advertisement",
        },
        {
            id: "job_position-filter",
            fieldname: "job_position",
            fieldtype: "link",
            model: 'Designation',
            placeholder: "Job Title",
        },
     
        // {
        //     id: "name",
        //     fieldname: "name",
        //     fieldtype: "link",
        //     model: 'Short_Listed_Applicants',
        //     linkfield: "name",
        //     columns: 1,
        //     placeholder: "Short List",
        // },
    ],
    actions: [
       
        {
            fun: wipe_all_transactions,
            title: 'Get JSON',
            icon: 'code',
            icon_color: 'orange',
        },
    ],
    columns: [
        {
            column_title: "Job Advertisement",
            column_name: "job_advertisement",
            column_type: "link",
            model: "Job_Advertisement",
            // column: 6,
            width: 300,
        },
        {
            column_title: "Job Title",
            column_name: "job_position",
            column_type: "text",
            // column: 6,
            width: 300,
        },
        {
            column_title: "Date of Application",
            column_name: "date_of_application",
            column_type: "date",
            // column: 6,
            width: 300,
        },
        {
            column_title: "Applicant",
            column_name: "applicant",
            column_type: "text",
            // column: 6,
            width: 300,
        },
        {
            column_title: "Applicant Email",
            column_name: "applicant_email",
            column_type: "text",
            // column: 6,
            width: 300,
        },
        {
            column_title: "Applicant Mobile No",
            column_name: "applicant_mobile_no",
            column_type: "text",
            // column: 6,
            width: 300,
        },
    ]      
}