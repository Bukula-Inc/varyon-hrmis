export default {
    setup: {
        model: 'Interview Score Sheet',
        title: "Interview Score Sheet",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true,
        is_grid_layout : true,
    },
    filters: [
     
        {
            id: "name",
            fieldname: "applicant",
            fieldtype: "link",
            // model: 'Employee',
            linkfield: "applicant",
            width: 1,
            placeholder: "Candidate Name",
        },
        // {
        //     id: "designation",
        //     fieldname: "designation",
        //     fieldtype: "link",
        //     model: 'Designation',
        //     placeholder: "Designation",
        // },      
        {
            id: "job-advertisement",
            fieldname: "job_advertisement",
            fieldtype: "link",
            model: 'Job_Advertisement',
            placeholder: "Job Advertisement",
        },    
        // {
        //     id: "job-advertisement",
        //     fieldname: "Job Advertisement",
        //     fieldtype: "link",
        //     model: 'Job_Advertisement',
        //     placeholder: "Job Advertisement",
        // },      
    ],
    actions: [],
    columns: [
        {
            column_title: "Name of Candidate",
            column_name: "applicant",
            column_type: "text",
            column: 4,
            // classname: "text-left"
        },
        {
            column_title: "Average Score",
            column_name: "average_score",
            column_type: "float",
            column: 4,
        },
        {
            column_title: "Percentage Score",
            column_name: "percentage_score",
            column_type: "text",
            column: 4,
            classnames: "text-right"
        },
        {
            column_title: "Comments",
            column_name: "comments",
            column_type: "longtext",
            column: 6,
            classnames: "text-right"
        },
    ]
}