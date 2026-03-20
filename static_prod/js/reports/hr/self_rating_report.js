import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Self Appraisal Report',
        title: " Self Appraisal Report",
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
            column_title: "Appraisal Date",
            column_name: "appraisal_date",
            column_type: "text",
            width: 200,
        },
        {
            column_title: "Assessment Period",
            column_name: "period_covered_for_the_assessment",
            column_type: "text",
            width: 200,
            
        },
        {
            column_title: "Salary Grade",
            column_name: "salary_grade",
            column_type: "text",
            width: 200,
            
        },
        {
            column_title: "Rated",
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
            column_title: "Purpose",
            column_name: "purpose_of_the_assessment",
            column_type: "text",
            width: 200,
        },
        {
            column_title: "Behavioral Imperatives Score",
            column_name: "behavioral_imperatives_score",
            column_type: "text",
            width: 200,
        },

        {
            column_title: "Performance Objective Score",
            column_name: "performance_objective_score",
            column_type: "text",
            width: 200,
        },
        {
            column_title: "NO. Performance KPI",
            column_name: "performance_kpi_qty",
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