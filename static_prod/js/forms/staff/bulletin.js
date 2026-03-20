;

export default {
    setup: {
        new_form_id: 'new-staff-bulletin',
        info_form_id: 'staff-bulletin-info',
        title: "Bulletin",
        layout_columns: 3,
        model: "Bulletin",
        allow_delete: false,
        allow_disable: false,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Bulletin Name",
            fieldname: "name",
            fieldtype: "read-only",
            columns: 1,
            placeholder: " ",
            required: true,
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
            id: "attachment",
            fieldlabel: "Attachment",
            fieldname: "attachment",
            fieldtype: "file",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: true,
        },

        {
            id: "bulletin-context",
            fieldlabel: "Bulletin Context",
            fieldname: "bulletin_context",
            fieldtype: "ready-only",
            height: 300,
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },
    
       
      
    ],
}