export default {
    setup: {
        new_form_id: 'new-grievance-type',
        info_form_id: 'grievance-type-info',
        title: "Grievance Type",
        layout_columns: 2,
        model: "Grievance_Type"
    },
    fields: [
        {
            id: "name",
            fieldlabel: "Grievance Type",
            fieldname: "name",
            fieldtype: "text",
            columns: 1,
            placeholder: " ",
            required: true,
            hidden: false,
        },
       
       
        {
            id: "sec",
            fieldlabel: "",
            fieldname: "sec",
            fieldtype: "section-break",
            columns: 1,
            placeholder: " ",
            required: false,
            hidden: false,
        },
       
        {
            id: "description",
            fieldlabel: "Description",
            fieldname: "description",
            fieldtype: "longtext",
            classnames: "h-[300px]",
            columns: 3,
            placeholder: " ",
            required: false,
            hidden: false,
        },
    ],
}