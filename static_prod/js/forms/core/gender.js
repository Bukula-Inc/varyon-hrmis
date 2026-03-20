export default {
    setup: {
        new_form_id: 'new-gender',
        info_form_id: 'gender-info',
        title: "Gender",
        layout_columns: 2,
        model: "Gender"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Gender Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Gender Name",
            required: true,
            hidden: false,
            description: "Gender Name",
        },
    ],
}