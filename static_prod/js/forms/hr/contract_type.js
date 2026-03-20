export default {
    setup: {
        new_form_id: 'new-contact-type',
        info_form_id: 'contact-type-info',
        title: "Contract Type",
        layout_columns: 3,
        model: "Hr_Contract_Type"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Contract Type",
            fieldname: "name",
            fieldtype: "text",
            columns: 3,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "is_short_term",
            fieldlabel: "Is Short Term",
            fieldname: "is_short_term",
            fieldtype: "check",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "is_graduate_applicable",
            fieldlabel: "Is Graduity Applicable",
            fieldname: "is_graduate_applicable",
            fieldtype: "check",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "description",
            fieldlabel: "Contract Type Description",
            fieldname: "description",
            fieldtype: "longtext",
            classnames: "h-[300px]",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },

    ],
}