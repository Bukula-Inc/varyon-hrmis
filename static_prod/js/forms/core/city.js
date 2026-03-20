export default {
    setup: {
        new_form_id: 'new-city',
        info_form_id: 'city-info',
        title: "City",
        layout_columns: 2,
        model: "City"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "City Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter City Name",
            required: true,
            hidden: false,
            description: "City Name",
        },
    ],
}