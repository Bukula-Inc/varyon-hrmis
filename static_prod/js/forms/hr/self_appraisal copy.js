export default {
    setup: {
        model: "Self_Appraisal",
        new_form_id: 'new-selfappraisal',
        info_form_id: 'self-appraisal-info',
        title: "Self Appraisal",
        layout_columns: 4,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    fields: [
        {
            id: "company",
            fieldlabel: "Council",
            fieldname: "company",
            fieldtype: "read-only",
            model: "Company",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            default: lite.user.company.name,
        },
        {
            id: "appraisal-setup",
            fieldlabel: "Appraisal Setup",
            fieldname: "appraisal_setup",
            fieldtype: "read-only",
            model: "Appraisal_Setup",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            
            default: lite.user.company.name,
        },
    
        {
            id: "appraisee",
            fieldlabel: "Appraisee wertyuiop",
            fieldname: "appraisee",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            
            filters: {
                status: "Active",
            }, 
        },
        {
            id: "appraisee-name",
            fieldlabel: "Appraisee Name",
            fieldname: "appraisee_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"appraisee",
            fetchfield: "full_name"
        },

        {
            id: "appraisal-closure-date",
            fieldlabel: "Appraisal Closure Date",
            fieldname: "appraisal_closure_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
            value: lite.utils.today()
            
        },
        {
            id: "department",
            fieldlabel: "Department /  Unit",
            fieldname: "department",
            fieldtype: "read-only",
            model: "Department",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"appraisee",
            fetchfield: "department"
        },
     
        {
            id: "appraisal-quarter",
            fieldlabel: "Appraisal Quarter",
            fieldname: "appraisal_quarter",
            fieldtype: "link",
            model: "Appraisal_Quarter",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            
        },
        {
            id: "total-open-score",
            fieldlabel: "Total Score (Open Ended)",
            fieldname: "total_open_score",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default:"0"
        },
        {
            id: "total-closed-score",
            fieldlabel: "Total Score (Closed Ended)",
            fieldname: "total_closed_score",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default:"0"
        },
        {
            id: "sec",
            fieldlabel: "Totals",
            fieldname: "ts",
            fieldtype: "section-break",
            columns: 1,
            required: true,
            hidden: false,
            
            addborder:true
        },
        {
            id: "total-questions",
            fieldlabel: "Total Questions",
            fieldname: "total_questions",
            fieldtype: "read-only",
            columns: 1,
            required: false,
            hidden:false,
            
            default:"0",
            is_figure:true
        },
        {
            id: "total-open-ended-questions",
            fieldlabel: "Total Open Ended Questions",
            fieldname: "total_open_ended_questions",
            fieldtype: "read-only",
            columns: 1,
            required: false,
            hidden:false,
            
            default:"0",
            is_figure:true
        },
        {
            id: "total-closed-ended-questions",
            fieldlabel: "Total closed Ended Questions",
            fieldname: "total_closed_ended_questions",
            fieldtype: "read-only",
            columns: 1,
            required: false,
            hidden:false,
            
            default:"0",
            is_figure:true
        },
        {
            id: "overall-score",
            fieldlabel: "Total Overall Score",
            fieldname: "overall_score",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            default:"0.0"
        },
    ]
}