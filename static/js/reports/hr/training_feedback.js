import { wipe_all_transactions } from "../../listviews/core/functions.js"

export default {
    setup: {
        model: 'Training Feedback Report',
        title: "Training Feedback Report",
        report_type: "script",
        include_opening: true,
        include_closing: true,
        allow_print: true,
        allow_download_csv: true,
        allow_download_excel: true,
        allow_download_pdf: true
    },
    filters: [],
    actions: [],
    columns: [
        {
            column_title: "Training Event",
            column_name: "training_event",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Employee",
            column_name: "employee",
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
            column_name: "organization",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Total Score",
            column_name: "total_score",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Overall Percentage Score",
            column_name: "overall_percentage_score",
            column_type: "text",
            width: 300,
        },
    ]
}