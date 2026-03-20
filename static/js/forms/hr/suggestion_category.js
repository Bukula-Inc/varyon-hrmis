export default {
    setup: {
        new_form_id: 'new-suggestion-category',
        info_form_id: 'suggestion-category-info',
        title: "Suggestion Category",
        layout_columns: 2,
        model: "Suggestion_Category"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Suggestion Category",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        }, 
    ],
}