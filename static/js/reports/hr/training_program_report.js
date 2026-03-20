import { wipe_all_transactions } from "../../listviews/core/functions.js"

export default {
    setup: {
        model: 'Training_Program_Report',
        title: "Training Program Report",
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
            column_title: "Training Program",
            column_name: "training_program",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Trainer",
            column_name: "trainer",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Participants",
            column_name: "participants",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Duration",
            column_name: "duration",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Training Methodology",
            column_name: "training_methodology",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Key Takeaways",
            column_name: "key_takeaways",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Overall Score",
            column_name: "overall_score",
            column_type: "text",
            width: 300,
        },
        {
            column_title: "Satisfaction Percentage",
            column_name: "satisfaction_percentage",
            column_type: "text",
            width: 300,
        },
    ]
}
