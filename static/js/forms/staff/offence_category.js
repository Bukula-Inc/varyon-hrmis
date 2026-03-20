export default {
    setup: {
        new_form_id: 'new-offence-category',
        info_form_id: 'offence-category-info',
        title: "Offence Category",
        layout_columns: 3,
        model: "Offence_Category",
        allow_print: false,
        allow_preview: false,
        allow_download: false,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Category",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
            default: "Category I"
        },
        {
            id: "title",
            fieldlabel: "Title",
            fieldname: "title",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "description",
            fieldlabel: "Description",
            fieldname: "description",
            fieldtype: "rich",
            columns: 3,
            placeholder: " ",
            required: true,
            hidden: false,
            height: 200
        },
    ],
}