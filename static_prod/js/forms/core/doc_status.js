export default {
    setup: {
        new_form_id: 'new-doc-status',
        info_form_id: 'doc-status-info',
        title: "Doc Status",
        layout_columns: 3,
        model: "Doc_Status"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Doc Status Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: "Enter Doc Status Name",
            required: true,
            hidden: false,
            
        },
        {
            id: "initial-docstatus",
            fieldlabel: "Initial Docstatus",
            fieldname: "initial_docstatus",
            fieldtype: "select",
            columns: 1,
            placeholder: "Select Initial Doc Status",
            required: true,
            hidden: false,
            description: "0 for draft, 1 for submitted, 2 for canceled and 3 for rejected.",
            options:[0,1,2,3]
        },
        {
            id: "status-color",
            fieldlabel: "Status Color",
            fieldname: "status_color",
            fieldtype: "color",
            columns: 1,
            placeholder: "Select Color",
            required: true,
            hidden: false,
            
        },
        {
            id: "inner-color",
            fieldlabel: "Text Color",
            fieldname: "inner_color",
            fieldtype: "color",
            columns: 1,
            placeholder: "Text Color",
            required: true,
            hidden: false,
            
        },
        

    ],
}