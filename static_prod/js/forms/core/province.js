export default {
    setup: {
        new_form_id: 'new-province',
        info_form_id: 'province-info',
        title: "Province",
        layout_columns: 2,
        model: "Province"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Province Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Province Name",
            required: true,
            hidden: false,
            description: "Province Name",
        },
    ],
}