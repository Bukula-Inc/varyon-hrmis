export default {
    setup: {
        model: "Closed_Ended_Question",
        new_form_id: 'new-appraisal-question-setting',
        info_form_id: 'appraisal-question-setting-info',
        title: "Closed Ended Question",
        layout_columns: 2,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Question",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            description: ""
        },
        {
            id: "sec",
            fieldlabel: "",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            placeholder: " ",
            addborder:true
        },
        {
            id: "include-in-self-rating",
            fieldlabel: "Include In Self Rating",
            fieldname: "include_in_self_rating",
            fieldtype: "check",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            description: ""
        },
        {
            id: "include-in-360",
            fieldlabel: "Include In 360",
            fieldname: "include_in_360",
            fieldtype: "check",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            description: ""
        },
    ]
}