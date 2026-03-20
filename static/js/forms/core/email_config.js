import { on_test_email_config } from "../../overrides/form/core/core.js";

export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
        title: "Email Configuration",
        layout_columns: 2,
        model: "Email_Config"
    },
    form_actions: [
        {
            title: "Test Email",
            icon: "forward_to_inbox",
            icon_color: "indigo",
            action: on_test_email_config,
            for_docstatus: [0, 1]
        },
    ],
    fields: [
        {
            id: "name",
            fieldlabel: "Config Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Config Name",
            required: true,
            hidden: true,
            default:"Email Config"
        },
        {
            id: "server-name",
            fieldlabel: "Server Name",
            fieldname: "server_name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Server Name",
            required: true,
            hidden: false,
        },
        {
            id: "port-no",
            fieldlabel: "Port No",
            fieldname: "port_no",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Port No",
            required: true,
            hidden: false,
        },
        {
            id: "email-address",
            fieldlabel: "Email Address",
            fieldname: "email_address",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Email Address",
            required: true,
            hidden: false,
        },
        {
            id: "email-password",
            fieldlabel: "Email Password",
            fieldname: "email_password",
            fieldtype: "password",
            columns: 1,
            placeholder: "Enter Email Password",
            required: true,
            hidden: false,
        },
    ],
}