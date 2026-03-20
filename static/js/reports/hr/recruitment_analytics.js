import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Recruitment Analytics',
        title: "Recruitment Analytics",
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
            model: 'Company',
            linkfield: "",
            columns: 1,
            placeholder: "Company",
        },
        {
            id: "date",
            fieldname: "date",
            fieldtype: "date",
            model: '',
            placeholder: "Date",
        },
      
      
    ],
    actions: [
       
      
    ],
    columns: [
        {
            column_title: "Job Advertisement",
            column_name: "job_advertisement",
            column_type: "text",
            width: 350,            
        },
        {
            column_title: "Job Application",
            column_name: "job_application",
            column_type: "text",
            width: 350,            
        },
        // {
        //     column_title: "Application ID",
        //     column_name: "application_id",
        //     column_type: "text",
        //     width: 350,
                
        // },
        {
            column_title: "Shortlisted",
            column_name: "shortlisted",
            column_type: "int",
            width: 350,                
        },
        {
            column_title: "Interviewed",
            column_name: "interviewed",
            column_type: "int",
            width: 350,
                
        },
        {
            column_title: "Offered",
            column_name: "offered",
            column_type: "text",
            width: 350,
           
            
            
        },
        // {
        //     column_title: "Job Title",
        //     column_name: "designation",
        //     column_type: "text",
        //     width: 370,
           
            
            
        // },
        // {
        //     column_title: "Council",
        //     column_name: "company",
        //     column_type: "text",
        //     width: 370,
        // },
     

    
     
    ]
}