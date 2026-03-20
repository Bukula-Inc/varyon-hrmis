export default {
    setup: {
        model: "Appraisal",
        new_form_id: 'new-appraisal-form',
        info_form_id: 'appraisal-form-info',
        title: "Appraisal Form",
        layout_columns: 4,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    fields: [
        {
            id: "appraisal-date",
            fieldlabel: "Appraisal Date",
            fieldname: "appraisal_date",
            fieldtype: "date",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
            
        },
        {
            id: "appraisal-setup",
            fieldlabel: "Appraisal Setup",
            fieldname: "appraisal_setup",
            fieldtype: "link",
            model: "Appraisal_Setup",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
            description: ""
        },
        {
            id: "appraisee",
            fieldlabel: "Appraisee",
            fieldname: "appraisee",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            description: ""
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
            id: "appraiser",
            fieldlabel: "Appraiser",
            fieldname: "appraiser",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            description: ""
        },

        {
            id: "appraiser-name",
            fieldlabel: "Appraiser Name",
            fieldname: "appraiser_name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            fetchfrom:"appraiser",
            fetchfield: "full_name"
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
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "total-open-score",
            fieldlabel: "Total Score (Open Ended)",
            fieldname: "total_open_score",
            fieldtype: "float",
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