import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Short Listed Applicants',
        title: "Short Listed Applicants",
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
            id: "name",
            fieldname: "name",
            fieldtype: "link",
            model: 'Short_Listed_Applicants',
            linkfield: "name",
            columns: 1,
            placeholder: "Short List",
        },
        {
            id: "company",
            fieldname: "Company",
            fieldtype: "link",
            model: 'Company',
            linkfield: "name",
            columns: 1,
            placeholder: "Company",
        },
        {
            id: "department",
            fieldname: "department",
            fieldtype: "link",
            model: 'Department',
            placeholder: "Department",
        },
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
            column_title: "Application Date",
            column_name: "application_date",
            column_type: "date",
            width: 200,
        },
        {
            column_title: "Applicant Last Name",
            column_name: "applicant_last_name",
            column_type: "text",
            width: 250,
        },
        {
          column_title: "Applicant Email",
          column_name: "email",
          column_type: "text",
          width: 300,
        },
        {
          column_title: "Position Contact",
          column_name: "contact_no",
          column_type: "text",
          width: 300,
        },
        {
          column_title: "Position Applied For",
          column_name: "position_name",
          column_type: "text",
          width: 300,
        },
        {
          column_title: "Interview Date",
          column_name: "interview_date",
          column_type: "date",
          width: 200,
        },
        {
          column_title: "Interview Status",
          column_name: "interview_status",
          column_type: "text",
          width: 200,
        },
        {
          column_title: "Screening Score",
          column_name: "screening_score",
          column_type: "number",
          width: 150,
        },
        {
          column_title: "Evaluation Score",
          column_name: "evaluation_score",
          column_type: "number",
          width: 150,
        },
        {
          column_title: "Decision Status",
          column_name: "decision_status",
          column_type: "text",
          width: 200,
        },
        {
          column_title: "Remarks",
          column_name: "remarks",
          column_type: "text",
          width: 350,
        },
    ]      
}