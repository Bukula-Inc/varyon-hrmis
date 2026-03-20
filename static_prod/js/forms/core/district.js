export default {
    setup: {
        new_form_id: 'new-district',
        info_form_id: 'district-info',
        title: "District",
        layout_columns: 2,
        model: "District"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "District Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter District Name",
            required: true,
            hidden: false,
            description: "District Name",
        },
    ],
}