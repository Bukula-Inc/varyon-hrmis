export default {
    setup: {
        new_form_id: 'new-appraisal-type',
        info_form_id: 'appraisal-type-info',
        title: "Appraisal Type",
        layout_columns: 2,
        model: "Appraisal_Type"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Appraisal Type",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
    ],
}