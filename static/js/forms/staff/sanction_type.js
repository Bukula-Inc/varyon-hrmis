export default {
    setup: {
        new_form_id: 'new-sanction-type',
        info_form_id: 'sanction-type-info',
        title: "Sanction Type",
        layout_columns: 3,
        model: "Sanction_Type",
        allow_print: false,
        allow_preview: false,
        allow_download: false,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Sanction Type",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "active-period",
            fieldlabel: "Active Period (Months)",
            fieldname: "active_period",
            fieldtype: "float",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "disciplinary-form",
            fieldlabel: "Disciplinary Form",
            fieldname: "disciplinary_nature",
            fieldtype: "select",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
            options:[
                "Educational",
                "Corrective",
                "Punitive"
            ]
        },
        {
            id: "description",
            fieldlabel: "Description",
            fieldname: "description",
            fieldtype: "rich",
            columns:3,
            placeholder: " ",
            required: false,
            hidden: false,
            height: 200
        },
    ],
}