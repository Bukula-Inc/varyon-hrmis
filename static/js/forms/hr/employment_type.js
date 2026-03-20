export default {
    setup: {
        new_form_id: 'new-employment-type',
        info_form_id: 'employment-type-info',
        title: "Employment Type",
        layout_columns: 2,
        model: "Employment_Type"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Employment Type",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
      
    ],
}