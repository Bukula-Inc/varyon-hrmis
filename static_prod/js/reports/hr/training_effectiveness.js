
export default {
    setup: {
        model: "Training Effectiveness",
        title: "Training Effectiveness Report",
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
            id: "program",
            fieldlabel: "Program",
            fieldname: "program",
            fieldtype: "link",
            model: "Training_Event",
            columns: 1,
            placeholder: "",
        },

    ],
    actions: [
       
       
    ],
    columns: [
        {
            column_title: "Program",
            column_name: "program",
            column_type: "text",
            width: 300,
        },

        {
            column_title: "Relevance",
            column_name: "relevance",
            column_type: "text",
            width: 300,
            
        },
        {
            column_title: "Content",
            column_name: "content",
            column_type: "text",
            width: 300,
            
        },
        {
            column_title: "Delivery",
            column_name: "delivery",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Organization",
            column_name: "origization",
            column_type: "text",
            width: 300,
            
        },
        {
            column_title: "Overall",
            column_name: "overall",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Impact On Work",
            column_name: "impact_on_work",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Participant Recommendation to Others",
            column_name: "recommendation",
            column_type: "text",
            width: 300,
        },
    ]
}