export default {
    setup: {
        model: "Interview_Round",
        new_form_id: 'new-interview-round',
        info_form_id: 'interview-round-info',
        title: "Interview Round",
        layout_columns: 3,
        
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Round Name",
            fieldname: "name",
            fieldtype: "text",
            model: "",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            description: ""
        },
     
        {
            id: "interview-type",
            fieldlabel: "Interview Type",
            fieldname: "interview_type",
            fieldtype: "link",
            model: "Interview_Type",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            
        },
        {
            id: "interviewers",
            fieldlabel: "Interviewers",
            fieldname: "interviewers",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            filters: {
                status: "Active",
            }, 
            
        },

        {
            id: "designation",
            fieldlabel: "Job Title",
            fieldname: "designation",
            fieldtype: "link",
            model: "Designation",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            
        },
     
        {
            id: "skillset",
            fieldlabel: "Expected Skillset",
            fieldname: "skillset",
            fieldtype: "table",
            model: "",
            required: false,
            hidden: false,
            
            fields: [
                {
                    id: "skill",
                    fieldlabel: "Skill",
                    fieldname: "skill",
                    fieldtype: "text",
                    model: "",
                    columns: 4,
                    placeholder: " ",
                    required: true,
                    hidden: false,
                    istablefield: true,
                },
                {
                    id: "description",
                    fieldlabel: "Description",
                    fieldname: "description",
                    fieldtype: "text",
                    columns: 4,
                    placeholder: " ",
                    required: false,
                    hidden: false,
                    istablefield: true,
                },
                
            ]
        },

    ]
}