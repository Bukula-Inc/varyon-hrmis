export default {
    setup: {
        new_form_id: 'new-state',
        info_form_id: 'state-info',
        title: "State",
        layout_columns: 2,
        model: "State"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "State Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter State Name",
            required: true,
            hidden: false,
            description: "State Name",
        },
    ],
}