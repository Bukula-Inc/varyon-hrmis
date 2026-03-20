export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
        title: "Workflow",
        layout_columns: 2,
        model: "Workflow_Action"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Workflow Action Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Select Workflow Action Name",
            required: true,
            hidden: false,
        },
        {
            id: "color",
            fieldlabel: "Color",
            fieldname: "color",
            fieldtype: "color",
            columns: 1,
            placeholder: "Select Color (Optional)",
            required: false,
            hidden: false,
        },
        {
            id: "icon",
            fieldlabel: "Icon (Optional) [Google Material Icon Name]",
            fieldname: "icon",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Icon Name",
            required: false,
            hidden: false,
        }
    ]
}