
export default {
    setup: {
        new_form_id: 'new-license',
        info_form_id: 'license-info',
        title: "License",
        layout_columns: 2,
        model: "License"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "License Name",
            fieldname: "name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: "Enter License Name",
            required: true,
            hidden: false,
            default:"License"
        },
        {
            id: "license-content",
            fieldlabel: "License Content",
            fieldname: "content",
            fieldtype: "rich",
            columns: 2,
            placeholder: "License Content",
            required: false,
            hidden: false,
            height:500
        },
    ]
}