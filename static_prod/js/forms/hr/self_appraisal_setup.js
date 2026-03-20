export default {
    setup: {
        model: "Self_Appraisal_Setup",
        new_form_id: 'new-self-appraisal-setup',
        info_form_id: 'self-appraisal-setup-info',
        title: "Self Appraisals",
        layout_columns: 3,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    fields: [
     
        {
            id: "appraisaw-quarter",
            fieldlabel: "Appraiser Quarter",
            fieldname: "appraisal_quarter",
            fieldtype: "link",
            model: "Appraisal_Quarter",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
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
            description: "Select Appraisal Closure Date",
            value: lite.utils.today()
            
        },
       
        {
            id: "sec",
            fieldlabel: "",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "include",
            fieldlabel: "Include Closed Ended Questions",
            fieldname: "include_closed_ended_questions",
            fieldtype: "check",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "include",
            fieldlabel: "Include Open Ended Questions",
            fieldname: "include_open_ended_questions",
            fieldtype: "check",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "appraisees",
            fieldlabel: "Appraisees",
            fieldname: "appraisees",
            fieldtype: "table",
            model: "Appraisal_Appraisee",
            required: true,
            hidden: false,
            
            fields: [
                {
                    id: "appraisee",
                    fieldlabel: "Appraisee",
                    fieldname: "appraisee",
                    fieldtype: "link",
                    model: "Employee",
                    columns: 9,
                    placeholder: " ",
                    required: true,
                    hidden: false,
                    istablefield: true,
                    filters: {
                        status: "Active",
                    }, 
                },
                {
                    id: "appraisee-name",
                    fieldlabel: "Appraisee Name",
                    fieldname: "appraisee_name",
                    fieldtype: "read-only",
                    columns: 9,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    fetchfrom:"appraisee",
                    fetchfield: "full_name",
                    istablefield: true,
                },
                {
                    id: "appraisee-department",
                    fieldlabel: "Appraisee Department",
                    fieldname: "appraisee_department",
                    fieldtype: "read-only",
                    columns: 9,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    fetchfrom:"appraisee",
                    fetchfield: "department",
                    istablefield: true,
                },
                
            ]
        },

    ]
}