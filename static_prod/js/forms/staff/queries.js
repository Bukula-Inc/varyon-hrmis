export default {
    setup: {
        new_form_id: 'new-staff-query',
        info_form_id: 'staff-query-info',
        title: "Query",
        layout_columns: 2,
        model: "Query",
        allow_disable: false,
    },
    fields: [
        {
            id: "query-name",
            fieldlabel: "Query Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "",
            required: true,
            hidden: false,
        },
   
       
        {
            id: "query-from",
            fieldlabel: "From",
            fieldname: "employee",
            fieldtype: "link",
            model: "Employee",
            columns: 1,
            required: false,
            hidden: false,
        },
        {
            id: "query-date",
            fieldlabel: "Date",
            fieldname: "date",
            fieldtype: "date",
            columns: 1,
            required: false,
            hidden: false,
        },
    
       
        {
            id: "query-subject",
            fieldlabel: "Subject",
            fieldname: "subject",
            fieldtype: "text",
            columns: 1,
            required: false,
            hidden: false,
        },
        {
            id: "query-info",
            fieldlabel: "",
            fieldname: "si",
            fieldtype: "section-break",
            addborder: true,
            columns: 1,
            required: false,
            hidden: false,
        },

        {
            id: "query-context",
            fieldlabel: "Query Context",
            fieldname: "context",
            fieldtype: "longtext",
            classnames: "h-[200px]",
            columns: 1,
            required: false,
            hidden: false,
        },
    
        // {
        //     id: "query-info",
        //     fieldlabel: "",
        //     fieldname: "si",
        //     fieldtype: "column-break",
        //     addborder: false,
        //     columns: 1,
        //     required: false,
        //     hidden: false,
        // },

        {
            id: "query-response",
            fieldlabel: "Response",
            fieldname: "response",
            fieldtype: "longtext",
            classnames: "h-[200px]",
            columns: 1,
            required: false,
            hidden: false,
        },
     
     
      
    ],
}