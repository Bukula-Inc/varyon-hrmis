
export default {
    setup: {
        new_form_id: 'new-staff-profile',
        info_form_id: 'staff-profile-info',
        title: "Employee",
        layout_columns: 4,
        allow_submit: false,
        allow_cancel: false,
        allow_delete: true,
        allow_print: false,
        allow_sending_mail: true,
        model: "Employee"
    },
    form_actions: [
      
    ],
    fields: [
        {
            id: "first-name",
            fieldlabel: "First Name",
            fieldname: "first_name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Select First Name",
            required: true,
            hidden: false,
        },
        {
            id: "middle-name",
            fieldlabel: "Middle Name",
            fieldname: "middle_name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
        {
            id: "last-name",
            fieldlabel: "Last Name",
            fieldname: "last_name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
        {
            id: "full-name",
            fieldlabel: "Full Names",
            fieldname: "full_name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
        },
        {
            id: "gender",
            fieldlabel: "Gender",
            fieldname: "gender",
            fieldtype: "select",
            options: [
                "Female",
                "Male"
            ],
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
    ],
}