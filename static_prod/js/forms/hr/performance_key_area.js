export default {
    setup: {
        new_form_id: 'new-pka',
        info_form_id: 'pka-info',
        title: "Performance Key Area",
        layout_columns: 3,
        allow_submit: false,
        allow_cancel: true,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: true,
        model: "Performance_Key_Area"
    },
    form_actions: [],
    fields: [
        {
            id: "name",
            fieldlabel: "Key Performance Area",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "area_type",
            fieldlabel: "Performance Area Type",
            fieldname: "area_type",
            fieldtype: "select",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            options: ["Strategic Goal", "Thematic Area"]
        },
        {
            id: "description",
            fieldlabel: "Description",
            fieldname: "description",
            fieldtype: "rich",
            height:340,
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },
    ],
}