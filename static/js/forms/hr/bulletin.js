export default {
    setup: {
        new_form_id: 'new-bulletin',
        info_form_id: 'bulletin-info',
        title: "Bulletin",
        layout_columns: 3,
        model: "Bulletin"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Bulletin Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "attachment",
            fieldlabel: "Attachment",
            fieldname: "attachment",
            fieldtype: "file",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "bulletin-id",
            fieldlabel: "",
            fieldname: "si",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            required: false,
            hidden: false,
        },

        {
            id: "bulletin-context",
            fieldlabel: "Bulletin Context",
            fieldname: "bulletin_context",
            fieldtype: "rich",
            height: 300,
            columns: 3,
            placeholder: " ",
            required: true,
            hidden: false,
        },
    ],
}