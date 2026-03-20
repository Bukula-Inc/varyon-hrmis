export default {
    setup: {
        model: "Interview_Feedback",
        new_form_id: 'new-interview-feedback',
        info_form_id: 'interview-feedback-info',
        title: "Interview Feedback",
        layout_columns: 3,
        allow_submit: true,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Interview",
            fieldname: "interview",
            fieldtype: "link",
            model: "Interview",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            description: ""
        },

        {
            id: "interviewer",
            fieldlabel: "Interviewer",
            fieldname: "interviewer",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
            fetchfrom:"interview",
            fetchfield: "interviewer"
        },
       
        {
            id: "result",
            fieldlabel: "Result",
            fieldname: "result",
            fieldtype: "select",
            options: [
                "Cleared ",
                "Rejected",
                

            ],
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
      
        {
            id: "skills",
            fieldlabel: "Skill Assessment",
            fieldname: "skills",
            fieldtype: "table",
            required: false,
            hidden: false,
            
            fields: [
                {
                    id: "skill",
                    fieldlabel: "Skill",
                    fieldname: "skill",
                    fieldtype: "text",
                    columns: 4,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                },
                {
                    id: "rating",
                    fieldlabel: "Rating",
                    fieldname: "rating",
                    fieldtype: "text",
                    columns: 4,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                }, 
            ]
        },

        {
            id: "feedback",
            fieldlabel: "Feedback",
            fieldname: "feedback",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            description: ""
        },

    ]
}
