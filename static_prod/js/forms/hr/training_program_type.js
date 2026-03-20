export default {
    setup: {
        model: "Training_Program_Type",
        new_form_id: 'new-training-program-type',
        info_form_id: 'training-program-type-info',
        title: "Training Program Type",
        layout_columns: 4,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: false,
    },

    fields: [
        {
            id: "name",
            fieldlabel: "Training Program Type",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            description: ""
        },
        {
            id: "description",
            fieldlabel: "Job Title",
            fieldname: "description",
            fieldtype: "rich",
            columns: 4,
            placeholder: " ",
            required: false,
            hidden: false,
            height: 300,
            
        },
    ]
}
