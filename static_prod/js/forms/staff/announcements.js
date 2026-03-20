export default {
    setup: {
        new_form_id: 'new-announcement',
        info_form_id: 'announcement-info',
        title: "Announcement",
        layout_columns: 3,
        model: "Announcement",
        allow_delete: false,
        allow_disable: false,
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Announcement Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
       
        {
            id: "posting-date",
            fieldlabel: "Posting Date",
            fieldname: "posting_date",
            fieldtype: "date",
            placeholder: " ",
            columns: 1,
            required: false,
            hidden: false,
        },
    
       
      
        {
            id: "announcement-id",
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
            id: "announcement-context",
            fieldlabel: "Announcement_Context",
            fieldname: "announcement_context",
            fieldtype: "longtext",
            classnames: "h-[300px]",
            placeholder: " ",
            columns: 3,
            required: false,
            hidden: false,
        },
    
       
      
    ],
}