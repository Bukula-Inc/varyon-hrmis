export default {
    setup: {
        allow_submit: false,
        new_form_id: 'new-banking',
        info_form_id: 'banking-info',
        title: "Account Branch Code",
        layout_columns: 6,
        model: "Account_Branch_Code"
    },
    form_actions: [
    ],
    fields:[
        {
            id: "bank",
            fieldlabel: "Bank",
            fieldname: "bank",
            fieldtype: "link",
            model: "Bank",
            columns: 2,
            required: false,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "name",
            fieldlabel: "Branch Name",
            fieldname: "name",
            fieldtype: "text",
            columns: 2,
            required: true,
            hidden: false,
            placeholder: " ",
        },
        {
            id: "sort_code",
            fieldlabel: "Branch COde",
            fieldname: "sort_code",
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