
export default {
    setup: {
        model: "Appraisal Report",
        title: "Appraisal Report",
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
            id: "appraisee",
            fieldlabel: "Appraisee",
            fieldname: "appraisee",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: "",
        },

    ],
    actions: [
       
       
    ],
    columns: [
        {
            column_title: "Appraisal Date",
            column_name: "appraisal_date",
            column_type: "text",
            width: 200,
        },

        {
            column_title: "Appraisal Quarter",
            column_name: "appraisal_quarter",
            column_type: "text",
            width: 200,
            
        },
        {
            column_title: "Appraiser",
            column_name: "appraiser_name",
            column_type: "text",
            width: 200,
            
        },
        {
            column_title: "Appraisee",
            column_name: "appraisee_name",
            column_type: "text",
            width: 200,
        },
        {
            column_title: "Department",
            column_name: "department",
            column_type: "text",
            width: 200,
            
        },
        {
            column_title: "Total Open Ended Questions",
            column_name: "total_open_ended_questions",
            column_type: "text",
            width: 200,
        },
        {
            column_title: "Total closed Ended Questions",
            column_name: "total_closed_ended_questions",
            column_type: "text",
            width: 200,
        },

        {
            column_title: "Total Score (Open Ended)",
            column_name: "total_open_score",
            column_type: "text",
            width: 200,
        },
        {
            column_title: "Total Score (Closed Ended)",
            column_name: "total_closed_score",
            column_type: "text",
            width: 200,
        },
        {
            column_title: "Total Overall Score",
            column_name: "overall_score",
            column_type: "text",
            width: 200,
        },
    ]
}