export default {
    setup: {
        new_form_id: 'new-module-group',
        info_form_id: 'module-group-info',
        title: "Module Group",
        layout_columns: 2,
        model: "Module_Group"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Group Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Group Name",
            required: true,
            hidden: false,
        },
        {
            id: "icon",
            fieldlabel: "Icon",
            fieldname: "icon",
            fieldtype: "text",
            columns: 1,
            placeholder: "Icon",
            required: false,
            hidden: false,
        },
        {
            id: "allow-multi-select",
            fieldlabel: "Allow Multi-Select",
            fieldname: "allow_multi_select",
            fieldtype: "check",
            columns: 1,
            placeholder: "Allow Multi-Select",
            required: false,
            hidden: false,
        },
    ]
}