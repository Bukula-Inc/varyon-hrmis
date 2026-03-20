export default {
    setup: {
        new_form_id: 'new-violation-type',
        info_form_id: 'violation-type-info',
        title: "Violation Type",
        layout_columns: 2,
        model: "Violation_Type"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Violation Type",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },    
    ],
}