import { wipe_all_transactions } from "../../listviews/core/functions.js"
export default {
    setup: {
        model: 'Industrial Relations Summary',
        title: "Industrial Relations Summary",
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
            column_title: "Disciplinary Committee",
            column_name: "disciplinary_committee",
            column_type: "int",
            width: 200,
        },
        {
            column_title: "Grievances",
            column_name: "period_covered_for_the_assessment",
            column_type: "text",
            width: 200,
            
        },
        {
            column_title: "Resolved Grievances",
            column_name: "resolved_grievances",
            column_type: "int",
            width: 200,
        },
        {
            column_title: "Pending Grievance",
            column_name: "pending_grievances",
            column_type: "int",
            width: 200,
            
        },
        {
            column_title: "Case Out Come",
            column_name: "appraisee_name",
            column_type: "text",
            width: 200,
            
        },     
        {
            column_title: "Charge",
            column_name: "charges",
            column_type: "text",
            width: 200,
            
        },

        {
            column_title: "Resolved Charge",
            column_name: "resolved_charges",
            column_type: "text",
            width: 200,
        },
        {
            column_title: "Pending Charges",
            column_name: "pending_charges",
            column_type: "text",
            width: 200,
        },

        {
            column_title: "Case Out Comes",
            column_name: "case_outcome",
            column_type: "text",
            width: 200,
        },
    ]
}