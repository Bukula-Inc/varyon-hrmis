export default {
    setup: {
        model: "Appraisal_Quarter",
        new_form_id: 'new-appraisalquarter',
        info_form_id: 'appraisal-quarter-info',
        title: "Appraisal Quarter",
        layout_columns: 2,
    },
    fields: [
        {
            id: "appraisal-quarter-name",
            fieldlabel: "Appraisal Quarter Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            description: "Enter Quarter Name"
        },
    ]
}