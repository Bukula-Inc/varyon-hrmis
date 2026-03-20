export default {
    setup: {
        model: "Appraisal_Question_Option",
        new_form_id: 'new-appraisal-question-setting',
        info_form_id: 'appraisal-question-setting-info',
        title: "Closed Ended Question",
        layout_columns: 2,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Option",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            description: ""
        },
        {
            id: "rate",
            fieldlabel: "Rate",
            fieldname: "rate",
            fieldtype: "float",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            description: ""
        },
       
    ]
}