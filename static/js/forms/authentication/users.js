export default {
    setup: {
        new_form_id: 'user-form',
        info_form_id: 'user-info',
        title: "User",
        layout_columns: 4,
        include_logo: false,
        model: "Lite_User"
    },
    fields: [
        {
            id: "first_name",
            fieldlabel: "First Name",
            fieldname: "first_name",
            fieldtype: "text",
            columns: 2,
            placeholder: "Enter First Name",
            required: true,
            hidden: false,
            description: "First Name"
        },
        {
            id: "last_name",
            fieldlabel: "Last Name",
            fieldname: "last_name",
            fieldtype: "text",
            columns: 2,
            placeholder: "Enter Last Name",
            required: true,
            hidden: false,
            description: "Last Name"
        },
        {
            id: "middle_name",
            fieldlabel: "Middle Name",
            fieldname: "middle_name",
            fieldtype: "text",
            columns: 2,
            placeholder: "Enter Middle Name",
            required: false,
            hidden: false,
            description: "Middle Name"
        },
        {
            id: "gender",
            fieldlabel: "Gender",
            fieldname: "gender",
            fieldtype: "select",
            options: ["Male", "Female"],
            columns: 2,
            placeholder: "Enter Gender",
            required: true,
            hidden: false,
            description: "Gender"
        },
        {
            id: "email",
            fieldlabel: "Email Address",
            fieldname: "email",
            fieldtype: "text",
            columns: 2,
            placeholder: "Enter Email Address",
            required: true,
            hidden: false,
            description: "Email Address"
        },
        {
            id: "password1",
            fieldlabel: "Password",
            fieldname: "password1",
            fieldtype: "text",
            columns: 2,
            placeholder: "Enter Password",
            required: true,
            hidden: false,
            description: "Password"
        },
        {
            id: "password2",
            fieldlabel: "Password Confirmation",
            fieldname: "password2",
            fieldtype: "text",
            columns: 2,
            placeholder: "Enter Password Confirmation",
            required: true,
            hidden: false,
            description: "Password Confirmation"
        },
        
    ],
}