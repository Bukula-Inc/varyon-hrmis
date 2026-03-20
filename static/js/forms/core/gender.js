export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
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