export default {
    setup: {
        new_form_id: 'form',
        info_form_id: 'info',
        title: "Ticket Priority Settings",
        layout_columns: 4,
        include_logo: false,
        model: "Priority",
        allow_submit: false,
        allow_cancel: false,
        allow_delete: false,
        allow_print: false,
        allow_sending_mail: true,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Ticket Priority",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            required: false,
            hidden: false,
            placeholder: "Enter Ticket Priority",
        },
        {
            id: "description",
            fieldlabel: "Priority  Description",
            fieldname: "description",
            fieldtype: "longtext",
            columns: 4,
            required: false,
            hidden: false,
            classnames: "h-[200px] p-2"
        },
    ],
};
