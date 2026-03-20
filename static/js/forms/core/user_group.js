export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
        title: "User Group",
        layout_columns: 3,
        model: "Lite_User_Group"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "User Group Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter User Group Name",
            required: true,
            hidden: false,
            description: "User Group Name",
        },
    ],
}