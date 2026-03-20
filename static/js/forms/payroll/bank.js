export default {
    setup: {
        allow_submit: false,
        new_form_id: 'new-banking',
        info_form_id: 'banking-info',
        title: "Bank",
        layout_columns: 6,
        model: "Bank"
    },
    form_actions: [
    ],
    fields:[
        {
            id: "name",
            fieldlabel: "Bank Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        
        {
            id: "descriptions",
            fieldlabel: "descriptions",
            fieldname: "descriptions",
            fieldtype: "text",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",

        },
    ]
}